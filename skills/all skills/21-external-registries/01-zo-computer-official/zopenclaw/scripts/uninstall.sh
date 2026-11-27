#!/bin/bash
set -euo pipefail

echo "=== zopenclaw Uninstall ==="
echo ""
echo "This will stop and remove the OpenClaw gateway and Tailscale services."
echo "OpenClaw config (~/.openclaw/) and Tailscale binaries are NOT removed."
echo ""

read -rp "Continue? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Cancelled."
  exit 0
fi

echo ""

# --- Stop and remove gateway ---

echo "--- Stopping OpenClaw gateway ---"
supervisorctl -s http://127.0.0.1:29011 stop openclaw-gateway 2>/dev/null || true
pkill -f 'openclaw gateway' 2>/dev/null || true
echo "[OK] Gateway stopped"
echo ""
echo "NOTE: Zo should run delete_user_service for 'openclaw-gateway'"

# --- Stop and remove Tailscale ---

echo ""
echo "--- Stopping Tailscale ---"
supervisorctl -s http://127.0.0.1:29011 stop tailscale 2>/dev/null || true
echo "[OK] Tailscale stopped"
echo ""
echo "NOTE: Zo should run delete_user_service for 'tailscale'"

# --- Remove startup script ---

rm -f /usr/local/bin/start-tailscale.sh
echo "[OK] Removed /usr/local/bin/start-tailscale.sh"

# --- Clean secrets ---

sed -i '/TAILSCALE_AUTHKEY/d' /root/.zo_secrets 2>/dev/null || true
sed -i '/OPENCLAW_GATEWAY_TOKEN/d' /root/.zo_secrets 2>/dev/null || true
echo "[OK] Removed Tailscale and gateway secrets from ~/.zo_secrets"

# --- Uninstall OpenClaw ---

echo ""
read -rp "Also uninstall OpenClaw (npm uninstall -g openclaw)? [y/N] " uninstall_oc
if [[ "$uninstall_oc" =~ ^[Yy]$ ]]; then
  npm uninstall -g openclaw 2>/dev/null || true
  echo "[OK] OpenClaw uninstalled"
else
  echo "[OK] OpenClaw kept installed"
fi

echo ""
echo "=== Uninstall complete ==="
echo ""
echo "What was NOT removed:"
echo "  - ~/.openclaw/ (config + workspace)"
echo "  - Tailscale binaries (/usr/bin/tailscale, /usr/sbin/tailscaled)"
echo "  - Tailscale state (/var/lib/tailscale/)"
echo ""
echo "Zo still needs to run delete_user_service for both services."
