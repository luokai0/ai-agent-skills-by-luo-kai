#!/usr/bin/env python3
"""Validate the six skills with explicitly verified Luo Kai original provenance."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "agent-evaluation-design": {
        "path": "ai-agent-skills/18-ai-agents-and-automation (by Luo Kai)/16-other-agents/agent-evaluation-design/SKILL.md",
        "sections": (
            "Protect evaluation data and prevent leakage",
            "Plan runs and interpret uncertainty",
            "Validate evaluators and model-based judges",
            "Add production feedback without corrupting the benchmark",
        ),
        "minimum_chars": 8000,
    },
    "skill-supply-chain-audit": {
        "path": "ai-agent-skills/06-security-and-auth (by Luo Kai)/05-devsecops/skill-supply-chain-audit/SKILL.md",
        "sections": (
            "Verify artifact integrity and build provenance",
            "Build a dependency inventory",
            "Review the installation and update path",
            "Apply risk-based review depth",
        ),
        "minimum_chars": 10000,
    },
    "mcp-server-hardening": {
        "path": "ai-agent-skills/18-ai-agents-and-automation (by Luo Kai)/02-mcp-tools/mcp-server-hardening/SKILL.md",
        "sections": (
            "Secure protocol lifecycle and session state",
            "Review every exposed MCP capability",
            "Harden downstream integrations and side effects",
            "MCP Authorization",
        ),
        "minimum_chars": 11000,
    },
    "agent-observability": {
        "path": "ai-agent-skills/18-ai-agents-and-automation (by Luo Kai)/16-other-agents/agent-observability/SKILL.md",
        "sections": (
            "Define reliable service-level indicators",
            "Control telemetry volume and metric cardinality",
            "Make telemetry failure safe",
            "Maintain dashboards and incident runbooks",
        ),
        "minimum_chars": 9000,
    },
    "prompt-injection-defense": {
        "path": "ai-agent-skills/18-ai-agents-and-automation (by Luo Kai)/03-context-engineering/prompt-injection-defense/SKILL.md",
        "sections": (
            "Enforce trust boundaries outside the model",
            "Preserve trust labels through transformations",
            "Defend multimodal and structured inputs",
            "Protect retrieval, ranking, and context assembly",
        ),
        "minimum_chars": 9500,
    },
    "ai-generated-change-verification": {
        "path": "ai-agent-skills/07-testing-and-quality (by Luo Kai)/10-ai-assisted-quality/ai-generated-change-verification/SKILL.md",
        "sections": (
            "Verify generated and non-text artifacts",
            "Review data, schema, and migration changes",
            "Establish an evidence hierarchy",
            "Verify CI and release gates",
        ),
        "minimum_chars": 9000,
    },
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    failures: list[str] = []
    for expected_name, spec in EXPECTED.items():
        path = ROOT / spec["path"]
        if not path.is_file():
            failures.append(f"{expected_name}: missing file: {spec['path']}")
            continue

        content = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            failures.append(f"{expected_name}: missing or malformed YAML frontmatter")
            continue

        try:
            frontmatter = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            failures.append(f"{expected_name}: invalid YAML frontmatter: {exc}")
            continue

        if not isinstance(frontmatter, dict):
            failures.append(f"{expected_name}: frontmatter must be a YAML mapping")
            continue

        metadata = frontmatter.get("metadata")
        if not isinstance(metadata, dict):
            failures.append(f"{expected_name}: metadata mapping is missing")
            continue

        checks = {
            "name": frontmatter.get("name") == expected_name,
            "description": isinstance(frontmatter.get("description"), str)
            and bool(frontmatter["description"].strip()),
            "author": metadata.get("author") == "Luo Kai",
            "provenance": metadata.get("provenance") == "original",
            "version": metadata.get("version") == "1.1.0",
            "no license field": "license" not in frontmatter
            and "license" not in metadata,
        }
        for label, passed in checks.items():
            if not passed:
                failures.append(f"{expected_name}: frontmatter check failed: {label}")

        body = content[match.end() :]
        numbered = re.findall(r"^## (\d+)\. ", body, re.MULTILINE)
        if not numbered or len(numbered) != len(set(numbered)):
            failures.append(f"{expected_name}: numbered sections are missing or duplicated")
        if len(body) < spec["minimum_chars"]:
            failures.append(
                f"{expected_name}: body unexpectedly short ({len(body)} characters)"
            )

        for heading in spec["sections"]:
            if heading.casefold() not in body.casefold():
                failures.append(f"{expected_name}: required coverage missing: {heading}")

        if re.search(
            r"^\s*(?:[-*]\s*)?(?:Former domain|Former skill ID|Former skill identity|"
            r"Preserved skill ID|Skill identity \(retired\))\s*:",
            body,
            re.MULTILINE | re.IGNORECASE,
        ):
            failures.append(f"{expected_name}: retired identity marker remains")

        if not failures or not any(item.startswith(f"{expected_name}:") for item in failures):
            print(
                f"PASS: {expected_name} v{metadata.get('version')} "
                f"({len(numbered)} numbered sections, {len(body)} characters)"
            )

    if failures:
        for item in failures:
            print(f"FAIL: {item}", file=sys.stderr)
        raise SystemExit(1)

    print(f"PASS: all {len(EXPECTED)} verified original skills satisfy validation rules")


if __name__ == "__main__":
    main()
