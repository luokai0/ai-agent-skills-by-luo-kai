#!/bin/bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  pairing-helper.sh list
  pairing-helper.sh device <request-id>
  pairing-helper.sh telegram <pairing-code>

Commands:
  list                 Show pending and paired devices.
  device <request-id>  Approve a pending device pairing request.
  telegram <code>      Approve a Telegram pairing code.
EOF
}

if [ "${1:-}" = "" ]; then
  usage
  exit 1
fi

case "$1" in
  list)
    openclaw devices list
    ;;
  device)
    if [ "${2:-}" = "" ]; then
      echo "Missing request-id"
      usage
      exit 1
    fi
    openclaw devices approve "$2"
    ;;
  telegram)
    if [ "${2:-}" = "" ]; then
      echo "Missing pairing code"
      usage
      exit 1
    fi
    openclaw pairing approve telegram "$2"
    ;;
  *)
    usage
    exit 1
    ;;
esac
