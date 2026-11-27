package lockfile

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestSaveAndLoad(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, Filename)

	lf := &LockFile{
		Skills: map[string]LockedSkill{
			"code-review": {
				Version:  "1.2.0",
				Checksum: "sha256:abc123",
				Source:   "http://localhost:8000",
			},
			"data-analysis": {
				Version:  "2.0.0",
				Checksum: "sha256:def456",
				Source:   "http://my-server:8000",
			},
		},
	}

	if err := Save(path, lf); err != nil {
		t.Fatalf("Save() error = %v", err)
	}

	// Verify file starts with header comment
	data, _ := os.ReadFile(path)
	if !strings.HasPrefix(string(data), "# agentskills.lock") {
		t.Error("lock file should start with header comment")
	}

	loaded, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if loaded == nil {
		t.Fatal("Load() returned nil")
	}
	if loaded.Version != 1 {
		t.Errorf("Version = %d, want 1", loaded.Version)
	}
	if len(loaded.Skills) != 2 {
		t.Errorf("len(Skills) = %d, want 2", len(loaded.Skills))
	}

	cr, ok := loaded.Get("code-review")
	if !ok {
		t.Fatal("code-review not found in loaded lock file")
	}
	if cr.Version != "1.2.0" {
		t.Errorf("code-review version = %s, want 1.2.0", cr.Version)
	}
	if cr.Checksum != "sha256:abc123" {
		t.Errorf("code-review checksum = %s, want sha256:abc123", cr.Checksum)
	}
}

func TestLoadNonExistent(t *testing.T) {
	lf, err := Load(filepath.Join(t.TempDir(), "does-not-exist.lock"))
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if lf != nil {
		t.Error("Load() should return nil for non-existent file")
	}
}

func TestSetAndRemove(t *testing.T) {
	lf := &LockFile{}

	lf.Set("test-skill", LockedSkill{Version: "1.0.0", Checksum: "sha256:aaa"})
	if _, ok := lf.Get("test-skill"); !ok {
		t.Error("Set() should add skill")
	}

	lf.Remove("test-skill")
	if _, ok := lf.Get("test-skill"); ok {
		t.Error("Remove() should delete skill")
	}
}

func TestGetOnNilSkills(t *testing.T) {
	lf := &LockFile{}
	_, ok := lf.Get("anything")
	if ok {
		t.Error("Get() on nil Skills should return false")
	}
}
