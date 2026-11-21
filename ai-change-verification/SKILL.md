---
name: ai-change-verification
description: Use when an AI-generated or AI-assisted code, configuration, prompt, or documentation change must be checked before merge or release, to confirm it does what was intended, breaks nothing, and leaves an auditable evidence trail.
author: Luo Kai
provenance: original
version: 1.2.0
---

# AI Change Verification

## Purpose and boundaries

This skill verifies changes produced or substantially shaped by an AI model. The goal is to establish, with evidence, that a change (1) implements the stated intent, (2) does not regress existing behavior, (3) introduces no unreviewed security, data, or dependency risk, and (4) is reproducible by a human reviewer.

In scope: diffs to source code, tests, infrastructure-as-code, SQL migrations, prompts and prompt templates, evaluation configs, and technical documentation that describes behavior.

Out of scope: deciding product direction, authoring net-new features from scratch (use a design skill for that), and certifying regulatory compliance. Do not claim compliance; report only what was checked.

## Inputs and assumptions

Required before starting:
- The change: diff or commit range, plus the base revision.
- Intent: a ticket, issue, or plain statement of expected behavior. If absent, write one from the diff and get the author to confirm it. Do not verify against an intent you invented without confirmation.
- Affected surfaces: services, public interfaces, data stores, and configuration keys touched.
- Existing test and check commands for the repository. Discover them from project files and CI config; do not assume.

Assumptions to state explicitly in the report: the base revision was green before the change; the test environment resembles production in the dimensions the change touches.

## Operating workflow

1. **Scope the diff.** List every changed file. Classify each as behavior, test, config, dependency, generated, or documentation. Flag generated files and confirm their source of truth was changed instead.
2. **Restate intent as testable claims.** Produce 3 to 10 numbered claims in the form "Given X, when Y, then Z." Each claim must map to at least one check.
3. **Read, do not trust.** Review the diff line by line for: silent exception swallowing, hardcoded credentials or environment values, widened permissions, removed validation, altered defaults, deleted or weakened assertions, and unexplained new dependencies.
4. **Check tests against claims.** For each claim, confirm a test exists and would fail on the base revision. A test that passes on both revisions does not verify the claim. Run it against base to confirm.
5. **Run the existing suite** on the change, then the new or modified tests in isolation, then once more with a fixed random seed or repeated runs if the code has concurrency or ordering sensitivity.
6. **Run static and security checks** the repository already uses (linter, type checker, dependency audit, secret scanner). Record new findings only; pre-existing findings go in an appendix.
7. **Exercise the boundary.** For changed interfaces, test at least: a valid nominal input, one invalid input, one empty or null input, and one boundary value.
8. **Verify migrations and config** on a disposable copy: apply forward, confirm, and where a rollback path is claimed, apply and confirm it.
9. **For prompts or model-facing text**, run the fixed evaluation set before and after the change, using identical model settings. Report the per-case diff, not only the aggregate.
10. **Write the report** using the deliverable contract below.

## Decision gates

- **Gate A (scope):** If the diff exceeds roughly 400 changed lines or mixes unrelated concerns, request a split before deep review.
- **Gate B (intent):** If intent cannot be confirmed by a human, stop and mark the result "unverified: intent unconfirmed."
- **Gate C (regression):** Any previously passing test that now fails blocks approval until the cause is explained and the change or test is corrected with justification.
- **Gate D (security):** Any new secret-like string, widened IAM or ACL scope, disabled certificate check, or new network egress target requires explicit human approval.
- **Gate E (destructive operations):** Any migration that drops, truncates, or rewrites data, any force-push, any production command, and any action that sends data to an external service requires explicit written approval from the owning maintainer before execution. Do not run such steps on shared or production resources under any circumstances without that approval.
- **Gate F (model drift):** If the evaluation shows a regression on more than 5% of previously passing cases, or on any case tagged safety-critical, block and escalate.

## Verification and evidence

Each claim receives one status: **verified** (test fails on base, passes on change, and was run), **partially verified** (covered by reasoning or a weaker test only), or **unverified**.

