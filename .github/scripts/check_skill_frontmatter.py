#!/usr/bin/env python3
"""Validate every skill frontmatter block before packaging or installation."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "ai-agent-skills"

def main() -> int:
    files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    failures = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8-sig")
            lines = text.splitlines()
            if not lines or lines[0].strip() != "---":
                raise ValueError("frontmatter must start on the first line with ---")
            try:
                end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
            except StopIteration:
                raise ValueError("frontmatter closing --- not found")
            data = yaml.safe_load("\n".join(lines[1:end]))
            if not isinstance(data, dict):
                raise ValueError("frontmatter must be a YAML mapping")
            for field in ("name", "description"):
                value = data.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"missing or empty required field: {field}")
        except Exception as exc:
            failures.append((relative, str(exc)))
    if failures:
        print(f"FAILED: {len(failures)} of {len(files)} skill files have invalid frontmatter")
        for path, error in failures:
            print(f" - {path}: {error}")
        return 1
    print(f"PASS: validated YAML frontmatter and required name/description fields in all {len(files)} skill files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
