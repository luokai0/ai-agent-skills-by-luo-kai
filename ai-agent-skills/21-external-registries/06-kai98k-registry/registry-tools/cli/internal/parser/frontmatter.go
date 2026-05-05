package parser

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"gopkg.in/yaml.v3"
)

var (
	nameRegex = regexp.MustCompile(`^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`)
	tagRegex  = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{0,31}$`)
)

type SkillMeta struct {
	Name            string   `yaml:"name"`
	Version         string   `yaml:"version"`
	Description     string   `yaml:"description"`
	Author          string   `yaml:"author"`
	Tags            []string `yaml:"tags"`
	License         string   `yaml:"license"`
	MinAgentVersion string   `yaml:"min_agent_version"`
}

// ParseSkillFile reads and validates SKILL.md from the given directory.
func ParseSkillFile(dir string) (*SkillMeta, error) {
	skillPath := filepath.Join(dir, "SKILL.md")
	data, err := os.ReadFile(skillPath)
	if err != nil {
		return nil, fmt.Errorf("reading SKILL.md: %w", err)
	}

	content := string(data)
	meta, err := extractFrontmatter(content)
	if err != nil {
		return nil, err
	}

	if err := validate(meta); err != nil {
		return nil, err
	}

	return meta, nil
}

func extractFrontmatter(content string) (*SkillMeta, error) {
	content = strings.TrimSpace(content)
	if !strings.HasPrefix(content, "---") {
		return nil, fmt.Errorf("SKILL.md must start with YAML frontmatter (---)")
	}

	parts := strings.SplitN(content[3:], "---", 2)
	if len(parts) < 2 {
		return nil, fmt.Errorf("SKILL.md frontmatter is not properly closed (missing closing ---)")
	}

	yamlContent := strings.TrimSpace(parts[0])
	var meta SkillMeta
	if err := yaml.Unmarshal([]byte(yamlContent), &meta); err != nil {
		return nil, fmt.Errorf("parsing frontmatter YAML: %w", err)
	}

	return &meta, nil
}

func validate(meta *SkillMeta) error {
	// name: required, [a-z0-9\-]{3,64}, no consecutive --
	if meta.Name == "" {
		return fmt.Errorf("name is required")
	}
	if len(meta.Name) < 3 || len(meta.Name) > 64 {
		return fmt.Errorf("name must be 3-64 characters, got %d", len(meta.Name))
	}
	if !nameRegex.MatchString(meta.Name) {
		return fmt.Errorf("name must match [a-z0-9-] pattern: %q", meta.Name)
	}
	if strings.Contains(meta.Name, "--") {
		return fmt.Errorf("name must not contain consecutive dashes: %q", meta.Name)
	}

	// version: required, semver
	if meta.Version == "" {
		return fmt.Errorf("version is required")
	}
	if !isValidSemver(meta.Version) {
		return fmt.Errorf("version must be valid semver (MAJOR.MINOR.PATCH): %q", meta.Version)
	}

	// description: required, 1-256 chars
	if meta.Description == "" {
		return fmt.Errorf("description is required")
	}
	if len(meta.Description) > 256 {
		return fmt.Errorf("description must be at most 256 characters, got %d", len(meta.Description))
	}

	// author: required
	if meta.Author == "" {
		return fmt.Errorf("author is required")
	}

	// tags: optional, max 10, each matches pattern
	if len(meta.Tags) > 10 {
		return fmt.Errorf("at most 10 tags allowed, got %d", len(meta.Tags))
	}
	for _, tag := range meta.Tags {
		if !tagRegex.MatchString(tag) {
			return fmt.Errorf("invalid tag %q: must match [a-z0-9-]{1,32}", tag)
		}
	}

	return nil
}

func isValidSemver(v string) bool {
	parts := strings.Split(v, ".")
	if len(parts) != 3 {
		return false
	}
	for _, p := range parts {
		if p == "" {
			return false
		}
		for _, c := range p {
			if c < '0' || c > '9' {
				return false
			}
		}
		// No leading zeros (except "0" itself)
		if len(p) > 1 && p[0] == '0' {
			return false
		}
	}
	return true
}
