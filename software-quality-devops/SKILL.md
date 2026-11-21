---
name: software-quality-devops
description: Use when designing, reviewing, or repairing CI/CD pipelines, test gates, release checks, or deployment safeguards for software projects, including when an AI agent must make or recommend changes to build, test, or deploy automation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Software Quality DevOps

## Purpose and boundaries

This skill covers the quality and delivery path between a committed change and a running artifact: build reproducibility, automated test gates, static and security checks, artifact promotion, deployment safeguards, and rollback readiness. It produces findings, pipeline changes, and release recommendations backed by evidence.

Out of scope: product feature design, infrastructure cost optimization, incident commander duties, and writing application code beyond what a pipeline fix requires.

## Inputs and assumptions

Collect before acting:
- Repository layout, default branch, and branch protection rules (read-only view).
- Pipeline definitions and their last 5 run logs, including failures.
- Test inventory: unit, integration, end-to-end, and their typical durations and flake history.
- Target environments and how promotion between them occurs.
- Current release cadence and rollback mechanism.

Assumptions to state explicitly in every deliverable: the CI platform in use, the language runtime versions, and whether secrets are injected at runtime. If any is unknown, mark it as unknown rather than guessing.

Version-sensitive details (action versions, runner images, tool flags, language runtime support windows) must be verified against current official documentation before being recommended. Do not present them from memory as current.

## Operating workflow

1. **Map the path.** List every stage from commit to production in order. Note which stages are gating, which are advisory, and which are skipped on some branches.
2. **Measure baseline.** Record median and p90 pipeline duration, failure rate by stage, and flake rate (failures that pass on immediate rerun without code change) over the sampled runs.
3. **Classify failures.** Bucket each failure as: real defect caught, environment problem, flaky test, configuration drift, or dependency change. Only the first is evidence the gate works.
4. **Identify gaps.** Compare coverage of checks against change risk: schema migrations without a rollback test, auth changes without security scanning, config changes without validation.
5. **Propose minimal changes.** Prefer one change per finding, ordered by risk reduction per unit of effort. Each change must name the failure it prevents.
6. **Validate in a non-production branch or staging pipeline** before proposing promotion to protected branches.

## Decision gates

Pause and request explicit human approval before:
- Modifying branch protection, required-check lists, or environment approval rules.
- Changing deployment targets, production secrets, or credentials of any kind.
- Deleting or force-rewriting pipeline history, artifacts, caches, or release tags.
- Triggering a production deployment, rollback, database migration, or data-altering job.
- Disabling a failing gate to unblock a release.
- Any action that sends notifications, opens external tickets, or publishes packages to a registry.

Proceed without approval only for read-only analysis and changes on feature branches that do not alter protections or secrets.

Quality threshold decisions: a gate may be relaxed only if the failing check is confirmed flaky by repeated runs (at least three reruns with identical results distribution documented) or confirmed misconfigured. Record the reason and an expiry date.

## Verification and evidence

Every recommendation must cite:
- The specific run ID or log excerpt that motivates it.
- The before and after metric (duration, failure count, flake rate) measured over a stated number of runs.
- Confirmation that the change was exercised, not only parsed.

Measurable quality checks to report:
- Pipeline p90 duration within the agreed budget.
- Flake rate below 2% per test suite, or the suite is quarantined with an owner.
- Zero unpinned external dependencies in build steps, or each unpinned one is listed with justification.
- Every production-bound artifact has a recorded build provenance and a checksum.
- Rollback path rehearsed within the last release cycle.

Domain examples:
- A nightly integration suite that fails only when run after a cache restore indicates a cache-key defect, not a test defect. Fix the key, not the test.
- A migration job that passes on empty fixtures but fails on production-sized data indicates missing scale-representative test data.
- A dependency update that changes a transitive version and breaks the build requires a lockfile diff review before merging.

Never claim a check passed unless its output was observed in this session or in cited logs.

## Failure handling

- If logs are incomplete or truncated, state what is missing and do not infer the cause.
- If a fix attempt fails twice, stop and report the hypotheses tested and their results.
- If a proposed change would weaken a gate, escalate under Decision gates.
- If the pipeline cannot be run in a safe environment, deliver analysis only and label recommendations as unverified.

What not to do:
- Do not add retries as a blanket fix for failing tests.
- Do not increase timeouts without identifying the slow step.
- Do not mark tests as skipped to achieve green status.
- Do not store secrets in pipeline files, logs, or deliverables.
- Do not state compliance outcomes (for example, that a pipeline satisfies a named standard); describe controls present and gaps instead.

## Deliverable contract

Produce a single report with these sections in order:
1. **Summary**: three sentences maximum, including overall risk rating (low, medium, high) with the reason.
2. **Assumptions and unknowns**: explicit list.
3. **Baseline metrics**: table of duration, failure rate by stage, flake rate, with sample size.
4. **Findings**: each with ID, evidence reference, classification, and severity.
5. **Recommended changes**: ordered list, each with the failure prevented, the exact file or setting affected, and verification steps.
6. **Approval requests**: every item from Decision gates that applies, stated as a question.
7. **Version-sensitive items to verify**: list of tool, action, or runtime references needing confirmation against current official documentation.

Keep the report under 1,500 words unless the user requests more detail.