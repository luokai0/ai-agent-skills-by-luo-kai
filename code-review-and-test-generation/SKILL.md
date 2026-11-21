---
name: code-review-and-test-generation
description: Use when reviewing code changes for correctness, risk, and maintainability, or when generating, extending, or repairing automated tests for a defined change set in a repository.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Code Review And Test Generation

## Purpose and boundaries

This skill produces two artifacts for a given change: a structured review of the diff, and tests that exercise the behavior the change introduces or modifies. It covers reading code, identifying defects and risks, proposing or writing tests, running them, and reporting results.

In scope: diffs, pull requests, single files, and modules within a checked-out repository; unit and integration tests written in the project's existing test framework; regression tests for reported bugs.

Out of scope: rewriting unrelated code, changing production behavior beyond what a fix requires, load or security penetration testing, certifying compliance, and deploying anything.

## Inputs and assumptions

Before starting, establish:

1. The change under review: diff range, commit hashes, or file list. If none is given, use the working tree diff and state that choice.
2. The stated intent: ticket text, PR description, or the bug report. If absent, infer intent from the code and label it as inferred.
3. The language, framework, and test runner, read from manifest and lockfiles and existing test files. Do not assume a framework that the repository does not already use.
4. The build and test commands documented in the repository. Prefer the documented command over guessed flags.
5. Whether network access, databases, or external services are reachable. Tests must not depend on live external systems unless the repository already does so in its test setup.

Record every assumption in the final report.

## Operating workflow

1. **Map the change.** List touched files, public interfaces altered, and data shapes changed. Group changes by behavior, not by file.
2. **Derive expected behavior.** Write one to five plain-language behavior statements the change must satisfy. Mark any that come from inference.
3. **Review for defects.** Check each category in order: input validation and boundary values; error paths and exception handling; null, empty, and zero-length inputs; concurrency and shared state; resource cleanup; off-by-one and time-zone or encoding handling; backward compatibility of public signatures and serialized formats; security-relevant handling of untrusted input.
4. **Classify findings.** Use severity levels: blocker (incorrect behavior or data loss), major (likely failure under realistic input), minor (clarity, naming, dead code), nit (style only, optional).
5. **Check existing coverage.** Locate current tests touching the changed code. Note which new behaviors have no coverage.
6. **Design tests.** For each behavior statement and each blocker or major finding, define at least one test: arrange, act, assert. Include one negative or error-path case per behavior. Use the repository's fixtures and helpers.
7. **Write tests.** Place them beside existing tests following the project's naming convention. Do not modify existing assertions to make tests pass unless the old assertion encoded the defect, and say so explicitly.
8. **Run.** Execute the narrowest test target first, then the full suite for the affected package.
9. **Report.** Produce the deliverable contract below.

## Decision gates

- **Gate A, before writing tests:** If the expected behavior is ambiguous and two reasonable interpretations produce different results, stop and ask the requester which is correct. Do not encode a guess as an assertion.
- **Gate B, before modifying production code:** The task is review and tests. Changing production code requires explicit approval, except for a one-line fix the requester has already asked for.
- **Gate C, before any action that deletes files, rewrites history, force-pushes, alters CI configuration, changes dependency versions, or touches credentials, migrations, or production data:** Require explicit approval with the exact command or file list shown.
- **Gate D, before contacting external services or posting comments to a remote review system:** Require explicit approval and show the text first.
- **Gate E, flaky tests:** If a test fails intermittently on rerun, quarantine it only with approval and record the reproduction rate.

## Verification and evidence

- Every blocker and major finding cites file path and line range, plus a concrete input that triggers the problem.
- Every new test is run and its pass or fail result is recorded. A test not executed is reported as not executed.
- Confirm each new test fails on the pre-change code where practical (by stashing the fix or checking out the base commit). Report which tests failed before and passed after. If this is not feasible, say why.
- Report the exact test command used and its summary line: total, passed, failed, skipped.
- Coverage numbers are reported only if the repository's own coverage tool produced them in this run. Do not estimate coverage.
- Mark any statement about library behavior or API signatures as requiring verification against current official documentation when the version is not confirmed from the lockfile.

## Failure handling

- **Build fails before tests run:** Report the first error verbatim, do not guess fixes to build configuration, and stop unless the fix is within the change under review.
- **Existing tests fail unrelated to the change:** Record them as pre-existing with the failing names. Do not fix them without approval.
- **New test cannot be made to pass without changing production behavior:** Report it as a candidate defect with the failing assertion. Do not weaken the assertion.
- **Missing dependency or tool:** Report the name and the repository's documented install step. Do not install globally without approval.
- **Time or resource limits reached:** Report what finished, what did not, and the next command to run.

## Deliverable contract

Return one report with these sections, in order:

1. **Scope:** change identifier, files reviewed, assumptions list.
2. **Findings:** table with severity, location, description, triggering input, and suggested fix.
3. **Tests added or changed:** file paths, test names, behavior each covers.
4. **Execution:** exact commands, pass/fail/skip counts, pre-change versus post-change results.
5. **Open items:** unresolved ambiguities, pre-existing failures, approvals needed.

Keep prose short. Use a finding only when it is specific enough for an author to act on without re-deriving it. Quality check: every finding has a location and a reproducer, every test has been executed, and no assertion was weakened silently.