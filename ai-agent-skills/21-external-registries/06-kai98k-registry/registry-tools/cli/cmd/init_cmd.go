package cmd

import (
	"fmt"
	"os"
	"path/filepath"
	"text/template"

	"github.com/spf13/cobra"
)

const skillTemplate = `---
name: "{{.Name}}"
version: "0.1.0"
description: ""
author: ""
tags: []
---

# {{.Name}}

Describe your skill here.
`

var initCmd = &cobra.Command{
	Use:   "init [name]",
	Short: "Create a new skill skeleton in the current directory",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		name := args[0]
		dirs := []string{
			filepath.Join(name, "scripts"),
			filepath.Join(name, "references"),
			filepath.Join(name, "assets"),
		}
		for _, d := range dirs {
			if err := os.MkdirAll(d, 0o755); err != nil {
				return fmt.Errorf("creating directory %s: %w", d, err)
			}
		}

		skillPath := filepath.Join(name, "SKILL.md")
		f, err := os.Create(skillPath)
		if err != nil {
			return fmt.Errorf("creating SKILL.md: %w", err)
		}
		defer f.Close()

		tmpl, err := template.New("skill").Parse(skillTemplate)
		if err != nil {
			return fmt.Errorf("parsing template: %w", err)
		}
		if err := tmpl.Execute(f, struct{ Name string }{Name: name}); err != nil {
			return fmt.Errorf("writing SKILL.md: %w", err)
		}

		fmt.Printf("Created %s/\n", name)
		fmt.Printf("  ├── SKILL.md\n")
		fmt.Printf("  ├── scripts/\n")
		fmt.Printf("  ├── references/\n")
		fmt.Printf("  └── assets/\n")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(initCmd)
}
