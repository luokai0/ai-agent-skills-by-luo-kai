#!/usr/bin/env python3
"""Build the public skill index and ZIP bundle from the repository tree."""
from __future__ import annotations

import json
import os
import re
import zipfile
from collections import Counter

import yaml
from pathlib import Path
from urllib.parse import quote

BASE = Path("ai-agent-skills")
ICONS = {
    "01": "⌨️", "02": "🎨", "03": "🧩", "04": "🗄️", "05": "☁️",
    "06": "🔐", "07": "🧪", "08": "🏛️", "09": "🧠", "10": "📱",
    "11": "🛠️", "12": "📈", "13": "⚛️", "14": "🧬", "15": "🌍",
    "16": "⚙️", "17": "🚀", "18": "🤖", "19": "💼", "20": "🌿",
    "21": "🔗", "22": "🦀",
}
CATEGORIES = {
    "01": "Programming Languages", "02": "Frontend Development",
    "03": "Backend Development", "04": "Databases and Storage",
    "05": "DevOps and Cloud", "06": "Security and Authentication",
    "07": "Testing and Quality", "08": "Architecture and Patterns",
    "09": "Data and AI", "10": "Mobile Development",
    "11": "Specialized Coding", "12": "Finance and Trading",
    "13": "Physics and Mathematics", "14": "Chemistry and Biology",
    "15": "Earth and Space Sciences", "16": "Engineering",
    "17": "Emerging Technology", "18": "AI Agents and Automation",
    "19": "Business and Entrepreneurship", "20": "Health and Wellness",
    "21": "External Registries", "22": "ClawHub Skills",
}

def read_frontmatter(text: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}
    try:
        data = yaml.safe_load(chr(10).join(lines[1:end]))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}

def normalize_license(value: str) -> str:
    label = str(value).strip()
    low = label.lower()
    if "apache" in low and "2.0" in low:
        return "Apache-2.0"
    if "cc by-nc-nd" in low or "attribution-noncommercial-noderivatives" in low:
        return "CC BY-NC-ND 4.0"
    if "cc by 4.0" in low or "attribution 4.0 international" in low:
        return "CC BY 4.0"
    if "cc0" in low or "publicdomain/zero/1.0" in low:
        return "CC0 1.0"
    if low == "mit" or "mit license" in low:
        return "MIT"
    return label[:80]

def infer_license_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="replace")[:30000].lower()
    if "apache license" in text and "version 2.0" in text:
        return "Apache-2.0"
    if "attribution-noncommercial-noderivatives 4.0" in text or "cc by-nc-nd 4.0" in text:
        return "CC BY-NC-ND 4.0"
    if "attribution 4.0 international" in text or "creativecommons.org/licenses/by/4.0" in text:
        return "CC BY 4.0"
    if "cc0 1.0" in text or "creativecommons.org/publicdomain/zero/1.0" in text:
        return "CC0 1.0"
    if "mit license" in text or "permission is hereby granted, free of charge" in text:
        return "MIT"
    return "License file (unclassified)"

def resolve_license(skill_file: Path, metadata: dict) -> str:
    meta = metadata.get("metadata") or {}
    if not isinstance(meta, dict):
        meta = {}
    explicit = metadata.get("license") or meta.get("license")
    if explicit:
        return normalize_license(explicit)

    current = skill_file.parent
    while current != BASE:
        for notice_name in ("UPSTREAM_LICENSE_NOTICE.md", "NOTICE.md", "LICENSE_SCOPE.md"):
            notice = current / notice_name
            if notice.is_file():
                notice_text = notice.read_text(encoding="utf-8-sig", errors="replace")
                match = re.search(r"(?im)^(?:upstream\s+)?license:\s*(.+)$", notice_text)
                if match:
                    return normalize_license(match.group(1))
        for license_name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
            license_file = current / license_name
            if license_file.is_file():
                return infer_license_file(license_file)
        if (current / "LICENSE_STATUS.md").is_file():
            return "Unverified"
        current = current.parent
    return "Unverified"

def main() -> None:
    if not BASE.is_dir():
        raise SystemExit(f"Missing collection directory: {BASE}")

    skills = []
    for root, dirs, names in os.walk(BASE):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "__pycache__", "node_modules"})
        skill_file = next((n for n in names if n.lower() == "skill.md"), None)
        if not skill_file:
            continue
        path = Path(root) / skill_file
        relative = path.as_posix()
        parts = Path(relative).parts
        category = parts[1].split("-", 1)[0] if len(parts) > 1 else "00"
        skill_name = Path(root).name
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            content = ""
        metadata = read_frontmatter(content)
        description = metadata.get("description", "")
        if not isinstance(description, str):
            description = str(description)
        license_label = resolve_license(path, metadata)
        encoded_path = "/".join(quote(segment, safe="") for segment in Path(relative).parts)
        skills.append({"n": metadata.get("name") or skill_name, "p": encoded_path, "c": category, "d": description[:1024], "l": license_label})

    skills.sort(key=lambda item: (item["c"], item["n"].casefold(), item["p"]))
    license_counts = Counter(item["l"] for item in skills)
    output = {"total": len(skills), "cats": CATEGORIES, "icons": ICONS, "license_counts": dict(license_counts), "skills": skills}
    Path("skills-index.json").write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Generated skills-index.json: {len(skills)} skills")
    print(f"License status counts: {dict(license_counts)}")

    bundle_path = Path("skills-bundle.zip")
    excluded_dirs = {".git", "__pycache__", "node_modules"}
    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for root, dirs, names in os.walk(BASE):
            dirs[:] = sorted(d for d in dirs if d not in excluded_dirs)
            for name in sorted(names):
                file_path = Path(root) / name
                if file_path.is_symlink() or not file_path.is_file() or file_path.suffix in {".pyc", ".pyo"}:
                    continue
                archive.write(file_path, file_path.as_posix())
    print(f"Bundled {len(skills)} skills into {bundle_path} ({bundle_path.stat().st_size / 1024 / 1024:.1f} MiB)")

if __name__ == "__main__":
    main()
