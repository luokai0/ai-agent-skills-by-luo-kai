package config

import (
	"fmt"
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

type Config struct {
	APIURL string `yaml:"api_url"`
	Token  string `yaml:"token"`
}

func configDir() string {
	home, err := os.UserHomeDir()
	if err != nil {
		return filepath.Join(".", ".agentskills")
	}
	return filepath.Join(home, ".agentskills")
}

func configPath() string {
	return filepath.Join(configDir(), "config.yaml")
}

func Load() (Config, error) {
	cfg := Config{
		APIURL: "http://localhost:8000",
	}

	data, err := os.ReadFile(configPath())
	if err != nil {
		if os.IsNotExist(err) {
			return cfg, nil
		}
		return cfg, fmt.Errorf("reading config: %w", err)
	}

	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return cfg, fmt.Errorf("parsing config: %w", err)
	}
	return cfg, nil
}

func Save(cfg Config) error {
	dir := configDir()
	if err := os.MkdirAll(dir, 0o700); err != nil {
		return fmt.Errorf("creating config dir: %w", err)
	}

	data, err := yaml.Marshal(cfg)
	if err != nil {
		return fmt.Errorf("marshaling config: %w", err)
	}

	if err := os.WriteFile(configPath(), data, 0o600); err != nil {
		return fmt.Errorf("writing config: %w", err)
	}
	return nil
}
