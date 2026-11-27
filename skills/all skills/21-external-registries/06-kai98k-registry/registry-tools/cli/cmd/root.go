package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "agentskills",
	Short: "AgentSkills CLI — publish and pull AI agent skill bundles",
	Long:  "AgentSkills is a CLI tool for publishing and pulling standardized AI Agent Skill Bundles from the AgentSkills Registry.",
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().String("api-url", "http://localhost:8000", "AgentSkills API base URL")
}
