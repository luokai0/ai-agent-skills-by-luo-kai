#!/usr/bin/env python3
"""Consolidate Linux distribution workflows while preserving each full profile."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
COLLECTION = ROOT / "ai-agent-skills/24-linux-system-operations (by Luo Kai)"
DEST = COLLECTION / "00-consolidated-linux-operations"
MAP = ROOT / "docs/SKILL_MERGE_MAP.md"
AUDIT = ROOT / "docs/SKILL_CONSOLIDATION_AUDIT.md"
MARKER = "## Agent execution contract — v1.1"
GROUPS = [
    ("debian-family-desktops", "Debian-Family Desktop Systems", ["01-ubuntu","02-debian","03-linux-mint","10-pop-os","15-elementary-os"]),
    ("debian-security-specialists", "Debian Security and Specialist Derivatives", ["06-kali-linux","16-zorin-os","17-parrot-os","21-mx-linux","22-tails"]),
    ("rpm-family", "RPM-Based Enterprise and Community Systems", ["04-fedora","07-red-hat-enterprise-linux","11-rocky-linux","12-almalinux"]),
    ("arch-family", "Arch-Family Rolling Systems", ["05-arch-linux","09-manjaro","25-garuda-linux"]),
    ("independent-source-based", "Independent and Source-Based Systems", ["13-gentoo","14-alpine-linux","19-slackware","20-void-linux"]),
    ("specialized-immutable", "Specialized and Immutable Systems", ["08-opensuse","18-nixos","23-qubes-os","24-steamos"]),
]
NAMES = {
    "01-ubuntu":"Ubuntu","02-debian":"Debian","03-linux-mint":"Linux Mint","04-fedora":"Fedora",
    "05-arch-linux":"Arch Linux","06-kali-linux":"Kali Linux","07-red-hat-enterprise-linux":"Red Hat Enterprise Linux",
    "08-opensuse":"openSUSE","09-manjaro":"Manjaro","10-pop-os":"Pop!_OS","11-rocky-linux":"Rocky Linux",
    "12-almalinux":"AlmaLinux","13-gentoo":"Gentoo","14-alpine-linux":"Alpine Linux","15-elementary-os":"elementary OS",
    "16-zorin-os":"Zorin OS","17-parrot-os":"Parrot OS","18-nixos":"NixOS","19-slackware":"Slackware",
    "20-void-linux":"Void Linux","21-mx-linux":"MX Linux","22-tails":"Tails","23-qubes-os":"Qubes OS",
    "24-steamos":"SteamOS","25-garuda-linux":"Garuda Linux",
}
RISK = [
    r"curl\s+[^|\n]+\|\s*(?:sh|bash)", r"wget\s+[^|\n]+\|\s*(?:sh|bash)",
    r"rm\s+-rf\s+/(?:\s|$)", r"mkfs(?:\.[a-z0-9]+)?\s+/dev/",
    r"dd\s+if=.*of=/dev/", r"chmod\s+-R\s+777", r"iptables\s+-F",
    r"nft\s+flush", r"setenforce\s+0", r"ufw\s+disable",
    r"iptables\s+-P\s+INPUT\s+ACCEPT",
]
REQUIRED = ["Execution environment contract","Task-specific operating procedure","Stop conditions and recovery","Evidence and handoff"]

def fail(message: str) -> None:
    raise SystemExit(message)

def parse(raw: str, path: Path) -> tuple[dict,str]:
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not m:
        fail(f"Invalid frontmatter: {path}")
    meta = yaml.safe_load(m.group(1))
    if not isinstance(meta, dict):
        fail(f"Frontmatter must be a mapping: {path}")
    return meta, raw[m.end():]

def source(path: Path) -> tuple[dict,str,str]:
    meta, body = parse(path.read_text(encoding="utf-8-sig"), path)
    if meta.get("author") != "Luo Kai" or str(meta.get("version")) != "1.1.0":
        fail(f"Unexpected author/version: {path}")
    if meta.get("source") or "license" in meta:
        fail(f"Source-linked or licensed skill is outside this migration: {path}")
    sid = str(meta.get("skill_id",""))
    if not re.fullmatch(r"linux-\d{4}", sid):
        fail(f"Invalid Linux skill ID {sid}: {path}")
    if body.count(MARKER) != 1:
        fail(f"Expected one v1.1 contract: {path}")
    contract = body[body.index(MARKER):]
    for h in REQUIRED:
        if not re.search(rf"(?m)^### {re.escape(h)}\s*$", contract):
            fail(f"Missing contract heading {h}: {path}")
    for pattern in RISK:
        if re.search(pattern, contract, re.I):
            fail(f"Unsafe contract pattern {pattern!r}: {path}")
    return meta, body, sid

def nest(body: str) -> str:
    out, fenced, fence = [], False, None
    for line in body.splitlines():
        s = line.lstrip()
        if s.startswith(chr(96)*3) or s.startswith("~~~"):
            marker = s[:3]
            if not fenced:
                fenced, fence = True, marker
            elif marker == fence:
                fenced, fence = False, None
        if not fenced:
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                line = "#" * min(6, len(m.group(1))+3) + " " + m.group(2)
        out.append(line)
    return "\n".join(out).strip()

def title(slug: str) -> str:
    acronyms = {"dns":"DNS","ssh":"SSH","vpn":"VPN","lvm":"LVM","api":"API","cpu":"CPU","gpu":"GPU","usb":"USB","wifi":"Wi-Fi"}
    return " ".join(acronyms.get(w,w.capitalize()) for w in slug.split("-"))

def tick(text: str) -> str:
    t = chr(96)
    return t + text + t

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if DEST.exists():
        fail(f"Destination already exists: {DEST}")
    distros = [d for _,_,group in GROUPS for d in group]
    if len(distros) != 25 or len(set(distros)) != 25:
        fail("Distribution groups must contain 25 unique distributions")

    task_sets, src, ids = {}, {}, set()
    for distro in distros:
        root = COLLECTION / distro
        tasks = sorted(p for p in root.iterdir() if p.is_dir())
        if len(tasks) != 50:
            fail(f"{distro}: expected 50 task folders, found {len(tasks)}")
        task_sets[distro] = {p.name for p in tasks}
        for task in tasks:
            path = task / "SKILL.md"
            if not path.is_file():
                fail(f"Missing source skill: {path}")
            meta, body, sid = source(path)
            if sid in ids:
                fail(f"Duplicate source ID: {sid}")
            ids.add(sid)
            src[(distro,task.name)] = (path,meta,body,sid)
    baseline = next(iter(task_sets.values()))
    for distro, names in task_sets.items():
        if names != baseline:
            fail(f"Task set mismatch in {distro}")

    outputs, map_rows, source_paths = [], [], []
    for gi,(group_slug,group_label,group_distros) in enumerate(GROUPS,1):
        for task_slug in sorted(baseline):
            action = title(task_slug)
            sid = f"linux-consolidated-g{gi:02d}-{task_slug}"
            name = f"Linux {action} across {group_label}"
            desc = f"One entry point for {action.lower()} across {len(group_distros)} Linux distributions. Each profile preserves exact commands, safeguards, verification, and recovery."
            profiles = []
            for pi,distro in enumerate(group_distros,1):
                path,meta,body,source_id = src[(distro,task_slug)]
                distro_name = str(meta.get("platform") or NAMES[distro])
                profiles.append(
                    f"### Profile {pi}: {distro_name}\n\n"
                    f"- Distribution profile: {tick(distro_name)}\n"
                    f"- Preserved skill ID: {tick(source_id)}\n"
                    f"- Workflow: {tick(task_slug)}\n\n{nest(body)}"
                )
                source_paths.append(path)
                rel_source = path.relative_to(COLLECTION).as_posix()
                rel_target = f"00-consolidated-linux-operations/{gi:02d}-{group_slug}/{task_slug}/SKILL.md"
                map_rows.append(f"| {tick(source_id)} | {tick(rel_source)} | {tick(rel_target)} |")

            body = f"""# {name}

