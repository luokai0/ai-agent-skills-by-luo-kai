# zopenclaw Architecture Reference

This document explains WHY each decision was made. Read this for context when debugging issues or when the user asks about the design.

## Why Tailscale

Tailscale creates a private mesh network (tailnet) between your devices. On Zo, it serves three purposes:

1. **Private access to Control UI** -- OpenClaw's browser-based management interface is only accessible on your tailnet, not the public internet
2. **HTTPS certificates** -- Tailscale provisions TLS certs automatically via its own CA, no manual SSL setup
3. **SSH access** -- You can SSH into your Zo from any device on your tailnet (`ssh root@zo-workspace`)

Without Tailscale, the Control UI would either be inaccessible (localhost only) or publicly exposed (security risk). Tailscale gives private access with zero config.

Tailscale runs in userspace networking mode (`--tun=userspace-networking`) because Zo containers don't have iptables/netfilter access.

## Why `register_user_service` (not raw supervisord)

Zo periodically reprovisions containers for maintenance. When this happens:

- Manual edits to `/etc/zo/supervisord-user.conf` get wiped
- Processes started with `nohup` or manual supervisord entries disappear
- Only `/root/` and `/home/` data survives, plus services registered via `register_user_service`

`register_user_service` is Zo's native process manager. Services registered through it:
- Auto-start on boot
- Auto-restart on crash
- Survive container reprovisions
- Get proper log files in `/dev/shm/`

Both Tailscale and the OpenClaw gateway are registered this way.

## Why the Two-Phase Bootstrap

OpenClaw's gateway has a `trustedProxies` config that tells it to trust `X-Forwarded-For` and `Tailscale-User-Login` headers from reverse proxies. Tailscale Serve acts as a reverse proxy on localhost.

**The deadlock:**
- If `trustedProxies` is set before device pairing, CLI connections fail (they don't send proxy headers, so the gateway can't identify the client)
- If `trustedProxies` is NOT set, Tailscale browser connections can't authenticate (gateway sees all traffic from 127.0.0.1 with no identity)

**The fix (two-phase bootstrap):**
1. Start gateway WITHOUT `trustedProxies`
2. Run `openclaw devices list` to pair the local CLI device (works because no proxy trust is required for direct connections)
3. Add `trustedProxies: ["127.0.0.1/32"]` to config
4. Restart gateway

Now both connection types work:
- Browser connections through Tailscale are trusted (they come through the proxy at 127.0.0.1 with identity headers)
- The already-paired CLI device still works via direct connection

## Why mcporter for Zo Tools

OpenClaw does not have native MCP client support. GitHub issue #29053 is an open feature request for it. The `mcpServers` block in `openclaw.json` is for exposing OpenClaw as an MCP server to other tools, not for consuming external MCP servers.

mcporter is the current standard bridge that connects external MCP servers into OpenClaw's tool system. It's maintained by Peter Steinberger (OpenClaw's creator) and is widely used in the community for integrating services like Linear, Context7, Firecrawl, and others.

For Zo, mcporter bridges the Zo MCP endpoint (`https://api.zo.computer/mcp`) into OpenClaw, giving the agent access to 50+ Zo tools: web search, Gmail, Calendar, Drive, media generation, sending SMS/email, and more. The config is a single command:

```bash
mcporter config add zo https://api.zo.computer/mcp \
  --header "Authorization: Bearer $ZO_ACCESS_TOKEN" \
  --scope home
```

The access token is a long-lived Zo access token (not a session token) created in Settings > Advanced > Access Tokens and stored as a secret. Unlike the 24-hour tokens used in some community guides, these don't expire silently.

When OpenClaw eventually ships native MCP client support, the mcporter bridge can be replaced with a direct config entry. Until then, mcporter is required.

## Why User Runs `openclaw onboard` Manually

OpenClaw supports many LLM providers (Anthropic, OpenAI, OpenRouter, Google, local models, etc.) and many messaging channels (Telegram, Discord, WhatsApp, Slack, Signal, iMessage, IRC, etc.). The onboarding wizard handles all of these.

If we replicated the wizard in our skill, we'd have to update it every time OpenClaw adds a provider or channel. Instead, we let the user run the official wizard in Zo's terminal, then we handle everything Zo-specific afterward.

## Why Secrets Go in Settings > Advanced

API keys and tokens must NEVER appear in chat. Chat logs are stored and could be reviewed. Zo's Settings > Advanced provides encrypted secret storage that's accessible to the environment as env vars. The install script reads `TAILSCALE_AUTHKEY` from env, not from user input.
