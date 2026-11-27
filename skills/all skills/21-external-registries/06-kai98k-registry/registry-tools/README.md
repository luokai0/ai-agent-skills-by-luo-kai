# AgentSkills Registry

**English** | [中文](./README.zh-TW.md)

AgentSkills is a centralized registry platform for AI Agent Skills, similar to npm or Docker Hub. Developers can publish (push) and download (pull) standardized **Skill Bundles** via the CLI tool. The platform handles version control, metadata parsing, and file storage.

## Why AgentSkills?

AI agents (such as Claude Code, AutoGPT, LangChain agents) are becoming increasingly powerful, but they lack a standardized way to **share and reuse capabilities**. AgentSkills solves this by providing:

- **Standardized Skill Format** — Each skill is a directory containing a `SKILL.md` (YAML frontmatter + Markdown instructions), optional `scripts/` for callable tools, `references/` for RAG/few-shot examples, and `assets/` for templates.
- **One-command sharing** — `agentskills push` packages and uploads a skill; `agentskills pull` downloads and extracts it. Just like `npm publish` / `npm install`.
- **Agent-agnostic** — Skill Bundles are plain files. Any agent framework can consume them by reading `SKILL.md` for instructions and loading the accompanying scripts/references.
- **Version control** — Every skill is versioned with strict semver. Teams can pin specific versions and upgrade on their own schedule.
- **Discoverability** — `agentskills search` lets developers find community-contributed skills by keyword or tag (e.g., `code-review`, `data-analysis`, `devops`).

### Skill Bundle Structure

```
my-skill/
├── SKILL.md         # Required: YAML frontmatter (name, version, description, author, tags) + Markdown instructions
├── scripts/         # Optional: scripts the agent can execute
├── references/      # Optional: RAG / few-shot reference documents
└── assets/          # Optional: static templates and resources
```

## How It Works

```
AI Agent (Claude Code, AutoGPT, etc.)
        │
        │  Executes CLI commands in shell
        ▼
   agentskills CLI ──── HTTP REST API ────► agentskills server
   (Go binary)                              (Go binary, built with -tags server)
```

The CLI is the sole interface between agents and the registry server. Agents interact with the platform by executing shell commands — no need to know the underlying HTTP API:

- `agentskills search code-review` → finds matching skills on the server
- `agentskills pull code-review` → downloads and extracts the skill bundle locally
- `agentskills push ./my-skill` → packages and uploads a skill to the server

## Architecture

- **Backend API + CLI Tool**: Go + Cobra in `cli/` (server built with `-tags server`)
- **Storage**: File-based (bundles stored as `.tar.gz` with JSON metadata)
- **Spec**: See [`reference/SDD.md`](./reference/SDD.md) for the complete design document

## Quick Start

### Run the Server (Docker)

```bash
docker build -t agentskills-server .
docker run -p 8000:8000 -v agentskills-data:/data agentskills-server
```

### Build the CLI

```bash
cd cli
go build -o bin/agentskills .
```

### Verify

```bash
# CLI usage
./cli/bin/agentskills --help

# Search for skills
./cli/bin/agentskills search test
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `agentskills init <name>` | Create a new skill skeleton directory |
| `agentskills login` | Save API token to local config |
| `agentskills push <path>` | Pack and upload a skill bundle |
| `agentskills pull <name>[@version]` | Download and extract a skill bundle |
| `agentskills search <keyword>` | Search for skills on the registry |
| `agentskills vendor <name>[@version]` | Vendor a skill locally with checksum lock |
| `agentskills vendor` | Restore all vendored skills from lock file |
| `agentskills vendor --remove <name>` | Remove a vendored skill |

## Project Structure

```
.
├── cli/                  # Go CLI + Server
│   ├── cmd/              # Cobra commands (incl. serve)
│   ├── server/           # HTTP handlers & file store
│   ├── internal/         # Internal packages
│   ├── Dockerfile
│   ├── Makefile
│   └── go.mod
├── reference/            # Design documents
│   └── SDD.md
├── Dockerfile            # Server Docker image
└── docker-compose.yml
```

## Supply Chain Safety

AgentSkills takes supply chain security seriously. Instead of blindly trusting external skills, you can **vendor** them into your repository with cryptographic verification:

```bash
# Vendor a skill — downloads to vendor/skills/ and locks the checksum
agentskills vendor code-review@1.2.0

# Restore all vendored skills on a new machine (verifies checksums)
agentskills vendor

# Remove a vendored skill
agentskills vendor --remove code-review
```

The `agentskills.lock` file records the exact version, SHA-256 checksum, and source server for every vendored skill. Commit this file to your repo to ensure reproducible, tamper-proof builds across your team.

**Security measures:**
- SHA-256 checksum verification on every download
- Path traversal protection in bundle extraction
- Per-file size limits (200 MB) to prevent zip bombs
- Bearer token authentication for publishing

## FAQ

**Q: Why does this project exist?**

AgentSkills Registry provides a standardized way for AI agents to share and reuse capabilities — just as npm revolutionized code sharing for JavaScript developers. Instead of every agent reinventing the wheel, skills can be published once and pulled by anyone.

**Q: Can agents create and publish skills autonomously?**

Yes. The entire workflow — from scaffolding `SKILL.md` to pushing bundles — can be driven entirely by an AI agent. The human only needs to express intent; the agent handles the rest. This repo itself was largely built by agents.

**Q: Can I host my own private registry?**

Yes. The server is a standalone Go binary — deploy it with a single Docker command. Point your CLI to it with `--api-url` and you have a fully private registry, just like self-hosting GitLab. Ideal for enterprise or air-gapped environments.

```bash
# Self-hosted example
docker run -p 8000:8000 -v my-data:/data agentskills-server
agentskills search test --api-url http://my-server:8000
```

**Q: Who is responsible for the quality of published skills?**

The skill author (human or agent). Consumers should review `SKILL.md` and any scripts before using a skill in production. We recommend pinning specific versions and auditing skill content, just as you would with any dependency.

**Q: What's the recommended setup for agent-driven development?**

Run an AI agent (Claude Code, Cursor, etc.) with access to the `agentskills` CLI. The human provides direction; the agent searches for existing skills, pulls them for reference, creates new skills, and pushes them to the registry — all through shell commands.

```
                  intent / direction
  Human Owner ─────────────────────────► AI Agent
                                          │
                                          │ agentskills CLI
                                          ▼
                                    AgentSkills Registry
```

## Contributing

We welcome contributions from both humans and AI agents. See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](./LICENSE).
