package cmd

import (
	"crypto/sha256"
	"fmt"
	"io"
	"os"

	"github.com/liuyukai/agentskills-cli/internal/api"
	"github.com/liuyukai/agentskills-cli/internal/bundle"
	"github.com/liuyukai/agentskills-cli/internal/config"
	"github.com/liuyukai/agentskills-cli/internal/parser"
	"github.com/spf13/cobra"
)

var pushCmd = &cobra.Command{
	Use:   "push [path]",
	Short: "Pack and upload a skill bundle",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		skillPath := args[0]

		cfg, err := config.Load()
		if err != nil {
			return fmt.Errorf("loading config: %w", err)
		}

		// Validate SKILL.md locally
		fmt.Print("Validating SKILL.md...        ")
		meta, err := parser.ParseSkillFile(skillPath)
		if err != nil {
			fmt.Println("✗")
			return fmt.Errorf("validation failed: %w", err)
		}
		fmt.Println("✓")

		// Pack bundle
		fmt.Print("Packing bundle...             ")
		bundlePath, err := bundle.Pack(skillPath)
		if err != nil {
			fmt.Println("✗")
			return fmt.Errorf("packing failed: %w", err)
		}
		defer os.Remove(bundlePath)

		fi, err := os.Stat(bundlePath)
		if err != nil {
			return err
		}
		fmt.Printf("✓ (%.1f KB)\n", float64(fi.Size())/1024)

		// Calculate checksum
		f, err := os.Open(bundlePath)
		if err != nil {
			return err
		}
		defer f.Close()
		h := sha256.New()
		if _, err := io.Copy(h, f); err != nil {
			return err
		}
		localChecksum := fmt.Sprintf("sha256:%x", h.Sum(nil))

		// Upload
		fmt.Printf("Uploading %s@%s...   ", meta.Name, meta.Version)
		client := api.NewClient(cfg.APIURL, cfg.Token)
		result, err := client.Publish(bundlePath)
		if err != nil {
			fmt.Println("✗")
			return fmt.Errorf("upload failed: %w", err)
		}
		fmt.Println("✓")

		// Verify checksum
		if result.Checksum != localChecksum {
			return fmt.Errorf("checksum mismatch: local=%s server=%s", localChecksum, result.Checksum)
		}

		fmt.Printf("Checksum: %s\n", result.Checksum)
		fmt.Printf("\nPublished %s@%s successfully.\n", meta.Name, meta.Version)
		return nil
	},
}

func init() {
	rootCmd.AddCommand(pushCmd)
}
