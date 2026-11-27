#!/bin/bash
set -euo pipefail

echo "=== zopenclaw install ==="
echo ""

# --- Validate prerequisites ---

if [ -z "${TAILSCALE_AUTHKEY:-}" ]; then
  if [ -f /root/.zo_secrets ]; then
    source /root/.zo_secrets
  fi
  if [ -z "${TAILSCALE_AUTHKEY:-}" ]; then
    echo "ERROR: TAILSCALE_AUTHKEY not found in environment."
    echo ""
    echo "To fix:"
    echo "  1. Go to https://login.tailscale.com/admin/settings/keys"
    echo "  2. Create a reusable auth key"
    echo "  3. Go to Zo Settings > Advanced"
    echo "  4. Add secret: TAILSCALE_AUTHKEY = your key (starts with tskey-auth-)"
    echo "  5. Re-run this script"
    exit 1
  fi
fi

echo "[OK] TAILSCALE_AUTHKEY found"

# --- Install Tailscale binary ---

if command -v tailscale &>/dev/null || test -x /usr/sbin/tailscaled; then
  echo "[OK] Tailscale binary already installed"
else
  echo "     Installing Tailscale..."
  curl -fsSL https://tailscale.com/install.sh | sh
  echo "[OK] Tailscale installed"
fi

# --- Write Tailscale startup script ---

cat > /usr/local/bin/start-tailscale.sh << 'TSEOF'
#!/bin/bash
set -e

source /root/.zo_secrets

TAILSCALE_STATE_DIR="/var/lib/tailscale"
mkdir -p "$TAILSCALE_STATE_DIR"
mkdir -p /var/run/tailscale

tailscaled \
  --tun=userspace-networking \
  --state="$TAILSCALE_STATE_DIR/tailscaled.state" \
  --socket=/var/run/tailscale/tailscaled.sock &
DAEMON_PID=$!

for i in $(seq 1 30); do
  [ -S /var/run/tailscale/tailscaled.sock ] && break
  sleep 1
done

tailscale up \
  --authkey="$TAILSCALE_AUTHKEY" \
  --hostname="zo-workspace" \
  --accept-routes

wait $DAEMON_PID
TSEOF

chmod 755 /usr/local/bin/start-tailscale.sh
echo "[OK] Tailscale startup script written to /usr/local/bin/start-tailscale.sh"

# --- Save auth key to .zo_secrets ---

SECRETS_FILE="/root/.zo_secrets"
touch "$SECRETS_FILE" && chmod 600 "$SECRETS_FILE"

if ! grep -q 'TAILSCALE_AUTHKEY' "$SECRETS_FILE" 2>/dev/null; then
  echo "export TAILSCALE_AUTHKEY=\"$TAILSCALE_AUTHKEY\"" >> "$SECRETS_FILE"
  echo "[OK] Auth key saved to ~/.zo_secrets"
else
  echo "[OK] Auth key already in ~/.zo_secrets"
fi

if ! grep -q 'source /root/.zo_secrets' /root/.bashrc 2>/dev/null; then
  echo 'source /root/.zo_secrets' >> /root/.bashrc
fi

# --- Install OpenClaw ---

if command -v openclaw &>/dev/null; then
  echo "[OK] OpenClaw already installed: $(openclaw --version)"
else
  echo "     Installing OpenClaw..."
  npm install -g openclaw@latest
  echo "[OK] OpenClaw installed: $(openclaw --version)"
fi

# --- Install mcporter ---

if command -v mcporter &>/dev/null; then
  echo "[OK] mcporter already installed: $(mcporter --version 2>/dev/null || echo 'unknown version')"
else
  echo "     Installing mcporter (MCP bridge for Zo tools)..."
  npm install -g mcporter@latest
  echo "[OK] mcporter installed"
fi

echo ""
echo "=== Install complete ==="
echo ""
echo "NEXT STEPS:"
echo "  1. Zo registers Tailscale as a Zo User Service (automatic)"
echo "  2. Open Zo's terminal and run: openclaw onboard"
echo "  3. Follow the prompts to pick your LLM provider and messaging channel"
echo "  4. When done, tell Zo to run the bootstrap"
