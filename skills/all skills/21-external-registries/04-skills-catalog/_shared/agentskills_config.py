#!/usr/bin/env python3
"""
Agent Skills Configuration Module

Shared configuration for skills that connect to the Agent Skills Catalog API.
Handles Skill Key storage, retrieval, and API URL configuration.

Usage:
    from agentskills_config import get_skill_key, get_api_url

    key = get_skill_key()  # Prompts if missing
    url = get_api_url()
"""

import os
import sys
from pathlib import Path
from typing import Optional

# Default API URL
CATALOG_URL = "https://skillscatalog.ai"

# Local key storage
KEY_DIR = Path.home() / ".agentskills"
KEY_FILE = KEY_DIR / "key"


def get_skill_key(prompt_if_missing: bool = True) -> Optional[str]:
    """
    Get the user's Skill Key.

    Priority:
    1. AGENTSKILLS_KEY environment variable
    2. ~/.agentskills/key file
    3. Prompt user (if prompt_if_missing=True)

    Args:
        prompt_if_missing: If True, prompt user to enter key if not found

    Returns:
        The Skill Key string, or None if not available
    """
    # Check environment variable first
    env_key = os.environ.get("AGENTSKILLS_KEY")
    if env_key:
        key = env_key.strip()
        if _validate_key_format(key):
            return key
        print("Warning: AGENTSKILLS_KEY has invalid format", file=sys.stderr)

    # Check key file
    if KEY_FILE.exists():
        try:
            key = KEY_FILE.read_text().strip()
            if _validate_key_format(key):
                return key
            print(f"Warning: Key in {KEY_FILE} has invalid format", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Could not read {KEY_FILE}: {e}", file=sys.stderr)

    # Prompt user
    if prompt_if_missing:
        return _prompt_for_key()

    return None


def _validate_key_format(key: str) -> bool:
    """
    Validate a Skill Key format.

    Format: sk-{3 char hint}_{random chars}
    Example: sk-usr_7Kx9mP2nQ4vR8tYw3zA5bC
    """
    if not key:
        return False
    if not key.startswith("sk-"):
        return False
    if len(key) < 20:  # Minimum reasonable length
        return False
    if "_" not in key[3:]:  # Must have underscore after prefix
        return False
    return True


def _prompt_for_key() -> Optional[str]:
    """Prompt user to enter their Skill Key."""
    print()
    print("To use this skill, I need your Skill Key.")
    print()
    print("  1. Go to https://skillscatalog.ai/settings/skill-keys")
    print("  2. Click 'Create Skill Key'")
    print("  3. Paste it below")
    print()

    try:
        key = input("Your Skill Key: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        return None

    if not key:
        print("No key provided.")
        return None

    if not _validate_key_format(key):
        print("Invalid key format. Skill Keys start with 'sk-'")
        return None

    # Save for future use
    save_key(key)
    print("Skill Key saved.")
    print()

    return key


def save_key(key: str) -> None:
    """
    Save Skill Key to file with secure permissions.

    Args:
        key: The Skill Key to save
    """
    try:
        # Create directory with restricted permissions
        KEY_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)

        # Write key file
        KEY_FILE.write_text(key)

        # Set restrictive permissions (owner read/write only)
        KEY_FILE.chmod(0o600)
    except Exception as e:
        print(f"Warning: Could not save key to {KEY_FILE}: {e}", file=sys.stderr)


def clear_key() -> None:
    """Remove saved Skill Key."""
    if KEY_FILE.exists():
        try:
            KEY_FILE.unlink()
            print(f"Removed {KEY_FILE}")
        except Exception as e:
            print(f"Could not remove {KEY_FILE}: {e}", file=sys.stderr)


def get_api_url() -> str:
    """
    Get the API URL.

    Can be overridden with AGENTSKILLS_API_URL environment variable.

    Returns:
        The API base URL (no trailing slash)
    """
    url = os.environ.get("AGENTSKILLS_API_URL", CATALOG_URL)
    return url.rstrip("/")


def get_auth_header() -> dict:
    """
    Get the Authorization header for API requests.

    Returns:
        Dict with Authorization header, or empty dict if no key

    Raises:
        SystemExit: If no key available and running interactively
    """
    key = get_skill_key(prompt_if_missing=True)
    if not key:
        print("Error: No Skill Key available. Cannot authenticate.")
        print("Get your key at: https://skillscatalog.ai/settings/skill-keys")
        sys.exit(1)

    return {"Authorization": f"Bearer {key}"}


# Convenience: show key location when run directly
if __name__ == "__main__":
    print(f"Key directory: {KEY_DIR}")
    print(f"Key file: {KEY_FILE}")
    print(f"Key file exists: {KEY_FILE.exists()}")
    print(f"API URL: {get_api_url()}")

    if KEY_FILE.exists():
        key = get_skill_key(prompt_if_missing=False)
        if key:
            # Show only prefix for security
            print(f"Stored key: {key[:11]}...")
