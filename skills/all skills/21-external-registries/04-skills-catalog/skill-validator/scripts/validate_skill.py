#!/usr/bin/env python3
"""
Skill Validator

Validates Agent Skills against the specification.
This script mirrors the validation logic from src/lib/spec-compliance/index.ts
to ensure consistent behavior between the skill and the catalog.

Usage:
    python validate_skill.py /path/to/skill
    python validate_skill.py /path/to/skill --json
    python validate_skill.py /path/to/skill --strict
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# Try to import yaml, fall back to basic parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class ValidationResult:
    """Result of skill validation - mirrors ComplianceResult from TypeScript"""
    is_compliant: bool
    score: int  # 0-100
    has_skill_md: bool
    has_valid_name: bool
    has_valid_description: bool
    name_matches_dir: bool
    has_valid_structure: bool
    skill_name: Optional[str]
    description: Optional[str]
    issues: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    # Additional fields for enhanced validation
    version: Optional[str] = None
    license: Optional[str] = None
    author: Optional[str] = None
    tags: list = field(default_factory=list)


def validate_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate a skill name according to spec.

    Rules (from src/lib/spec-compliance/index.ts):
    - 1-64 characters
    - lowercase alphanumeric and hyphens only
    - cannot start with hyphen
    - cannot end with hyphen
    - no consecutive hyphens

    Extended rules (from specs/20-skill-manifest-system.md):
    - must start with a letter
    """
    if not name or len(name) == 0:
        return False, "Name is required"

    if len(name) > 64:
        return False, "Name exceeds 64 characters"

    # Must be lowercase alphanumeric and hyphens only
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Name must be lowercase alphanumeric and hyphens only"

    # Must start with a letter (extended rule from Spec 20)
    if not re.match(r'^[a-z]', name):
        return False, "Name must start with a letter"

    if name.startswith("-"):
        return False, "Name cannot start with a hyphen"

    if name.endswith("-"):
        return False, "Name cannot end with a hyphen"

    if "--" in name:
        return False, "Name cannot contain consecutive hyphens"

    return True, None


def validate_description(desc: str) -> tuple[bool, Optional[str]]:
    """
    Validate description according to spec.

    Rules:
    - 1-1024 characters
    - non-empty
    """
    if not desc or len(desc.strip()) == 0:
        return False, "Description is required"

    if len(desc) > 1024:
        return False, "Description exceeds 1024 characters"

    return True, None


def validate_version(version: str) -> tuple[bool, Optional[str]]:
    """Validate version follows semver format (warning only)."""
    if not version:
        return True, None  # Version is optional

    # Basic semver pattern
    semver_pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'

    if not re.match(semver_pattern, version):
        return False, f"Version '{version}' should follow semver format (e.g., 1.0.0)"

    return True, None


def parse_frontmatter(content: str) -> Optional[dict]:
    """
    Parse YAML frontmatter from SKILL.md content.
    Mirrors parseFrontmatter from TypeScript.
    """
    # Check for frontmatter delimiters
    if not content.startswith("---"):
        return None

    # Find closing delimiter
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        # Try with just --- at end of line
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None

    frontmatter_str = content[3:3 + end_match.start()].strip()

    if HAS_YAML:
        try:
            return yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError:
            return None
    else:
        # Basic parsing without yaml library
        result = {}
        current_key = None

        for line in frontmatter_str.split("\n"):
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith("#"):
                continue

            # Handle array items
            if line.strip().startswith("- ") and current_key:
                if current_key not in result:
                    result[current_key] = []
                if isinstance(result[current_key], list):
                    result[current_key].append(line.strip()[2:].strip())
                continue

            # Handle key: value pairs
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                current_key = key
                if value:
                    result[key] = value
                else:
                    result[key] = []  # Prepare for array

        return result


