---
name: review-feedback-handling
description: Use when processing code review, test review, or QA feedback on a change, to triage comments, decide what to act on or push back on, implement fixes, and verify each resolution with evidence before closing the thread.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Review Feedback Handling

## Purpose and boundaries

This skill governs how you respond to feedback on test code, test plans, test results, and related quality artifacts (pull request review comments, QA defect reviews, test-plan sign-off notes). The goal is to resolve each point correctly: accept valid feedback with a verified change, decline or redirect invalid feedback with a stated reason, and surface disagreements that need a human decision.

In scope: triaging comments, reproducing claimed defects, applying fixes to tests or test-related code, writing reply text, and recording verification evidence.

Out of scope: rewriting the product feature under review beyond what a comment requires, changing CI policy or branch protection, deleting tests to make a suite pass, editing reviewer comments, and closing threads on another person's behalf.

## Inputs and assumptions

Before acting, collect:

- The full list of comments with author, location (file, line, test name), and status.
- The change under review (diff, commit range, or test plan version).
- How to run the relevant tests locally and in CI. If unknown, ask; do not guess commands.
- Project conventions documented in contributing or testing guides.

Assume reviewers may be wrong, incomplete, or referring to an earlier revision. Assume your own prior work may contain the defect being raised until you prove otherwise.

## Operating workflow

1. **Snapshot the state.** Record the current commit, branch, and a list of all open comments. Work from this snapshot so later edits do not blur what was addressed.
2. **Classify each comment** into one of: defect (behavior is wrong), test gap (missing coverage or assertion), flakiness or determinism, readability or naming, style nit, question, or disagreement.
3. **Reproduce before changing.** For defects and test gaps, write or run the smallest check that demonstrates the claim. If you cannot reproduce it, record the exact steps you tried and the output.
4. **Decide the response** using the gates below.
5. **Implement one logical fix per comment** where practical, so each can be reverted or reviewed independently.
6. **Re-run the affected tests**, then the broader suite the change touches.
7. **Reply on each thread** with what changed (commit or line reference), the evidence, or the reasoning for declining.
8. **Re-check for regressions** introduced by the fix, especially around shared fixtures, test ordering, and mocks.

Batch comments that touch the same code, but still reply to each individually.

## Decision gates

Apply these in order:

- **Gate 1: Reproduces?** If the claimed failure reproduces, fix it. If it does not reproduce after a documented good-faith attempt, ask the reviewer for the exact input, environment, or command. Do not apply speculative changes.
- **Gate 2: Correct?** If it reproduces but the reviewer's proposed fix is wrong or would weaken coverage, implement a better fix and explain why.
- **Gate 3: Scope?** If the fix requires changing product behavior, a shared test utility used by other teams, a public interface, or test data that others depend on, stop and request explicit approval before proceeding.
- **Gate 4: Cost?** For style nits, apply if the change is under the project's formatting rules or takes under a few minutes. Otherwise accept the point as a follow-up issue with a link, and say so.
- **Gate 5: Disagreement?** If you believe the comment is incorrect after reproduction, reply with the evidence and the specific question. Leave the thread open for the reviewer to resolve.

Require explicit approval before any of the following: deleting or skipping tests, lowering assertion strictness or coverage thresholds, adding retries to hide flakiness, changing shared fixtures or test data used elsewhere, posting replies or resolving threads on behalf of others, and any action touching production data, credentials, or external services.

## Verification and evidence

A thread is resolved only when you can state:

- The command run and its result (pass/fail counts, relevant output excerpt).
- For a defect fix: the test that failed before the change and passes after it.
- For a coverage claim: the coverage report or assertion added, not a percentage alone.
- For a flakiness fix: the number of repeated runs and their results, stated as observed, not guaranteed.

Use the project's own test runner and coverage tool; verify exact flags and option names against the current official documentation for the version in use, since these change between releases. Do not claim a fix is "verified in CI" until CI has actually run.

Quality checks before marking the review complete:

- Every comment has a reply and a status: fixed, declined with reason, deferred with link, or awaiting reviewer.
- No test was weakened, skipped, or retried to pass unless approved.
- The affected test suite passes locally and the diff contains no unrelated changes.
- Assertions check specific expected values, not only absence of exceptions.

## Failure handling

- **Fix breaks other tests:** Revert that single change, isolate the coupling, and re-apply in a narrower form. Report the coupling in the thread.
- **Cannot reproduce:** Document steps, environment, and output. Ask the reviewer; keep the thread open.
- **Flaky result after fix:** Do not merge a retry as the fix. Identify the nondeterminism source (timing, shared state, ordering, unseeded randomness) and report it.
- **Conflicting reviewer comments:** Summarize both positions with evidence and request a decision from the reviewer or maintainer.
- **Time pressure:** Fix blocking defects first, then correctness gaps, then readability. Defer nits explicitly rather than silently skipping them.

## Deliverable contract

Produce a feedback resolution log containing:

1. A table: comment ID or link, author, classification, gate outcome, action taken, commit reference, evidence summary.
2. The full test commands executed and their final results.
3. A list of items awaiting approval or reviewer input, each with the specific question.
4. A list of deferred items with follow-up references.
5. A short statement of residual risk, such as untested environments or unverified CI results.

Do not state that feedback has been fully addressed unless every comment is in a terminal state (fixed with evidence, declined with reason, deferred with reference, or explicitly awaiting a named person).