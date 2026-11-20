#!/usr/bin/env python3
"""Remove retired profile labels from consolidated skills without altering procedures."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COLLECTIONS = [
    (ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations", 360, "Windows"),
    (ROOT / "ai-agent-skills/24-linux-system-operations (by Luo Kai)/00-consolidated-linux-operations", 300, "Linux"),
]
RETIRED_LINE = re.compile(r"^(?:-\s*)?(?:Former skill ID|Preserved skill ID|Source skill ID|Original skill ID):\s*.*$")
IDENTITY_LABEL = re.compile(r"^\*\*(?:Former skill identity \(retired\)|Skill identity):\*\* .+? · (?=\*\*Version:\*\*)")
FORBIDDEN = re.compile(
    r"(?im)^(?:-\s*)?(?:Former skill ID|Preserved skill ID|Source skill ID|Original skill ID):|"
    r"^\*\*(?:Former skill identity \(retired\)|Skill identity):\*\*"
)


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def split_frontmatter(raw: str, path: Path) -> tuple[dict, int]:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not match:
        fail(f"Invalid frontmatter: {path}")
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(f"Invalid YAML in {path}: {exc}")
    if not isinstance(metadata, dict):
        fail(f"Frontmatter must be a mapping: {path}")
    return metadata, match.end()


def clean_body(body: str, path: Path) -> tuple[str, int]:
    lines = []
    changes = 0
    for line in body.splitlines():
        if RETIRED_LINE.match(line):
            changes += 1
            continue
        if line.startswith("Former domain: "):
            line = "**Domain profile:** " + line[len("Former domain: "):]
            changes += 1
        if IDENTITY_LABEL.match(line):
            line = IDENTITY_LABEL.sub("", line, count=1)
            changes += 1
        lines.append(line)
    result = "\n".join(lines).rstrip() + "\n"
    if FORBIDDEN.search(result):
        fail(f"Retired profile identity remains: {path}")
    return result, changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write the validated cleanup")
    args = parser.parse_args()

    planned = []
    total = 0
    changes = 0
    for root, expected, family in COLLECTIONS:
        if not root.is_dir():
            fail(f"Missing consolidated {family} directory: {root}")
        files = sorted(root.rglob("SKILL.md"))
        if len(files) != expected:
            fail(f"{family}: expected {expected} skills, found {len(files)}")
        for path in files:
            raw = path.read_text(encoding="utf-8")
            metadata, body_start = split_frontmatter(raw, path)
            details = metadata.get("metadata") or {}
            if not isinstance(details, dict):
                fail(f"Missing metadata mapping: {path}")
            if details.get("author") != "Luo Kai" or str(details.get("version", "")) != "1.2.0":
                fail(f"Unexpected author or version: {path}")
            if "license" in metadata or "license" in details:
                fail(f"License field is not allowed in consolidated frontmatter: {path}")
            body, count = clean_body(raw[body_start:], path)
            planned.append((path, raw, raw[:body_start] + body))
            total += 1
            changes += count

    updated = [(path, new) for path, old, new in planned if old != new]
    if total != 660:
        fail(f"Expected 660 consolidated skills, found {total}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "300 consolidated Linux skills" not in readme or "660" not in readme:
        fail("Root README does not reflect the current consolidated collection")
    print(f"Validated {total} consolidated skills (360 Windows + 300 Linux).")
    print(f"Retired profile labels to normalize: {changes}.")
    print(f"Skill files requiring updates: {len(updated)}.")
    if not args.apply:
        print("DRY RUN ONLY. No repository files were changed.")
        return
    for path, content in updated:
        path.write_text(content, encoding="utf-8")
    print(f"APPLIED: normalized {len(updated)} skill files.")


if __name__ == "__main__":
    main()
