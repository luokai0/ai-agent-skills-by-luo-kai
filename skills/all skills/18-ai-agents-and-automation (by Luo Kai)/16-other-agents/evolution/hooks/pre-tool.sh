#!/bin/bash
# Pre-tool hook for makepad-skills
# Triggers: Version detection, dev branch validation

TOOL_NAME="$1"
TOOL_INPUT="$2"

# State file to track if version detection has been done this session
STATE_FILE="/tmp/makepad-skills-session-$$"

# Only run detection once per session
if [ -f "$STATE_FILE" ]; then
    exit 0
fi

# Mark session as initialized
touch "$STATE_FILE"

# Find Cargo.toml in current directory or parents
find_cargo_toml() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/Cargo.toml" ]; then
            echo "$dir/Cargo.toml"
            return 0
        fi
        dir=$(dirname "$dir")
    done
    return 1
}

CARGO_TOML=$(find_cargo_toml)

if [ -n "$CARGO_TOML" ]; then
    # Check if this is a Makepad project
    if ! grep -q 'makepad' "$CARGO_TOML"; then
        exit 0
    fi

    echo "[makepad-skills] This is a Makepad project." >&2

    # Detect Makepad branch
    MAKEPAD_BRANCH=$(grep -A5 'makepad-widgets' "$CARGO_TOML" | grep 'branch' | head -1 | sed 's/.*branch *= *"\([^"]*\)".*/\1/')

    if [ -n "$MAKEPAD_BRANCH" ]; then
        if [ "$MAKEPAD_BRANCH" = "dev" ]; then
            echo "[makepad-skills] Detected Makepad branch: dev ✓" >&2
        else
            echo "[makepad-skills] Detected Makepad branch: $MAKEPAD_BRANCH" >&2
            echo "[makepad-skills] ⚠️  WARNING: Not using 'dev' branch!" >&2
            echo "[makepad-skills] Recommended: branch = \"dev\" for latest stable API." >&2
            echo "[makepad-skills] Current skills are based on the dev branch." >&2
        fi
    else
        # No branch specified - might be using crates.io or default branch
        if grep -q 'makepad-widgets.*git' "$CARGO_TOML"; then
            echo "[makepad-skills] ⚠️  WARNING: No branch specified for git dependency!" >&2
            echo "[makepad-skills] Recommended: Add branch = \"dev\" to makepad-widgets dependency." >&2
        fi
    fi
fi
