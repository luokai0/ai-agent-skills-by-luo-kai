#!/bin/bash
set -euo pipefail

echo "=== zopenclaw Health Check ==="
echo ""

PASS=0
FAIL=0

check() {
  local label="$1"
  local cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "[OK]   $label"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] $label"
    FAIL=$((FAIL + 1))
  fi
}

check "OpenClaw installed" "openclaw --version"

PROFILE=$(openclaw config get tools.profile 2>/dev/null || echo "unknown")
if [ "$PROFILE" = "full" ]; then
  echo "[OK]   tools.profile = full"
  PASS=$((PASS + 1))
else
  echo "[FAIL] tools.profile = $PROFILE (should be 'full')"
  FAIL=$((FAIL + 1))
fi

check "Tailscale connected" "tailscale status --json 2>/dev/null | jq -e '.BackendState == \"Running\"'"
check "Tailscale service (supervisord)" "supervisorctl -s http://127.0.0.1:29011 status tailscale 2>/dev/null | grep RUNNING"
check "Gateway service (supervisord)" "supervisorctl -s http://127.0.0.1:29011 status openclaw-gateway 2>/dev/null | grep RUNNING"
check "Gateway RPC probe" "openclaw gateway status 2>&1 | grep -qE 'RPC probe: ok|Listening:'"
check "Gateway Tailscale mode = serve" "jq -e '.gateway.tailscale.mode == \"serve\"' ~/.openclaw/openclaw.json"

TS_HOST=$(tailscale status --json 2>/dev/null | jq -r '.Self.DNSName // empty' | sed 's/\.$//')
if [ -n "$TS_HOST" ]; then
  echo "[OK]   Tailscale hostname: $TS_HOST"
  echo "       Control UI: https://$TS_HOST"
  PASS=$((PASS + 1))
else
  echo "[FAIL] Could not resolve Tailscale hostname"
  FAIL=$((FAIL + 1))
fi

check "Tailscale Serve HTTPS enabled (443)" "tailscale serve status --json 2>/dev/null | jq -e '.TCP[\"443\"].HTTPS == true'"
if [ -n "$TS_HOST" ]; then
  if tailscale serve status --json 2>/dev/null | jq -e --arg host "$TS_HOST" '.Web[$host + ":443"].Handlers["/"].Proxy == "http://127.0.0.1:18789"' &>/dev/null; then
    echo "[OK]   Tailscale Serve target = http://127.0.0.1:18789"
    PASS=$((PASS + 1))
  else
    echo "[FAIL] Tailscale Serve target is not http://127.0.0.1:18789"
    FAIL=$((FAIL + 1))
  fi
fi

if jq -e '.gateway.trustedProxies' ~/.openclaw/openclaw.json &>/dev/null; then
  echo "[OK]   trustedProxies configured"
  PASS=$((PASS + 1))
else
  echo "[FAIL] trustedProxies not set in config"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
