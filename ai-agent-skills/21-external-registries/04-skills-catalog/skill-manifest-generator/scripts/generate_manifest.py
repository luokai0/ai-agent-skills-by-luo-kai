#!/usr/bin/env python3
"""
Skill Manifest Generator

Generates MANIFEST.json files for Agent Skills according to Spec 20.
Provides content integrity verification, file inventory, and external reference tracking.

Usage:
    python generate_manifest.py /path/to/skill
    python generate_manifest.py /path/to/skill --verify
    python generate_manifest.py /path/to/skill --output /path/to/output.json
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Try to import yaml, fall back to basic parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Version of this generator
GENERATOR_VERSION = "1.0.0"
MANIFEST_VERSION = "1.0"
SCHEMA_URL = "https://agentskills.io/schemas/manifest.v1.json"

# Default exclusions (always ignored)
DEFAULT_EXCLUSIONS = {
    ".git",
    ".gitignore",
    ".DS_Store",
    "Thumbs.db",
    "__pycache__",
    "node_modules",
    ".env",
    "MANIFEST.json",
    ".skillignore",
}

# File extensions to scan for URLs
URL_SCAN_EXTENSIONS = {
    ".py", ".js", ".ts", ".mjs", ".jsx", ".tsx",
    ".sh", ".bash", ".zsh",
    ".md", ".txt",
    ".json", ".yaml", ".yml",
    ".html", ".htm",
}

# URL pattern for detection
URL_PATTERN = re.compile(r'https?://[^\s"\'`<>)\]]+')

# URLs to exclude from detection
EXCLUDED_URL_PATTERNS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "example.com",
    "example.org",
    "placeholder.com",
    "schema.org",
    "json-schema.org",
    "agentskills.io/schemas",  # Our own schema URLs
]

# File type classification by extension
FILE_TYPE_MAP = {
    # Manifest
    "SKILL.md": "manifest",
    # Scripts
    ".py": "script",
    ".js": "script",
    ".ts": "script",
    ".mjs": "script",
    ".jsx": "script",
    ".tsx": "script",
    ".sh": "script",
    ".bash": "script",
    # Config
    ".json": "config",
    ".yaml": "config",
    ".yml": "config",
    ".toml": "config",
    ".ini": "config",
    # Reference/docs
    ".md": "reference",
    ".txt": "reference",
    ".rst": "reference",
    # Assets
    ".png": "asset",
    ".jpg": "asset",
    ".jpeg": "asset",
    ".gif": "asset",
    ".svg": "asset",
    ".pdf": "asset",
    ".docx": "asset",
    ".xlsx": "asset",
    ".csv": "asset",
}

# Size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_TOTAL_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_FILE_COUNT = 1000
MAX_DEPTH = 6
WARN_DEPTH = 4


def sha256_file(filepath: Path) -> str:
    """Compute SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def sha256_string(content: str) -> str:
    """Compute SHA256 hash of a string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def get_file_type(filepath: Path) -> str:
    """Determine the type of a file based on name/extension."""
    name = filepath.name
    if name in FILE_TYPE_MAP:
        return FILE_TYPE_MAP[name]

    ext = filepath.suffix.lower()
    return FILE_TYPE_MAP.get(ext, "other")


def is_binary_file(filepath: Path) -> bool:
    """Check if a file is binary (non-text)."""
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(8192)
            # Check for null bytes (common in binary files)
            if b"\x00" in chunk:
                return True
            # Try to decode as UTF-8
            try:
                chunk.decode("utf-8")
                return False
            except UnicodeDecodeError:
                return True
    except Exception:
        return True


def load_skillignore(skill_path: Path) -> set:
    """Load custom exclusions from .skillignore file."""
    ignore_file = skill_path / ".skillignore"
    patterns = set()

    if ignore_file.exists():
        with open(ignore_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.add(line)

    return patterns


def should_exclude(filepath: Path, skill_path: Path, custom_ignores: set) -> bool:
    """Check if a file should be excluded from the manifest."""
    name = filepath.name
    rel_path = filepath.relative_to(skill_path)
    rel_str = str(rel_path)

    # Check default exclusions
    for part in rel_path.parts:
        if part in DEFAULT_EXCLUSIONS:
            return True
        if part.endswith(".pyc"):
            return True
        if part.startswith(".env"):
            return True
        if part.endswith(".log"):
            return True

    # Check custom ignores (simple pattern matching)
    for pattern in custom_ignores:
        # Handle directory patterns (ending with /)
        if pattern.endswith("/"):
            dir_pattern = pattern[:-1]
            if any(part == dir_pattern for part in rel_path.parts):
                return True
        # Handle glob patterns (*)
        elif "*" in pattern:
            import fnmatch
            if fnmatch.fnmatch(rel_str, pattern) or fnmatch.fnmatch(name, pattern):
                return True
        # Handle exact matches
        elif rel_str == pattern or name == pattern:
            return True

    return False


def get_folder_depth(filepath: Path, skill_path: Path) -> int:
    """Get the depth of a file relative to skill root."""
    rel_path = filepath.relative_to(skill_path)
    return len(rel_path.parts) - 1  # -1 because file itself doesn't count


def detect_urls_in_file(filepath: Path) -> list:
    """Detect external URLs in a file."""
    urls = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                matches = URL_PATTERN.findall(line)
                for url in matches:
                    # Clean up trailing punctuation
                    url = url.rstrip(".,;:!?)")

                    # Check if URL should be excluded
                    should_exclude = False
                    for pattern in EXCLUDED_URL_PATTERNS:
                        if pattern in url.lower():
                            should_exclude = True
                            break

                    if not should_exclude:
                        urls.append({
                            "url": url,
                            "line": line_num,
                        })
    except Exception:
        pass  # Skip files that can't be read as text

    return urls


def classify_url_type(url: str, context: str = "") -> str:
    """Classify the type of external URL."""
    url_lower = url.lower()

    if any(api in url_lower for api in ["/api/", "/v1/", "/v2/", "/graphql"]):
        return "api"
    if any(ext in url_lower for ext in [".bin", ".model", ".weights", ".zip", ".tar"]):
        return "download"
    if any(pkg in url_lower for pkg in ["npm", "pypi", "github.com", "unpkg", "jsdelivr"]):
        return "import"
    if any(doc in url_lower for doc in ["docs.", "documentation", "readme", ".md"]):
        return "link"

    return "unknown"


def parse_skill_frontmatter(skill_path: Path) -> dict:
    """Parse the SKILL.md frontmatter to extract metadata."""
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return {}

    try:
        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for frontmatter
        if not content.startswith("---"):
            return {}

        # Find the closing ---
        end_index = content.find("---", 3)
        if end_index == -1:
            return {}

        frontmatter_str = content[3:end_index].strip()

        if HAS_YAML:
            return yaml.safe_load(frontmatter_str) or {}
        else:
            # Basic parsing without yaml library
            result = {}
            for line in frontmatter_str.split("\n"):
                if ":" in line and not line.startswith(" ") and not line.startswith("-"):
                    key, value = line.split(":", 1)
                    result[key.strip()] = value.strip().strip('"').strip("'")
            return result
    except Exception as e:
        print(f"Warning: Could not parse SKILL.md frontmatter: {e}", file=sys.stderr)
        return {}


def generate_manifest(skill_path: Path, output_path: Optional[Path] = None) -> dict:
    """Generate a manifest for a skill directory."""
    skill_path = skill_path.resolve()

    if not skill_path.is_dir():
        raise ValueError(f"Not a directory: {skill_path}")

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"Missing SKILL.md in {skill_path}")

    # Load custom ignores
    custom_ignores = load_skillignore(skill_path)

    # Parse skill metadata
    metadata = parse_skill_frontmatter(skill_path)

    # Collect all files
    files = []
    external_refs = []
    total_bytes = 0
    max_depth = 0
    folders = set()
    warnings = []
    errors = []

    for filepath in skill_path.rglob("*"):
        if not filepath.is_file():
            continue

        if should_exclude(filepath, skill_path, custom_ignores):
            continue

        rel_path = filepath.relative_to(skill_path)
        rel_str = str(rel_path).replace("\\", "/")  # Normalize path separators

        # Track folders
        if len(rel_path.parts) > 1:
            folders.add(rel_path.parts[0])

        # Check depth
        depth = get_folder_depth(filepath, skill_path)
        max_depth = max(max_depth, depth)

        if depth >= MAX_DEPTH:
            errors.append(f"File too deep ({depth} levels): {rel_str}")
        elif depth >= WARN_DEPTH:
            warnings.append(f"Deep nesting ({depth} levels): {rel_str}")

        # Check file size
        file_size = filepath.stat().st_size
        if file_size > MAX_FILE_SIZE:
            errors.append(f"File too large ({file_size / 1024 / 1024:.1f}MB): {rel_str}")

        total_bytes += file_size

        # Compute hash
        file_hash = sha256_file(filepath)
        file_type = get_file_type(filepath)

        files.append({
            "path": rel_str,
            "size": file_size,
            "sha256": file_hash,
            "type": file_type,
        })

        # Detect URLs (only in text files)
        if filepath.suffix.lower() in URL_SCAN_EXTENSIONS and not is_binary_file(filepath):
            urls = detect_urls_in_file(filepath)
            for url_info in urls:
                external_refs.append({
                    "url": url_info["url"],
                    "file": rel_str,
                    "line": url_info["line"],
                    "type": classify_url_type(url_info["url"]),
                })

    # Check total size
    if total_bytes > MAX_TOTAL_SIZE:
        errors.append(f"Total size too large ({total_bytes / 1024 / 1024:.1f}MB)")

    # Check file count
    if len(files) > MAX_FILE_COUNT:
        errors.append(f"Too many files ({len(files)})")

    # Sort files by path for deterministic output
    files.sort(key=lambda f: f["path"])

    # Compute integrity hash
    hash_lines = [f"{f['path']}:{f['sha256']}" for f in files]
    hash_content = "\n".join(hash_lines)
    integrity_hash = sha256_string(hash_content)

    # Build manifest
    manifest = {
        "$schema": SCHEMA_URL,
        "manifestVersion": MANIFEST_VERSION,
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "generator": f"skill-manifest-generator/{GENERATOR_VERSION}",
        "skill": {
            "name": metadata.get("name", skill_path.name),
        },
        "integrity": {
            "algorithm": "sha256",
            "hash": integrity_hash,
        },
        "files": files,
        "externalReferences": external_refs,
        "structure": {
            "maxDepth": max_depth,
            "totalFiles": len(files),
            "totalBytes": total_bytes,
            "folders": sorted(folders),
        },
    }

    # Add optional skill metadata
    if metadata.get("version"):
        manifest["skill"]["version"] = metadata["version"]
    if metadata.get("license"):
        manifest["license"] = {
            "spdxId": metadata["license"],
        }
        license_file = skill_path / "LICENSE"
        if license_file.exists():
            manifest["license"]["file"] = "LICENSE"

    # Print warnings and errors
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"Error: {error}", file=sys.stderr)

    if errors:
        manifest["_errors"] = errors
    if warnings:
        manifest["_warnings"] = warnings

    # Write manifest
    output_file = output_path or (skill_path / "MANIFEST.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return manifest


def verify_manifest(skill_path: Path) -> dict:
    """Verify that a manifest matches the current skill contents."""
    skill_path = skill_path.resolve()
    manifest_file = skill_path / "MANIFEST.json"

    if not manifest_file.exists():
        raise ValueError(f"No MANIFEST.json found in {skill_path}")

    with open(manifest_file) as f:
        manifest = json.load(f)

    results = {
        "valid": True,
        "files_checked": 0,
        "files_matched": 0,
        "files_mismatched": [],
        "files_missing": [],
        "files_new": [],
        "integrity_match": False,
    }

    # Load custom ignores for finding new files
    custom_ignores = load_skillignore(skill_path)

    # Check each file in manifest
    manifest_files = {f["path"]: f for f in manifest.get("files", [])}

    for rel_path, file_info in manifest_files.items():
        filepath = skill_path / rel_path
        results["files_checked"] += 1

        if not filepath.exists():
            results["files_missing"].append(rel_path)
            results["valid"] = False
        else:
            current_hash = sha256_file(filepath)
            if current_hash == file_info["sha256"]:
                results["files_matched"] += 1
            else:
                results["files_mismatched"].append({
                    "path": rel_path,
                    "expected": file_info["sha256"][:16] + "...",
                    "actual": current_hash[:16] + "...",
                })
                results["valid"] = False

    # Check for new files not in manifest
    for filepath in skill_path.rglob("*"):
        if not filepath.is_file():
            continue
        if should_exclude(filepath, skill_path, custom_ignores):
            continue

        rel_path = str(filepath.relative_to(skill_path)).replace("\\", "/")
        if rel_path not in manifest_files:
            results["files_new"].append(rel_path)
            results["valid"] = False

    # Verify integrity hash
    hash_lines = [f"{f['path']}:{f['sha256']}" for f in manifest.get("files", [])]
    hash_content = "\n".join(hash_lines)
    computed_hash = sha256_string(hash_content)

    manifest_hash = manifest.get("integrity", {}).get("hash", "")
    results["integrity_match"] = (computed_hash == manifest_hash)

    if not results["integrity_match"]:
        results["valid"] = False

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate or verify MANIFEST.json for Agent Skills"
    )
    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to the skill directory"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify existing manifest instead of generating"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output path for manifest (default: skill_path/MANIFEST.json)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    try:
        if args.verify:
            results = verify_manifest(args.skill_path)

            if args.json:
                print(json.dumps(results, indent=2))
            else:
                if results["valid"]:
                    print(f"✓ Manifest verified successfully")
                    print(f"  {results['files_matched']}/{results['files_checked']} files match")
                else:
                    print(f"✗ Manifest verification failed")

                    if results["files_missing"]:
                        print(f"\nMissing files ({len(results['files_missing'])}):")
                        for path in results["files_missing"]:
                            print(f"  - {path}")

                    if results["files_mismatched"]:
                        print(f"\nModified files ({len(results['files_mismatched'])}):")
                        for info in results["files_mismatched"]:
                            print(f"  - {info['path']}")

                    if results["files_new"]:
                        print(f"\nNew files ({len(results['files_new'])}):")
                        for path in results["files_new"]:
                            print(f"  + {path}")

                    if not results["integrity_match"]:
                        print(f"\n✗ Integrity hash mismatch")

            sys.exit(0 if results["valid"] else 1)

        else:
            manifest = generate_manifest(args.skill_path, args.output)

            if args.json:
                print(json.dumps(manifest, indent=2))
            else:
                output_file = args.output or (args.skill_path / "MANIFEST.json")
                print(f"✓ Generated {output_file}")
                print(f"  Files: {manifest['structure']['totalFiles']}")
                print(f"  Size: {manifest['structure']['totalBytes'] / 1024:.1f} KB")
                print(f"  Depth: {manifest['structure']['maxDepth']}")
                print(f"  External URLs: {len(manifest['externalReferences'])}")
                print(f"  Integrity: sha256:{manifest['integrity']['hash'][:16]}...")

                if manifest.get("_errors"):
                    print(f"\n✗ {len(manifest['_errors'])} error(s) found")
                    sys.exit(1)
                elif manifest.get("_warnings"):
                    print(f"\n⚠ {len(manifest['_warnings'])} warning(s)")

            sys.exit(0)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
