---
name: zopenclaw
description: |
  Install and run OpenClaw on Zo Computer with Tailscale private networking, browser Control UI, and Zo MCP tools via mcporter. Use this skill whenever the user wants to set up OpenClaw on their Zo, install OpenClaw, run OpenClaw, host OpenClaw, or asks about getting OpenClaw running on Zo. Also use when the user mentions "openclaw", "open claw", "personal agent framework", or asks about running a persistent AI agent on their Zo with Telegram/Discord/WhatsApp access. Handles Tailscale setup, OpenClaw installation, mcporter setup for Zo tools, two-phase gateway bootstrap, reprovision-safe service registration, and health verification. NOT for general Zo agent setup (use heartbeats and native Zo skills instead).
compatibility: Requires Zo Computer, Node.js (pre-installed on Zo), npm, curl, jq
metadata:
  author: skeletorjs
  category: Integration
  display-name: Install OpenClaw on Zo
  tags: openclaw, agent, tailscale, personal-agent, framework
---
# zopenclaw

Install OpenClaw on Zo Computer with Tailscale private networking.

## What This Sets Up

- OpenClaw agent framework (persistent, 24/7)
- Tailscale private mesh network (secure access to Control UI + SSH)
- Browser-based Control UI via HTTPS on your tailnet
- Gateway registered as a Zo User Service (survives reprovisions and crashes)
- Zo MCP tools bridged into OpenClaw via mcporter (web search, Gmail, Calendar, media generation, etc.)

## Prerequisites

- Zo Computer account (any tier)
- Tailscale account (free tier works)
- API key from an LLM provider (Anthropic, OpenAI, OpenRouter, etc.)
- A messaging channel token (Telegram bot, Discord bot, or WhatsApp)
- Tailscale Serve enabled for this node (required for Control UI over HTTPS)

## When to Read References

- **references/architecture.md** -- When debugging, when the user asks WHY something works the way it does, or when you need to understand the two-phase bootstrap, Tailscale networking mode, or the `register_user_service` pattern
- **references/troubleshooting.md** -- When something isn't working: gateway crashes, Tailscale not connecting, `tools.profile` reverting, port conflicts, reprovision issues, or workspace size limits

## How to Run This Skill

There are six steps. Steps 1 and 3 require user action. Steps 2, 4, 5, and 6 are automated by Zo.

### Step 1: Save your Tailscale auth key (user action)

1. Go to https://login.tailscale.com/admin/settings/keys
2. Create a **reusable** auth key (reusable is important -- Zo restarts between sessions)
3. Go to Zo [Settings > Advanced](/?t=settings&s=advanced)
4. Add a secret: name = `TAILSCALE_AUTHKEY`, value = the key (starts with `tskey-auth-`)

### Step 2: Run the install script (Zo runs)

```bash
bash /home/workspace/Skills/zopenclaw/scripts/install.sh
```

This script:
- Validates `TAILSCALE_AUTHKEY` exists in environment
- Installs Tailscale binary (if not present)
- Writes Tailscale startup script (`/usr/local/bin/start-tailscale.sh`)
- Saves auth key to `~/.zo_secrets`
- Installs OpenClaw via npm (if not present)

After the script completes, Zo registers Tailscale as a Zo User Service:

```
register_user_service(
  label="tailscale",
  protocol="tcp",
  local_port=41641,
  entrypoint="/usr/local/bin/start-tailscale.sh",
  workdir="/root"
)
```

Wait for Tailscale to connect (~10 seconds), then verify:

```bash
tailscale status
```

**Important: Enable Tailscale Serve (user action).** Serve must be enabled for this node before the Control UI will work over HTTPS. Get the node ID and give the user the enablement link:

```bash
tailscale status --json | jq -r '.Self.ID'
```

Tell the user to open:

`https://login.tailscale.com/f/serve?node=<node-id>`

If Serve is not enabled, the Control UI will fail with "requires device identity" because only insecure origins will reach the gateway. Do not proceed to Step 3 until the user confirms Serve is enabled.

### Step 3: Run OpenClaw onboarding (user action)

The user opens Zo's terminal panel and runs:

```
openclaw onboard
```

This is interactive -- the user picks their LLM provider, model, and messaging channel. Do NOT try to automate this. Do NOT use `--install-daemon` (we use `register_user_service` instead).

Wait for the user to confirm onboarding is complete before proceeding.

### Step 4: Run the bootstrap script (Zo runs)

```bash
bash /home/workspace/Skills/zopenclaw/scripts/bootstrap.sh
```

