#!/usr/bin/env python3
"""Remove license metadata only from independently authored Luo Kai skills."""
from __future__ import annotations
import argparse
import os
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "ai-agent-skills"

def parse_frontmatter(raw: str, path: Path) -> tuple[dict, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not match:
        raise SystemExit(f"Invalid frontmatter: {path}")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise SystemExit(f"Frontmatter must be a mapping: {path}")
    return metadata, match.group(1)

def is_original_luo_kai(metadata: dict) -> bool:
    details = metadata.get("metadata") or {}
    if not isinstance(details, dict):
        details = {}
    author = str(details.get("author") or metadata.get("author") or "").casefold().replace("-", " ").strip()
    source = metadata.get("source") or details.get("source")
    provenance = str(details.get("provenance") or metadata.get("provenance") or "").casefold().strip()
    return author == "luo kai" and not source and provenance in {"", "original"}

def remove_key_block(lines: list[str], key: str, indent: int) -> tuple[list[str], int]:
    output, removed, index = [], 0, 0
    while index < len(lines):
        line = lines[index]
        stripped = line.lstrip(" ")
        current_indent = len(line) - len(stripped)
        if current_indent == indent and stripped.startswith(key + ":"):
            removed += 1
            index += 1
            while index < len(lines):
                continuation = lines[index]
                if not continuation.strip():
                    index += 1
                    continue
                next_indent = len(continuation) - len(continuation.lstrip(" "))
                if next_indent > indent:
                    index += 1
                    continue
                break
            continue
        output.append(line)
        index += 1
    return output, removed

def strip_license_fields(frontmatter: str) -> tuple[str, int]:
    lines = frontmatter.splitlines()
    lines, top_removed = remove_key_block(lines, "license", 0)
    lines, nested_removed = remove_key_block(lines, "license", 2)
    cleaned = "\n".join(lines)
    yaml.safe_load(cleaned)
    return cleaned, top_removed + nested_removed

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    args = parser.parse_args()
    if not SKILLS_ROOT.is_dir():
        raise SystemExit(f"Missing skill root: {SKILLS_ROOT}")
    original_count, changed = 0, []
    for root, dirs, files in os.walk(SKILLS_ROOT):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__", "node_modules"})
        skill_name = next((name for name in files if name.casefold() == "skill.md"), None)
        if not skill_name:
            continue
        path = Path(root) / skill_name
        raw = path.read_text(encoding="utf-8-sig")
        metadata, frontmatter = parse_frontmatter(raw, path)
        if not is_original_luo_kai(metadata):
            continue
        original_count += 1
        cleaned, removed = strip_license_fields(frontmatter)
        if removed:
            match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
            body = raw[match.end():]
            changed.append((path, "---\n" + cleaned + "\n---\n" + body, removed))
    total_fields = sum(item[2] for item in changed)
    print(f"Original Luo Kai skills inspected: {original_count}")
    print(f"Files with license metadata to remove: {len(changed)}")
    print(f"License metadata fields to remove: {total_fields}")
    if not args.apply:
        print("DRY RUN ONLY. Third-party, adapted, and source-linked skills were left untouched.")
        return
    for path, content, _ in changed:
        path.write_text(content, encoding="utf-8")
    print(f"APPLIED: removed {total_fields} license metadata fields from {len(changed)} original skills.")

if __name__ == "__main__":
    main()
