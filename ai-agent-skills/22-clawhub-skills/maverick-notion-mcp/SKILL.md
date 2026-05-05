---
name: maverick-notion-mcp
description: Search, read, and update Notion pages, databases, blocks, comments, and workspace content via Notion's hosted MCP server (https://mcp.notion.com/mcp). Use when the user asks about Notion pages, databases, docs, wikis, or workspace content. Do NOT use for Linear/Jira/GitHub work items.
homepage: https://developers.notion.com/guides/mcp/overview
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires":
          {
            "bins": ["mcporter", "jq", "flock", "shasum"],
            "env":
              [
                "MAVERICK_NOTION_MCP_REFRESH_TOKEN",
                "MAVERICK_NOTION_MCP_CLIENT_ID",
                "MAVERICK_NOTION_MCP_ACCESS_TOKEN",
              ],
          },
        "primaryEnv": "MAVERICK_NOTION_MCP_REFRESH_TOKEN",
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
          ],
      },
  }
---

# Notion

## Quick start

Always invoke through `bash {baseDir}/scripts/invoke.sh` — never call `mcporter` directly. The wrapper seeds the OAuth vault from the env-supplied tokens when needed, then calls `mcporter`.

```sh
bash {baseDir}/scripts/invoke.sh call maverick-notion.notion-get-self
bash {baseDir}/scripts/invoke.sh call maverick-notion.notion-search query="roadmap"
```

For structured output (also surfaces transport errors as JSON envelopes — workaround for mcporter [#153](https://github.com/steipete/mcporter/issues/153)):

```sh
bash {baseDir}/scripts/invoke.sh call --output json maverick-notion.notion-search query="roadmap" | jq '.result.content'
```

Discover available tools and schemas:

```sh
bash {baseDir}/scripts/invoke.sh list maverick-notion --schema
```

## Safety

Write operations (`notion-create-pages`, `notion-update-page`, `notion-move-pages`, `notion-duplicate-page`, `notion-create-database`, `notion-update-data-source`, `notion-create-view`, `notion-update-view`, `notion-create-comment`, and broad workspace changes) modify Notion content visible to the connected workspace. Confirm clear user intent before invoking write tools — search and read tools are safe to call freely while exploring. Search before assuming page, database, user, or block IDs, and read the current record before modifying it.

## Authentication

Tokens are provisioned and rotated automatically. If a call returns HTTP 401 that doesn't recover within a few seconds, the OAuth grant has been revoked — re-authorize the integration to refresh credentials.

## Data flow

Tool calls travel to Notion's hosted MCP service at `https://mcp.notion.com/mcp` over HTTPS, authenticated via OAuth. Notion sees the workspace content referenced by each call. Use this skill for Notion-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used to invoke Notion's hosted MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version (e.g. `mcporter@<version>`).
- **`jq`** ([stedolan.github.io/jq](https://stedolan.github.io/jq/)) — JSON processor used by the vault initializer. System dependency; install via your OS package manager (`apt install jq`, `brew install jq`, etc.).
- **`flock`** (part of [util-linux](https://github.com/util-linux/util-linux)) — file locking used to serialize concurrent vault writes. Available by default on Linux; on macOS install via `brew install flock`.
- **`shasum`** (Perl, ships with [`Digest::SHA`](https://metacpan.org/pod/Digest::SHA)) — computes the SHA-256 hashes used to derive the mcporter vault key and the provisioned-token marker. Preinstalled on macOS and on Debian/Ubuntu (incl. the deployed `cloudflare/sandbox` Ubuntu 22.04 image); on minimal Linux images install `perl-Digest-SHA`. The script invokes `shasum -a 256` rather than GNU `sha256sum` so it runs on stock macOS without `coreutils`.
