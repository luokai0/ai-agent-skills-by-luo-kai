package cmd

import (
	"fmt"
	"text/tabwriter"
	"os"

	"github.com/liuyukai/agentskills-cli/internal/api"
	"github.com/liuyukai/agentskills-cli/internal/config"
	"github.com/spf13/cobra"
)

var searchCmd = &cobra.Command{
	Use:   "search <keyword>",
	Short: "Search for skills on the registry",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		keyword := args[0]

		cfg, err := config.Load()
		if err != nil {
			return fmt.Errorf("loading config: %w", err)
		}

		client := api.NewClient(cfg.APIURL, cfg.Token)
		results, err := client.Search(keyword)
		if err != nil {
			return fmt.Errorf("search failed: %w", err)
		}

		if len(results.Results) == 0 {
			fmt.Println("No skills found.")
			return nil
		}

		w := tabwriter.NewWriter(os.Stdout, 0, 0, 2, ' ', 0)
		fmt.Fprintln(w, "NAME\tVERSION\tDOWNLOADS\tDESCRIPTION")
		for _, r := range results.Results {
			fmt.Fprintf(w, "%s\t%s\t%d\t%s\n", r.Name, r.LatestVersion, r.Downloads, r.Description)
		}
		w.Flush()
		return nil
	},
}

func init() {
	rootCmd.AddCommand(searchCmd)
}
