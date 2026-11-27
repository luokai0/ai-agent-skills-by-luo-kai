#!/usr/bin/env python3
"""
Agent Skills Installer

Install skills to AI coding agent harnesses.
Supports Claude Code, Goose, OpenCode, Cursor, and others.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for shared imports
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR.parent.parent
SHARED_DIR = SKILLS_DIR / "_shared"
sys.path.insert(0, str(SHARED_DIR))

# Optional imports
try:
    from agentskills_config import get_skill_key, get_api_url, get_auth_header
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ============================================================================
# Harness Definitions
# ============================================================================

HARNESSES = {
    "claude-code": {
        "name": "Claude Code",
        "path": Path.home() / ".claude" / "skills",
        "type": "global",
        "detect": lambda: (Path.home() / ".claude").exists(),
    },
    "goose": {
        "name": "Goose",
        "path": Path.home() / ".config" / "goose" / "skills",
        "type": "global",
        "detect": lambda: shutil.which("goose") is not None or (Path.home() / ".config" / "goose").exists(),
    },
    "opencode": {
        "name": "OpenCode",
        "path": Path.cwd() / ".opencode" / "skill",
        "type": "project",
        "detect": lambda: (Path.cwd() / ".opencode").exists() or shutil.which("opencode") is not None,
    },
    "cursor": {
        "name": "Cursor",
        "path": Path.cwd() / ".cursor" / "skills",
        "type": "project",
        "detect": lambda: (Path.cwd() / ".cursor").exists(),
    },
}


# ============================================================================
# Skill Parsing
# ============================================================================

def get_skill_name(skill_path: Path) -> str:
    """Extract skill name from SKILL.md or directory name."""
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        try:
            content = skill_md.read_text()
            if content.startswith("---"):
                end = content.find("---", 3)
                if end > 0:
                    frontmatter = content[3:end]
                    for line in frontmatter.split("\n"):
                        if line.startswith("name:"):
                            return line.split(":", 1)[1].strip().strip("\"'")
        except Exception:
            pass
    return skill_path.name


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Check if path contains a valid skill."""
    if not skill_path.exists():
        return False, f"Path does not exist: {skill_path}"

    if not skill_path.is_dir():
        return False, f"Path is not a directory: {skill_path}"

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, f"Missing SKILL.md in {skill_path}"

    return True, ""


# ============================================================================
# Installation Functions
# ============================================================================

def install_skill(
    source_path: Path,
    harness_id: str,
    force: bool = False,
) -> tuple[bool, str]:
    """Install a skill to a harness."""

    if harness_id not in HARNESSES:
        return False, f"Unknown harness: {harness_id}"

    harness = HARNESSES[harness_id]
    skill_name = get_skill_name(source_path)

    # Determine target path
    target_base = harness["path"]
    target_path = target_base / skill_name

    # Check if already installed
    if target_path.exists() and not force:
        return False, f"Skill already installed at {target_path}. Use --force to overwrite."

    # Create parent directories
    try:
        target_base.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        return False, f"Permission denied creating {target_base}"

    # Remove existing if force
    if target_path.exists() and force:
        try:
            shutil.rmtree(target_path)
        except Exception as e:
            return False, f"Failed to remove existing installation: {e}"

    # Copy skill files
    try:
        shutil.copytree(source_path, target_path)
    except Exception as e:
        return False, f"Failed to copy files: {e}"

    return True, str(target_path)


def uninstall_skill(skill_name: str, harness_id: str) -> tuple[bool, str]:
    """Uninstall a skill from a harness."""

    if harness_id not in HARNESSES:
        return False, f"Unknown harness: {harness_id}"

    harness = HARNESSES[harness_id]
    target_path = harness["path"] / skill_name

    if not target_path.exists():
        return False, f"Skill not found: {target_path}"

    try:
        shutil.rmtree(target_path)
        return True, f"Removed {target_path}"
    except Exception as e:
        return False, f"Failed to remove: {e}"


def list_installed_skills(harness_id: Optional[str] = None) -> dict:
    """List installed skills for one or all harnesses."""

    result = {}
    harnesses_to_check = [harness_id] if harness_id else HARNESSES.keys()

    for hid in harnesses_to_check:
        if hid not in HARNESSES:
            continue

        harness = HARNESSES[hid]
        skills_path = harness["path"]

        if not skills_path.exists():
            result[hid] = []
            continue

        skills = []
        for item in skills_path.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                skills.append({
                    "name": item.name,
                    "path": str(item),
                })

        result[hid] = skills

    return result


def detect_harnesses() -> list[str]:
    """Detect which harnesses are installed."""
    detected = []
    for hid, harness in HARNESSES.items():
        try:
            if harness["detect"]():
                detected.append(hid)
        except Exception:
            pass
    return detected


# ============================================================================
# Catalog Integration
# ============================================================================

