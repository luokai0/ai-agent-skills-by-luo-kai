---
name: debugging-and-root-cause
description: Use when a defect, test failure, crash, regression, or unexpected behavior needs diagnosis to a verified root cause before a fix is proposed or merged, including flaky tests and intermittent production symptoms.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Debugging And Root Cause

## Purpose and boundaries

This skill turns a symptom into a verified root cause and a minimal, tested correction. It covers reproduction, isolation, hypothesis testing, causal explanation, and regression protection for application code, tests, build pipelines, and configuration.

In scope: failing tests, regressions after a change, crashes with stack traces, wrong outputs, intermittent or flaky failures, performance regressions traced to a specific change.

Out of scope: feature design, broad refactoring not required by the fix, incident communication, and security vulnerability disclosure (route those to their owners). Do not use this skill to justify a workaround as a fix without naming the underlying cause.

## Inputs and assumptions

Collect before acting:
- Exact symptom: error text, stack trace, expected versus actual output, timestamps.
- Environment: commit or build identifier, runtime and dependency versions from the lock file, OS, configuration, feature flags.
- Reproduction data: inputs, seed values, request payloads, sanitized sample records.
- Change history: commits, deploys, or dependency updates within the suspect window.

Assumptions must be written down. If the environment cannot be matched, record the gap and treat conclusions as provisional.

## Operating workflow

1. **State the symptom precisely.** Write one sentence: "Given X, the system does Y, but expected Z." Reject vague phrasing such as "it's broken."
2. **Reproduce deterministically.** Find the smallest input and environment that fails every time. For intermittent failures, run the case in a loop (for example 100 iterations) and record the failure rate before and after any change.
3. **Bisect the space.** Narrow by commit (binary search over history with a reliable pass/fail check), by input (delta-minimize the failing input), or by component (add boundary assertions or logs at interfaces).
4. **Form ranked hypotheses.** List at least two candidate causes. For each, state a prediction that would be false if the hypothesis were wrong.
5. **Test one hypothesis at a time.** Change one variable, observe, and record the result. Do not stack speculative edits.
6. **Explain the mechanism.** A root cause answers: what condition, in which code path, produced the wrong state, and why the symptom appeared where it did.
7. **Apply the minimal fix** at the cause, not at the symptom location.
8. **Add a regression guard** that fails before the fix and passes after.

## Decision gates

- **Gate A, reproduction:** Proceed to fixing only when the failure reproduces reliably, or when the failure rate is measured and documented for intermittent cases. If it cannot be reproduced after reasonable effort, stop and report what was tried; do not guess a fix.
- **Gate B, cause identification:** Proceed only when a single hypothesis is confirmed by evidence that the alternatives fail to explain. Correlation alone does not qualify.
- **Gate C, scope:** If the fix requires changing more than the failing module's contract, schema, public API, or data, stop and seek approval.
- **Gate D, flaky tests:** Do not increase timeouts, add retries, or delete assertions as the primary fix until a race, ordering dependency, shared state, or time dependency has been ruled in or out.

## Verification and evidence

Each conclusion must cite evidence:
- Reproduction command and observed output, before and after.
- The regression test name and its failure on the unfixed commit.
- Full existing test suite for the affected package passes, with the count of tests run recorded.
- For performance causes, measured timings from at least five runs with the same method before and after.

Quality checks:
- The regression test fails on the pre-fix code. Confirm this explicitly; a test that passed before the fix proves nothing.
- The fix diff touches the minimum set of files; record the line count.
- No new skips, disabled tests, broadened exception handlers, or widened tolerances unless justified in writing.

Mark version-sensitive details (runtime flags, debugger commands, library behavior changes) as requiring verification against current official documentation before relying on them.

## Failure handling

- **Cannot reproduce:** Report the attempted environments, inputs, and the gap. Request production-equivalent data or logs. Do not ship speculative changes.
- **Multiple causes found:** Fix them separately, each with its own test and evidence, and state which symptom each explains.
- **Fix breaks other tests:** Revert the hypothesis, re-examine whether the existing tests encoded incorrect behavior, and escalate that question rather than silently editing expectations.
- **Evidence contradicts hypothesis:** Discard it explicitly and return to step 4.

## Deliverable contract

Produce a report containing:
1. Symptom statement and environment identifiers.
2. Reproduction steps and measured failure rate.
3. Ranked hypotheses with the evidence for and against each.
4. Root cause in one paragraph naming the code path and triggering condition.
5. Patch summary, changed files, and minimal diff rationale.
6. Regression test name and before/after results.
7. Open risks and unverified assumptions, including any version-sensitive items.

## What not to do

- Do not apply a fix before a cause is confirmed.
- Do not catch and suppress the exception to make the symptom disappear.
- Do not add sleeps, retries, or longer timeouts to hide races.
- Do not run destructive commands (dropping databases, force-resetting shared branches, deleting production data or logs) without explicit approval.
- Do not send sanitized or unsanitized production data, credentials, or customer records to external tools or services without explicit approval.
- Do not deploy, roll back, or change feature flags in shared environments without explicit approval.
- Do not invent flags, API names, or benchmark numbers; verify them against current documentation.