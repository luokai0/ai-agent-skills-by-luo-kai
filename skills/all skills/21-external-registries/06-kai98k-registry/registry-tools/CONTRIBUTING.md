# Contributing to AgentSkills Registry

Welcome! We appreciate contributions from both **humans and AI agents**. Whether you're fixing a bug, adding a feature, or sharing a new Skill Bundle, this guide will help you get started.

## Ways to Contribute

- **Code** — Improve the CLI, server, or internal packages
- **Skill Bundles** — Add useful skills to `examples/` for the community
- **Issues** — Report bugs, suggest features, or ask questions

## Development Setup

```bash
# Clone the repo
git clone https://github.com/kai98k/agent-skills-registry.git
cd agent-skills-registry

# Build the CLI
cd cli
go build -o bin/agentskills .

# Run tests (including server tests)
go test -v -race -tags server ./...

# Start the server locally (Docker)
cd ..
docker build -t agentskills-server .
docker run -p 8000:8000 -v agentskills-data:/data agentskills-server
```

## Contributing Code

### Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Run tests: `cd cli && go test -tags server ./...`
5. Commit with a descriptive message (see convention below)
6. Push and open a Pull Request

### Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add version listing endpoint
fix: correct checksum comparison in download handler
docs: update FAQ section in README
test: add integration test for publish flow
refactor: simplify store metadata loading
```

### Testing

All PRs must pass existing tests. If you add new functionality, add corresponding tests.

```bash
# Run all tests (CLI + server)
cd cli
go test -v -race -tags server ./...
```

### Server Code

Files that are only needed for the server must include the build tag:

```go
//go:build server

package server
```

This ensures the server code is excluded from CLI-only builds.

## Contributing Skill Bundles

We welcome community-contributed skills in the `examples/` directory.

### Requirements

1. Create your skill in `examples/<skill-name>/`
2. Include a valid `SKILL.md` with proper YAML frontmatter:

```yaml
---
name: "my-skill"          # Required: [a-z0-9-], 3-64 chars
version: "1.0.0"          # Required: strict semver
description: "..."        # Required: 1-256 chars
author: "your-name"       # Required
tags:                      # Optional: max 10
  - relevant-tag
---
```

3. Add practical content — `scripts/`, `references/`, or `assets/` that make the skill genuinely useful
4. Open a PR with a brief description of what the skill does and when an agent would use it

### Example Structure

```
examples/my-skill/
├── SKILL.md              # Skill definition and instructions
├── scripts/              # Executable scripts (optional)
├── references/           # RAG / few-shot documents (optional)
└── assets/               # Templates and resources (optional)
```

## Agent-Driven Development

We actively encourage AI agents to contribute to this project. In fact, this repo was largely built by agents.

### Guidelines for Agent Contributors

- **Agents can open PRs** — An AI agent (Claude Code, Cursor, etc.) can autonomously search the codebase, write code, run tests, and submit pull requests.
- **Co-author attribution** — Agent-authored commits should include a `Co-Authored-By` trailer:

```
feat: add health check endpoint

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

- **Human review required** — All PRs (from humans or agents) go through the same review process. A human maintainer is responsible for the final review and merge.
- **Test before submitting** — Agents should run `go test -tags server ./...` and verify their changes work before opening a PR.

### Recommended Agent Workflow

```
Human: "Add a health check endpoint to the server"
  │
  ▼
Agent: explores codebase → implements handler → adds test → runs tests → opens PR
  │
  ▼
Human: reviews PR → merges
```

## Code Style

- Go code must be formatted with `gofmt`
- Follow existing patterns in the codebase
- Keep changes focused — one feature or fix per PR

## Questions?

Open an [issue](https://github.com/kai98k/agent-skills-registry/issues) and we'll be happy to help.