def download_from_catalog(
    vendor_key: str,
    skill_key: str,
    dest_path: Path,
) -> tuple[bool, str]:
    """Download a skill from the catalog."""

    if not HAS_REQUESTS:
        return False, "requests library not installed. Run: pip install requests"

    if not HAS_CONFIG:
        return False, "agentskills_config not available"

    api_url = get_api_url()
    headers = get_auth_header()

    try:
        # Get skill details
        response = requests.get(
            f"{api_url}/api/catalog/{vendor_key}/{skill_key}",
            headers=headers,
            timeout=30,
        )

        if response.status_code == 404:
            return False, f"Skill not found: {vendor_key}/{skill_key}"

        if response.status_code != 200:
            return False, f"API error: {response.status_code}"

        data = response.json()

        # Check if we have content
        content = data.get("content")
        if not content:
            # Skill exists but no downloadable content
            # Try to get from GitHub if repo URL is available
            skill_data = data.get("skill", {})
            repo_url = skill_data.get("repo")
            if repo_url:
                return False, f"Skill found but content not available. Source: {repo_url}"
            return False, "Skill found but no downloadable content"

        # Create destination directory
        dest_path.mkdir(parents=True, exist_ok=True)

        # Write files
        files_written = 0
        for file_path, file_content in content.items():
            full_path = dest_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(file_content)
            files_written += 1

        return True, f"Downloaded {files_written} files to {dest_path}"

    except requests.exceptions.Timeout:
        return False, "Request timed out"
    except requests.exceptions.ConnectionError:
        return False, f"Could not connect to {api_url}"
    except Exception as e:
        return False, str(e)


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Install Agent Skills to harnesses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install from local directory
  python install_skill.py ./my-skill --harness claude-code
  python install_skill.py /path/to/skill --harness goose

  # Install from catalog
  python install_skill.py anthropic/document-skills --harness claude-code

  # List installed skills
  python install_skill.py --list
  python install_skill.py --list --harness claude-code

  # Uninstall a skill
  python install_skill.py --uninstall my-skill --harness claude-code

Supported harnesses:
  claude-code   ~/.claude/skills/
  goose         ~/.config/goose/skills/
  opencode      .opencode/skill/ (project-local)
  cursor        .cursor/skills/ (project-local)
        """,
    )

    parser.add_argument(
        "source",
        nargs="?",
        help="Skill path (local) or vendor/skill (catalog)",
    )
    parser.add_argument(
        "--harness", "-H",
        choices=list(HARNESSES.keys()),
        help="Target harness",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List installed skills",
    )
    parser.add_argument(
        "--uninstall", "-u",
        metavar="SKILL",
        help="Uninstall a skill by name",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing installation",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    # List mode
    if args.list:
        installed = list_installed_skills(args.harness)

        if args.json:
            print(json.dumps(installed, indent=2))
        else:
            for hid, skills in installed.items():
                harness = HARNESSES[hid]
                print(f"\n{harness['name']} ({harness['path']}):")
                if skills:
                    for skill in skills:
                        print(f"  - {skill['name']}")
                else:
                    print("  (no skills installed)")

        sys.exit(0)

    # Uninstall mode
    if args.uninstall:
        if not args.harness:
            print("Error: --harness required for uninstall", file=sys.stderr)
            sys.exit(1)

        success, message = uninstall_skill(args.uninstall, args.harness)

        if args.json:
            print(json.dumps({"success": success, "message": message}))
        else:
            if success:
                print(f"Uninstalled: {args.uninstall}")
                print(f"  {message}")
            else:
                print(f"Error: {message}", file=sys.stderr)

        sys.exit(0 if success else 1)

    # Install mode
    if not args.source:
        parser.print_help()
        sys.exit(1)

    # Determine if source is local or catalog
    source = args.source
    is_catalog = "/" in source and not Path(source).exists()

    if is_catalog:
        # Catalog source: vendor/skill
        parts = source.split("/", 1)
        if len(parts) != 2:
            print(f"Error: Invalid catalog reference: {source}", file=sys.stderr)
            print("Use format: vendor/skill (e.g., anthropic/document-skills)")
            sys.exit(1)

        vendor_key, skill_key = parts

        # Download to temp location
        import tempfile
        temp_dir = Path(tempfile.mkdtemp()) / skill_key

        print(f"Downloading {vendor_key}/{skill_key} from catalog...")
        success, message = download_from_catalog(vendor_key, skill_key, temp_dir)

        if not success:
            print(f"Error: {message}", file=sys.stderr)
            sys.exit(1)

        source_path = temp_dir
    else:
        # Local source
        source_path = Path(source).resolve()

        # Validate
        valid, error = validate_skill(source_path)
        if not valid:
            print(f"Error: {error}", file=sys.stderr)
            sys.exit(1)

    # Determine harness
    harness_id = args.harness
    if not harness_id:
        detected = detect_harnesses()
        if not detected:
            print("Error: No harnesses detected. Use --harness to specify.", file=sys.stderr)
            print("Supported: " + ", ".join(HARNESSES.keys()))
            sys.exit(1)
        elif len(detected) == 1:
            harness_id = detected[0]
            print(f"Auto-detected harness: {HARNESSES[harness_id]['name']}")
        else:
            print("Multiple harnesses detected. Please specify with --harness:")
            for hid in detected:
                print(f"  {hid} - {HARNESSES[hid]['name']}")
            sys.exit(1)

    # Install
    skill_name = get_skill_name(source_path)
    print(f"\nInstalling skill: {skill_name}")
    print(f"  Source: {source_path}")
    print(f"  Target: {HARNESSES[harness_id]['path'] / skill_name}")
    print()

    success, result = install_skill(source_path, harness_id, force=args.force)

    if args.json:
        print(json.dumps({
            "success": success,
            "skill": skill_name,
            "harness": harness_id,
            "path": result if success else None,
            "error": result if not success else None,
        }))
    else:
        if success:
            print(f"  Success! Skill installed to {HARNESSES[harness_id]['name']}.")
            print(f"  Location: {result}")
            print()
            if harness_id == "claude-code":
                print("  The skill will be available in your next Claude Code session.")
            elif harness_id == "goose":
                print("  The skill will be available in your next Goose session.")
            else:
                print("  Restart your agent to use the new skill.")
        else:
            print(f"  Error: {result}", file=sys.stderr)

    # Cleanup temp dir if catalog download
    if is_catalog and 'temp_dir' in dir():
        try:
            shutil.rmtree(temp_dir.parent)
        except Exception:
            pass

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
