package cmd

import (
	"crypto/sha256"
	"fmt"
	"io"
	"os"
	"strings"

	"github.com/liuyukai/agentskills-cli/internal/api"
	"github.com/liuyukai/agentskills-cli/internal/bundle"
	"github.com/liuyukai/agentskills-cli/internal/config"
	"github.com/spf13/cobra"
)

var pullCmd = &cobra.Command{
	Use:   "pull <name>[@version]",
	Short: "Download and extract a skill bundle",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		nameVersion := args[0]
		name, version := parsePullArg(nameVersion)

		cfg, err := config.Load()
		if err != nil {
			return fmt.Errorf("loading config: %w", err)
		}

		client := api.NewClient(cfg.APIURL, cfg.Token)

		// Resolve version if not specified
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
			fmt.Println("✗")
			return fmt.Errorf("download failed: %w", err)
		}
		defer os.Remove(tmpFile)
		fmt.Println("✓")

		// Verify checksum
		fmt.Print("Verifying checksum...  ")
		f, err := os.Open(tmpFile)
		if err != nil {
			return err
		}
		defer f.Close()
		h := sha256.New()
		if _, err := io.Copy(h, f); err != nil {
			return err
		}
		actual := fmt.Sprintf("%x", h.Sum(nil))
		if expectedChecksum != "" && actual != expectedChecksum {
			fmt.Println("✗")
			return fmt.Errorf("checksum mismatch: expected=%s actual=%s", expectedChecksum, actual)
		}
		fmt.Println("✓")

		// Extract
		if err := bundle.Unpack(tmpFile, name); err != nil {
			return fmt.Errorf("extraction failed: %w", err)
		}
		fmt.Printf("Extracted to ./%s/\n", name)
		return nil
	},
}

func parsePullArg(s string) (name, version string) {
	if idx := strings.LastIndex(s, "@"); idx > 0 {
		return s[:idx], s[idx+1:]
	}
	return s, ""
}

func init() {
	rootCmd.AddCommand(pullCmd)
}
