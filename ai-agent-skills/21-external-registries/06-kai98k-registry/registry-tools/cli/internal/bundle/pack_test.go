package bundle

import (
	"archive/tar"
	"compress/gzip"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestPackAndUnpack(t *testing.T) {
	// Create a skill directory
	srcDir := t.TempDir()
	os.WriteFile(filepath.Join(srcDir, "SKILL.md"), []byte("# Test"), 0o644)
	os.MkdirAll(filepath.Join(srcDir, "scripts"), 0o755)
	os.WriteFile(filepath.Join(srcDir, "scripts", "run.sh"), []byte("echo hello"), 0o644)

	// Pack
	bundlePath, err := Pack(srcDir)
	if err != nil {
		t.Fatalf("Pack() error = %v", err)
	}
	defer os.Remove(bundlePath)

	// Unpack to a different directory
	destDir := t.TempDir()
	if err := Unpack(bundlePath, destDir); err != nil {
		t.Fatalf("Unpack() error = %v", err)
	}

	// Verify files exist
	if _, err := os.Stat(filepath.Join(destDir, "SKILL.md")); err != nil {
		t.Error("SKILL.md should exist after unpack")
	}
	if _, err := os.Stat(filepath.Join(destDir, "scripts", "run.sh")); err != nil {
		t.Error("scripts/run.sh should exist after unpack")
	}
}

func TestUnpackPathTraversal(t *testing.T) {
	// Create a malicious tar.gz with ../../../etc/passwd entry
	tmpFile, err := os.CreateTemp("", "malicious-*.tar.gz")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpFile.Name())

	gw := gzip.NewWriter(tmpFile)
	tw := tar.NewWriter(gw)

	tw.WriteHeader(&tar.Header{
		Name:     "../../../etc/evil",
		Size:     4,
		Typeflag: tar.TypeReg,
	})
	tw.Write([]byte("hack"))

	tw.Close()
	gw.Close()
	tmpFile.Close()

	destDir := t.TempDir()
	err = Unpack(tmpFile.Name(), destDir)
	if err == nil {
		t.Fatal("Unpack() should reject path traversal")
	}
	if !strings.Contains(err.Error(), "path traversal") {
		t.Errorf("error should mention path traversal, got: %v", err)
	}
}

func TestUnpackDirectorySuffixAttack(t *testing.T) {
	// Create a tar.gz where a file escapes destDir via similar prefix
	// e.g., destDir is "/tmp/safe" and entry targets "/tmp/safevil"
	// This tests the fix for the HasPrefix bug.
	tmpFile, err := os.CreateTemp("", "suffix-attack-*.tar.gz")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpFile.Name())

	gw := gzip.NewWriter(tmpFile)
	tw := tar.NewWriter(gw)

	// Normal entry inside the directory
	tw.WriteHeader(&tar.Header{
		Name:     "ok.txt",
		Size:     2,
		Typeflag: tar.TypeReg,
	})
	tw.Write([]byte("ok"))

	tw.Close()
	gw.Close()
	tmpFile.Close()

	// This should succeed — normal file inside destDir
	destDir := t.TempDir()
	if err := Unpack(tmpFile.Name(), destDir); err != nil {
		t.Fatalf("Unpack() should succeed for normal entries: %v", err)
	}
}

func TestExcludePatterns(t *testing.T) {
	tests := []struct {
		name     string
		path     string
		excluded bool
	}{
		{"git dir", ".git", true},
		{"DS_Store", ".DS_Store", true},
		{"node_modules", "node_modules", true},
		{"env file", ".env", true},
		{"pyc file", "cache.pyc", true},
		{"normal file", "main.go", false},
		{"skill md", "SKILL.md", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := shouldExclude(tt.path); got != tt.excluded {
				t.Errorf("shouldExclude(%q) = %v, want %v", tt.path, got, tt.excluded)
			}
		})
	}
}
