#!/usr/bin/env python3
"""Validate consolidated Windows skills and legacy or consolidated Linux skills."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WINDOWS_ROOT = ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)"
CONSOLIDATED_ROOT = WINDOWS_ROOT / "00-consolidated-desktop-operations"
LINUX_ROOT = ROOT / "ai-agent-skills/24-linux-system-operations (by Luo Kai)"

WINDOWS_DOMAINS = 40
WINDOWS_LEGACY_PER_DOMAIN = 29
WINDOWS_ORIGINAL_TOTAL = 1200
WINDOWS_CONSOLIDATED_MANUAL = 12
WINDOWS_CONSOLIDATED_FINAL = 360

LINUX_DOMAINS = 25
LINUX_PER_DOMAIN = 50
LINUX_TOTAL = 1250
LINUX_CONSOLIDATED_TOTAL = 300
LINUX_CONSOLIDATED_ROOT = LINUX_ROOT / "00-consolidated-linux-operations"
LINUX_GROUP_SIZES = [5, 5, 4, 3, 4, 4]
LINUX_REQUIRED_HEADINGS = ("Execution environment contract", "Task-specific operating procedure", "Stop conditions and recovery", "Evidence and handoff")

WINDOWS_MARKER = "Agent execution contract — v1.1"
LINUX_MARKER = "## Agent execution contract — v1.1"

RISK_PATTERNS = [
    r"\bcurl\b[^\n]*\|\s*(?:sh|bash)", r"\bwget\b[^\n]*\|\s*(?:sh|bash)",
    r"\brm\s+-rf\b", r"\bmkfs(?:\.[a-z0-9]+)?\b", r"\b(?:wipefs|shred|blkdiscard)\b",
    r"\bdd\s+if=", r"\b(?:iptables\s+-F|nft\s+flush\s+ruleset)\b", r"\bsetenforce\s+0\b",
    r"\bchmod\s+-R\s+777\b", r"Invoke-Expression", r"Set-ExecutionPolicy\s+Bypass",
    r"Set-MpPreference", r"Format-Volume", r"Clear-Disk", r"Disable-NetFirewallProfile",
    r"Remove-Item\s+-Recurse", r"Start-Process\s+-Verb\s+RunAs",
]

WINDOWS_REMOVED_SOURCE_IDS = {
    f"windows-{((domain - 1) * 30 + 1):04d}" for domain in range(1, WINDOWS_DOMAINS + 1)
}

WINDOWS_GROUP_SIZES = {
    1: 3, 2: 3, 3: 3, 4: 5, 5: 5, 6: 3,
    7: 2, 8: 2, 9: 3, 10: 5, 11: 4, 12: 2,
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def frontmatter(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not match:
        fail(f"invalid frontmatter boundary: {path}")
    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(f"invalid YAML in {path}: {exc}")
    if not isinstance(meta, dict):
        fail(f"frontmatter must be a mapping: {path}")
    return meta, raw


def validate_legacy_skill(path: Path, seen_ids: set[str]) -> None:
    meta, raw = frontmatter(path)
    metadata = meta.get("metadata", {})
    skill_id = metadata.get("skill_id") if isinstance(metadata, dict) else None
    version = str(metadata.get("version", "")) if isinstance(metadata, dict) else ""
    if not skill_id or not str(skill_id).startswith("windows-"):
        fail(f"missing/invalid legacy Windows skill ID: {path}")
    skill_id = str(skill_id)
    if skill_id in seen_ids:
        fail(f"duplicate Windows skill ID: {skill_id}")
    seen_ids.add(skill_id)
    if version != "1.1.0":
        fail(f"{skill_id}: expected legacy version 1.1.0, found {version!r}")
    if raw.count(WINDOWS_MARKER) != 1:
        fail(f"{skill_id}: expected exactly one v1.1 execution contract")
    contract_start = raw.find(WINDOWS_MARKER)
    contract = raw[contract_start:]
    for heading in ("### Execution plan", "### Stop conditions and recovery", "### Evidence and handoff"):
        if heading not in contract:
            fail(f"{skill_id}: missing {heading}")
    for pattern in RISK_PATTERNS:
        if re.search(pattern, contract, re.I):
            fail(f"{skill_id}: prohibited command pattern in execution contract: {pattern}")


def validate_consolidated_skill(path: Path, seen_ids: set[str]) -> str:
    meta, raw = frontmatter(path)
    metadata = meta.get("metadata", {})
    if not isinstance(metadata, dict):
        fail(f"missing metadata mapping: {path}")
    skill_id = metadata.get("skill_id")
    if not skill_id or not str(skill_id).startswith("windows-consolidated-"):
        fail(f"missing/invalid consolidated skill ID: {path}")
    skill_id = str(skill_id)
    if skill_id in seen_ids:
        fail(f"duplicate consolidated skill ID: {skill_id}")
    seen_ids.add(skill_id)
    if str(metadata.get("version", "")) != "1.2.0":
        fail(f"{skill_id}: expected consolidated version 1.2.0")
    if metadata.get("author") != "Luo Kai":
        fail(f"{skill_id}: author metadata must be Luo Kai")
    if "license" in meta or "license" in metadata:
        fail(f"{skill_id}: consolidated frontmatter must not contain a license field")
    for heading in (
        "## Objective", "## When to use", "## Required operating discipline",
        "## Domain profiles",
        "## Stop conditions and recovery", "## Privacy-safe evidence and handoff",
        "## Completion checklist",
    ):
        if heading not in raw:
            fail(f"{skill_id}: missing {heading}")
    if not re.search(r"(?m)^### (?:[A-E]\. |Profile )", raw):
        fail(f"{skill_id}: missing domain profiles")
    if not re.search(r"(?mi)^## Unified .*workflow\s*$", raw):
        fail(f"{skill_id}: missing unified workflow")
    if skill_id.startswith("windows-consolidated-g"):
        match = re.fullmatch(r"windows-consolidated-g(\d{2})-w(\d{2})", skill_id)
        if not match:
            fail(f"{skill_id}: invalid generated group/workflow ID")
        group_number = int(match.group(1))
        expected_profiles = WINDOWS_GROUP_SIZES.get(group_number)
        if expected_profiles is None:
            fail(f"{skill_id}: unknown consolidated group")
        contracts = list(re.finditer(r"(?m)^#{4,6} Agent execution contract — v1\.1\s*$", raw))
        if len(contracts) != expected_profiles:
            fail(f"{skill_id}: expected {expected_profiles} retained domain contracts, found {len(contracts)}")
        for contract_match in contracts:
            tail = raw[contract_match.start():]
            end_match = re.search(r"(?m)^#{4,6} Completion checklist\s*$", tail)
            contract = tail[:end_match.start()] if end_match else tail
            for heading in ("Execution plan", "Stop conditions and recovery", "Evidence and handoff"):
                if not re.search(r"(?m)^#{5,6} " + re.escape(heading) + r"\s*$", contract):
                    fail(f"{skill_id}: retained source contract is missing {heading}")
            for pattern in RISK_PATTERNS:
                if re.search(pattern, contract, re.I):
                    fail(f"{skill_id}: prohibited command pattern in retained contract: {pattern}")

    return skill_id


def validate_windows() -> int:
    if not WINDOWS_ROOT.is_dir():
        fail(f"missing Windows collection: {WINDOWS_ROOT}")
    if not CONSOLIDATED_ROOT.is_dir():
        fail(f"missing consolidated Windows collection: {CONSOLIDATED_ROOT}")

    legacy_files = sorted(
        p for p in WINDOWS_ROOT.rglob("SKILL.md")
        if CONSOLIDATED_ROOT not in p.parents
    )
    consolidated_files = sorted(CONSOLIDATED_ROOT.rglob("SKILL.md"))

    legacy_ids: set[str] = set()
    if legacy_files:
        domains = sorted(
            p for p in WINDOWS_ROOT.iterdir()
            if p.is_dir() and p != CONSOLIDATED_ROOT
        )
        if len(domains) != WINDOWS_DOMAINS:
            fail(f"Windows legacy stage: expected {WINDOWS_DOMAINS} domains, found {len(domains)}")
        expected_legacy_ids = {
            f"windows-{i:04d}" for i in range(1, WINDOWS_ORIGINAL_TOTAL + 1)
        } - WINDOWS_REMOVED_SOURCE_IDS
        for domain in domains:
            files = sorted(domain.glob("*/SKILL.md"))
            if len(files) != WINDOWS_LEGACY_PER_DOMAIN:
                fail(
                    f"Windows {domain.name}: expected {WINDOWS_LEGACY_PER_DOMAIN} remaining "
                    f"legacy workflows, found {len(files)}"
                )
            for path in files:
                validate_legacy_skill(path, legacy_ids)
        if legacy_ids != expected_legacy_ids:
            missing = sorted(expected_legacy_ids - legacy_ids)[:5]
            extra = sorted(legacy_ids - expected_legacy_ids)[:5]
            fail(f"Windows legacy ID sequence mismatch; missing={missing}, extra={extra}")
        if len(legacy_files) != WINDOWS_DOMAINS * WINDOWS_LEGACY_PER_DOMAIN:
            fail("Windows legacy skill count does not match the 40 x 29 migration stage")
    elif legacy_files:
        fail("unexpected Windows legacy state")

    consolidated_ids: set[str] = set()
    for path in consolidated_files:
        validate_consolidated_skill(path, consolidated_ids)

    manual_ids = {f"windows-consolidated-{i:04d}" for i in range(1, WINDOWS_CONSOLIDATED_MANUAL + 1)}
    if len(consolidated_files) == WINDOWS_CONSOLIDATED_MANUAL:
        if consolidated_ids != manual_ids:
            fail("Windows pilot stage must contain the twelve mapped consolidated skills")
        if len(legacy_files) != WINDOWS_DOMAINS * WINDOWS_LEGACY_PER_DOMAIN:
            fail("Windows pilot stage must retain all remaining legacy workflows")
        total = len(legacy_files) + len(consolidated_files)
        if total != 1172:
            fail(f"Windows pilot-stage total should be 1172, found {total}")
        print("PASS Windows pilot stage: 1,160 legacy workflows + 12 consolidated workflows")
        return total

    if len(consolidated_files) == WINDOWS_CONSOLIDATED_FINAL:
        generated_ids = {
            f"windows-consolidated-g{group:02d}-w{task:02d}"
            for group, size in WINDOWS_GROUP_SIZES.items()
            for task in range(2, 31)
        }
        expected_ids = manual_ids | generated_ids
        if consolidated_ids != expected_ids:
            missing = sorted(expected_ids - consolidated_ids)[:5]
            extra = sorted(consolidated_ids - expected_ids)[:5]
            fail(f"Windows final ID sequence mismatch; missing={missing}, extra={extra}")
        if legacy_files:
            fail("Windows final stage must not retain duplicate legacy SKILL.md files")
        print("PASS Windows consolidated stage: 360 skills across 12 groups")
        return len(consolidated_files)

    fail(
        "Windows collection is in an unsupported partial state: "
        f"{len(legacy_files)} legacy + {len(consolidated_files)} consolidated skills"
    )


def validate_linux_legacy() -> int:
    domains = sorted(path for path in LINUX_ROOT.iterdir() if path.is_dir() and re.match(r"^\d{2}-", path.name))
    if len(domains) != LINUX_DOMAINS:
        fail(f"Expected {LINUX_DOMAINS} Linux distribution folders, found {len(domains)}")
    total = 0
    seen_ids = set()
    for domain in domains:
        skills = sorted(domain.rglob("SKILL.md"))
        if len(skills) != LINUX_PER_DOMAIN:
            fail(f"{domain.name}: expected {LINUX_PER_DOMAIN} skills, found {len(skills)}")
        for skill in skills:
            meta, raw = frontmatter(skill)
            skill_id = str(meta.get("skill_id", ""))
            if not skill_id.startswith("linux-") or skill_id in seen_ids:
                fail(f"Invalid or duplicate Linux skill ID in {skill}: {skill_id}")
            seen_ids.add(skill_id)
            if str(meta.get("version", "")) != "1.1.0":
                fail(f"Unexpected legacy Linux skill version in {skill}")
            if raw.count(LINUX_MARKER) != 1:
                fail(f"Expected exactly one v1.1 execution contract in {skill}")
            contract = raw.split(LINUX_MARKER, 1)[1]
            for heading in LINUX_REQUIRED_HEADINGS:
                if not re.search(rf"(?m)^### {re.escape(heading)}\s*$", contract):
                    fail(f"Missing Linux contract section {heading} in {skill}")
            for pattern in RISK_PATTERNS:
                if re.search(pattern, contract, re.I):
                    fail(f"Unsafe Linux execution-contract pattern {pattern!r} in {skill}")
            total += 1
    if total != LINUX_TOTAL:
        fail(f"Expected {LINUX_TOTAL} legacy Linux skills, found {total}")
    print(f"PASS: validated {total} legacy Linux skills across {len(domains)} distributions.")
    return total


def validate_linux_consolidated_skill(skill: Path, group_number: int, group_size: int, task_slug: str) -> None:
    meta, raw = frontmatter(skill)
    details = meta.get("metadata") or {}
    if not isinstance(details, dict):
        fail(f"Missing nested metadata in {skill}")
    expected_id = f"linux-consolidated-g{group_number:02d}-{task_slug}"
    if details.get("skill_id") != expected_id:
        fail(f"Expected consolidated ID {expected_id} in {skill}")
    if details.get("author") != "Luo Kai" or str(details.get("version", "")) != "1.2.0":
        fail(f"Unexpected author or version in {skill}")
    if details.get("platform") != "Linux distributions" or details.get("category") != "Linux System Operations":
        fail(f"Incorrect platform/category metadata in {skill}")
    if "license" in meta or "license" in details:
        fail(f"Original consolidated skill must not include license metadata: {skill}")
    if not isinstance(meta.get("name"), str) or not meta["name"].strip():
        fail(f"Missing skill name in {skill}")
    if not isinstance(meta.get("description"), str) or not meta["description"].strip():
        fail(f"Missing skill description in {skill}")

    if len(re.findall(r"(?m)^### Profile \d+:", raw)) != group_size:
        fail(f"Expected {group_size} distribution profiles in {skill}")
    contract_pattern = r"(?m)^#{4,6} Agent execution contract — v1\.1\s*$"
    matches = list(re.finditer(contract_pattern, raw))
    if len(matches) != group_size:
        fail(f"Expected {group_size} retained execution contracts in {skill}")

    for heading in (
        "Objective", "Distribution profiles", "Unified workflow",
        "Stop conditions and recovery", "Privacy-safe evidence and handoff",
        "Completion checklist",
    ):
        if not re.search(rf"(?m)^## {re.escape(heading)}\s*$", raw):
            fail(f"Missing top-level section {heading} in {skill}")

    for heading in LINUX_REQUIRED_HEADINGS:
        nested_heading = rf"(?m)^#{{4,6}} {re.escape(heading)}\s*$"
        if len(re.findall(nested_heading, raw)) != group_size:
            fail(f"Expected {group_size} retained {heading} sections in {skill}")

    for match in matches:
        tail = raw[match.end():]
        end_match = re.search(r"(?m)^#{4,6} Completion checklist\s*$", tail)
        contract_end = match.end() + end_match.start() if end_match else len(raw)
        contract = raw[match.start():contract_end]
        for pattern in RISK_PATTERNS:
            if re.search(pattern, contract, re.I):
                fail(f"Unsafe retained execution-contract pattern {pattern!r} in {skill}")

    if "Copyright (c) 2026 Luo Kai. All rights reserved" not in raw:
        fail(f"Missing original-work copyright notice in {skill}")


def validate_linux_consolidated() -> int:
    groups = sorted(path for path in LINUX_CONSOLIDATED_ROOT.iterdir() if path.is_dir())
    if len(groups) != len(LINUX_GROUP_SIZES):
        fail(f"Expected six consolidated Linux groups, found {len(groups)}")
    task_baseline = None
    seen_ids = set()
    for group_number, (group, group_size) in enumerate(zip(groups, LINUX_GROUP_SIZES), 1):
        if not group.name.startswith(f"{group_number:02d}-"):
            fail(f"Unexpected Linux group ordering/name: {group.name}")
        task_dirs = sorted(path for path in group.iterdir() if path.is_dir())
        if len(task_dirs) != 50:
            fail(f"{group.name}: expected 50 task folders, found {len(task_dirs)}")
        task_names = {path.name for path in task_dirs}
        if task_baseline is None:
            task_baseline = task_names
        elif task_names != task_baseline:
            fail(f"Task set differs in consolidated group {group.name}")
        for task_dir in task_dirs:
            skill = task_dir / "SKILL.md"
            if not skill.is_file():
                fail(f"Missing consolidated Linux skill: {skill}")
            validate_linux_consolidated_skill(skill, group_number, group_size, task_dir.name)
            skill_id = f"linux-consolidated-g{group_number:02d}-{task_dir.name}"
            if skill_id in seen_ids:
                fail(f"Duplicate consolidated Linux ID: {skill_id}")
            seen_ids.add(skill_id)

    legacy_domains = [
        path for path in LINUX_ROOT.iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name) and path != LINUX_CONSOLIDATED_ROOT
    ]
    remaining = [skill for domain in legacy_domains for skill in domain.rglob("SKILL.md")]
    if remaining:
        fail(f"Found {len(remaining)} standalone Linux skills outside the consolidated root")
    if len(seen_ids) != LINUX_CONSOLIDATED_TOTAL:
        fail(f"Expected {LINUX_CONSOLIDATED_TOTAL} consolidated Linux skills, found {len(seen_ids)}")
    print(f"PASS: validated {len(seen_ids)} consolidated Linux skills across six groups.")
    return len(seen_ids)


def validate_linux() -> int:
    if LINUX_CONSOLIDATED_ROOT.is_dir():
        return validate_linux_consolidated()
    return validate_linux_legacy()

def validate_readmes() -> None:
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    linux_readme = (LINUX_ROOT / "README.md").read_text(encoding="utf-8")
    if "[Linux system operations]" not in root_readme:
        fail("root README is missing the Linux collection")
    if "[Windows computer operations]" not in root_readme:
        fail("root README is missing the Windows collection")

    consolidated_docs = "300 consolidated skills" in linux_readme
    if consolidated_docs:
        if "300 consolidated Linux workflows" not in root_readme or "50 workflows per group" not in root_readme:
            fail("root README is missing the consolidated Linux counts")
        if "six distribution groups" not in linux_readme.casefold():
            fail("Linux README is missing the six distribution groups")
    elif "50 independently addressable workflows" not in root_readme:
        fail("legacy root README is missing the 50-workflow Linux count")

    for label, folder in (("Windows", WINDOWS_ROOT), ("Linux", LINUX_ROOT)):
        readme = (folder / "README.md").read_text(encoding="utf-8")
        if "SKILL_QUALITY_STANDARD.md" not in readme:
            fail(f"{label}: collection README is missing its quality-standard link")
        if not (folder / "SKILL_QUALITY_STANDARD.md").is_file():
            fail(f"{label}: quality standard file is missing")
    print("PASS root and collection README quality-standard links")


windows_total = validate_windows()
linux_total = validate_linux()
validate_readmes()
print(f"PASS combined skill count: {windows_total + linux_total}")
