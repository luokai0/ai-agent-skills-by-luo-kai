#!/usr/bin/env python3
"""Validate every skill frontmatter block before packaging or installation."""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "ai-agent-skills"

class UniqueKeyLoader(yaml.SafeLoader):
    pass

def construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                "found an unhashable key", key_node.start_mark
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"found duplicate key {key!r}", key_node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping

UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_unique_mapping
)


def has_status_override(path: Path) -> bool:
    current = path.parent
    while current != SKILLS_ROOT:
        if (current / "LICENSE_STATUS.md").is_file():
            return True
        current = current.parent
    return False


def is_original_collection_path(path: Path) -> bool:
    try:
        first = path.relative_to(SKILLS_ROOT).parts[0]
    except (ValueError, IndexError):
        return False
    return "(by Luo Kai)" in first

def main() -> int:
    files = sorted(p for p in SKILLS_ROOT.rglob("*") if p.is_file() and p.name.casefold() == "skill.md")
    failures = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        try:
            if path.name != "SKILL.md":
                raise ValueError("filename must be exactly SKILL.md (case-sensitive)")
            text = path.read_text(encoding="utf-8-sig")
            lines = text.splitlines()
            if not lines or lines[0].strip() != "---":
                raise ValueError("frontmatter must start on the first line with ---")
            try:
                end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
            except StopIteration:
                raise ValueError("frontmatter closing --- not found")
            data = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeyLoader)
            if not isinstance(data, dict):
                raise ValueError("frontmatter must be a YAML mapping")
            for field in ("name", "description"):
                value = data.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"missing or empty required field: {field}")
            details = data.get("metadata") or {}
            if not isinstance(details, dict):
                details = {}
            author = str(details.get("author") or data.get("author") or "").casefold().replace("-", " ").strip()
            source = data.get("source") or details.get("source")
            provenance = str(details.get("provenance") or data.get("provenance") or "").casefold().strip()
            if author == "luo kai" and not source and provenance in {"", "original"} and not has_status_override(path):
                if "license" in data or "license" in details:
                    raise ValueError("original Luo Kai skills must not include a license field")
            if is_original_collection_path(path):
                values = [str(v).casefold().strip() for v in (data.get("license"), details.get("license")) if v is not None]
                if any(v in {"proprietary. see repository license", "proprietary. see license_scope.md", "proprietary. see license scope"} for v in values):
                    raise ValueError("obsolete repository-license placeholder must be removed")
        except Exception as exc:
            failures.append((relative, str(exc)))
    if failures:
        print(f"FAILED: {len(failures)} of {len(files)} skill files have invalid frontmatter")
        for path, error in failures:
            print(f" - {path}: {error}")
        return 1
    print(f"PASS: validated YAML frontmatter, unique keys, and required name/description fields in all {len(files)} skill files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
