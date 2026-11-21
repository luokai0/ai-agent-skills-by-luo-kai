---
name: code-review-execution
description: Use when performing, coordinating, or structuring a code review of a change set, pull request, or patch, including triaging findings, deciding merge readiness, and writing actionable review comments.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Code Review Execution

## Purpose and boundaries

This skill covers executing a code review: reading a change, testing its claims, finding defects and risks, and producing a merge recommendation with traceable findings. It applies to pull requests, patches, and staged diffs in application, library, infrastructure, and data code.

Out of scope: writing the feature itself, designing architecture from scratch, security penetration testing, and performance benchmarking beyond reading existing evidence. Route those to the appropriate skill or owner.

## Inputs and assumptions

Required before starting:
- The diff or change reference, and the base it targets.
- The stated intent: linked ticket, PR description, or commit messages.
- Access to the repository at the change's head commit, so surrounding code can be read.
- The project's contribution guidelines, style rules, and CI status.

Assumptions to state explicitly if unverified: that CI results correspond to the current head commit; that the described behavior matches the ticket; that no generated or vendored files are being reviewed as hand-written code.

If intent is missing, reconstruct it from the diff, record the reconstruction as an assumption, and ask the author to confirm before issuing a final verdict.

## Operating workflow

1. **Scope the change.** Count files and lines changed. Separate generated, lockfile, vendored, and formatting-only changes from logic changes. Review logic first.
2. **State the claim.** Write one or two sentences describing what the change is supposed to do. Every later check tests this claim.
3. **Read the diff in two passes.** Pass one: structure, interfaces, data flow, and file layout. Pass two: line-level correctness, edge cases, error paths, and concurrency.
4. **Read context, not just the diff.** Open each modified function in full. Check callers of changed signatures, and check tests that cover the touched behavior.
5. **Check the specific risk classes** (see Verification).
6. **Run or inspect evidence.** Confirm CI results, run the test suite locally when the change is non-trivial, and reproduce any bug you claim.
7. **Classify each finding** (see Decision gates) and write it as a comment with location, reasoning, and a suggested direction.
8. **Issue a verdict** with a summary of blocking items, non-blocking items, and what you did not verify.

## Decision gates

Classify every finding:
- **Blocking:** incorrect behavior for a reachable input, data loss or corruption, a security or privacy regression, a broken public contract, a missing migration or rollback path, or a failing required check.
- **Non-blocking (should fix):** unclear naming, missing edge-case test, duplicated logic likely to drift, misleading comment.
- **Nit:** style or preference the project does not enforce. Prefix with "nit:" and never block on it.
- **Question:** you do not understand the intent. Ask before judging.

Approve only when: no blocking findings remain, required CI passes on the head commit, and the claim in step 2 is supported by code or tests. Request changes when any blocking finding exists. Escalate to a domain owner when the change touches authentication, payments, personal data, schema migrations on large tables, or infrastructure with production blast radius.

Size gate: if the change exceeds roughly 400 changed lines of logic, recommend splitting, unless it is a mechanical change such as a rename or generated update.

## Verification and evidence

Check these risk classes for every review:
- **Boundaries:** empty, null, zero, maximum, and off-by-one inputs; unicode and timezone handling where relevant.
- **Errors:** every new error path returns, logs, or propagates as the surrounding code expects; no swallowed exceptions; no partial writes without cleanup.
- **Concurrency:** shared mutable state, check-then-act sequences, missing locks or transactions, retry safety and idempotency.
- **Data:** schema changes are backward compatible during rolling deploys; migrations are reversible or have a documented forward-only plan; indexes exist for new query paths.
- **Contracts:** public function, API, and event shapes are unchanged or versioned; callers in the repository are updated.
- **Tests:** new behavior has tests that would fail without the change; tests assert outcomes, not implementation details; no disabled or skipped tests without a tracked reason.
- **Dependencies:** new packages have justified need, acceptable license per project policy, and pinned versions. Verify current version and advisory status against the registry or official documentation. Do not assume a version is safe or current from memory.

Evidence standard: every blocking finding must cite a file and line, and state a concrete input or sequence that triggers it. "This might be slow" is not a finding; "this loops over all rows per request, and the endpoint is called per item" is.

Measurable quality checks: the review records files read, checks completed from the list above, and CI run identifier. Coverage claims must come from the project's reported tool output, not estimates.

## Failure handling

- **CI red or missing:** do not approve. Record the failing job and whether it reproduces locally.
- **Cannot reproduce a claimed bug:** ask for a failing test or steps; do not block on speculation.
- **Scope too large to review properly:** say which parts were reviewed in depth and which were skimmed, and recommend splitting.
- **Disagreement with author:** restate the concrete input that causes the issue. If unresolved, escalate to the module owner rather than repeating the argument.
- **Insufficient access:** list what was not inspected in the verdict.

## Deliverable contract

The review output contains, in order:
1. Verdict: approve, request changes, or comment-only.
2. Change claim and whether it was verified.
3. Blocking findings, each with location, trigger, and suggested direction.
4. Non-blocking findings and nits, grouped by file.
5. Questions for the author.
6. Evidence reviewed: CI run, commands executed, files read in depth.
7. Unverified areas and assumptions.

Do not:
- Approve with unresolved blocking items or red required checks.
- Block on personal style preference.
- Rewrite the author's change wholesale in comments.
- Post comments that cannot be acted on without further explanation.
- Share credentials, internal URLs, or customer data found in a diff; flag them and request explicit approval from the owner before any further external disclosure.
- Merge or push changes to the author's branch without explicit approval from the author or maintainer.