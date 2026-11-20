#!/usr/bin/env python3
"""Audit all repository skills for overlapping capabilities and ownership eligibility."""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "skills-index.json"
DEFAULT_OUTPUT = ROOT / "docs/REPOSITORY_WIDE_OVERLAP_AUDIT.md"
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
TOKEN = re.compile(r"[a-z0-9][a-z0-9+#.-]*")
STOP = {
    "the", "and", "for", "with", "from", "that", "this", "when", "where", "what",
    "how", "why", "into", "onto", "your", "you", "are", "can", "will", "should",
    "must", "use", "using", "used", "skill", "skills", "user", "users", "agent",
    "agents", "task", "tasks", "work", "working", "help", "helps", "based", "make",
    "makes", "across", "within", "without", "their", "them", "they", "its", "has",
    "have", "had", "been", "being", "also", "such", "any", "all", "each", "other",
    "more", "most", "some", "many", "include", "includes", "including", "ensure",
    "provides", "provide", "supports", "support", "allows", "allow", "ability",
    "best", "good", "new", "current", "common", "different", "various", "related",
    "overview", "guide", "guidance", "reference", "references", "example", "examples",
}


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def read_frontmatter(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER.match(raw)
    if not match:
        return {}, raw
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}, raw[match.end():]
    return (metadata if isinstance(metadata, dict) else {}), raw[match.end():]


def ownership(metadata: dict, category: str, license_value: str) -> str:
    details = metadata.get("metadata") or {}
    if not isinstance(details, dict):
        details = {}
    author = str(metadata.get("author") or details.get("author") or "").strip().casefold()
    provenance = str(metadata.get("provenance") or details.get("provenance") or "").strip().casefold()
    if provenance in {"original"} and author in {"luo kai", "luo-kai"} and category not in {"21", "22"}:
        return "original_with_license_field" if license_value else "verified_original"
    if provenance in {"adapted", "adaptation"}:
        return "adapted"
    if provenance in {"third-party", "third_party", "external", "imported"} or category in {"21", "22"}:
        return "third_party"
    if provenance in {"unverified", ""}:
        return "unverified"
    return "unverified"


def tokens_for(text: str) -> set[str]:
    return {
        token for token in TOKEN.findall(text.casefold())
        if token not in STOP and (len(token) >= 3 or token in {"c", "go", "r"})
    }


def cosine(left: dict[str, float], right: dict[str, float], left_norm: float, right_norm: float) -> float:
    if not left or not right or not left_norm or not right_norm:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    dot = sum(weight * right.get(token, 0.0) for token, weight in left.items())
    return dot / (left_norm * right_norm)


