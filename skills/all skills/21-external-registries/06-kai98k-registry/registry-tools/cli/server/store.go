//go:build server

package server

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// SkillMeta is the persisted metadata for a single skill.
type SkillMeta struct {
	Name        string        `json:"name"`
	Owner       string        `json:"owner"`
	Description string        `json:"description"`
	Tags        []string      `json:"tags"`
	Downloads   int64         `json:"downloads"`
	Versions    []VersionMeta `json:"versions"`
}

// VersionMeta is the persisted metadata for a single version.
type VersionMeta struct {
	Version     string `json:"version"`
	Description string `json:"description"`
	Checksum    string `json:"checksum"`
	SizeBytes   int64  `json:"size_bytes"`
	PublishedAt string `json:"published_at"`
}

// Store is a file-system-based storage backend.
// Layout:
//
//	{dataDir}/bundles/{name}/meta.json
//	{dataDir}/bundles/{name}/{version}/bundle.tar.gz
type Store struct {
	dataDir string
	mu      sync.RWMutex
}

func NewStore(dataDir string) *Store {
	return &Store{dataDir: dataDir}
}

func (s *Store) bundlesDir() string {
	return filepath.Join(s.dataDir, "bundles")
}

func (s *Store) skillDir(name string) string {
	return filepath.Join(s.bundlesDir(), name)
}

func (s *Store) metaPath(name string) string {
	return filepath.Join(s.skillDir(name), "meta.json")
}

func (s *Store) bundlePath(name, version string) string {
	return filepath.Join(s.skillDir(name), version, "bundle.tar.gz")
}

// SaveBundle persists a bundle file and updates skill metadata.
func (s *Store) SaveBundle(name, owner, description, version, checksum string, sizeBytes int64, tags []string, bundleData []byte) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Ensure directories exist.
	versionDir := filepath.Join(s.skillDir(name), version)
	if err := os.MkdirAll(versionDir, 0o755); err != nil {
		return fmt.Errorf("creating version dir: %w", err)
	}

	// Write bundle file.
	if err := os.WriteFile(s.bundlePath(name, version), bundleData, 0o644); err != nil {
		return fmt.Errorf("writing bundle: %w", err)
	}

	// Load or create meta.
	meta, _ := s.loadMetaLocked(name)
	if meta == nil {
		meta = &SkillMeta{
			Name:  name,
			Owner: owner,
			Tags:  tags,
		}
	}
	meta.Description = description
	meta.Owner = owner
	if len(tags) > 0 {
		meta.Tags = tags
	}

	// Append version (or replace if same version exists).
	vm := VersionMeta{
		Version:     version,
		Description: description,
		Checksum:    checksum,
		SizeBytes:   sizeBytes,
		PublishedAt: time.Now().UTC().Format(time.RFC3339),
	}
	replaced := false
	for i, v := range meta.Versions {
		if v.Version == version {
			meta.Versions[i] = vm
			replaced = true
			break
		}
	}
	if !replaced {
		meta.Versions = append(meta.Versions, vm)
	}

	return s.saveMetaLocked(name, meta)
}

// GetSkill returns metadata for a skill, or nil if not found.
func (s *Store) GetSkill(name string) *SkillMeta {
	s.mu.RLock()
	defer s.mu.RUnlock()
	meta, _ := s.loadMetaLocked(name)
	return meta
}

// GetBundlePath returns the file path for a specific version bundle, or empty if not found.
func (s *Store) GetBundlePath(name, version string) string {
	p := s.bundlePath(name, version)
	if _, err := os.Stat(p); err != nil {
		return ""
	}
	return p
}

// IncrementDownloads atomically increments the download counter.
func (s *Store) IncrementDownloads(name string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	meta, _ := s.loadMetaLocked(name)
	if meta == nil {
		return
	}
	meta.Downloads++
	_ = s.saveMetaLocked(name, meta)
}

// Search returns skills whose name, description, or tags match the keyword.
func (s *Store) Search(keyword string) []SkillMeta {
	s.mu.RLock()
	defer s.mu.RUnlock()

	keyword = strings.ToLower(keyword)
	var results []SkillMeta

	entries, err := os.ReadDir(s.bundlesDir())
	if err != nil {
		return results
	}

	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}
		meta, err := s.loadMetaLocked(entry.Name())
		if err != nil || meta == nil {
			continue
		}
		if matchesKeyword(meta, keyword) {
			results = append(results, *meta)
		}
	}
	return results
}

func matchesKeyword(meta *SkillMeta, keyword string) bool {
	if keyword == "" {
		return true
	}
	if strings.Contains(strings.ToLower(meta.Name), keyword) {
		return true
	}
	if strings.Contains(strings.ToLower(meta.Description), keyword) {
		return true
	}
	for _, tag := range meta.Tags {
		if strings.Contains(strings.ToLower(tag), keyword) {
			return true
		}
	}
	return false
}

// LatestVersion returns the last version in the list (most recently published).
func (m *SkillMeta) LatestVersion() *VersionMeta {
	if len(m.Versions) == 0 {
		return nil
	}
	return &m.Versions[len(m.Versions)-1]
}

// FindVersion returns a specific version or nil.
func (m *SkillMeta) FindVersion(version string) *VersionMeta {
	for i := range m.Versions {
		if m.Versions[i].Version == version {
			return &m.Versions[i]
		}
	}
	return nil
}

func (s *Store) loadMetaLocked(name string) (*SkillMeta, error) {
	data, err := os.ReadFile(s.metaPath(name))
	if err != nil {
		return nil, err
	}
	var meta SkillMeta
	if err := json.Unmarshal(data, &meta); err != nil {
		return nil, err
	}
	return &meta, nil
}

func (s *Store) saveMetaLocked(name string, meta *SkillMeta) error {
	data, err := json.MarshalIndent(meta, "", "  ")
	if err != nil {
		return fmt.Errorf("marshaling meta: %w", err)
	}
	return os.WriteFile(s.metaPath(name), data, 0o644)
}
