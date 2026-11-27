#!/usr/bin/env bash
set -euo pipefail

input="${*:-}"
if [[ -z "$input" ]]; then
  echo "Usage: bash Skills/visual-explainer/scripts/slugify.sh \"My Explainer Title\"" >&2
  exit 1
fi

slug="$(printf '%s' "$input" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')"

if [[ -z "$slug" ]]; then
  echo "Unable to derive slug from input" >&2
  exit 1
fi

printf '%s\n' "$slug"