This script:
- Sets `tools.profile` to `full`
- Patches gateway config to current schema (`gateway.bind`, `gateway.tailscale.mode`, `gateway.auth.mode`, `gateway.controlUi.enabled`) and removes deprecated keys (`host`, `tailscaleServe`, `tokenAuth`, `enableControlUI`)
- Sets `gateway.auth.allowTailscale = true` (allows Tailscale-authenticated browser access)
- Sets `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback = true` (fixes "requires device identity" error through Tailscale Serve)
- Sets `gateway.tailscale.resetOnExit = false` (prevents Serve reset when gateway stops, since we manage Serve separately)
- Removes any existing `trustedProxies` (needed for two-phase bootstrap)
- Migrates gateway token to `~/.zo_secrets`
- Pre-publishes Tailscale Serve to port 18789 (best effort -- may need manual setup if Serve is not yet enabled)
- Stops any existing gateway processes

After the script completes, Zo performs the bootstrap sequence:

**Phase 1 -- Start gateway WITHOUT trustedProxies:**

```
register_user_service(
  label="openclaw-gateway",
  protocol="tcp",
  local_port=18789,
  entrypoint="bash -c 'cd /root/.openclaw && exec openclaw gateway run'",
  workdir="/root/.openclaw"
)
```

Wait for readiness (poll instead of fixed sleep), then pair the local device:

```bash
for i in $(seq 1 20); do
  if openclaw gateway status 2>&1 | grep -qE 'RPC probe: ok|Listening:'; then
    break
  fi
  sleep 1
done
openclaw devices list
```

If there is a pending request, approve it:

```bash
/home/workspace/Skills/zopenclaw/scripts/pairing-helper.sh device <request-id>
```

**Phase 2 -- Add trustedProxies and restart:**

```bash
jq '.gateway.trustedProxies = ["127.0.0.1/32"]' ~/.openclaw/openclaw.json > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json
supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway
```

**Phase 3 -- Verify Tailscale Serve HTTPS (bootstrap.sh already attempts this, but verify/fix here):**

```bash
tailscale serve status --json | jq .
```

If the serve mapping is missing or wrong, reset and re-publish:

```bash
tailscale serve reset
tailscale serve --bg --yes 18789
tailscale serve status --json | jq .
```

Expected proxy target:

`https://<tailscale-hostname>/ -> http://127.0.0.1:18789`

If you see `127.0.0.1:3000` (or any other port), reset and re-run the commands above.

**Phase 4 -- Provision HTTPS certificate:**

```bash
TS_HOST=$(tailscale status --json | jq -r '.Self.DNSName' | sed 's/\.$//')
tailscale cert "$TS_HOST"
```

### Step 5: Verify (Zo runs)

```bash
bash /home/workspace/Skills/zopenclaw/scripts/verify.sh
```

On success:

- Tell the user their Control UI is at `https://<tailscale-hostname>`
- Tell the user to access ONLY the HTTPS tailnet hostname URL
- Do NOT use `http://<tailscale-ip>:18789` or any non-HTTPS proxy URL

If the UI says "pairing required", approve pending requests:

```bash
openclaw devices list
openclaw devices approve <request-id>
```

If Telegram asks for pairing code:

```bash
/home/workspace/Skills/zopenclaw/scripts/pairing-helper.sh telegram <PAIRING_CODE>
```

### Step 6: Connect Zo Tools via mcporter (Zo runs)

OpenClaw does not have native MCP client support (it's an open feature request). mcporter bridges MCP servers into OpenClaw's tool system, giving your agent access to Zo's 50+ tools (web search, Gmail, Calendar, Drive, media generation, etc.).

**Prerequisites:** The user needs a Zo access token.

1. Direct the user to [Settings > Advanced](/?t=settings&s=advanced)
2. In the **Access Tokens** area, create a new token
3. Save the token value as a secret named `ZO_ACCESS_TOKEN` in the **Secrets** area on the same page

**Configure mcporter (Zo runs):**

mcporter was installed by the install script in Step 2. Add Zo's MCP server:

```bash
source /root/.zo_secrets
mcporter config add zo https://api.zo.computer/mcp \
  --header "Authorization: Bearer $ZO_ACCESS_TOKEN" \
  --scope home
```

Verify the connection:

```bash
mcporter list
mcporter call zo.web_search --args '{"query": "test", "time_range": "day"}'
```

If `mcporter list` shows the zo server and the test call returns results, the bridge is working.

Restart the gateway so OpenClaw picks up the new tools:

```bash
supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway
```

The user can now ask their OpenClaw agent to use Zo tools (search the web, check email, manage calendar, generate images, etc.) via the mcporter bridge.

## Telegram Group Messages (Important)

If OpenClaw warns:

`channels.telegram.groupPolicy is "allowlist" but groupAllowFrom is empty`

then group chats will be silently dropped. Fix one of these:

- Add allowed sender IDs to `channels.telegram.groupAllowFrom` (or `channels.telegram.allowFrom`)
- Set `channels.telegram.groupPolicy` to `open`

If any checks fail, read `references/troubleshooting.md` for diagnosis and fixes.
