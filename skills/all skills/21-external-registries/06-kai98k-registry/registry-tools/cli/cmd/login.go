package cmd

import (
	"fmt"

	"github.com/liuyukai/agentskills-cli/internal/config"
	"github.com/spf13/cobra"
)

var loginCmd = &cobra.Command{
	Use:   "login",
	Short: "Save API token to local config",
	RunE: func(cmd *cobra.Command, args []string) error {
		fmt.Print("Enter API token: ")
		var token string
		if _, err := fmt.Scanln(&token); err != nil {
			return fmt.Errorf("reading token: %w", err)
		}

		apiURL, _ := cmd.Flags().GetString("api-url")
		cfg := config.Config{
			APIURL: apiURL,
			Token:  token,
		}
		if err := config.Save(cfg); err != nil {
			return fmt.Errorf("saving config: %w", err)
		}

		fmt.Println("Token saved to ~/.agentskills/config.yaml")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(loginCmd)
}
