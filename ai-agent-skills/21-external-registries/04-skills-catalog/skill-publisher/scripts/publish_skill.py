#!/usr/bin/env python3
"""
Agent Skills Publisher

Submit skills for publication to skillscatalog.ai.
Validates, scans, and submits skills via the API.
"""

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for shared imports
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR.parent.parent
SHARED_DIR = SKILLS_DIR / "_shared"
sys.path.insert(0, str(SHARED_DIR))

try:
    from agentskills_config import get_skill_key, get_api_url, get_auth_header
except ImportError:
    print("Error: Could not import agentskills_config.")
    print("Make sure the _shared/agentskills_config.py module exists.")
    sys.exit(1)

# Optional: import requests
try:
    import requests
except ImportError:
    requests = None  # type: ignore


# ============================================================================
# Skill Parsing
# ============================================================================

def parse_skill_md(skill_path: Path) -> Optional[dict]:
    """Parse SKILL.md frontmatter."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text()
    if not content.startswith("---"):
        return None

    end = content.find("---", 3)
    if end < 0:
        return None

    frontmatter = content[3:end]
    metadata = {}

    for line in frontmatter.strip().split("\n"):
        if ":" in line and not line.strip().startswith("-"):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            if key == "tags":
                # Handle tags array on following lines
                continue
            metadata[key] = value

    # Parse tags
    if "tags:" in frontmatter:
        tags = []
        in_tags = False
        for line in frontmatter.strip().split("\n"):
            if line.strip() == "tags:":
                in_tags = True
                continue
            if in_tags:
                if line.strip().startswith("-"):
                    tags.append(line.strip()[1:].strip())
                else:
                    break
        metadata["tags"] = tags

    return metadata


def collect_skill_files(skill_path: Path) -> dict:
    """Collect all skill files for upload."""
    files = {}

    # File extensions to include
    extensions = {
        ".md", ".py", ".js", ".ts", ".jsx", ".tsx",
        ".json", ".yaml", ".yml", ".sh", ".bash",
    }

    for root, dirs, filenames in os.walk(skill_path):
        # Skip hidden and common non-skill directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {
            "node_modules", "__pycache__", "venv", ".venv", "dist", "build"
        }]

        for filename in filenames:
            file_path = Path(root) / filename

            if any(filename.endswith(ext) for ext in extensions) or filename in {"MANIFEST.json", "Dockerfile"}:
                try:
                    relative_path = str(file_path.relative_to(skill_path))
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    files[relative_path] = content
                except Exception:
                    pass

    return files


# ============================================================================
# Validation
# ============================================================================

def validate_skill(skill_path: Path) -> tuple[bool, list]:
    """Run basic validation on the skill."""
    errors = []

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
        return False, errors

    # Parse metadata
    metadata = parse_skill_md(skill_path)
    if not metadata:
        errors.append("Could not parse SKILL.md frontmatter")
        return False, errors

    # Required fields
    required = ["name", "description", "version"]
    for field in required:
        if field not in metadata:
            errors.append(f"Missing required field: {field}")

    # Validate version format
    if "version" in metadata:
        if not re.match(r"^\d+\.\d+\.\d+$", metadata["version"]):
            errors.append(f"Invalid version format: {metadata['version']} (expected semver)")

    return len(errors) == 0, errors


# ============================================================================
# Safety Scanning
# ============================================================================

def run_safety_scan(skill_path: Path) -> tuple[str, int]:
    """Run safety scan using the safety scanner skill."""
    scanner_script = SKILLS_DIR / "skill-safety-scanner" / "scripts" / "safety_scan.py"

    if not scanner_script.exists():
        return "?", 0

    import subprocess
    result = subprocess.run(
        [sys.executable, str(scanner_script), str(skill_path), "--json"],
        capture_output=True,
        text=True,
    )

    try:
        data = json.loads(result.stdout)
        return data.get("grade", "?"), data.get("score", 0)
    except json.JSONDecodeError:
        return "?", 0


# ============================================================================
# API Submission
# ============================================================================

def submit_to_api(
    skill_path: Path,
    metadata: dict,
    files: dict,
    catalog_type: str,
    org_id: Optional[str] = None,
) -> dict:
    """Submit skill to the API for publication."""
    if requests is None:
        return {
            "success": False,
            "error": "requests library not installed. Run: pip install requests",
        }

    api_url = get_api_url()
    headers = get_auth_header()
    headers["Content-Type"] = "application/json"

    # Prepare payload
    payload = {
        "catalogType": catalog_type,
        "sourceType": "CLI_UPLOAD",
        "skillKey": metadata.get("name"),
        "version": metadata.get("version"),
        "files": files,
        "metadata": metadata,
    }

    if org_id:
        payload["orgId"] = org_id

    try:
        response = requests.post(
            f"{api_url}/api/publish/submit",
            headers=headers,
            json=payload,
            timeout=60,
        )

        if response.status_code == 200:
            return {"success": True, **response.json()}
        else:
            try:
                error_data = response.json()
                return {"success": False, "error": error_data.get("error", "Unknown error")}
            except json.JSONDecodeError:
                return {"success": False, "error": f"HTTP {response.status_code}"}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": f"Could not connect to {api_url}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# Main Flow
# ============================================================================

def publish_skill(
    skill_path: Path,
    catalog: str = "public",
    org_id: Optional[str] = None,
    dry_run: bool = False,
) -> bool:
    """Run the full publication workflow."""

    skill_name = skill_path.name
    metadata = parse_skill_md(skill_path)
    if metadata:
        skill_name = metadata.get("name", skill_name)

    print(f"\nPublishing skill: {skill_name}")

    # Step 1: Validate
    print("  Validating...", end=" ", flush=True)
    valid, errors = validate_skill(skill_path)
    if not valid:
        print("FAILED")
        for error in errors:
            print(f"    - {error}")
        return False
    print("OK")

    # Step 2: Safety scan
    print("  Scanning safety...", end=" ", flush=True)
    grade, score = run_safety_scan(skill_path)
    print(f"Grade {grade} ({score}/100)")

    if grade == "F":
        print("\n  Error: Skill has critical safety issues.")
        print("  Run skill-safety-scanner for details.")
        return False

    if grade in ("D", "?"):
        print("\n  Warning: Safety score is low. Review findings before publishing.")

    # Step 3: Collect files
    files = collect_skill_files(skill_path)
    print(f"  Files: {len(files)} files collected")

    # Determine catalog type
    if catalog == "public":
        catalog_type = "LEGENDARY_PUBLIC"
    elif catalog == "org":
        if not org_id:
            print("\n  Error: --org-id required for org catalog")
            return False
        catalog_type = "ORG_PUBLIC"
    elif catalog == "org-private":
        if not org_id:
            print("\n  Error: --org-id required for org-private catalog")
            return False
        catalog_type = "ORG_PRIVATE"
    else:
        print(f"\n  Error: Unknown catalog type: {catalog}")
        return False

    # Step 4: Dry run or submit
    if dry_run:
        print("\n  [Dry run] Would submit to:", catalog_type)
        print(f"  [Dry run] Skill: {metadata.get('name')}@{metadata.get('version')}")
        print(f"  [Dry run] Files: {len(files)}")
        return True

    print(f"  Submitting to {catalog} catalog...", end=" ", flush=True)

    # Check if we have the requests library
    if requests is None:
        print("\n")
        print("  Note: 'requests' library not installed.")
        print("  To submit via API, run: pip install requests")
        print()
        print("  Your skill is ready for publication!")
        print("  You can also submit via the web UI at:")
        print(f"    https://skillscatalog.ai/my-skills")
        print()
        return True

    result = submit_to_api(skill_path, metadata, files, catalog_type, org_id)

    if result.get("success"):
        print("OK")
        print()
        request_id = result.get("request", {}).get("id", "unknown")
        status = result.get("request", {}).get("status", "pending")
        print(f"  Success! Publication request submitted.")
        print(f"  Request ID: {request_id}")
        print(f"  Status: {status}")
        print()
        print("  Track your submission at:")
        print("    https://skillscatalog.ai/my-skills")
        return True
    else:
        print("FAILED")
        error = result.get("error", "Unknown error")
        print(f"\n  Error: {error}")

        if "connect" in error.lower() or "timeout" in error.lower():
            print("\n  Your skill is ready for publication!")
            print("  You can submit via the web UI at:")
            print(f"    https://skillscatalog.ai/my-skills")

        return False


def main():
    parser = argparse.ArgumentParser(
        description="Submit a skill for publication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python publish_skill.py /path/to/my-skill
  python publish_skill.py ./my-skill --catalog public
  python publish_skill.py ./my-skill --catalog org --org-id abc123
  python publish_skill.py ./my-skill --dry-run
        """,
    )
    parser.add_argument("path", help="Path to the skill directory")
    parser.add_argument(
        "--catalog",
        choices=["public", "org", "org-private"],
        default="public",
        help="Target catalog (default: public)",
    )
    parser.add_argument(
        "--org-id",
        help="Organization ID (required for org catalogs)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and scan without submitting",
    )
    args = parser.parse_args()

    skill_path = Path(args.path).resolve()

    if not skill_path.exists():
        print(f"Error: Path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"Error: Path is not a directory: {skill_path}", file=sys.stderr)
        sys.exit(1)

    success = publish_skill(
        skill_path,
        catalog=args.catalog,
        org_id=args.org_id,
        dry_run=args.dry_run,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
