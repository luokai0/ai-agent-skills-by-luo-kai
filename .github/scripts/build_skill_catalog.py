#!/usr/bin/env python3
"""Build the public skill index and ZIP bundle from the repository tree."""
from __future__ import annotations

import json
import os
import zipfile
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
        description = ""
        try:
            content = path.read_text(encoding="utf-8-sig", errors="replace")
            in_frontmatter = False
            for line in content.splitlines():
                if line.strip() == "---":
                    if in_frontmatter:
                        break
                    in_frontmatter = True
                    continue
                if in_frontmatter and line.startswith("description:"):
                    description = line.split(":", 1)[1].strip().strip('"').strip("'")
                    break
        except OSError:
            pass
        encoded_path = "/".join(quote(segment, safe="") for segment in Path(relative).parts)
        skills.append({"n": skill_name, "p": encoded_path, "c": category, "d": description[:1024]})

    skills.sort(key=lambda item: (item["c"], item["n"].casefold(), item["p"]))
    output = {"total": len(skills), "cats": CATEGORIES, "icons": ICONS, "skills": skills}
    Path("skills-index.json").write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Generated skills-index.json: {len(skills)} skills")

    bundle_path = Path("skills-bundle.zip")
    excluded_dirs = {".git", "__pycache__", "node_modules"}
    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for root, dirs, names in os.walk(BASE):
            dirs[:] = sorted(d for d in dirs if d not in excluded_dirs)
            for name in sorted(names):
                file_path = Path(root) / name
                if file_path.is_symlink() or file_path.suffix in {".pyc", ".pyo"}:
                    continue
                archive.write(file_path, file_path.as_posix())
    print(f"Bundled {len(skills)} skills into {bundle_path} ({bundle_path.stat().st_size / 1024 / 1024:.1f} MiB)")

if __name__ == "__main__":
    main()
