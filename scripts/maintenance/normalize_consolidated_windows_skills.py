#!/usr/bin/env python3
"""Normalize generated Windows profile labels and repair repeated template artifacts."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations"
EXPECTED_GENERATED = 348
GROUP_LABELS = {
    "Desktop and window management": "Desktop and Window Management",
    "Workspace and file operations": "Workspace and File Operations",
    "Search, archives, and storage": "Search, Archives, and Storage",
    "Shells, processes, and startup": "Shells, Processes, and Startup",
    "Configuration, software, and devices": "Configuration, Software, and Devices",
    "Input, output, and peripherals": "Input, Output, and Peripherals",
    "Network and secure connectivity": "Network and Secure Connectivity",
    "Browser and productivity applications": "Browser and Productivity Applications",
    "Development and virtualization": "Development and Virtualization",
    "Health, security, and privacy": "Health, Security, and Privacy",
    "Accessibility, remote support, and visual automation": "Accessibility, Remote Support, and Visual Automation",
    "Backup, recovery, and provisioning": "Backup, Recovery, and Provisioning",
}

def parse_frontmatter(raw: str, path: Path) -> dict:
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if not match:
        raise SystemExit(f"Invalid frontmatter: {path}")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise SystemExit(f"Frontmatter must be a mapping: {path}")
    return metadata

def normalize(raw: str, metadata: dict) -> str:
    details = metadata.get("metadata") or {}
    skill_id = str(details.get("skill_id", "")) if isinstance(details, dict) else ""
    if not re.fullmatch(r"windows-consolidated-g\d{2}-w\d{2}", skill_id):
        return raw
    name = str(metadata.get("name", ""))
    action_match = re.match(r"Windows (.+?) across ", name)
    action = action_match.group(1) if action_match else ""
    updated = raw.replace("Windows Windows ", "Windows ")
    updated = re.sub(r"(?<!\.)\.\.(?=\s)", ".", updated)
    for old, new in GROUP_LABELS.items():
        updated = updated.replace(old, new)
    if action:
        updated = updated.replace(
            f"Use when the user requests {action.lower()} in any of these domains:",
            f"Use when the user needs the {action.lower()} workflow in any of these domains:",
        )
    if skill_id.endswith("-w02"):
        updated = updated.replace(
            "For this request, inspect configuration means changing or inspecting only",
            "For this request, inspect configuration means inspecting only",
        )
    return updated

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write normalized files; default is dry-run")
    args = parser.parse_args()
    if not SKILLS_ROOT.is_dir():
        raise SystemExit(f"Missing consolidated Windows directory: {SKILLS_ROOT}")
    files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    generated = []
    for path in files:
        raw = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(raw, path)
        details = metadata.get("metadata") or {}
        skill_id = str(details.get("skill_id", "")) if isinstance(details, dict) else ""
        if skill_id.startswith("windows-consolidated-g"):
            generated.append((path, raw, normalize(raw, metadata)))
    if len(generated) != EXPECTED_GENERATED:
        raise SystemExit(f"Expected {EXPECTED_GENERATED} generated skills, found {len(generated)}")
    changed = [(path, old, new) for path, old, new in generated if old != new]
    if sum(new.count("Windows Windows ") for _, _, new in generated):
        raise SystemExit("Normalization left duplicate Windows labels")
    print(f"Scanned {len(files)} consolidated Windows skills; generated profiles: {len(generated)}.")
    print(f"Files requiring normalization: {len(changed)}.")
    if not args.apply:
        print("DRY RUN ONLY. No files were changed.")
        return
    for path, _, new in changed:
        path.write_text(new, encoding="utf-8")
    print(f"APPLIED: normalized {len(changed)} generated Windows skills.")

if __name__ == "__main__":
    main()
