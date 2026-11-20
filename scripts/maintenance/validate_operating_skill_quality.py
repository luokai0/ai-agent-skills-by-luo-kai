#!/usr/bin/env python3
"""Validate legacy and consolidated Windows skills plus the Linux v1.1 collection."""
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
        "## Domain profiles", "## Unified discovery workflow",
        "## Stop conditions and recovery", "## Privacy-safe evidence and handoff",
        "## Completion checklist",
    ):
        if heading not in raw:
            fail(f"{skill_id}: missing {heading}")
    if not re.search(r"(?m)^### (?:[A-E]\. |Profile )", raw):
        fail(f"{skill_id}: missing domain profiles")
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


def validate_linux() -> int:
    if not LINUX_ROOT.is_dir():
        fail(f"missing Linux collection: {LINUX_ROOT}")
    domains = sorted(p for p in LINUX_ROOT.iterdir() if p.is_dir())
    if len(domains) != LINUX_DOMAINS:
        fail(f"Linux: expected {LINUX_DOMAINS} domains, found {len(domains)}")
    ids: list[str] = []
    total = 0
    for domain in domains:
        skill_dirs = sorted(p for p in domain.iterdir() if p.is_dir())
        if len(skill_dirs) != LINUX_PER_DOMAIN:
            fail(f"Linux/{domain.name}: expected {LINUX_PER_DOMAIN} skill folders, found {len(skill_dirs)}")
        for skill_dir in skill_dirs:
            skill = skill_dir / "SKILL.md"
            if not skill.is_file():
                fail(f"missing SKILL.md: {skill}")
            meta, raw = frontmatter(skill)
            skill_id = meta.get("skill_id")
            version = str(meta.get("version", ""))
            if not skill_id or not str(skill_id).startswith("linux-"):
                fail(f"missing/invalid Linux skill ID in {skill}")
            ids.append(str(skill_id))
            if version != "1.1.0":
                fail(f"{skill_id}: expected version 1.1.0, found {version!r}")
            if raw.count(LINUX_MARKER) != 1:
                fail(f"{skill_id}: expected exactly one v1.1 contract")
            contract = raw.split(LINUX_MARKER, 1)[1]
            for heading in (
                "### Execution environment contract", "### Task-specific operating procedure",
                "### Stop conditions and recovery", "### Evidence and handoff",
            ):
                if heading not in contract:
                    fail(f"{skill_id}: missing {heading}")
            for pattern in RISK_PATTERNS:
                if re.search(pattern, contract, re.I):
                    fail(f"{skill_id}: prohibited command pattern in execution contract: {pattern}")
            total += 1
    expected_ids = {f"linux-{i:04d}" for i in range(1, LINUX_TOTAL + 1)}
    if len(ids) != LINUX_TOTAL or len(set(ids)) != LINUX_TOTAL or set(ids) != expected_ids:
        fail("Linux ID sequence is incomplete, duplicated, or out of range")
    print(f"PASS Linux: {total} skills, {LINUX_DOMAINS} folders x {LINUX_PER_DOMAIN}, unique IDs, v1.1 contracts")
    return total


def validate_readmes() -> None:
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "[Linux system operations]" not in root_readme or "50 independently addressable workflows" not in root_readme:
        fail("root README is missing the Linux collection or corrected 50-workflow count")
    if "[Windows computer operations]" not in root_readme:
        fail("root README is missing the Windows collection")
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
