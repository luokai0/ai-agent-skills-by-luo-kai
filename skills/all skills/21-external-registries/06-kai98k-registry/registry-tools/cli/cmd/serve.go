//go:build server

package cmd

import (
	"fmt"
	"log"
	"net/http"

	"github.com/liuyukai/agentskills-cli/server"
	"github.com/spf13/cobra"
)

var serveCmd = &cobra.Command{
	Use:   "serve",
	Short: "Start the AgentSkills registry HTTP server",
	RunE: func(cmd *cobra.Command, args []string) error {
		port, _ := cmd.Flags().GetInt("port")
		dataDir, _ := cmd.Flags().GetString("data-dir")
		token, _ := cmd.Flags().GetString("token")

		store := server.NewStore(dataDir)
		handler := server.NewHandler(store, token)

		mux := http.NewServeMux()
		handler.RegisterRoutes(mux)

		addr := fmt.Sprintf(":%d", port)
		log.Printf("AgentSkills server listening on %s (data: %s)", addr, dataDir)
		return http.ListenAndServe(addr, mux)
	},
}

func init() {
	serveCmd.Flags().Int("port", 8000, "Port to listen on")
	serveCmd.Flags().String("data-dir", "/data", "Data directory for bundles and metadata")
	serveCmd.Flags().String("token", "", "Bearer token required for publish (empty = no auth)")
	rootCmd.AddCommand(serveCmd)
}