## Objective

Provide one reliable entry point for {action.lower()} across the {group_label.lower()} family without flattening distribution-specific behavior.

## When to use

Use when the user needs this workflow on a distribution in this family. Confirm the exact distribution and release, then follow only its matching profile.

## Required operating discipline

- Detect the actual distribution, release, architecture, kernel, PID 1, package manager, filesystem model, and execution context.
- Select the exact matching profile. Never transfer commands or recovery assumptions from another distribution.
- Start with read-only inspection and least privilege.
- Obtain explicit approval for consequential changes, preview impact, and establish recovery first.
- Verify the resulting state independently and protect credentials, remote access, encryption, backups, and user data.

## Distribution profiles

{chr(10).join(profiles)}

## Unified workflow

1. Identify the target distribution and release using local evidence.
2. Select exactly one matching profile. Stop if the target is unsupported or ambiguous.
3. Follow that profile's complete execution contract, native commands, approval gates, and stop conditions.
4. Perform read-only checks before proposing changes.
5. Obtain approval for consequential actions and execute only the approved scope.
6. Verify independently and report evidence, uncertainty, and recovery status.

## Stop conditions and recovery

Stop if the distribution or release cannot be confirmed, the selected profile does not match, required approval is absent, remote access or data integrity is at risk, or a security control would need to be weakened. Do not improvise cross-distribution substitutes.

