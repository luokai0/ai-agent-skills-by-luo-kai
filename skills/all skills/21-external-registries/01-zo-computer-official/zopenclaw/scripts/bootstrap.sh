#!/bin/bash
set -euo pipefail

CONFIG="$HOME/.openclaw/openclaw.json"

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: $CONFIG not found."
  echo "Run 'openclaw onboard' in Zo's terminal first."
  exit 1
fi

echo "=== zopenclaw bootstrap ==="
echo ""

# --- Phase 1: Fix tools.profile ---

echo "--- Fixing tools.profile ---"
openclaw config set tools.profile full
PROFILE=$(openclaw config get tools.profile 2>/dev/null || echo "unknown")
if [ "$PROFILE" = "full" ]; then
  echo "[OK] tools.profile = full"
else
  echo "[WARN] tools.profile = $PROFILE (expected 'full')"
  echo "       Trying direct config edit..."
  TMPFILE=$(mktemp)
  jq '.tools.profile = "full"' "$CONFIG" > "$TMPFILE" && mv "$TMPFILE" "$CONFIG"
  echo "[OK] tools.profile patched directly"
fi

# --- Phase 2: Patch gateway config (WITHOUT trustedProxies) ---

echo ""
echo "--- Patching gateway config ---"

TMPFILE=$(mktemp)
jq '
  .gateway.bind = "loopback"
  | .gateway.tailscale.mode = "serve"
  | .gateway.tailscale.resetOnExit = false
  | .gateway.auth.mode = "token"
  | .gateway.auth.allowTailscale = true
  | .gateway.controlUi.enabled = true
  | .gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback = true
  | del(.gateway.host, .gateway.tailscaleServe, .gateway.tokenAuth, .gateway.enableControlUI, .gateway.trustedProxies)
' "$CONFIG" > "$TMPFILE" && mv "$TMPFILE" "$CONFIG"

echo "[OK] gateway.bind = loopback"
echo "[OK] gateway.tailscale.mode = serve"
echo "[OK] gateway.auth.mode = token"
echo "[OK] gateway.auth.allowTailscale = true"
echo "[OK] gateway.controlUi.enabled = true"
echo "[OK] gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback = true"
echo "[OK] removed deprecated gateway keys and cleared trustedProxies for pairing"

# --- Phase 3: Migrate gateway token to .zo_secrets ---

SECRETS_FILE="/root/.zo_secrets"
GW_TOKEN=$(jq -r '.gateway.auth.token // .gateway.token // empty' "$CONFIG")

if [ -n "$GW_TOKEN" ]; then
  if ! grep -q 'OPENCLAW_GATEWAY_TOKEN' "$SECRETS_FILE" 2>/dev/null; then
    echo "export OPENCLAW_GATEWAY_TOKEN=\"$GW_TOKEN\"" >> "$SECRETS_FILE"
    echo "[OK] Gateway token migrated to ~/.zo_secrets"
  else
    echo "[OK] Gateway token already in ~/.zo_secrets"
  fi
else
  echo "[OK] No gateway token to migrate (will be set on first start)"
fi

# --- Phase 4: Stop existing gateway ---

echo ""
echo "--- Stopping existing gateway processes ---"
supervisorctl -s http://127.0.0.1:29011 stop openclaw-gateway 2>/dev/null || true
pkill -f 'openclaw gateway' 2>/dev/null || true
sleep 2
echo "[OK] Existing gateway processes stopped"

# --- Phase 5: Pre-publish Tailscale Serve (best effort) ---

echo ""
echo "--- Preparing Tailscale Serve mapping ---"
if tailscale serve reset >/dev/null 2>&1 && tailscale serve --bg --yes 18789 >/dev/null 2>&1; then
  echo "[OK] Tailscale Serve published to local gateway port 18789"
else
  echo "[WARN] Could not publish Tailscale Serve automatically."
  echo "       Enable Serve for this node in Tailscale admin, then run:"
  echo "       tailscale serve reset"
  echo "       tailscale serve --bg --yes 18789"
fi

echo ""
echo "=== Bootstrap config complete ==="
echo ""
echo "NEXT STEPS (Zo handles these automatically):"
echo "  1. Register gateway as Zo User Service"
echo "  2. Poll for readiness until gateway responds"
echo "  3. Run 'openclaw devices list' to pair local device"
echo "  4. Add trustedProxies to config"
echo "  5. Restart gateway"
echo "  6. Confirm Tailscale Serve is active"
