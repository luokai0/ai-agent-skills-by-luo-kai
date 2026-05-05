<p align="center">
  <picture>
    <source srcset=".github/RisingWave-logo-dark.svg" width="400px" media="(prefers-color-scheme: dark)">
    <img src=".github/RisingWave-logo-light.svg" width="400px">
  </picture>
</p>

<div align="center">

### Agent Skills for RisingWave

</div>

<p align="center">
  <a href="https://docs.risingwave.com/">Docs</a> | <a href="#installation">Installation</a> | <a href="#available-skills">Skills</a> | <a href="CONTRIBUTING.md">Contributing</a>
</p>

<div align="center">
  <a href="https://github.com/risingwavelabs/agent-skills/blob/main/LICENSE" target="_blank">
    <img alt="License" src="https://img.shields.io/badge/license-Apache%202.0-blue" />
  </a>
  <a href="https://go.risingwave.com/slack" target="_blank">
    <img alt="Slack" src="https://badgen.net/badge/Slack/Join%20RisingWave/0abd59?icon=slack" />
  </a>
  <a href="https://x.com/risingwavelabs" target="_blank">
    <img alt="X" src="https://img.shields.io/twitter/follow/risingwavelabs" />
  </a>
  <a href="https://github.com/risingwavelabs/agent-skills/actions/workflows/validate.yml" target="_blank">
    <img alt="Validate" src="https://github.com/risingwavelabs/agent-skills/actions/workflows/validate.yml/badge.svg" />
  </a>
</div>

---

Official Agent Skills for [RisingWave](https://risingwave.com/) — the streaming SQL database. These skills help AI coding agents adopt best practices when building real-time pipelines, designing materialized views, configuring CDC ingestion, and optimizing streaming workloads.

Compatible with Claude Code, GitHub Copilot, Cursor, Windsurf, Gemini CLI, and [18+ other AI agents](#supported-agents).

## Installation

```bash
npx skills add risingwavelabs/agent-skills
```

The CLI auto-detects installed agents and prompts you to select where to install.

### Install a specific skill

```bash
npx skills add risingwavelabs/agent-skills --skill risingwave
npx skills add risingwavelabs/agent-skills --skill risingwave-best-practices
```

### Claude Code Plugin

```bash
claude plugin marketplace add risingwavelabs/agent-skills
claude plugin install risingwave@risingwave-agent-skills
claude plugin install risingwave-best-practices@risingwave-agent-skills
```

## What is this?

Agent Skills are packaged instructions that extend AI coding agents with domain-specific expertise. This repository provides skills for RisingWave — covering connections, the Source → Materialized View → Sink pipeline pattern, CDC ingestion, time-windowed aggregations, watermarks, and streaming SQL best practices.

When an agent loads these skills, it understands RisingWave-specific concepts that differ from standard PostgreSQL: port 4566, `CREATE SOURCE` vs `CREATE TABLE`, `EMIT ON WINDOW CLOSE`, watermark semantics, `BACKGROUND_DDL`, and more.

Skills follow the open specification at [agentskills.io](https://agentskills.io).

## Available Skills

<details>
<summary><strong>risingwave</strong></summary>

Core skill covering connections, MCP server setup, and the fundamental pipeline pattern.

**Use when:**

- Connecting to RisingWave (port 4566, psql, JDBC, any PostgreSQL client)
- Setting up the [RisingWave MCP server](https://github.com/risingwavelabs/risingwave-mcp)
- Creating sources, materialized views, or sinks
- Ingesting from Kafka, CDC databases (PostgreSQL, MySQL), or cloud storage
- Writing time-windowed aggregations (TUMBLE, HOP, SESSION)
- Using watermarks and `EMIT ON WINDOW CLOSE`
- Querying the system catalog (`rw_catalog`)

</details>

<details>
<summary><strong>risingwave-best-practices</strong></summary>

**14 rules** covering schema design, materialized view patterns, CDC setup, sink configuration, and performance — prioritized by impact.

| Category | Rules | Impact |
|----------|-------|--------|
| Schema Design | 3 | CRITICAL / HIGH |
| Materialized Views | 3 | CRITICAL / HIGH |
| Streaming SQL | 3 | CRITICAL / HIGH |
| Sink Configuration | 2 | HIGH / MEDIUM |
| Performance | 3 | HIGH / MEDIUM |

**Use when:**

- Designing sources, tables, or pipelines
- Writing or reviewing materialized views
- Configuring CDC from PostgreSQL or MySQL
- Setting up sinks to Kafka, Iceberg, or other destinations
- Debugging slow backfills or high-volume sink output

</details>

---

## Quick Start

After installation, your AI agent will reference these skills when working with RisingWave. Example prompts:

```
Create a Kafka source for user events and a materialized view that counts events per minute
```

```
Set up PostgreSQL CDC into RisingWave and join the CDC table with a Kafka stream
```

```
Why is my EMIT ON WINDOW CLOSE materialized view not producing any output?
```

```
Create an Iceberg sink for my fraud detection materialized view
```

```
Review this RisingWave pipeline for best practices
```

## Supported Agents

Skills are agent-agnostic — the same skill works across all supported AI coding assistants:

| Agent | Config Directory |
|-------|-----------------|
| [Claude Code](https://claude.ai/code) | `.claude/skills/` |
| [Cursor](https://cursor.sh) | `.cursor/skills/` |
| [Windsurf](https://codeium.com/windsurf) | `.windsurf/skills/` |
| [GitHub Copilot](https://github.com/features/copilot) | `.github/skills/` |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `.gemini/skills/` |
| [Cline](https://github.com/cline/cline) | `.cline/skills/` |
| [Codex](https://openai.com/codex) | `.codex/skills/` |
| [Goose](https://github.com/block/goose) | `.goose/skills/` |
| [Roo Code](https://roo.ai) | `.roo/skills/` |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | `.openhands/skills/` |

And others including Amp, Kiro CLI, Trae, Zencoder, and more.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) to add new rules, improve existing skills, or propose a new skill.

## License

Apache 2.0 — see [LICENSE](./LICENSE) for details.