## Privacy-safe evidence and handoff

Collect only necessary evidence. Redact secrets, tokens, private keys, password hashes, recovery material, unnecessary usernames, hostnames, IP addresses, serial numbers, and internal domains. Report the detected target, profile used, approved actions, verification, uncertainty, and recovery state.

## Completion checklist

- Exact distribution and release confirmed.
- Matching profile and original execution contract followed.
- Read-only baseline captured.
- Approval obtained for consequential actions.
- Native commands and safeguards respected.
- Final state independently verified.
- Sensitive evidence minimized and redacted.
- Remaining risks and recovery state reported.

Copyright (c) 2026 Luo Kai. All rights reserved for original material in this consolidated skill. See COPYRIGHT.md.
"""
            metadata = {
                "name": name,
                "description": desc,
                "metadata": {
                    "author":"Luo Kai",
                    "platform":"Linux distributions",
                    "category":"Linux System Operations",
                    "skill_id":sid,
                    "version":"1.2.0",
                },
            }
            front = yaml.safe_dump(metadata,sort_keys=False,allow_unicode=True).strip()
            target = DEST / f"{gi:02d}-{group_slug}" / task_slug / "SKILL.md"
            outputs.append((target,f"---\n{front}\n---\n\n{body}\n"))

    if len(outputs) != 300 or len(source_paths) != 1250 or len(ids) != 1250:
        fail("Expected exactly 1,250 unique sources and 300 outputs")
    current_map = MAP.read_text(encoding="utf-8")
    current_audit = AUDIT.read_text(encoding="utf-8")
    heading = "## Linux distribution consolidation — 2026-11-20"
    if heading in current_map or heading in current_audit:
        fail("Linux consolidation map/audit section already exists")
    map_section = (
        "\n\n" + heading + "\n\n"
        "The 1,250 distribution-specific workflows are consolidated into 300 skills across six families. "
        "Every profile retains its complete original body, execution contract, commands, safeguards, verification, and recovery guidance.\n\n"
        "| Preserved profile ID | Original profile path | Consolidated skill path |\n|---|---|---|\n"
        + "\n".join(map_rows) + "\n"
    )
    audit_section = (
        "\n\n" + heading + "\n\n"
        "- Verified 25 distribution folders, each containing the same 50 task workflows.\n"
        "- Validated 1,250 unique original skill IDs and v1.1 execution contracts.\n"
        "- Consolidated into 300 skills across six groups with 5, 5, 4, 3, 4, and 4 distribution profiles per task.\n"
        "- Preserved every original profile body, command, decision point, safety boundary, verification step, and recovery instruction.\n"
        "- Retained the 25 distribution README files as supporting documentation and removed only standalone SKILL.md files after mapping.\n"
        "- Third-party and per-skill rights-status records remain outside the Luo Kai original-work copyright scope.\n"
    )
    print("Validated 25 distributions and 50 identical task folders per distribution.")
    print("Mapped 1,250 unique original skills into 300 consolidated profile-based skills.")
    print("Group profile sizes:", [len(g[2]) for g in GROUPS])
    print("DRY RUN ONLY." if not args.apply else "APPLYING migration.")
    if not args.apply:
        return

    for path,content in outputs:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding="utf-8")
    for path in source_paths:
        path.unlink()
    MAP.write_text(current_map+map_section,encoding="utf-8")
    AUDIT.write_text(current_audit+audit_section,encoding="utf-8")
    print("APPLIED: created 300 Linux skills and removed 1,250 standalone files after mapping.")

if __name__ == "__main__":
    main()
