---
name: test-repair-and-plan-execution
description: Use when a test suite has failing, flaky, or broken tests and a written repair plan or migration plan must be executed step by step, verified, and reported without weakening coverage or hiding real defects.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Test Repair And Plan Execution

## Purpose and boundaries

This skill covers executing a defined plan to repair failing or broken tests: fixing test code, test fixtures, environment wiring, and test-data assumptions, then proving the suite is healthy again. It also covers executing a multi-step plan (for example, a framework upgrade or test-layer migration) where each step must be checked before the next begins.

In scope: diagnosing failure causes, classifying them, applying the smallest correct fix, re-running affected tests, and recording evidence.

Out of scope: inventing new product requirements, changing production behavior to make tests pass without a confirmed defect, deleting coverage to reduce failure counts, and rewriting the test strategy unless the plan explicitly asks for it.

## Inputs and assumptions

Before acting, confirm:
- The failing test list or the plan document, with its ordered steps and acceptance criteria.
- The exact command used to run tests, the runner version, and the CI configuration, read from the repository rather than assumed.
- Whether the goal is "suite green" or "plan step N complete." These differ and must be stated.
- Baseline results: the last known passing commit, if any, and current failure output.

If version-sensitive APIs, runner options, or library behaviors are involved, verify them against current official documentation for the pinned version. Do not rely on memory for flag names or deprecation status.

## Operating workflow

1. **Reproduce.** Run the failing tests in isolation and then as part of the full suite. Record the command, exit code, and the first failure message. A failure that does not reproduce is classified as flaky, not fixed.
2. **Classify each failure** into one of: test defect (wrong assertion, stale expectation, bad fixture), environment defect (missing service, port collision, timezone, locale), dependency drift (changed library behavior), data defect (order-dependent state, shared database rows), or product defect (correct test exposing a real bug).
3. **Group failures** by root cause. Ten failures from one missing fixture is one repair.
4. **Apply the smallest fix** per group. Prefer correcting setup and isolation over loosening assertions. If an assertion must change, state the old and new expected behavior and why the old one was wrong.
5. **Execute plan steps in order.** Complete one step, run its verification, record evidence, then start the next. Do not batch steps whose verification would be ambiguous together.
6. **Re-run** the isolated tests, then the full suite, then any gating CI stage.
7. **Repeat the full suite** at least three times for any test that was flaky, to check stability.

## Decision gates

Stop and request explicit approval before:
- Deleting, skipping (`skip`, `xfail`, disabled marks), or quarantining any test. Skipping requires an owner and a tracking reference.
- Changing production code. A test that exposes a product defect is reported, not silently "fixed" in test code.
- Modifying shared fixtures, seed data, or databases used by other suites.
- Running commands against shared, staging, or production systems, or anything that sends external messages, charges, or writes to third-party services.
- Deleting snapshot files, golden files, or recorded fixtures. Regenerating them is allowed only after reviewing the diff.
- Any action that is irreversible or affects data outside the repository.

Proceed without asking for: editing test files in the working branch, local test runs, adding diagnostic logging in test code, and reverting your own uncommitted changes.

## Verification and evidence

Each repair must have:
- A failing-before and passing-after run of the same command.
- For flaky tests, at least three consecutive passing runs, with the seed or ordering recorded if randomized.
- A diff confined to the planned scope. Flag any change outside it.
- Coverage that does not decrease for the touched modules. Measure with the project's existing tool and report the number before and after.

Quality checks, all measurable:
- Zero newly skipped or deleted tests unless approved.
- Failure count strictly decreasing across steps, or an explained increase.
- Every assertion change has a written rationale.
- No test sleeps longer than a fixed wait introduced to hide a race; race conditions are fixed with explicit synchronization.

Do not claim performance numbers, pass rates across environments, or compliance status unless measured and shown.

## Failure handling

- If a fix makes a different test fail, revert it and reclassify the group.
- If reproduction fails inconsistently, capture logs, seed, and timing for three runs before changing code.
- If a plan step is blocked by a missing dependency or unclear acceptance criterion, stop at that step, state the blocker, and list the specific information needed.
- If the root cause is a product defect, produce a minimal reproduction and escalate instead of patching around it.

## Deliverable contract

Produce a report containing:
1. Summary: starting failure count, ending failure count, and the goal stated in Inputs.
2. Table of root-cause groups: cause, affected tests, fix applied, files changed.
3. Plan step status: each step marked complete, blocked, or deferred, with its verification evidence.
4. Assertion or expectation changes with rationale.
5. Open items requiring approval, with the specific decision needed.
6. Exact commands run and their results.

Do not state the suite is healthy unless the final full-suite run in the recorded environment passed.