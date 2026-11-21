---
name: code-quality-maintenance
description: Use when reviewing, refactoring, or stabilizing an existing codebase for readability, maintainability, lint and type cleanliness, dead code, duplication, complexity, or test health, without changing intended behavior.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Code Quality Maintenance

## Purpose and boundaries

This skill covers incremental improvement of existing code: reducing complexity, removing dead and duplicated code, tightening types and lint compliance, clarifying naming and structure, and repairing flaky or misleading tests. The governing constraint is behavior preservation. Every change must be justified by a measurable quality signal and verified against existing or newly added tests.

In scope: refactors within a module or service, lint and type remediation, dead-code removal confirmed by reference search, test cleanup, dependency hygiene inside a single repository, and documentation of invariants that the code already relies on.

Out of scope: new features, architectural rewrites, performance tuning without a profile, security-policy changes, dependency upgrades that change major versions, and anything touching production infrastructure or data.

## Inputs and assumptions

Before starting, establish:

1. The repository, branch, and a clean working tree. Record the base commit.
2. The quality target: a specific module, a metric threshold, a lint rule set, or a named pain point (for example, "the billing module has 40 duplicated validation blocks").
3. The project's existing toolchain: linters, formatters, type checker, test runner, coverage tool. Read the configuration files rather than assuming defaults. Version-specific flags and rule names must be checked against the tool's current official documentation before use.
4. Whether a reliable test suite exists for the target area. If coverage is absent or the suite is flaky, treat that as the first finding, not a license to refactor blindly.
5. Public interfaces that external consumers depend on (exported functions, HTTP contracts, serialized schemas, CLI arguments). These are frozen unless the owner approves change.

If any assumption is unverified, state it in the deliverable.

## Operating workflow

1. **Baseline.** Run the full test suite, type checker, and linter on the untouched tree. Record pass/fail counts, warning counts, and coverage for the target scope. Save the output.
2. **Measure.** Collect concrete signals: cyclomatic complexity per function where the toolchain provides it, function length, duplicate-block counts, unused exports and imports, `any` or untyped usages, and skipped or quarantined tests. Rank findings by impact-to-risk ratio.
3. **Select a batch.** Choose one cohesive batch of 3 to 10 related changes in one module. Small batches keep review and rollback cheap.
4. **Characterize before changing.** For code with weak tests, write characterization tests that pin current observable behavior, including odd behavior, and mark them as characterization. Do not "fix" pinned behavior in the same batch.
5. **Refactor in small steps.** Apply one transformation at a time (extract function, rename, inline single-use helper, replace conditional chain with lookup, narrow a type). Run the relevant tests after each step.
6. **Remove dead code only with evidence.** Confirm no references exist via static search, and check dynamic access patterns (reflection, string-based dispatch, configuration references, generated code). Dead code that is referenced by configuration is not dead.
7. **Re-measure.** Repeat the baseline commands and compare.
8. **Commit in logical units.** One commit per transformation type, with messages stating what changed and why.

## Decision gates

Stop and request approval before proceeding when any of the following apply:

- The change alters a public interface, serialized format, database schema, or message contract.
- Removing code would delete a path that tests do not cover and that cannot be confirmed as unreachable.
- The change requires a dependency upgrade, a new dependency, or a change to build or CI configuration.
- Lint or type rules would be disabled, loosened globally, or suppressed in bulk rather than per line with a reason.
- Coverage on the target scope would drop.
- Any action would touch data stores, deploy artifacts, rotate credentials, or alter shared CI resources. These require explicit human approval; do not proceed on inference.

Proceed without asking only for changes that are internal, covered by passing tests, and reversible by reverting a commit.

## Verification and evidence

A change is accepted only when all of the following hold:

- Full test suite passes with no new skips, and no test was weakened (assertions removed, tolerance widened, or timeouts raised to mask failures).
- Type checker and linter report no new errors; warning count in scope is equal or lower.
- Target metric improved: for example, function count above complexity threshold dropped, or duplicated blocks reduced, measured with the same tool and settings as the baseline.
- Public API diff is empty, verified by comparing exported symbols or generated signatures.
- For dead-code removal: search results show zero references across source, tests, configuration, and documentation, and the build succeeds.

Record evidence as a table: metric, baseline, after, command used.

## Failure handling

- **Test fails after a refactor step:** revert that step, not the batch. Diagnose whether the test encodes an assumption the refactor violated. Fix the refactor, not the test, unless the test is demonstrably wrong and the owner agrees.
- **Flaky test appears:** rerun in isolation to classify. Quarantine only with an owner-approved ticket reference; never silently delete.
- **Metric regresses:** a tool may flag new issues caused by a rename or extraction. Address them within the batch or revert.
- **Unexpected behavior discovered:** stop, document the observation with a reproduction, and escalate. Do not patch behavior under a quality label.

## Deliverable contract

Produce:

1. A summary of baseline and final metrics with exact commands.
2. A list of changes grouped by batch, each with its rationale and commit reference.
3. An explicit list of deferred items with reasons (approval needed, unclear behavior, out of scope).
4. Any unverified assumptions, including tool versions and configuration details requiring confirmation against current official documentation.
5. Residual risks, stated plainly.

What not to do: do not bundle behavior changes with cleanup, do not suppress warnings to pass gates, do not reformat entire files unrelated to the batch (this inflates diffs and hides real changes), do not invent tool flags or rule identifiers, and do not claim quality improvements that were not measured.