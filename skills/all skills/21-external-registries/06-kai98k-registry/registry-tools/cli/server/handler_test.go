//go:build server

package server

import (
	"bytes"
	"encoding/json"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"

	"github.com/liuyukai/agentskills-cli/internal/bundle"
)

// setupTestServer creates a temp data dir, store, handler, and test server.
func setupTestServer(t *testing.T) (*httptest.Server, string) {
	t.Helper()
	dataDir := t.TempDir()
	store := NewStore(dataDir)
	handler := NewHandler(store, "test-token")
	mux := http.NewServeMux()
	handler.RegisterRoutes(mux)
	return httptest.NewServer(mux), dataDir
}

// createTestSkillDir creates a minimal skill directory with a SKILL.md.
func createTestSkillDir(t *testing.T, name, version string) string {
	t.Helper()
	dir := t.TempDir()
	skillContent := "---\nname: \"" + name + "\"\nversion: \"" + version + "\"\ndescription: \"A test skill\"\nauthor: \"tester\"\ntags:\n  - test\n---\n\n# " + name + "\n\nTest skill.\n"
	if err := os.WriteFile(filepath.Join(dir, "SKILL.md"), []byte(skillContent), 0o644); err != nil {
		t.Fatal(err)
	}
	return dir
}

func publishBundle(t *testing.T, serverURL, token, skillDir string) {
	t.Helper()

	// Pack the skill directory into a bundle.
	bundlePath, err := bundle.Pack(skillDir)
	if err != nil {
		t.Fatalf("packing bundle: %v", err)
	}
	defer os.Remove(bundlePath)

	bundleData, err := os.ReadFile(bundlePath)
	if err != nil {
		t.Fatal(err)
	}

	// Build multipart request.
	var body bytes.Buffer
	writer := multipart.NewWriter(&body)
	part, err := writer.CreateFormFile("file", "bundle.tar.gz")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := part.Write(bundleData); err != nil {
		t.Fatal(err)
	}
	writer.Close()

	req, _ := http.NewRequest("POST", serverURL+"/v1/skills/publish", &body)
	req.Header.Set("Content-Type", writer.FormDataContentType())
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatalf("publish request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		b, _ := io.ReadAll(resp.Body)
		t.Fatalf("publish returned %d: %s", resp.StatusCode, string(b))
	}
}

func TestPublishAndSearch(t *testing.T) {
	ts, _ := setupTestServer(t)
	defer ts.Close()

	// Publish a skill.
	skillDir := createTestSkillDir(t, "hello-world", "1.0.0")
	publishBundle(t, ts.URL, "test-token", skillDir)

	// Search for it.
	resp, err := http.Get(ts.URL + "/v1/skills?q=hello")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("search returned %d", resp.StatusCode)
	}

	var result searchResult
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Fatal(err)
	}
	if result.Total != 1 {
		t.Fatalf("expected 1 result, got %d", result.Total)
	}
	if result.Results[0].Name != "hello-world" {
		t.Fatalf("expected name hello-world, got %s", result.Results[0].Name)
	}
}

func TestGetSkill(t *testing.T) {
	ts, _ := setupTestServer(t)
	defer ts.Close()

	skillDir := createTestSkillDir(t, "my-skill", "2.0.0")
	publishBundle(t, ts.URL, "test-token", skillDir)

	resp, err := http.Get(ts.URL + "/v1/skills/my-skill")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("get skill returned %d", resp.StatusCode)
	}

	var info skillInfoResponse
	if err := json.NewDecoder(resp.Body).Decode(&info); err != nil {
		t.Fatal(err)
	}
	if info.Name != "my-skill" {
		t.Fatalf("expected name my-skill, got %s", info.Name)
	}
	if info.LatestVersion == nil || info.LatestVersion.Version != "2.0.0" {
		t.Fatalf("expected latest version 2.0.0, got %+v", info.LatestVersion)
	}
}

func TestDownload(t *testing.T) {
	ts, _ := setupTestServer(t)
	defer ts.Close()

	skillDir := createTestSkillDir(t, "dl-test", "1.0.0")
	publishBundle(t, ts.URL, "test-token", skillDir)

	resp, err := http.Get(ts.URL + "/v1/skills/dl-test/versions/1.0.0/download")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		b, _ := io.ReadAll(resp.Body)
		t.Fatalf("download returned %d: %s", resp.StatusCode, string(b))
	}

	checksum := resp.Header.Get("X-Checksum-SHA256")
	if checksum == "" {
		t.Fatal("expected X-Checksum-SHA256 header")
	}

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err)
	}
	if len(data) == 0 {
		t.Fatal("downloaded bundle is empty")
	}
}

func TestPublishUnauthorized(t *testing.T) {
	ts, _ := setupTestServer(t)
	defer ts.Close()

	skillDir := createTestSkillDir(t, "no-auth", "1.0.0")
	bundlePath, _ := bundle.Pack(skillDir)
	defer os.Remove(bundlePath)

	bundleData, _ := os.ReadFile(bundlePath)

	var body bytes.Buffer
	writer := multipart.NewWriter(&body)
	part, _ := writer.CreateFormFile("file", "bundle.tar.gz")
	part.Write(bundleData)
	writer.Close()

	req, _ := http.NewRequest("POST", ts.URL+"/v1/skills/publish", &body)
	req.Header.Set("Content-Type", writer.FormDataContentType())
	req.Header.Set("Authorization", "Bearer wrong-token")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusUnauthorized {
		t.Fatalf("expected 401, got %d", resp.StatusCode)
	}
}

func TestGetSkillNotFound(t *testing.T) {
	ts, _ := setupTestServer(t)
	defer ts.Close()

	resp, err := http.Get(ts.URL + "/v1/skills/nonexistent")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusNotFound {
		t.Fatalf("expected 404, got %d", resp.StatusCode)
	}
}
