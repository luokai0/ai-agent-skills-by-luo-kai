#!/usr/bin/env python3
"""Validate the v1.1 Windows and Linux agent-skill quality contracts."""
from __future__ import annotations
import re
import sys
from collections import Counter
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
COLLECTIONS = {
    "windows": (ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)", 40, 30, "windows", 1200),
    "linux": (ROOT / "ai-agent-skills/24-linux-system-operations (by Luo Kai)", 25, 50, "linux", 1250),
}
MARKER = "## Agent execution contract — v1.1"
RISK_PATTERNS = [
    r"\bcurl\b[^\n]*\|\s*(?:sh|bash)", r"\bwget\b[^\n]*\|\s*(?:sh|bash)",
    r"\brm\s+-rf\b", r"\bmkfs(?:\.[a-z0-9]+)?\b", r"\b(?:wipefs|shred|blkdiscard)\b",
    r"\bdd\s+if=", r"\b(?:iptables\s+-F|nft\s+flush\s+ruleset)\b", r"\bsetenforce\s+0\b",
    r"\bchmod\s+-R\s+777\b", r"Invoke-Expression", r"Set-ExecutionPolicy\s+Bypass",
    r"Set-MpPreference", r"Format-Volume", r"Clear-Disk", r"Disable-NetFirewallProfile",
    r"Remove-Item\s+-Recurse", r"Start-Process\s+-Verb\s+RunAs",
]

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def validate(label: str, config: tuple) -> None:
    folder, expected_domains, per_domain, prefix, expected_total = config
    if not folder.is_dir():
        fail(f"missing collection directory: {folder}")
    domains = sorted(p for p in folder.iterdir() if p.is_dir())
    if len(domains) != expected_domains:
        fail(f"{label}: expected {expected_domains} domains, found {len(domains)}")
    ids: list[str] = []
    total = 0
    for domain in domains:
        skill_dirs = sorted(p for p in domain.iterdir() if p.is_dir())
        if len(skill_dirs) != per_domain:
            fail(f"{label}/{domain.name}: expected {per_domain} skill folders, found {len(skill_dirs)}")
        domain_count = 0
        for skill_dir in skill_dirs:
            skill = skill_dir / "SKILL.md"
            if not skill.is_file():
                fail(f"missing SKILL.md: {skill}")
            raw = skill.read_text(encoding="utf-8")
            match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
            if not match:
                fail(f"invalid frontmatter boundary: {skill}")
            try:
                meta = yaml.safe_load(match.group(1))
            except yaml.YAMLError as exc:
                fail(f"invalid YAML in {skill}: {exc}")
            if label == "windows":
                metadata = meta.get("metadata", {}) if isinstance(meta, dict) else {}
                skill_id = metadata.get("skill_id")
                version = str(metadata.get("version", ""))
                required_sections = ["### Execution plan", "### Stop conditions and recovery", "### Evidence and handoff"]
            else:
                skill_id = meta.get("skill_id") if isinstance(meta, dict) else None
                version = str(meta.get("version", "")) if isinstance(meta, dict) else ""
                required_sections = ["### Execution environment contract", "### Task-specific operating procedure", "### Stop conditions and recovery", "### Evidence and handoff"]
            if not skill_id or not str(skill_id).startswith(prefix + "-"):
                fail(f"missing/invalid skill ID in {skill}")
            ids.append(str(skill_id))
            if version != "1.1.0":
                fail(f"{skill_id}: expected version 1.1.0, found {version!r}")
            if raw.count(MARKER) != 1:
                fail(f"{skill_id}: expected exactly one v1.1 contract")
            contract = raw.split(MARKER, 1)[1]
            for heading in required_sections:
                if heading not in contract:
                    fail(f"{skill_id}: missing {heading}")
            for pattern in RISK_PATTERNS:
                if re.search(pattern, contract, re.I):
                    fail(f"{skill_id}: prohibited command pattern in new contract: {pattern}")
            domain_count += 1
            total += 1
        if domain_count != per_domain:
            fail(f"{label}/{domain.name}: incomplete skill folder")
    expected_ids = {f"{prefix}-{i:04d}" for i in range(1, expected_total + 1)}
    if len(ids) != expected_total or len(set(ids)) != expected_total:
        fail(f"{label}: expected {expected_total} unique IDs; found {len(ids)} files/{len(set(ids))} unique IDs")
    if set(ids) != expected_ids:
        fail(f"{label}: ID sequence is incomplete or out of range")
    print(f"PASS {label}: {total} skills, {expected_domains} folders x {per_domain}, unique IDs, v1.1 contracts")

for name, config in COLLECTIONS.items():
    validate(name, config)

root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
if "[Linux system operations]" not in root_readme or "50 independently addressable workflows" not in root_readme:
    fail("root README is missing the Linux collection or corrected 50-workflow count")
if "[Windows computer operations]" not in root_readme:
    fail("root README is missing the Windows collection")
for name, config in COLLECTIONS.items():
    readme = (config[0] / "README.md").read_text(encoding="utf-8")
    if "SKILL_QUALITY_STANDARD.md" not in readme:
        fail(f"{name}: collection README is missing its quality-standard link")
    if not (config[0] / "SKILL_QUALITY_STANDARD.md").is_file():
        fail(f"{name}: quality standard file is missing")
print("PASS README and collection quality-standard links")
