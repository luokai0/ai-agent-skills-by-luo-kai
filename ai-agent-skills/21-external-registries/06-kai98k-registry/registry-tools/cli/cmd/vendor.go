package cmd

import (
	"crypto/sha256"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"

	"github.com/liuyukai/agentskills-cli/internal/api"
	"github.com/liuyukai/agentskills-cli/internal/bundle"
	"github.com/liuyukai/agentskills-cli/internal/config"
	"github.com/liuyukai/agentskills-cli/internal/lockfile"
	"github.com/spf13/cobra"
)

const vendorDir = "vendor/skills"

var vendorCmd = &cobra.Command{
	Use:   "vendor [name[@version]]",
	Short: "Vendor skills locally with checksum lock for supply-chain safety",
	Long: `Vendor downloads skills into vendor/skills/ and records their exact
version and checksum in agentskills.lock.

  agentskills vendor code-review@1.2.0   # vendor a specific skill
  agentskills vendor                      # restore all skills from lock file
  agentskills vendor --remove code-review # remove a vendored skill`,
	Args: cobra.MaximumNArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		removeName, _ := cmd.Flags().GetString("remove")
		if removeName != "" {
			return vendorRemove(removeName)
		}
		if len(args) == 0 {
			return vendorSync(cmd)
		}
		return vendorAdd(cmd, args[0])
	},
}

func init() {
	vendorCmd.Flags().String("remove", "", "Remove a vendored skill")
	rootCmd.AddCommand(vendorCmd)
}

// vendorAdd downloads a single skill and records it in the lock file.
func vendorAdd(cmd *cobra.Command, nameVersion string) error {
	name, version := parsePullArg(nameVersion)

	cfg, err := config.Load()
	if err != nil {
		return fmt.Errorf("loading config: %w", err)
	}
	if cmd.Flags().Changed("api-url") {
		apiURL, _ := cmd.Flags().GetString("api-url")
		cfg.APIURL = apiURL
	}

	client := api.NewClient(cfg.APIURL, cfg.Token)

	// Resolve version
	if version == "" {
		fmt.Printf("Fetching latest version of %s...\n", name)
		info, err := client.GetSkill(name)
		if err != nil {
			return fmt.Errorf("fetching skill info: %w", err)
		}
		version = info.LatestVersion.Version
	}

	// Download
	fmt.Printf("Downloading %s@%s...  ", name, version)
	tmpFile, expectedChecksum, err := client.Download(name, version)
	if err != nil {
		fmt.Println("x")
		return fmt.Errorf("download failed: %w", err)
	}
	defer os.Remove(tmpFile)
	fmt.Println("ok")

	// Verify checksum
	checksum, err := fileChecksum(tmpFile)
	if err != nil {
		return err
	}
	if expectedChecksum != "" && checksum != expectedChecksum {
		return fmt.Errorf("checksum mismatch: expected=%s actual=%s", expectedChecksum, checksum)
	}

	// Extract to vendor/skills/<name>/
	destDir := filepath.Join(vendorDir, name)
	if err := os.RemoveAll(destDir); err != nil {
		return fmt.Errorf("cleaning vendor dir: %w", err)
	}
	if err := os.MkdirAll(vendorDir, 0o755); err != nil {
		return fmt.Errorf("creating vendor dir: %w", err)
	}
	if err := bundle.Unpack(tmpFile, destDir); err != nil {
		return fmt.Errorf("extraction failed: %w", err)
	}

	// Update lock file
	lf, err := lockfile.Load(lockfile.Filename)
	if err != nil {
		return fmt.Errorf("loading lock file: %w", err)
	}
	if lf == nil {
		lf = &lockfile.LockFile{Skills: make(map[string]lockfile.LockedSkill)}
	}
	lf.Set(name, lockfile.LockedSkill{
		Version:  version,
		Checksum: "sha256:" + checksum,
		Source:   cfg.APIURL,
	})
	if err := lockfile.Save(lockfile.Filename, lf); err != nil {
		return fmt.Errorf("saving lock file: %w", err)
	}

	fmt.Printf("Vendored %s@%s -> %s\n", name, version, destDir)
	fmt.Printf("Lock file updated: %s\n", lockfile.Filename)
	return nil
}

// vendorSync restores all skills from the lock file.
func vendorSync(cmd *cobra.Command) error {
	lf, err := lockfile.Load(lockfile.Filename)
	if err != nil {
		return fmt.Errorf("loading lock file: %w", err)
	}
	if lf == nil || len(lf.Skills) == 0 {
		fmt.Println("No lock file found. Use 'agentskills vendor <name>' to add skills.")
		return nil
	}

	cfg, err := config.Load()
	if err != nil {
		return fmt.Errorf("loading config: %w", err)
	}

	fmt.Printf("Restoring %d skill(s) from %s...\n", len(lf.Skills), lockfile.Filename)

	var failed []string
	for name, locked := range lf.Skills {
		source := locked.Source
		if source == "" {
			source = cfg.APIURL
		}
		client := api.NewClient(source, cfg.Token)

		fmt.Printf("  %s@%s...  ", name, locked.Version)

		tmpFile, _, err := client.Download(name, locked.Version)
		if err != nil {
			fmt.Println("x (download failed)")
			failed = append(failed, name)
			continue
		}

		// Verify checksum against lock file
		checksum, err := fileChecksum(tmpFile)
		if err != nil {
			os.Remove(tmpFile)
			fmt.Println("x (checksum error)")
			failed = append(failed, name)
			continue
		}

		expectedChecksum := strings.TrimPrefix(locked.Checksum, "sha256:")
		if checksum != expectedChecksum {
			os.Remove(tmpFile)
			fmt.Printf("x (checksum mismatch: expected=%s actual=%s)\n", expectedChecksum, checksum)
			failed = append(failed, name)
			continue
		}

		// Extract
		destDir := filepath.Join(vendorDir, name)
		os.RemoveAll(destDir)
		if err := bundle.Unpack(tmpFile, destDir); err != nil {
			os.Remove(tmpFile)
			fmt.Printf("x (extract failed: %v)\n", err)
			failed = append(failed, name)
			continue
		}
		os.Remove(tmpFile)

		fmt.Println("ok")
	}

	if len(failed) > 0 {
		return fmt.Errorf("failed to restore %d skill(s): %s", len(failed), strings.Join(failed, ", "))
	}

	fmt.Println("All skills restored successfully.")
	return nil
}

// vendorRemove removes a vendored skill and its lock file entry.
func vendorRemove(name string) error {
	destDir := filepath.Join(vendorDir, name)
	if err := os.RemoveAll(destDir); err != nil {
		return fmt.Errorf("removing vendor dir: %w", err)
	}

	lf, err := lockfile.Load(lockfile.Filename)
	if err != nil {
		return fmt.Errorf("loading lock file: %w", err)
	}
	if lf != nil {
		lf.Remove(name)
		if err := lockfile.Save(lockfile.Filename, lf); err != nil {
			return fmt.Errorf("saving lock file: %w", err)
		}
	}

	fmt.Printf("Removed %s from vendor and lock file.\n", name)
	return nil
}

// fileChecksum returns the hex-encoded SHA256 checksum of a file.
func fileChecksum(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", fmt.Errorf("opening file for checksum: %w", err)
	}
	defer f.Close()

	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", fmt.Errorf("computing checksum: %w", err)
	}
	return fmt.Sprintf("%x", h.Sum(nil)), nil
}
