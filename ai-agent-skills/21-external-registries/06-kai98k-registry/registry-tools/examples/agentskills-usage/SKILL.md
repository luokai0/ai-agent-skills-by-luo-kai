---
name: "agentskills-usage"
version: "1.0.0"
description: "Teaches AI agents how to use the AgentSkills Registry CLI to search, pull, and push skill bundles"
author: "agentskills"
tags:
  - meta
  - tutorial
  - cli
  - agent
---

# AgentSkills Registry Usage

You are an AI agent that can interact with the AgentSkills Registry to discover, download, and publish reusable skill bundles. Use the `agentskills` CLI tool to communicate with the registry server.

## Prerequisites

- The `agentskills` CLI must be installed and available in PATH.
- A registry server must be running (default: `http://localhost:8000`).
- To publish skills, you need an API token configured via `agentskills login`.

## Available Commands

### Search for Skills

Find skills by keyword or tag:

```bash
agentskills search <keyword>
```

Example:

```bash
agentskills search code-review
```

Output:

```
NAME                VERSION  DOWNLOADS  DESCRIPTION
code-review-agent   1.2.0    42         Automated PR code review skill
code-review-style   0.3.0    18         Style-focused code review
```

### Pull (Download) a Skill

Download a skill bundle and extract it to the current directory:

```bash
# Pull the latest version
agentskills pull <skill-name>

# Pull a specific version
agentskills pull <skill-name>@<version>
```

Example:

```bash
agentskills pull code-review-agent
```

This creates a `code-review-agent/` directory containing:

```
code-review-agent/
├── SKILL.md         # Read this to understand the skill's instructions
├── scripts/         # Executable scripts you can call
├── references/      # Reference documents for RAG / few-shot learning
└── assets/          # Static templates and resources
```

**After pulling a skill, read its `SKILL.md` to understand what it does and how to use it.**

### Create a New Skill

Scaffold a new skill bundle:

```bash
agentskills init <skill-name>
```

Then edit the generated `SKILL.md` to define:
- **YAML frontmatter**: name, version, description, author, tags
- **Markdown body**: instructions that tell agents what this skill does and how to use it

### Push (Publish) a Skill

Upload a skill bundle to the registry:

```bash
agentskills push <path-to-skill-directory>
```

Example:

```bash
agentskills push ./my-new-skill
```

The CLI will validate `SKILL.md`, pack the directory into a `.tar.gz` bundle, upload it to the server, and verify the checksum.

### Configure API Endpoint

By default, the CLI connects to `http://localhost:8000`. Override with the `--api-url` flag:

```bash
agentskills search code-review --api-url https://registry.example.com
```

### Save API Token

To publish skills, save your token first:

```bash
agentskills login
```

## Workflow for Agents

When you need a capability you don't have:

1. **Search** the registry for relevant skills: `agentskills search <keyword>`
2. **Pull** the skill you need: `agentskills pull <skill-name>`
3. **Read** the skill's `SKILL.md` to learn its instructions
4. **Apply** the skill's instructions, scripts, and references to your current task

When you've built a useful capability worth sharing:

1. **Init** a new skill: `agentskills init <skill-name>`
2. **Write** clear instructions in `SKILL.md`, add scripts/references as needed
3. **Push** to the registry: `agentskills push ./<skill-name>`
