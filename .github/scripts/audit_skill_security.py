#!/usr/bin/env python3
"""Static screening and provenance inventory for skills; never executes skill code."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Install it with: python -m pip install PyYAML", file=sys.stderr)
    raise SystemExit(2)

TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".py", ".sh", ".bash", ".zsh", ".ps1",
    ".bat", ".cmd", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".rb", ".pl", ".php", ".go", ".rs", ".java", ".kt", ".swift",
    ".c", ".h", ".cpp", ".hpp", ".cs", ".yaml", ".yml", ".json",
    ".toml", ".ini", ".cfg", ".conf", ".xml", ".html", ".htm",
    ".sql", ".tf", ".dockerfile", ".properties",
}
SCRIPT_SUFFIXES = {
    ".py", ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".js",
    ".mjs", ".cjs", ".rb", ".pl", ".php", ".go", ".rs", ".java",
    ".kt", ".swift", ".c", ".cpp", ".cs",
}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".tox"}

CRITICAL_PATTERNS = [
    ("encoded-powershell-execution", re.compile(
        r"(?:subprocess\.(?:run|Popen|call)|os\.system|child_process\.exec)\s*\([^)]{0,1200}"
        r"(?:powershell(?:\.exe)?)[^)]{0,400}(?:-enc(?:odedcommand)?|frombase64string)[^)]{0,400}"
        r"(?:iex|invoke-expression)", re.I | re.S)),
    ("base64-dynamic-execution", re.compile(r"\b(?:eval|exec)\s*\(\s*(?:base64\.(?:b64decode|urlsafe_b64decode)|atob)\s*\(", re.I)),
    ("root-filesystem-wipe", re.compile(r"\brm\s+-[a-z]*r[a-z]*f[a-z]*\s+/(?:\s|$)", re.I)),
    ("raw-disk-overwrite", re.compile(r"\bdd\b[^\n]{0,200}\bof=/dev/(?:sd[a-z]|nvme\d)", re.I)),
]
REVIEW_PATTERNS = [
    ("remote-pipe-to-shell", re.compile(r"\b(?:curl|wget)\b[^\n|]{0,500}\|\s*(?:sudo\s+)?(?:ba)?sh\b", re.I)),
    ("encoded-powershell-indicator", re.compile(r"powershell.{0,100}(?:-enc(?:odedcommand)?|frombase64string)", re.I)),
    ("dynamic-execution", re.compile(r"\b(?:eval|exec)\s*\(", re.I)),
    ("shell-or-subprocess", re.compile(r"\b(?:subprocess\.(?:run|Popen|call)|os\.system|child_process\.exec|shell=True)\b", re.I)),
    ("network-client", re.compile(r"\b(?:requests\.(?:get|post|put|delete)|urllib\.request|fetch\s*\(|axios\.|http\.request|curl\s|wget\s)", re.I)),
    ("environment-or-secret-access", re.compile(r"(?:os\.environ|process\.env|\.env\b|id_rsa|credentials\.json|api[_-]?key|access[_-]?token)", re.I)),
    ("prompt-override-language", re.compile(r"(?:ignore|disregard|override)\s+(?:all\s+)?(?:previous|prior|above)\s+instructions", re.I)),
    ("obfuscation-or-decoding", re.compile(r"(?:base64\.(?:b64decode|decodebytes)|frombase64string|atob\s*\()", re.I)),
    ("privileged-or-destructive-command", re.compile(r"\b(?:sudo\s|chmod\s+777|chown\s+-R|mkfs\.|diskpart\b|format\s+[a-z]:)", re.I)),
]

def read_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing opening frontmatter delimiter"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, "missing closing frontmatter delimiter"
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except Exception as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter is not a YAML mapping"
    return data, None

def inherited_license(skill_dir: Path, skills_root: Path):
    """Find the nearest license inside the collection; a local LICENSE_STATUS.md blocks inheritance."""
    for parent in (skill_dir, *skill_dir.parents):
        if parent == skills_root or skills_root not in parent.parents:
            break
        matches = [
            name for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "NOTICE", "NOTICE.md")
            if (parent / name).is_file()
        ]
        if matches:
            return [
                (parent / name).relative_to(skills_root.parent).as_posix()
                for name in matches
            ]
        if (parent / "LICENSE_STATUS.md").is_file():
            return []
    return []

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--report", default="audit-report.json")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    skills_root = repo_root / "ai-agent-skills"
    if not skills_root.is_dir():
        print(f"Skill root not found: {skills_root}", file=sys.stderr)
        return 2

    findings = []
    inventory = []
    scanned_files = 0
    skill_files = sorted(p for p in skills_root.rglob("*") if p.is_file() and p.name.lower() == "skill.md")
    skill_dirs = {p.parent for p in skill_files}

    for skill_file in skill_files:
        rel_skill = skill_file.relative_to(repo_root).as_posix()
        metadata, parse_error = read_frontmatter(skill_file)
        skill_dir = skill_file.parent
        meta = (metadata or {}).get("metadata") or {}
        if not isinstance(meta, dict):
            meta = {}
        license_value = (metadata or {}).get("license") or meta.get("license")
        license_files = inherited_license(skill_dir, skills_root)
        author = (metadata or {}).get("author") or meta.get("author")
        provenance = meta.get("provenance") or (metadata or {}).get("provenance")
        source = meta.get("source") or meta.get("repository") or (metadata or {}).get("source")
        if license_value:
            license_status = str(license_value)
        elif license_files:
            license_status = "LICENSE-FILE:" + ",".join(license_files)
        else:
            license_status = "UNKNOWN"

        inventory.append({
            "skill_path": rel_skill,
            "name": (metadata or {}).get("name") or skill_dir.name,
            "author": author,
            "provenance": provenance or "unrecorded",
            "source": source,
            "license": license_status,
        })
        if parse_error:
            findings.append({"severity": "review", "type": "frontmatter", "path": rel_skill, "line": 1, "detail": parse_error})

    for file_path in sorted(p for p in skills_root.rglob("*") if p.is_file()):
        if file_path.is_symlink() or any(part in SKIP_DIRS for part in file_path.parts):
            continue
        if not any(parent in skill_dirs for parent in file_path.parents):
            continue
        try:
            if file_path.stat().st_size > 2_000_000:
                findings.append({"severity": "review", "type": "oversized-file-not-inspected", "path": file_path.relative_to(repo_root).as_posix(), "line": 0, "detail": "File exceeds 2 MB static text scan limit"})
                continue
            if file_path.suffix.lower() not in TEXT_SUFFIXES and file_path.name.lower() not in {"dockerfile", "makefile"}:
                continue
            content = file_path.read_text(encoding="utf-8-sig", errors="replace")
        except (OSError, UnicodeError) as exc:
            findings.append({"severity": "review", "type": "file-read-error", "path": file_path.relative_to(repo_root).as_posix(), "line": 0, "detail": str(exc)})
            continue

        scanned_files += 1
        relative = file_path.relative_to(repo_root).as_posix()
        executable = file_path.suffix.lower() in SCRIPT_SUFFIXES or file_path.name.lower() in {"dockerfile", "makefile"}
        if executable:
            for kind, pattern in CRITICAL_PATTERNS:
                for match in pattern.finditer(content):
                    line_no = content.count("\n", 0, match.start()) + 1
                    findings.append({"severity": "critical", "type": kind, "path": relative, "line": line_no, "detail": "High-confidence dangerous execution pattern; inspect in context before use."})

        for kind, pattern in REVIEW_PATTERNS:
            match = pattern.search(content)
            if match:
                line_no = content.count("\n", 0, match.start()) + 1
                findings.append({"severity": "review", "type": kind, "path": relative, "line": line_no, "detail": "Sensitive capability or instruction pattern requires human review in context."})

    counts = Counter(item["severity"] for item in findings)
    license_counts = Counter(item["license"] for item in inventory)
    report = {
        "scope": "Static screening only; not a malware-free guarantee.",
        "skills_discovered": len(skill_files),
        "text_files_scanned": scanned_files,
        "findings_by_severity": dict(counts),
        "license_status_counts": dict(license_counts),
        "skills": inventory,
        "findings": findings,
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Skills discovered: {len(skill_files)}")
    print(f"Text files scanned: {scanned_files}")
    print(f"License status groups: {dict(license_counts)}")
    print(f"Findings: {dict(counts)}")
    critical = [item for item in findings if item["severity"] == "critical"]
    for item in critical:
        print(f"[CRITICAL] {item['path']}:{item['line']} {item['type']} - {item['detail']}")
    review = [item for item in findings if item["severity"] == "review"]
    for item in review[:40]:
        print(f"[REVIEW] {item['path']}:{item['line']} {item['type']} - {item['detail']}")
    if len(review) > 40:
        print(f"... {len(review) - 40} additional review findings are in {report_path}")
    print(f"Full report: {report_path}")
    return 1 if critical else 0

if __name__ == "__main__":
    raise SystemExit(main())