def get_folder_depth(skill_path: Path) -> int:
    """Calculate the maximum folder depth in the skill."""
    max_depth = 0

    for root, dirs, files in os.walk(skill_path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        rel_path = Path(root).relative_to(skill_path)
        depth = len(rel_path.parts)
        max_depth = max(max_depth, depth)

    return max_depth


def check_structure(skill_path: Path) -> tuple[bool, list]:
    """
    Check if skill has valid structure.

    Valid structure:
    - SKILL.md at root
    - Optional: scripts/, references/, assets/ directories
    - Max depth of 6 levels (warning at 4+)
    """
    issues = []
    warnings = []

    # Check for non-standard top-level directories
    valid_dirs = {"scripts", "references", "assets", ".git", "__pycache__", "node_modules"}

    for item in skill_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            if item.name.lower() not in valid_dirs:
                warnings.append(f"Non-standard directory: {item.name}")

    # Check depth
    depth = get_folder_depth(skill_path)
    if depth > 6:
        issues.append(f"Folder depth ({depth}) exceeds maximum of 6")
    elif depth >= 4:
        warnings.append(f"Deep nesting ({depth} levels) may be hard to maintain")

    return len(issues) == 0, issues + warnings


def validate_skill(skill_path: Path, strict: bool = False) -> ValidationResult:
    """
    Run complete validation on a skill directory.
    Mirrors checkCompliance from TypeScript.
    """
    issues = []
    warnings = []

    # Get directory name
    dir_name = skill_path.name

    # Check 1: SKILL.md exists
    skill_md_path = skill_path / "SKILL.md"
    has_skill_md = skill_md_path.exists()

    if not has_skill_md:
        # Also check for case-insensitive match
        for item in skill_path.iterdir():
            if item.name.lower() == "skill.md":
                skill_md_path = item
                has_skill_md = True
                if item.name != "SKILL.md":
                    warnings.append(f"SKILL.md should be uppercase (found: {item.name})")
                break

    if not has_skill_md:
        issues.append("Missing required SKILL.md file")

    # Parse frontmatter if SKILL.md exists
    frontmatter = None
    if has_skill_md:
        try:
            content = skill_md_path.read_text(encoding="utf-8")
            frontmatter = parse_frontmatter(content)
            if frontmatter is None:
                issues.append("SKILL.md missing YAML frontmatter (must start with ---)")
        except Exception as e:
            issues.append(f"Could not read SKILL.md: {e}")

    # Check 2: Valid name
    has_valid_name = False
    skill_name = None
    if frontmatter:
        skill_name = frontmatter.get("name")
        if skill_name:
            valid, reason = validate_name(skill_name)
            has_valid_name = valid
            if not valid:
                issues.append(f"Invalid name: {reason}")
        else:
            issues.append("Missing 'name' field in frontmatter")

    # Check 3: Valid description
    has_valid_description = False
    description = None
    if frontmatter:
        description = frontmatter.get("description")
        if description:
            valid, reason = validate_description(description)
            has_valid_description = valid
            if not valid:
                issues.append(f"Invalid description: {reason}")
        else:
            issues.append("Missing 'description' field in frontmatter")

    # Check 4: Name matches directory
    name_matches_dir = skill_name == dir_name if skill_name else False
    if skill_name and not name_matches_dir:
        issues.append(f"Name '{skill_name}' does not match directory name '{dir_name}'")

    # Check 5: Valid structure
    has_valid_structure, structure_issues = check_structure(skill_path)
    for issue in structure_issues:
        if "exceeds" in issue.lower():
            issues.append(issue)
        else:
            warnings.append(issue)

    # Optional field validation (warnings only, unless strict mode)
    version = frontmatter.get("version") if frontmatter else None
    if version:
        valid, reason = validate_version(version)
        if not valid:
            if strict:
                issues.append(reason)
            else:
                warnings.append(reason)

    license_id = frontmatter.get("license") if frontmatter else None
    author = frontmatter.get("author") if frontmatter else None
    tags = frontmatter.get("tags", []) if frontmatter else []

    # Validate tags
    if tags:
        if len(tags) > 10:
            warnings.append(f"Too many tags ({len(tags)}), maximum is 10")
        for tag in tags:
            if not re.match(r'^[a-z0-9-]+$', str(tag)):
                warnings.append(f"Tag '{tag}' should be lowercase with hyphens only")

    # Calculate score (each check is worth 20 points)
    checks = [
        has_skill_md,
        has_valid_name,
        has_valid_description,
        name_matches_dir,
        has_valid_structure,
    ]
    passed_checks = sum(1 for c in checks if c)
    score = round((passed_checks / len(checks)) * 100)

    # Overall compliance requires all critical checks
    is_compliant = has_skill_md and has_valid_name and has_valid_description and name_matches_dir

    return ValidationResult(
        is_compliant=is_compliant,
        score=score,
        has_skill_md=has_skill_md,
        has_valid_name=has_valid_name,
        has_valid_description=has_valid_description,
        name_matches_dir=name_matches_dir,
        has_valid_structure=has_valid_structure,
        skill_name=skill_name,
        description=description,
        issues=issues,
        warnings=warnings,
        version=version,
        license=license_id,
        author=author,
        tags=tags if isinstance(tags, list) else [],
    )


def print_result(result: ValidationResult, skill_path: Path):
    """Print validation result in human-readable format."""
    status_icon = "✓" if result.is_compliant else "✗"
    status_text = "COMPLIANT" if result.is_compliant else "NON-COMPLIANT"

    print(f"\n{status_icon} Skill Validation Report")
    print(f"  Path: {skill_path}")
    print(f"  Skill: {result.skill_name or 'Unknown'}")
    print(f"  Status: {status_text} ({result.score}/100)")

    print(f"\n  Checks:")
    checks = [
        ("SKILL.md exists", result.has_skill_md),
        ("Valid frontmatter", result.has_skill_md and result.skill_name is not None),
        (f"Name format valid ({result.skill_name})" if result.skill_name else "Name format", result.has_valid_name),
        ("Name matches directory", result.name_matches_dir),
        (f"Description valid ({len(result.description or '')} chars)" if result.description else "Description valid", result.has_valid_description),
        ("Structure valid", result.has_valid_structure),
    ]

    for label, passed in checks:
        icon = "✓" if passed else "✗"
        print(f"    {icon} {label}")

    if result.issues:
        print(f"\n  Issues ({len(result.issues)}):")
        for issue in result.issues:
            print(f"    ✗ {issue}")

    if result.warnings:
        print(f"\n  Warnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"    ⚠ {warning}")

    if not result.issues and not result.warnings:
        print(f"\n  No issues found.")

    # Show optional metadata if present
    if result.version or result.license or result.author:
        print(f"\n  Metadata:")
        if result.version:
            print(f"    Version: {result.version}")
        if result.license:
            print(f"    License: {result.license}")
        if result.author:
            print(f"    Author: {result.author}")
        if result.tags:
            print(f"    Tags: {', '.join(result.tags)}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate Agent Skills against the specification"
    )
    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to the skill directory"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only output errors (exit code indicates pass/fail)"
    )

    args = parser.parse_args()
    skill_path = args.skill_path.resolve()

    if not skill_path.is_dir():
        print(f"Error: Not a directory: {skill_path}", file=sys.stderr)
        sys.exit(1)

    result = validate_skill(skill_path, strict=args.strict)

    if args.json:
        output = asdict(result)
        output["skill_path"] = str(skill_path)
        print(json.dumps(output, indent=2))
    elif not args.quiet:
        print_result(result, skill_path)

    # Exit code: 0 = compliant, 1 = non-compliant
    sys.exit(0 if result.is_compliant else 1)


if __name__ == "__main__":
    main()