Evidence to record per check: exact command, revision hash, environment identifier, exit status, and the relevant output excerpt. Do not paraphrase results as passing without the command that produced them.

Quality thresholds:
- Every claim has a status and at least one evidence item.
- Zero new unexplained static-analysis or secret-scan findings.
- Changed lines have line or branch coverage not lower than the base for the touched modules, as reported by the project's own tool.
- Flaky tests: a test that fails then passes on rerun is reported as flaky, not as passing.

Do not state benchmark numbers, performance improvements, or security guarantees unless measured in this review and reported with method.

## Failure handling

- **Test fails on change, passes on base:** Treat as a regression. Identify the smallest failing input, bisect the diff if multiple edits are involved, and report the root cause before proposing a fix.
- **Test passes on both:** The test does not verify the claim. Mark the claim partially verified and propose a discriminating test.
- **Environment cannot reproduce:** Record the missing dependency or access, do not substitute assumptions silently, and downgrade affected claims.
- **Evaluation results are noisy:** Rerun identical settings at least three times, report the spread, and do not claim improvement inside the noise band.
- **Reviewer disagrees with a status:** Keep the status with the evidence attached, and escalate rather than editing the report to match the disagreement.

## Deliverable contract

Produce a single report with these sections, in this order:

1. **Summary:** one of APPROVE, APPROVE WITH CONDITIONS, BLOCK, or UNVERIFIED, with one sentence of reasoning.
2. **Scope:** file classification table and total changed lines.
3. **Claims:** numbered list, each with status and evidence references.
4. **Findings:** new issues by severity (blocking, major, minor), each with file, line, and reproduction.
5. **Commands run:** exact commands, revision hashes, environment identifiers, and exit codes.
6. **Approvals requested:** every gate triggered, with the approver required.
7. **Limitations:** what was not checked and why.
8. **Appendix:** pre-existing findings, clearly separated from new ones.

Do not omit the limitations section. A review with no stated limitations is not credible.
## AI change provenance and release evidence (v1.1)

Treat every AI-assisted change as a traceable transformation. Bind the change request, accepted intent, base revision, candidate revision, tool/model configuration, generated artifacts, test run, reviewer decision, and release decision into one change record. Keep generated output distinguishable from human-authored edits where practical; authorship labels must not be used as a substitute for review.

For every changed behavior, write a claim and a discriminating test that fails on the base revision and passes on the candidate. Add negative assertions for forbidden behavior, permission expansion, unintended network access, secret exposure, and unexpected file or data mutation. A test that passes on both revisions does not prove the change.

Review generated dependencies, migrations, configuration defaults, and scripts as carefully as application code. Check that examples and documentation do not introduce unsafe commands or claim unsupported capabilities. For prompt or skill changes, compare trajectories under a frozen evaluation suite and inspect regressions case by case.

Before release, produce a reproducibility bundle: exact revisions, commands, environment, test outputs, static-analysis findings, approvals, and known limitations. If any result cannot be reproduced, downgrade its status. Keep rollback instructions and identify the exact artifact or configuration to restore.

## Ultron routing contract

**Choose this skill when:** approving a concrete AI-generated or AI-assisted change to code, configuration, documentation, infrastructure, or data transformation. It owns provenance, baseline-versus-candidate comparison, discriminating tests, negative assertions, reproducibility, and rollback evidence.

**Choose `code-review-and-test-generation` when:** the change needs a structured diff review and new regression tests.

**Choose `code-review-execution` when:** an independent reviewer must assess the patch and issue a merge recommendation without authoring the change.

**Choose `agent-evaluation-design` when:** the question is whether an agent/model behavior or release should pass a reusable evaluation policy, rather than whether one specific artifact is correct.

**Handoff contract:** receive the exact candidate diff and base identity, test evidence, affected surfaces, and expected external postconditions. Return a traceable change decision with tests, failures, residual risks, and rollback artifact. Do not treat a model's explanation of its own change as verification.

**Why the boundary exists:** artifact correctness, independent code review, and agent capability evaluation are related but distinct assurance claims.
