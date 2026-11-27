# zopenclaw Troubleshooting

## `tools.profile` reverts to "messaging"

After OpenClaw updates or re-running onboard, `tools.profile` can silently reset. This blocks shell, file, and web access. Fix:

```bash
openclaw config set tools.profile full
openclaw config get tools.profile
```

## Gateway not picking up config/workspace changes

Config and workspace changes require a gateway restart:

```bash
supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway
```

## Tailscale not connecting

```bash
# Check auth key exists
grep TAILSCALE /root/.zo_secrets

# Check error logs
tail -50 /dev/shm/tailscale_err.log

# Check status
tailscale status
```

## Container reprovision wiped something

If Tailscale or the gateway stopped after a reprovision and services were registered via `register_user_service`, they should auto-recover. If not, re-run the install and bootstrap scripts.

If services were registered manually (raw supervisord edits), they're gone. Re-run the full skill.

## Port conflict on 18789

```bash
pkill -f 'openclaw gateway'
sleep 2
supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway
```

## Gateway crashes and stays offline

Check logs:

```bash
tail -50 /dev/shm/openclaw-gateway.log
tail -50 /dev/shm/openclaw-gateway_err.log
```

If registered via `register_user_service`, it should auto-restart. If it keeps crashing, check the config:

```bash
cat ~/.openclaw/openclaw.json | jq '.gateway'
```

## Tailscale hostname not resolving

Enable MagicDNS on your tailnet: https://login.tailscale.com/admin/dns

## Control UI error: "requires device identity (use HTTPS or localhost secure context)"

This error means the browser reached the gateway without a secure trusted context.

Common causes:

- Using non-HTTPS URL (for example `http://<tailscale-ip>:18789`)
- Using the wrong proxy URL/domain
- Tailscale Serve not enabled for the node
- Tailscale Serve pointing to the wrong local port (for example `127.0.0.1:3000` instead of `127.0.0.1:18789`)
- Device not paired yet

Check and fix:

```bash
# 1) Confirm Tailscale is running
tailscale status --json | jq -r '.BackendState, .Self.DNSName, .Self.ID'

# 2) Confirm Serve is enabled/configured for HTTPS and port 18789
tailscale serve status --json | jq .

# 3) If needed, reset and re-publish the gateway
tailscale serve reset
tailscale serve --bg --yes 18789
tailscale serve status --json | jq .

# 4) Provision cert (should succeed when Serve/TLS is allowed)
TS_HOST=$(tailscale status --json | jq -r '.Self.DNSName' | sed 's/\.$//')
tailscale cert "$TS_HOST"

# 5) Pair pending devices if UI says "pairing required"
openclaw devices list
openclaw devices approve <request-id>
```

Use ONLY this URL in browser:

`https://<tailscale-hostname>`

Do NOT use:

- `http://<tailscale-ip>:18789`
- any non-HTTPS host/proxy URL

If Telegram pairing is requested, approve with:

```bash
openclaw pairing approve telegram <PAIRING_CODE>
```

## Telegram group messages are silently dropped

Symptom:

Doctor warning shows:

`channels.telegram.groupPolicy is "allowlist" but groupAllowFrom (and allowFrom) is empty`

Impact:

- Direct messages can work
- Group messages are silently ignored

Fix options:

1. Add sender IDs to `channels.telegram.groupAllowFrom` (preferred for strict allowlists)
2. Or set `channels.telegram.groupPolicy` to `open` if you want broad group access

Then restart the gateway:

```bash
supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway
```

## `openclaw onboard` fails with validation error

Symptom:

Onboarding crashes during model validation, often with errors about unsupported config keys (e.g., `compat` key in models.json).

Cause:

OpenClaw's local model registry (`~/.openclaw/models.json` or the npm-installed models data) may contain provider entries with config keys that the current version's validator doesn't recognize.

Fix:

```bash
# Find the models.json that onboarding uses
find /root/.openclaw -name "models.json" 2>/dev/null
find $(npm root -g)/openclaw -name "models.json" 2>/dev/null

# Inspect the failing provider entry
cat <path-to-models.json> | jq '.[] | select(.id == "<provider-id>")'

# Remove the offending key (e.g., a bad "compat" block)
TMPFILE=$(mktemp)
jq 'map(if .id == "<provider-id>" then del(.compat) else . end)' <path-to-models.json> > "$TMPFILE" && mv "$TMPFILE" <path-to-models.json>
```

Then retry `openclaw onboard`. If it fails again on a different key, inspect and remove that key too. If the provider itself is broken, remove the entire entry and pick a different provider during onboarding.

## mcporter: Zo tools not appearing in OpenClaw

Symptom:

After configuring mcporter with Zo's MCP endpoint, the OpenClaw agent can't use Zo tools, or `mcporter list` doesn't show the zo server.

Check:

```bash
# Verify mcporter config
mcporter config list

# Test the connection directly
mcporter call zo.web_search --args '{"query": "test", "time_range": "day"}'

# Check if ZO_ACCESS_TOKEN is set
grep ZO_ACCESS_TOKEN /root/.zo_secrets
```

Common causes:

- **Token not saved:** The user needs to create an access token at Settings > Advanced > Access Tokens, then save it as `ZO_ACCESS_TOKEN` in Settings > Advanced > Secrets
- **Token expired or invalid:** Zo access tokens created in Settings > Advanced should be long-lived, but verify the token is still valid
- **Gateway not restarted:** After adding the mcporter config, restart the gateway: `supervisorctl -s http://127.0.0.1:29011 restart openclaw-gateway`
- **mcporter not installed:** Verify with `which mcporter`. If missing, run `npm install -g mcporter@latest`

## Workspace files exceed 20,000 chars

OpenClaw loads all `.md` files from `/root/.openclaw/workspace/` into agent context at session start. If total size exceeds 20,000 characters, content gets silently truncated. Monitor:

```bash
total=0
for f in /root/.openclaw/workspace/*.md; do
  chars=$(wc -c < "$f")
  printf "%6d chars  %s\n" "$chars" "$f"
  total=$((total + chars))
done
echo "------"
printf "%6d total (limit: 20,000)\n" "$total"
```