def make_report(index: dict) -> str:
    entries = index.get("skills")
    categories = index.get("cats") or {}
    if not isinstance(entries, list):
        fail("skills-index.json has no skills array")

    docs = []
    category_counts = Counter()
    ownership_counts = Counter()
    license_counts = Counter()
    parse_failures = 0
    missing_paths = 0

    for entry in entries:
        category = str(entry.get("c", "??"))
        rel = unquote(str(entry.get("p", "")))
        path = ROOT / rel
        if not rel or not path.is_file():
            missing_paths += 1
            continue
        metadata, body = read_frontmatter(path)
        if not metadata:
            parse_failures += 1
        details = metadata.get("metadata") or {}
        if not isinstance(details, dict):
            details = {}
        license_value = str(metadata.get("license") or details.get("license") or "").strip()
        license_label = license_value or "No license field"
        ownership_label = ownership(metadata, category, license_value)
        category_counts[category] += 1
        ownership_counts[ownership_label] += 1
        license_counts[license_label] += 1

        title = str(metadata.get("name") or entry.get("n") or path.parent.name)
        description = str(metadata.get("description") or entry.get("d") or "")
        headings = " ".join(
            line.lstrip("# ").strip()
            for line in body.splitlines()
            if line.startswith("#") and len(line.lstrip("# ").strip()) > 2
        )
        title_terms = tokens_for(title.replace("-", " ") + " " + str(entry.get("n", "")).replace("-", " "))
        desc_terms = tokens_for(description + " " + headings[:1800])
        all_terms = title_terms | desc_terms
        docs.append({
            "name": title,
            "slug": str(entry.get("n") or path.parent.name),
            "category": category,
            "category_name": categories.get(category, "Unknown"),
            "path": rel,
            "description": description,
            "ownership": ownership_label,
            "license": license_label,
            "title_terms": title_terms,
            "terms": all_terms,
        })

    if missing_paths:
        fail(f"{missing_paths} catalog paths do not resolve to repository files")
    if len(docs) != int(index.get("total", len(entries))):
        fail(f"Catalog says {index.get('total')} skills but only {len(docs)} paths were read")

    document_frequency = Counter()
    for doc in docs:
        document_frequency.update(doc["terms"])
    n_docs = len(docs)
    idf = {
        term: math.log((n_docs + 1) / (freq + 1)) + 1.0
        for term, freq in document_frequency.items()
    }
    vectors = []
    norms = []
    postings = defaultdict(list)
    for i, doc in enumerate(docs):
        vector = {term: idf[term] for term in doc["terms"]}
        norm = math.sqrt(sum(weight * weight for weight in vector.values()))
        vectors.append(vector)
        norms.append(norm)
        informative = sorted(
            (term for term in doc["terms"] if document_frequency[term] <= 160),
            key=lambda term: idf[term],
            reverse=True,
        )[:28]
        for term in informative:
            postings[term].append(i)

    pairs = {}
    for i, doc in enumerate(docs):
        candidates = set()
        for term in doc["terms"]:
            if document_frequency[term] <= 160:
                candidates.update(postings[term])
        candidates = {j for j in candidates if j > i}
        if not candidates:
            continue
        for j in candidates:
            other = docs[j]
            shared = len(doc["terms"] & other["terms"])
            if shared < 3:
                continue
            similarity = cosine(vectors[i], vectors[j], norms[i], norms[j])
            title_union = doc["title_terms"] | other["title_terms"]
            title_jaccard = (
                len(doc["title_terms"] & other["title_terms"]) / len(title_union)
                if title_union else 0.0
            )
            score = 0.82 * similarity + 0.18 * title_jaccard
            if score >= 0.38 or (title_jaccard >= 0.58 and similarity >= 0.20):
                pairs[(i, j)] = (score, similarity, title_jaccard, shared)

    parent = list(range(len(docs)))
    sizes = [1] * len(docs)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (i, j), values in sorted(pairs.items(), key=lambda item: item[1][0], reverse=True):
        if values[0] < 0.43:
            continue
        a, b = find(i), find(j)
        if a == b or sizes[a] + sizes[b] > 5:
            continue
        parent[b] = a
        sizes[a] += sizes[b]

    groups = defaultdict(list)
    for i in range(len(docs)):
        root = find(i)
        if sizes[root] >= 2:
            groups[root].append(i)

    candidate_groups = []
    for members in groups.values():
        member_pairs = []
        for pos, i in enumerate(members):
            for j in members[pos + 1:]:
                pair = (min(i, j), max(i, j))
                if pair in pairs:
                    member_pairs.append(pairs[pair][0])
        if member_pairs:
            candidate_groups.append((sum(member_pairs) / len(member_pairs), members))
    candidate_groups.sort(key=lambda item: item[0], reverse=True)

    lines = [
        "# Repository-wide skill overlap audit",
        "",
        "**Audit type:** Read-only discovery. No skill files are modified by this report.",
        f"**Catalog total:** {len(docs):,} skills across {len(categories)} collections.",
        "**Audit date:** 2026-11-20",
        "",
        "## Ownership and license boundaries",
        "",
        "Only entries explicitly marked as original and authored by Luo Kai are eligible for an original-only consolidation review. A folder label or author field alone is not proof of ownership. Adapted, imported, external-registry, ClawHub, and unverified entries are never treated as Luo Kai-owned originals by this audit.",
        "",
        "| Ownership classification | Skills |",
        "|---|---:|",
    ]
    for key, label in [
        ("verified_original", "Verified original by Luo Kai"),
        ("original_with_license_field", "Original metadata with a license field to review"),
        ("adapted", "Adapted"),
        ("third_party", "Third-party or external registry"),
        ("unverified", "Unverified provenance"),
    ]:
        lines.append(f"| {label} | {ownership_counts[key]:,} |")
    lines.extend([
        "",
        f"Frontmatter parse failures: {parse_failures:,}. Missing catalog paths: {missing_paths:,}.",
        "",
        "## Collection inventory",
        "",
        "| Collection | Skills |",
        "|---|---:|",
    ])
    for category, label in sorted(categories.items()):
        lines.append(f"| {category} — {label} | {category_counts[category]:,} |")
    lines.extend([
        "",
        "## Declared license inventory",
        "",
        "| License metadata | Skills |",
        "|---|---:|",
    ])
    for label, count in license_counts.most_common():
        lines.append(f"| {label.replace('|', '/')} | {count:,} |")
    lines.extend([
        "",
        "## Candidate overlap groups",
        "",
        f"Similarity candidates found: {len(pairs):,} pairs. Small candidate groups (2–5 skills): {len(candidate_groups):,}.",
        "Similarity is a triage signal, not proof that two skills are interchangeable. Every group needs a human capability comparison before merging. Preserve distinct platform behavior, safety controls, examples, and verification. Do not delete any member until its complete useful content has been incorporated and validated.",
        "",
    ])

    shown = 0
    for rank, (avg, members) in enumerate(candidate_groups, 1):
        if shown >= 100:
            break
        group_docs = [docs[i] for i in members]
        classes = {doc["ownership"] for doc in group_docs}
        if classes == {"verified_original"}:
            status = "Eligible for original-only manual merge review"
        elif "third_party" in classes or "unverified" in classes:
            status = "Do not merge until ownership and redistribution rights are verified"
        elif "original_with_license_field" in classes:
            status = "Review license metadata and ownership before any change"
        else:
            status = "Adaptation and license review required"
        lines.extend([
            f"### Candidate group {rank} — similarity {avg:.3f}",
            "",
            f"**Review status:** {status}",
            "",
        ])
        for doc in group_docs:
            desc = re.sub(r"\s+", " ", doc["description"]).strip()
            if len(desc) > 210:
                desc = desc[:207].rstrip() + "..."
            lines.extend([
                f"- **{doc['name']}** ({doc['category']} — {doc['category_name']})",
                f"  - Ownership: {doc['ownership']}; license metadata: {doc['license']}",
                f"  - Path: {doc['path']}",
                f"  - Description: {desc or 'No description available'}",
            ])
        lines.append("")
        shown += 1

    if len(candidate_groups) > shown:
        lines.append(f"Additional candidate groups not expanded here: {len(candidate_groups) - shown:,}. Narrow by collection or capability before reviewing the next batch.")
    lines.extend([
        "",
        "## Consolidation gate",
        "",
        "1. Confirm that every member is legally eligible for the same treatment. Missing license information is not permission.",
        "2. Compare the complete procedures, not just names or descriptions. Identify what each skill does uniquely.",
        "3. Combine all distinct useful capabilities into one independently authored skill; do not reduce it to a summary.",
        "4. Retain platform-specific commands, examples, safety constraints, approval gates, verification, and recovery paths.",
        "5. Validate frontmatter, references, examples, and safety boundaries before retiring redundant entries.",
        "6. Keep third-party notices and license terms where required. Original Luo Kai work must not receive a license field unless explicitly requested.",
        "",
        "---",
        "Copyright (c) 2026 Luo Kai. All rights reserved for original audit tooling and report text.",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the report to the repository")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()
    if not INDEX.is_file():
        fail("skills-index.json is missing")
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    report = make_report(index)
    print(report.splitlines()[0])
    print(f"Catalog skills: {index.get('total')}")
    print(f"Report characters: {len(report):,}")
    if args.write:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(f"REPORT WRITTEN: {output.relative_to(ROOT)}")
    else:
        print("DRY RUN ONLY. Use --write to save the report.")


if __name__ == "__main__":
    main()
