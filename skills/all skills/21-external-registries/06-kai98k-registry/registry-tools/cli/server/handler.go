//go:build server

package server

import (
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/liuyukai/agentskills-cli/internal/bundle"
	"github.com/liuyukai/agentskills-cli/internal/parser"
)

// Handler holds the HTTP handler dependencies.
type Handler struct {
	store *Store
	token string // if non-empty, require this bearer token for publish
}

func NewHandler(store *Store, token string) *Handler {
	return &Handler{store: store, token: token}
}

// RegisterRoutes registers all API routes on the given mux.
// Uses Go 1.22+ enhanced ServeMux patterns.
func (h *Handler) RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("GET /v1/skills", h.handleSearch)
	mux.HandleFunc("GET /v1/skills/{name}", h.handleGetSkill)
	mux.HandleFunc("GET /v1/skills/{name}/versions/{version}/download", h.handleDownload)
	mux.HandleFunc("POST /v1/skills/publish", h.handlePublish)
}

// --- Search ---

type searchResult struct {
	Total   int           `json:"total"`
	Page    int           `json:"page"`
	PerPage int           `json:"per_page"`
	Results []searchEntry `json:"results"`
}

type searchEntry struct {
	Name          string   `json:"name"`
	Description   string   `json:"description"`
	Owner         string   `json:"owner"`
	Downloads     int64    `json:"downloads"`
	LatestVersion string   `json:"latest_version"`
	Tags          []string `json:"tags"`
}

func (h *Handler) handleSearch(w http.ResponseWriter, r *http.Request) {
	keyword := r.URL.Query().Get("q")
	skills := h.store.Search(keyword)

	entries := make([]searchEntry, 0, len(skills))
	for _, s := range skills {
		latestVer := ""
		if lv := s.LatestVersion(); lv != nil {
			latestVer = lv.Version
		}
		entries = append(entries, searchEntry{
			Name:          s.Name,
			Description:   s.Description,
			Owner:         s.Owner,
			Downloads:     s.Downloads,
			LatestVersion: latestVer,
			Tags:          s.Tags,
		})
	}

	writeJSON(w, http.StatusOK, searchResult{
		Total:   len(entries),
		Page:    1,
		PerPage: len(entries),
		Results: entries,
	})
}

// --- GetSkill ---

type skillInfoResponse struct {
	Name          string              `json:"name"`
	Owner         string              `json:"owner"`
	Downloads     int64               `json:"downloads"`
	LatestVersion *versionInfoResponse `json:"latest_version"`
}

type versionInfoResponse struct {
	Version     string `json:"version"`
	Description string `json:"description"`
	Checksum    string `json:"checksum"`
	SizeBytes   int64  `json:"size_bytes"`
	PublishedAt string `json:"published_at"`
}

func (h *Handler) handleGetSkill(w http.ResponseWriter, r *http.Request) {
	name := r.PathValue("name")
	meta := h.store.GetSkill(name)
	if meta == nil {
		http.Error(w, fmt.Sprintf("skill %q not found", name), http.StatusNotFound)
		return
	}

	resp := skillInfoResponse{
		Name:      meta.Name,
		Owner:     meta.Owner,
		Downloads: meta.Downloads,
	}
	if lv := meta.LatestVersion(); lv != nil {
		resp.LatestVersion = &versionInfoResponse{
			Version:     lv.Version,
			Description: lv.Description,
			Checksum:    lv.Checksum,
			SizeBytes:   lv.SizeBytes,
			PublishedAt: lv.PublishedAt,
		}
	}

	writeJSON(w, http.StatusOK, resp)
}

// --- Download ---

