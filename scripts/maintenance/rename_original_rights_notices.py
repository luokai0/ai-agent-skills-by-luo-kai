#!/usr/bin/env python3
"""Replace collection-level proprietary LICENSE notices with copyright notices.

Only direct collection roots explicitly labelled '(by Luo Kai)' are touched.
Nested third-party LICENSE files are preserved.
"""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "ai-agent-skills"

TEMPLATE = """<!-- Copyright (c) 2026 Luo Kai. All rights reserved. -->
# Copyright notice — {collection}

Copyright (c) 2026 Luo Kai. All rights reserved for original material authored by Luo Kai and clearly identified as original work in this collection.

Scope: This notice applies only to original skills whose author metadata identifies Luo Kai and that have no recorded source metadata.

This notice does not apply to any skill with a per-skill LICENSE_STATUS.md, recorded source metadata, independent attribution or rights notice, or third-party material. Those materials retain their own authorship, license terms, and attribution.

No license is granted for original material in this collection. Access to the repository does not grant permission to reproduce, modify, redistribute, publish, or commercially exploit that original material without prior written permission, except where applicable law permits.

This notice does not claim ownership of third-party software, documentation, trademarks, imported material, or independently owned works.
"""

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    args = parser.parse_args()
    roots = sorted(p for p in SKILLS_ROOT.iterdir() if p.is_dir() and "(by Luo Kai)" in p.name)
    if len(roots) != 22:
        raise SystemExit(f"Expected 22 Luo Kai collection roots, found {len(roots)}")

    renames = []
    updates = []
    creates = []
    for collection in roots:
        title = collection.name.replace(" (by Luo Kai)", "")
        old_license = collection / "LICENSE"
        old_scope = collection / "LICENSE_SCOPE.md"
        copyright = collection / "COPYRIGHT.md"

        if not copyright.exists():
            creates.append((copyright, TEMPLATE.format(collection=title)))
        else:
            current = copyright.read_text(encoding="utf-8-sig")
            exclusion = "per-skill LICENSE_STATUS.md"
            if exclusion not in current:
                current = current.rstrip() + "\n\nThis notice excludes any skill with a per-skill LICENSE_STATUS.md, recorded source metadata, or an independent rights notice.\n"
                updates.append((copyright, current))

        for old in (old_license, old_scope):
            if old.is_file():
                renames.append(old)

        for doc in collection.rglob("*.md"):
            if doc in {old_license, old_scope, copyright}:
                continue
            current = doc.read_text(encoding="utf-8-sig")
            updated = current.replace("LICENSE_SCOPE.md", "COPYRIGHT.md")
            updated = updated.replace("repository-level LICENSE", "repository-level COPYRIGHT.md notice")
            updated = updated.replace("repository LICENSE", "repository COPYRIGHT.md notice")
            updated = updated.replace("License: Proprietary. See repository COPYRIGHT.md notice", "Copyright (c) 2026 Luo Kai. All rights reserved.")
            updated = updated.replace("original-work license scope", "original-work copyright notice")
            if updated != current:
                updates.append((doc, updated))

    print(f"Luo Kai collection roots inspected: {len(roots)}")
    print(f"Collection-level LICENSE files to remove: {sum(1 for p in renames if p.name == 'LICENSE')}")
    print(f"LICENSE_SCOPE.md files to remove: {sum(1 for p in renames if p.name == 'LICENSE_SCOPE.md')}")
    print(f"COPYRIGHT.md files to create: {len(creates)}")
    print(f"Existing copyright/doc files to update: {len(updates)}")
    if not args.apply:
        print("DRY RUN ONLY. Nested third-party LICENSE files are never changed.")
        return

    for path, content in creates + updates:
        path.write_text(content, encoding="utf-8")
    for path in renames:
        path.unlink()
    print("APPLIED: collection-level proprietary notices replaced with COPYRIGHT.md notices.")

if __name__ == "__main__":
    main()
