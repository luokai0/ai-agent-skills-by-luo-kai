#!/usr/bin/env python3
"""Validated migration of the remaining 29 Windows workflows into 12 profile groups."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
COLLECTION = ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)"
CONSOLIDATED = COLLECTION / "00-consolidated-desktop-operations"
MAP_PATH = ROOT / "docs/SKILL_MERGE_MAP.md"
AUDIT_PATH = ROOT / "docs/SKILL_CONSOLIDATION_AUDIT.md"
GROUPS = [
    ("workspace-and-window", "Desktop and window management", ["01-desktop-shell", "02-windows-navigation", "03-window-multitasking"]),
    ("workspace-files", "Workspace and file operations", ["04-start-taskbar", "05-file-explorer", "06-file-operations"]),
    ("search-archive-storage", "Search, archives, and storage", ["07-search-metadata", "08-archives-transfer", "09-storage-volumes"]),
    ("shell-process-startup", "Shells, processes, and startup", ["10-powershell-fundamentals", "11-powershell-advanced", "12-terminal-cmd", "13-process-services", "14-startup-scheduling"]),
    ("configuration-software-devices", "Configuration, software, and devices", ["15-registry-policy", "16-app-installation", "17-package-management", "18-windows-updates", "19-devices-drivers"]),
    ("input-output-peripherals", "Input, output, and peripherals", ["20-display-audio-input", "37-clipboard-input", "38-printers-peripherals"]),
    ("network-connectivity", "Network and secure connectivity", ["21-wifi-ethernet", "22-dns-firewall-vpn"]),
    ("browser-productivity", "Browser and productivity applications", ["23-browser-webapps", "24-office-productivity"]),
    ("development-virtualization", "Development and virtualization", ["25-developer-workstations", "26-git-source-control", "27-wsl-virtualization"]),
    ("health-security-privacy", "Health, security, and privacy", ["28-performance-monitoring", "29-battery-thermal-power", "30-logs-diagnostics", "31-security-defender", "32-privacy-permissions"]),
    ("accessibility-remote-visual", "Accessibility, remote support, and visual automation", ["33-accessibility", "34-remote-desktop", "35-ui-automation", "36-screenshots-ocr"]),
    ("backup-provisioning", "Backup, recovery, and provisioning", ["39-backup-recovery", "40-provisioning-accounts"]),
]
EXPECTED_TASKS = 29
EXPECTED_SOURCES = 1160
EXPECTED_OUTPUTS = 348
SOURCE_VERSION = "1.1.0"
NEW_VERSION = "1.2.0"
MARKER = "Agent execution contract — v1.1"
RISK_PATTERNS = [
    r"\bcurl\b[^\n]*\|\s*(?:sh|bash)", r"\bwget\b[^\n]*\|\s*(?:sh|bash)",
    r"\brm\s+-rf\b", r"\bmkfs(?:\.[a-z0-9]+)?\b", r"\b(?:wipefs|shred|blkdiscard)\b",
    r"\bdd\s+if=", r"\b(?:iptables\s+-F|nft\s+flush\s+ruleset)\b", r"\bsetenforce\s+0\b",
    r"\bchmod\s+-R\s+777\b", r"Invoke-Expression", r"Set-ExecutionPolicy\s+Bypass",
    r"Set-MpPreference", r"Format-Volume", r"Clear-Disk", r"Disable-NetFirewallProfile",
    r"Remove-Item\s+-Recurse", r"Start-Process\s+-Verb\s+RunAs",
]


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def parse_skill(path: Path) -> tuple[dict, str, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not match:
        fail("invalid frontmatter boundary: " + str(path))
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail("invalid YAML in " + str(path) + ": " + str(exc))
    if not isinstance(metadata, dict):
        fail("frontmatter must be a mapping: " + str(path))
    return metadata, raw[match.end():].strip(), raw


def validate_source(path: Path) -> tuple[dict, str]:
    metadata, body, raw = parse_skill(path)
    details = metadata.get("metadata") or {}
    if not isinstance(details, dict) or str(details.get("author", "")).casefold() != "luo kai":
        fail("source is not identified as original Luo Kai work: " + str(path))
    skill_id = str(details.get("skill_id", ""))
    if not skill_id.startswith("windows-"):
        fail("missing Windows source ID: " + str(path))
    if str(details.get("version", "")) != SOURCE_VERSION:
        fail(skill_id + ": expected source version " + SOURCE_VERSION)
    if raw.count(MARKER) != 1:
        fail(skill_id + ": expected exactly one v1.1 execution contract")
    contract = raw[raw.find(MARKER):]
    for heading in ("### Execution plan", "### Stop conditions and recovery", "### Evidence and handoff"):
        if heading not in contract:
            fail(skill_id + ": missing " + heading)
    for pattern in RISK_PATTERNS:
        if re.search(pattern, contract, re.I):
            fail(skill_id + ": prohibited command pattern " + pattern)
    if not isinstance(metadata.get("name"), str) or ":" not in metadata["name"]:
        fail(skill_id + ": cannot determine workflow name")
    return metadata, body


def nest_headings(body: str) -> str:
    output = []
    fenced = False
    for line in body.splitlines():
        if line.lstrip().startswith(chr(96) * 3) or line.lstrip().startswith("~~~"):
            fenced = not fenced
            output.append(line)
            continue
        if not fenced:
            match = re.match(r"^(#{1,3})(\s+.*)$", line)
            if match:
                line = "#" * (len(match.group(1)) + 3) + match.group(2)
            line = line.replace("**Skill identity:**", "**Former skill identity (retired):**", 1)
        output.append(line)
    return "\n".join(output).strip()


def build_replacement(group_index: int, group_label: str, task_dir: str,
                      sources: list[tuple[str, Path, dict, str]]) -> tuple[str, str]:
    task_number = int(task_dir.split("-", 1)[0])
    actions = [meta["name"].split(":", 1)[1].strip() for _, _, meta, _ in sources]
    if len({action.casefold() for action in actions}) != 1:
        fail("workflow name mismatch in group " + str(group_index) + ", task " + task_dir)
    action = actions[0]
    skill_id = f"windows-consolidated-g{group_index:02d}-w{task_number:02d}"
    skill_name = f"Windows {action} across {group_label}"
    description = (
        f"Consolidated {action.lower()} workflow across {len(sources)} Windows domains: "
        f"{group_label}. Preserves each profile's original procedures, tools, safety rules, "
        "examples, verification, and recovery guidance."
    )
    frontmatter = (
        "---\n"
        f"name: {json.dumps(skill_name, ensure_ascii=False)}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "metadata:\n"
        '  author: "Luo Kai"\n'
        '  platform: "Windows 10 and Windows 11"\n'
        '  category: "Windows Computer Operations"\n'
        f'  skill_id: "{skill_id}"\n'
        f'  version: "{NEW_VERSION}"\n'
        "---\n\n"
    )
    sections = [
        f"# {skill_name}",
        "## Objective",
        f"Combine the {action.lower()} workflows from {len(sources)} related Windows domains. Select only the profile that matches the user's target. Each profile retains its complete original workflow body, including task instructions, preferred tools, command examples, approval rules, verification, recovery, and completion criteria.",
        "## When to use",
        "Use when the user requests " + action.lower() + " in any of these domains: " + "; ".join(meta["name"].split(":", 1)[0].strip() for _, _, meta, _ in sources) + ".",
        "## Required operating discipline",
        "- Confirm the exact device, account/session, target, and applicable domain before acting.",
        "- Select only the relevant domain profile; do not execute every profile by default.",
        "- Preserve each profile's native tools, platform distinctions, approval gates, and recovery rules.",
        "- Prefer least privilege, observable actions, read-only inspection, and independent verification.",
        "- Never bypass security controls, consent, organizational policy, or user approval.",
        "- Do not discard or replace source procedures; use the full domain profile when a task-specific detail is needed.",
        "## Domain profiles",
    ]
    for number, (domain, path, meta, body) in enumerate(sources, 1):
        sections.append(f"### Profile {number}: {meta['name'].split(':', 1)[0].strip()}")
        sections.append("Former domain: " + domain)
        sections.append("Former skill ID: " + str(meta["metadata"]["skill_id"]))
        sections.append(nest_headings(body))
    sections.extend([
        "## Unified discovery workflow",
        "1. Bind the request to the exact device, session, target, and one or more relevant domain profiles.",
        "2. Capture the baseline using the profile's native UI and bounded diagnostics.",
        "3. Follow that profile's original workflow and task-specific safety boundary.",
        "4. Stop when identity, permission, policy, or expected state is unclear.",
        "5. Obtain explicit approval before consequential or externally visible changes.",
        "6. Verify the result independently using the profile's stated evidence.",
        "7. Report actions, unchanged state, evidence, limitations, and remaining risk.",
        "## Stop conditions and recovery",
        "Stop if target identity is ambiguous, a command or control is unavailable without a documented fallback, policy blocks the action, unsaved work may be lost, or the observed state differs from expectations. Preserve the last known-good state and exact error. Use the relevant profile's recovery route; do not improvise destructive workarounds.",
        "## Privacy-safe evidence and handoff",
        "Use the evidence and handoff requirements in the selected profile. Redact passwords, tokens, private paths, account identifiers, IP addresses, clipboard contents, and unrelated personal information. Mark unknown values as unknown.",
        "## Completion checklist",
        "- [ ] The exact target and applicable profile(s) were confirmed.",
        "- [ ] Original domain-specific procedures and safety rules were followed.",
        "- [ ] No unrelated files, settings, accounts, devices, or processes were changed.",
        "- [ ] Any consequential action had explicit approval and a recoverable plan.",
        "- [ ] The resulting state was independently verified.",
        "- [ ] Limitations, remaining risks, and evidence were reported accurately.",
        "---",
        "Copyright (c) 2026 Luo Kai. All rights reserved for original material in this consolidated skill.",
    ])
    return skill_id, frontmatter + "\n\n".join(sections).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write replacements and delete retired source files")
    args = parser.parse_args()

    for path in (COLLECTION, CONSOLIDATED, MAP_PATH, AUDIT_PATH):
        if not path.exists():
            fail("required path is missing: " + str(path))

    manual_files = sorted(CONSOLIDATED.glob("*/SKILL.md"))
    if len(manual_files) != 12:
        fail(f"expected 12 completed discovery pilots, found {len(manual_files)}")
    manual_ids = set()
    for path in manual_files:
        meta, _, _ = parse_skill(path)
        manual_ids.add(str((meta.get("metadata") or {}).get("skill_id", "")))
    if manual_ids != {f"windows-consolidated-{i:04d}" for i in range(1, 13)}:
        fail("the twelve existing discovery pilots do not match expected IDs")

    replacements = []
    source_paths = []
    map_entries = []
    for group_index, (group_slug, group_label, domains) in enumerate(GROUPS, 1):
        task_sets = []
        for domain in domains:
            domain_path = COLLECTION / domain
            if not domain_path.is_dir():
                fail("missing original domain directory: " + str(domain_path))
            task_sets.append({
                p.name for p in domain_path.iterdir()
                if p.is_dir() and (p / "SKILL.md").is_file()
            })
        if any(tasks != task_sets[0] for tasks in task_sets[1:]):
            fail(f"workflow folders do not match across group {group_index}: {domains}")
        task_names = sorted(task_sets[0])
        if len(task_names) != EXPECTED_TASKS or "01-discover-current-state" in task_names:
            fail(f"group {group_index} expected 29 remaining workflows, found {len(task_names)}")

        for task_dir in task_names:
            sources = []
            for domain in domains:
                path = COLLECTION / domain / task_dir / "SKILL.md"
                metadata, body = validate_source(path)
                sources.append((domain, path, metadata, body))
                source_paths.append(path)
            skill_id, content = build_replacement(group_index, group_label, task_dir, sources)
            output_path = CONSOLIDATED / f"{group_index:02d}-{group_slug}" / task_dir / "SKILL.md"
            if output_path.exists():
                fail("replacement path already exists: " + str(output_path))
            replacements.append((output_path, content, skill_id))
            retired_ids = ", ".join(meta["metadata"]["skill_id"] for _, _, meta, _ in sources)
            retired_paths = "\n".join("  - " + path.relative_to(ROOT).as_posix() for _, path, _, _ in sources)
            map_entries.append(
                f"\n\n### {skill_id}\n\n"
                f"- Replacement: {output_path.relative_to(ROOT).as_posix()}\n"
                f"- Workflow: {task_dir}\n"
                f"- Domains merged: {', '.join(domains)}\n"
                f"- Retired IDs: {retired_ids}\n"
                f"- Retired paths:\n{retired_paths}\n"
                "- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.\n"
            )

    if len(source_paths) != EXPECTED_SOURCES or len(replacements) != EXPECTED_OUTPUTS:
        fail(f"unexpected migration size: {len(source_paths)} sources, {len(replacements)} replacements")
    if len(set(source_paths)) != len(source_paths):
        fail("duplicate source path detected")
    if len({skill_id for _, _, skill_id in replacements}) != EXPECTED_OUTPUTS:
        fail("duplicate replacement skill ID detected")

    map_text = MAP_PATH.read_text(encoding="utf-8") + "".join(map_entries)
    audit_text = AUDIT_PATH.read_text(encoding="utf-8") + (
        "\n\n## Windows workflow consolidation completed — 2026-11-20\n\n"
        "The remaining 29 workflows across all 40 Windows domains have been consolidated into "
        "348 profile-based skills across the same 12 domain groups. The 1,160 original standalone "
        "files were replaced by 348 consolidated files; every source body is retained inside its "
        "domain profile, with only duplicate frontmatter replaced by stable consolidated metadata.\n\n"
        "- Previously completed discovery skills: 12\n"
        "- New consolidated workflows: 348\n"
        "- Windows skills after consolidation: 360\n"
        "- Linux skills unchanged: 1,250\n"
        "- Combined Windows + Linux workflows: 1,610\n"
        "- Net reduction from the Windows collection: 812 skill files\n"
        "- Migration map: docs/SKILL_MERGE_MAP.md\n"
    )

    print(f"Validated {len(source_paths)} original skills across {len(GROUPS)} groups.")
    print(f"Prepared {len(replacements)} consolidated skills; net Windows reduction: {len(source_paths) - len(replacements)}.")
    print("Sample replacement:", replacements[0][0].relative_to(ROOT).as_posix())
    print("Sample retired source:", source_paths[0].relative_to(ROOT).as_posix())
    if not args.apply:
        print("DRY RUN ONLY. No files were changed.")
        return

    for output_path, content, _ in replacements:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
    for source_path in source_paths:
        source_path.unlink()
    MAP_PATH.write_text(map_text, encoding="utf-8")
    AUDIT_PATH.write_text(audit_text, encoding="utf-8")
    print("APPLIED: replacements written, retired originals removed, map and audit updated.")


if __name__ == "__main__":
    main()
