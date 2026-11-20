#!/usr/bin/env python3
"""Clean retired profile identifiers while preserving every operating procedure."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COLLECTIONS = [
    (ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations", 360, "windows"),
    (ROOT / "ai-agent-skills/24-linux-system-operations (by Luo Kai)/00-consolidated-linux-operations", 300, "linux"),
]
WINDOWS_STANDARD = ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)/SKILL_QUALITY_STANDARD.md"
LINUX_STANDARD = ROOT / "ai-agent-skills/24-linux-system-operations (by Luo Kai)/SKILL_QUALITY_STANDARD.md"
WINDOWS_README = ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)/README.md"
LINUX_README = ROOT / "ai-agent-skills/24-linux-system-operations (by Luo Kai)/README.md"
ROOT_README = ROOT / "README.md"
AUDIT = ROOT / "docs/SKILL_CONSOLIDATION_AUDIT.md"

IDENTITY_LABEL = re.compile(r"^\*\*(?:Former skill identity \(retired\)|Skill identity):\*\* .+? · (?=\*\*Version:\*\*)")
RETIRED_LINE = re.compile(r"^(?:Former skill ID|Preserved skill ID|Source skill ID|Original skill ID):\s*.*$")
FORBIDDEN_BODY = re.compile(
    r"(?im)^(?:Former skill ID|Preserved skill ID|Source skill ID|Original skill ID):|"
    r"^\*\*(?:Former skill identity \(retired\)|Skill identity):\*\*"
)


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def parse_frontmatter(raw: str, path: Path) -> tuple[dict, int]:
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


def normalize_body(body: str, path: Path) -> tuple[str, int]:
    output = []
    changed = 0
    for line in body.splitlines():
        if RETIRED_LINE.match(line):
            changed += 1
            continue
        if line.startswith("Former domain: "):
            line = "**Domain profile:** " + line[len("Former domain: "):]
            changed += 1
        if IDENTITY_LABEL.match(line):
            line = IDENTITY_LABEL.sub("", line, count=1)
            changed += 1
        output.append(line)
    normalized = "\n".join(output).rstrip() + "\n"
    if FORBIDDEN_BODY.search(normalized):
        fail(f"Retired profile identity remains after normalization: {path}")
    return normalized, changed


def update_text(path: Path, replacements: list[tuple[str, str]]) -> str:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        count = text.count(old)
        if count != 1:
            fail(f"{path}: expected exactly one documentation anchor, found {count}: {old[:90]}")
        text = text.replace(old, new, 1)
    return text


def documentation_updates() -> dict[Path, str]:
    windows_standard = update_text(WINDOWS_STANDARD, [
        (
            "This standard defines the quality bar for the 1,200 Windows computer-operation skills. “150 times more useful” is treated as a demand for a major practical improvement, not a word-count multiplier. More text without better decisions is not quality.",
            "This standard defines the quality bar for 360 consolidated Windows computer-operation skills across 40 domains. “150 times more useful” means stronger decisions, safer execution, clearer verification, and more reliable recovery, not artificial length.",
        ),
        (
            "Every skill preserves its original objective, stable ID, native tools, and domain-specific instructions, and includes an **Agent execution contract — v1.1**.",
            "Every consolidated skill preserves its task objective, native tools, complete domain-specific procedures, and operating safeguards, and includes the relevant **Agent execution contract — v1.1**.",
        ),
        (
            "1. YAML frontmatter parses and the original windows-#### ID is unchanged.",
            "1. YAML frontmatter parses; the consolidated skill ID is stable, unique, and uses the required group/workflow format.",
        ),
    ])
    linux_standard = update_text(LINUX_STANDARD, [
        (
            "Every consolidated skill contains three to five distribution profiles. Each profile preserves its original objective, stable linux-#### ID, distribution-specific commands, safety rules, and rights boundaries. The consolidated skill uses a stable linux-consolidated-gNN-task-slug ID.",
            "Every consolidated skill contains three to five distribution profiles. Each profile preserves its task objective, distribution-specific commands, safety rules, and rights boundaries. The consolidated skill uses a stable linux-consolidated-gNN-task-slug ID.",
        ),
        (
            "1. YAML frontmatter parses; the consolidated ID is stable and every profile retains its original linux-#### ID.",
            "1. YAML frontmatter parses; the consolidated ID is stable and unique, and every profile retains its distribution-specific procedures and safeguards.",
        ),
    ])
    root_readme = update_text(ROOT_README, [
        (
            "**1,250 original, distribution-specific skills for AI agents operating 25 well-known Linux systems.** Each distribution has its own folder and 50 independently addressable workflows.",
            "**300 consolidated Linux skills for AI agents operating 25 distributions, organized into six distribution-family groups with 50 workflows per group.**",
        ),
    ])
    windows_readme = update_text(WINDOWS_README, [
        (
            "Every replacement contains explicit domain profiles. The full original workflow bodies are retained inside their corresponding profiles, including objectives, operating discipline, procedures, preferred tools, command examples, safety boundaries, execution contracts, verification, recovery, and completion checklists. Shared discovery guidance is added at the consolidated-skill level.",
            "Every consolidated skill contains explicit domain profiles. Each profile retains its complete procedures, preferred tools, command examples, safety boundaries, execution contracts, verification, recovery, and completion criteria. Shared discovery guidance makes the combined workflow easier to select and execute.",
        ),
    ])
    linux_readme = update_text(LINUX_README, [
        (
            "Each skill contains three to five exact distribution profiles, preserving the original procedures, native commands, safety controls, verification, and recovery guidance.",
            "Each skill contains three to five exact distribution profiles, preserving the complete procedures, native commands, safety controls, verification, and recovery guidance.",
        ),
    ])
    audit = AUDIT.read_text(encoding="utf-8")
    status_old = "**Status:** Structural and representative-content audit completed; twelve Windows consolidation pilots committed to main; the first workflow has now been consolidated across all 40 Windows domains. Remaining workflow batches are still pending."
    status_new = "**Status:** Windows and Linux consolidation completed on main; 660 consolidated operating skills are validated across both collections. The remaining work is ongoing quality, security, and documentation maintenance."
    if status_old not in audit:
        fail("Audit status anchor not found")
    audit = audit.replace(status_old, status_new, 1)
    audit_replacements = [
        (
            "The remaining 29 workflows across all 40 Windows domains have been consolidated into 348 profile-based skills across the same 12 domain groups. The 1,160 original standalone files were replaced by 348 consolidated files; every source body is retained inside its domain profile, with only duplicate frontmatter replaced by stable consolidated metadata.",
            "The remaining 29 workflows across all 40 Windows domains are represented by 348 consolidated skills across the same 12 domain groups. Every domain profile retains its complete procedures, examples, execution controls, verification, and recovery guidance. Redundant profile-identity metadata is not part of the user-facing instructions.",
        ),
        ("- Linux skills unchanged: 1,250", "- Linux consolidated skills: 300"),
        ("- Combined Windows + Linux workflows: 1,610", "- Combined Windows + Linux workflows: 660"),
    ]
    for old, new in audit_replacements:
        if old not in audit:
            fail(f"Audit count/content anchor not found: {old[:90]}")
        audit = audit.replace(old, new, 1)
    audit += (
        "\n\n## Current consolidated state — 2026-11-20\n\n"
        "- Windows: 360 consolidated skills across 12 groups and 40 operating domains.\n"
        "- Linux: 300 consolidated skills across six groups and 25 distributions.\n"
        "- Combined operating collection: 660 consolidated skills.\n"
        "- No standalone Windows or Linux task SKILL.md files remain outside the consolidated roots.\n"
        "- All consolidated skill frontmatter is authored by Luo Kai, version 1.2.0, and contains no license field.\n"
        "- User-facing profile instructions no longer expose retired skill identifiers.\n"
    )
    return {
        WINDOWS_STANDARD: windows_standard,
        LINUX_STANDARD: linux_standard,
        ROOT_README: root_readme,
        WINDOWS_README: windows_readme,
        LINUX_README: linux_readme,
        AUDIT: audit,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write the validated profile and documentation updates")
    args = parser.parse_args()

    planned = []
    total_skills = 0
    total_identity_changes = 0
    for root, expected_count, family in COLLECTIONS:
        if not root.is_dir():
            fail(f"Missing consolidated {family} directory: {root}")
        files = sorted(root.rglob("SKILL.md"))
        if len(files) != expected_count:
            fail(f"{family}: expected {expected_count} consolidated skills, found {len(files)}")
        for path in files:
            raw = path.read_text(encoding="utf-8")
            metadata, body_start = parse_frontmatter(raw, path)
            details = metadata.get("metadata") or {}
            if not isinstance(details, dict):
                fail(f"{family}: missing metadata mapping: {path}")
            if details.get("author") != "Luo Kai" or str(details.get("version", "")) != "1.2.0":
                fail(f"{family}: unexpected author/version: {path}")
            if "license" in metadata or "license" in details:
                fail(f"{family}: license field is not allowed in consolidated frontmatter: {path}")
            body, changes = normalize_body(raw[body_start:], path)
            updated = raw[:body_start] + body
            planned.append((path, raw, updated))
            total_skills += 1
            total_identity_changes += changes

    docs = documentation_updates()
    changed = [(path, old, new) for path, old, new in planned if old != new]
    print(f"Validated {total_skills} consolidated skills (360 Windows + 300 Linux).")
    print(f"Profile identity/label adjustments: {total_identity_changes}.")
    print(f"Skill files requiring updates: {len(changed)}.")
    print(f"Documentation files requiring updates: {len(docs)}.")
    if not args.apply:
        print("DRY RUN ONLY. No repository files were changed.")
        return

    for path, content in changed:
        path.write_text(content, encoding="utf-8")
    for path, content in docs.items():
        path.write_text(content, encoding="utf-8")
    print(f"APPLIED: updated {len(changed)} skill files and {len(docs)} documentation files.")


if __name__ == "__main__":
    main()