func (h *Handler) handleDownload(w http.ResponseWriter, r *http.Request) {
	name := r.PathValue("name")
	version := r.PathValue("version")

	meta := h.store.GetSkill(name)
	if meta == nil {
		http.Error(w, fmt.Sprintf("skill %q not found", name), http.StatusNotFound)
		return
	}

	vm := meta.FindVersion(version)
	if vm == nil {
		http.Error(w, fmt.Sprintf("version %q not found", version), http.StatusNotFound)
		return
	}

	bundlePath := h.store.GetBundlePath(name, version)
	if bundlePath == "" {
		http.Error(w, "bundle file not found", http.StatusNotFound)
		return
	}

	w.Header().Set("X-Checksum-SHA256", strings.TrimPrefix(vm.Checksum, "sha256:"))
	w.Header().Set("Content-Type", "application/gzip")
	http.ServeFile(w, r, bundlePath)

	h.store.IncrementDownloads(name)
}

// --- Publish ---

type publishResult struct {
	Name        string `json:"name"`
	Version     string `json:"version"`
	Checksum    string `json:"checksum"`
	PublishedAt string `json:"published_at"`
}

func (h *Handler) handlePublish(w http.ResponseWriter, r *http.Request) {
	// Auth check.
	if h.token != "" {
		auth := r.Header.Get("Authorization")
		if !strings.HasPrefix(auth, "Bearer ") || strings.TrimPrefix(auth, "Bearer ") != h.token {
			http.Error(w, "unauthorized", http.StatusUnauthorized)
			return
		}
	}

	// Parse multipart (max 50 MB).
	if err := r.ParseMultipartForm(50 << 20); err != nil {
		http.Error(w, "invalid multipart form: "+err.Error(), http.StatusBadRequest)
		return
	}

	file, _, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "missing file field: "+err.Error(), http.StatusBadRequest)
		return
	}
	defer file.Close()

	// Save uploaded bundle to temp file.
	tmpFile, err := os.CreateTemp("", "upload-*.tar.gz")
	if err != nil {
		http.Error(w, "server error", http.StatusInternalServerError)
		log.Printf("creating temp file: %v", err)
		return
	}
	defer os.Remove(tmpFile.Name())
	defer tmpFile.Close()

	if _, err := io.Copy(tmpFile, file); err != nil {
		http.Error(w, "server error", http.StatusInternalServerError)
		log.Printf("writing upload: %v", err)
		return
	}

	// Unpack to temp dir to read SKILL.md.
	tmpDir, err := os.MkdirTemp("", "upload-extract-*")
	if err != nil {
		http.Error(w, "server error", http.StatusInternalServerError)
		log.Printf("creating temp dir: %v", err)
		return
	}
	defer os.RemoveAll(tmpDir)

	if err := bundle.Unpack(tmpFile.Name(), tmpDir); err != nil {
		http.Error(w, "invalid bundle: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Parse and validate SKILL.md.
	meta, err := parser.ParseSkillFile(tmpDir)
	if err != nil {
		http.Error(w, "invalid SKILL.md: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Calculate checksum.
	bundleData, err := os.ReadFile(tmpFile.Name())
	if err != nil {
		http.Error(w, "server error", http.StatusInternalServerError)
		log.Printf("reading bundle: %v", err)
		return
	}
	checksum := fmt.Sprintf("sha256:%x", sha256.Sum256(bundleData))

	// Persist.
	if err := h.store.SaveBundle(
		meta.Name, meta.Author, meta.Description, meta.Version,
		checksum, int64(len(bundleData)), meta.Tags, bundleData,
	); err != nil {
		http.Error(w, "server error", http.StatusInternalServerError)
		log.Printf("saving bundle: %v", err)
		return
	}

	skill := h.store.GetSkill(meta.Name)
	vm := skill.FindVersion(meta.Version)

	writeJSON(w, http.StatusCreated, publishResult{
		Name:        meta.Name,
		Version:     meta.Version,
		Checksum:    checksum,
		PublishedAt: vm.PublishedAt,
	})
}

// --- Helpers ---

func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(v); err != nil {
		log.Printf("writing JSON response: %v", err)
	}
}
