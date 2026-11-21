---
name: software-quality-and-security-review
description: Use when reviewing source code, pull requests, diffs, or modules in any programming language for correctness, maintainability, and security defects, and when producing a prioritized, evidence-backed review report.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Software Quality And Security Review

## Purpose and boundaries

This skill guides a structured review of code for defects in three areas: correctness and reliability, maintainability and design, and security. It produces findings ranked by severity, each tied to a file location, a reproduction or reasoning trace, and a concrete fix direction.

In scope: diffs, pull requests, single files, modules, and small services; language-idiom issues (memory safety, concurrency, error handling, type misuse, injection, deserialization, secrets handling, authorization checks, dependency risk indicators).

Out of scope: rewriting the codebase, performance tuning without a measured bottleneck, style-only feedback unless it hides a defect, and certifying compliance with any standard. Do not claim the code is "secure" or "bug-free"; state only what was checked.

## Inputs and assumptions

Required inputs: the code or diff, the language and runtime version if known, and the intended behavior (ticket, docstring, or stated purpose). If intent is missing, infer it from tests and call sites, and label the inference as an assumption.

Optional inputs: existing test results, linter or static analyzer output, dependency manifests, threat model, deployment context (public-facing, internal, batch).

Assumptions must be listed explicitly in the report. Never assume that code is unreachable, that input is trusted, or that a framework provides protection unless the framework behavior is confirmed in its current official documentation.

## Operating workflow

1. **Scope the review.** List the files and the changed line ranges. Identify entry points: HTTP handlers, CLI arguments, message consumers, file parsers, deserializers, environment reads.
2. **Map data flow.** For each entry point, trace untrusted input to sinks: SQL/shell/template construction, file paths, deserialization, eval-like constructs, outbound requests, logs, and persistent storage.
3. **Check trust boundaries.** Confirm where authentication, authorization, validation, and encoding occur, and whether they run on every path, including error and retry paths.
4. **Review correctness.** Examine null/none handling, integer overflow and truncation, off-by-one ranges, resource release on all exits, race conditions on shared state, time-of-check/time-of-use gaps, partial failure and retry idempotency, and silent error swallowing.
5. **Review language-specific hazards.** Examples: unchecked casts or unsafe blocks in Rust and C#; goroutine leaks and unsynchronized maps in Go; mutable default arguments and pickle or yaml unsafe loading in Python; prototype pollution and unhandled promise rejections in JavaScript; `unsafe` pointer arithmetic and unchecked buffer sizes in C/C++.
6. **Review maintainability.** Flag duplicated logic that has already diverged, functions whose behavior cannot be stated in one sentence, hidden global state, and tests that assert implementation rather than behavior. Keep these findings at low severity unless they cause a defect.
7. **Verify each candidate finding** before reporting (see Verification and evidence).
8. **Rank and write the report** using the Deliverable contract.

## Decision gates

- **Gate A, severity:** Critical if exploitable without authentication or causes data loss or corruption in normal use. High if exploitable with ordinary user privileges or causes a crash or incorrect results on a common path. Medium if the defect requires an unusual input, race window, or misconfiguration. Low for maintainability and hardening suggestions.
- **Gate B, reachability:** Report a finding as confirmed only if a concrete path from an entry point reaches the defect. Otherwise report it as "suspected, reachability unknown" and state what would confirm it.
- **Gate C, scope of fix:** If the fix requires changing a public interface, schema, persisted data format, or dependency version, flag it and request approval before recommending it as a default.
- **Gate D, sensitive material:** If the code or diff contains credentials, tokens, private keys, personal data, or production connection strings, stop quoting them. Report location and type only, and recommend rotation. Obtain explicit approval before reproducing any such value in output.
- **Gate E, active testing:** Do not run exploit payloads, network scans, load tests, or code that writes to shared, production, or third-party systems without explicit approval and a stated isolated environment.

## Verification and evidence

Every finding must include:
- File path and line range.
- The input or condition that triggers the defect.
- The observed or derived behavior, with the reasoning chain.
- A reproduction: a minimal failing unit test or a command in an isolated environment, if approved. If reproduction is not performed, say so.

Use static analyzers and linters as evidence sources, but do not report their output verbatim; confirm each hit. Discard hits you cannot reproduce or reason through, and list them under "Dismissed with reason" for transparency.

Quality checks before finalizing:
- Every Critical and High finding has a reproduction or a complete reasoning trace.
- No finding cites a line that does not exist in the reviewed revision.
- Each recommendation is checked against the language version in use.
- Any library, function, or flag name is verified against current official documentation. Mark version-sensitive details as "verify against current official documentation" rather than asserting them.

## Failure handling

- **Missing context:** Proceed with stated assumptions, and mark affected findings as provisional.
- **Analyzer unavailable or failing:** Continue manual review and note the gap in the report.
- **Conflicting intent and behavior:** Report the conflict as a finding; do not resolve it by choosing the more convenient reading.
- **Reproduction blocked by approval gate:** Record the finding as unverified and state the approval needed.
- **Large diff:** Prioritize entry points and security-relevant modules; state the unreviewed portion explicitly.

## Deliverable contract

Produce one report with these sections, in order:

1. **Summary:** scope, revision reviewed, overall risk statement limited to what was checked, counts by severity.
2. **Assumptions and gaps:** list.
3. **Findings:** ordered by severity, each with ID, severity, location, trigger, evidence, impact, and recommended fix.
4. **Dismissed with reason:** candidate issues rejected and why.
5. **Approvals needed:** any pending decisions under Gates C, D, or E.
6. **Verification performed:** what was run, what was only read.

Do not include praise, filler, or compliance claims. Do not paste secrets. Do not state that a fix is verified unless it was tested.