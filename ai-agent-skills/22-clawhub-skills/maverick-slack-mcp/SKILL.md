---
name: maverick-slack-mcp
description: Search, read, and update Slack messages, channel history, canvases, and users via Slack's hosted MCP server (https://mcp.slack.com/mcp). Use when the user asks about Slack messages, channels, threads, canvases, users, or wants to send a Slack message.
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "requires":
          {
            "bins": ["mcporter", "jq", "flock", "shasum"],
            "env":
              [
                "MAVERICK_SLACK_MCP_REFRESH_TOKEN",
                "MAVERICK_SLACK_MCP_CLIENT_ID",
                "MAVERICK_SLACK_MCP_ACCESS_TOKEN",
              ],
          },
        "primaryEnv": "MAVERICK_SLACK_MCP_REFRESH_TOKEN",
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

# Slack

## Quick start

Always invoke through `bash {baseDir}/scripts/invoke.sh` — never call `mcporter` directly. The wrapper seeds the OAuth vault from the env-supplied tokens when needed, then calls `mcporter`.

```sh
bash {baseDir}/scripts/invoke.sh call maverick-slack.search_messages query="launch"
bash {baseDir}/scripts/invoke.sh call maverick-slack.conversations_list
bash {baseDir}/scripts/invoke.sh call maverick-slack.users_list
```

For structured output (also surfaces transport errors as JSON envelopes — workaround for mcporter [#153](https://github.com/steipete/mcporter/issues/153)):

```sh
bash {baseDir}/scripts/invoke.sh call --output json maverick-slack.search_messages query="launch" | jq '.result.content'
```

Discover available tools and schemas:

```sh
bash {baseDir}/scripts/invoke.sh list maverick-slack --schema
```

## Safety

Write operations (`chat_postMessage`, canvas edits, replies, message updates, and other externally visible Slack changes) modify Slack content visible to the connected workspace. Confirm clear user intent before invoking write tools — search and read tools are safe to call freely while exploring. Show the exact composed message and get confirmation before posting, and never post to a channel the user has not explicitly named.

## Authentication

Tokens are provisioned and rotated automatically. If a call returns HTTP 401 that doesn't recover within a few seconds, the OAuth grant has been revoked — re-authorize the integration to refresh credentials.

## Data flow

Tool calls travel to Slack's hosted MCP service at `https://mcp.slack.com/mcp` over HTTPS, authenticated via OAuth. Slack sees the message, channel, thread, canvas, and user data referenced by each call. Use this skill for Slack-related work only; do not pass unrelated sensitive content through these tools.

## Dependencies

- **`mcporter`** ([github.com/steipete/mcporter](https://github.com/steipete/mcporter)) — MCP CLI used to invoke Slack's hosted MCP server. Auto-installed via `npm install -g --ignore-scripts mcporter` if missing on PATH (see `install` spec in frontmatter). The install spec uses unpinned `mcporter` (npm `latest`); operators with strict supply-chain controls should override the install to pin a specific version (e.g. `mcporter@<version>`).
- **`jq`** ([stedolan.github.io/jq](https://stedolan.github.io/jq/)) — JSON processor used by the vault initializer. System dependency; install via your OS package manager (`apt install jq`, `brew install jq`, etc.).
- **`flock`** (part of [util-linux](https://github.com/util-linux/util-linux)) — file locking used to serialize concurrent vault writes. Available by default on Linux; on macOS install via `brew install flock`.
- **`shasum`** (Perl, ships with [`Digest::SHA`](https://metacpan.org/pod/Digest::SHA)) — computes the SHA-256 hashes used to derive the mcporter vault key and the provisioned-token marker. Preinstalled on macOS and on Debian/Ubuntu (incl. the deployed `cloudflare/sandbox` Ubuntu 22.04 image); on minimal Linux images install `perl-Digest-SHA`. The script invokes `shasum -a 256` rather than GNU `sha256sum` so it runs on stock macOS without `coreutils`.
