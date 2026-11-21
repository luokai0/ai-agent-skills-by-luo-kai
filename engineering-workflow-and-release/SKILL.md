---
name: engineering-workflow-and-release
description: Use when planning, reviewing, or executing a software delivery workflow, branching and merge strategy, build-to-release pipeline, or release cutover for an engineering team, including release readiness checks, rollback planning, and release notes.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Engineering Workflow And Release

## Purpose and boundaries

This skill governs how a change moves from proposal to production: branching, review, integration, build, verification, release, and rollback. It produces workflow designs, release plans, readiness assessments, and release records.

In scope: branching model selection, merge policy, required checks, versioning scheme, release train or cadence, environment promotion, change freeze rules, rollback and roll-forward plans, release notes, and post-release review.

Out of scope: application architecture decisions (use a design-review skill), incident command during a live outage, security policy authoring, and vendor-specific CI syntax without checking current official documentation.

## Inputs and assumptions

Collect before advising:
- Team size, number of services or deployable units, and deployment targets.
- Current branching and merge practice, and the pain it causes (conflicts, late integration, unreleased work piling up).
- Existing CI stages, test suites with approximate runtime and flake rate, and artifact types.
- Release frequency goal and customer or regulatory constraints on change windows.
- Data stores and schema change practices, since these dominate rollback difficulty.

If any of these are missing, state the assumption explicitly in the deliverable. Do not assume a specific CI product, cloud provider, or tool version. Mark any tool-specific behavior as "verify against current official documentation."

## Operating workflow

1. Map the current path from commit to production. Record each stage, owner, average duration, and failure rate.
2. Identify the dominant bottleneck: integration delay, unreliable tests, manual approvals, environment drift, or schema coupling.
3. Select a branching model matched to release cadence. Short-lived trunk-based branches suit frequent deploys; release branches suit multiple supported versions. Do not adopt a long-lived integration branch to hide unfinished work.
4. Define merge requirements: review count, required status checks, linear or merge-commit policy, and who may bypass checks (ideally nobody).
5. Define versioning: state the scheme and where the version is derived (tag, manifest, or build metadata). Confirm it is unique per artifact.
6. Design promotion: build once, promote the same immutable artifact through environments. Rebuilding per environment is a defect.
7. Separate deploy from release. Use flags, traffic shifting, or staged rollout where the platform supports them; verify exact mechanisms against current documentation.
8. Write the rollback path for each release, classified by reversibility (see Decision gates).
9. Draft release notes from merged change records, grouped by user impact, with breaking changes first.

## Decision gates

Proceed to release only when all hold:
- All required checks pass on the exact artifact being promoted.
- Migration review is complete: schema changes are backward compatible with the previous application version (expand, migrate, contract).
- Rollback is classified and tested or rehearsed for the release's reversibility class.
- On-call owner and release lead are named, and the change window is confirmed.

Escalate for explicit human approval before:
- Any irreversible data migration, deletion, or column drop.
- Changes that affect external partners, public APIs, billing, or customer data.
- Bypassing a required check, force-pushing to protected branches, or deleting release tags.
- Releasing outside an agreed change window or during a declared freeze.
- Handling credentials, personal data, or regulated records in release tooling.

Reversibility classes:
- R1: code-only, stateless; roll back by redeploying prior artifact.
- R2: backward-compatible schema change; roll back by code redeploy, keep schema.
- R3: one-way data transformation or contract step; rollback requires a restore plan and explicit approval before release.

## Verification and evidence

Each release must carry evidence, not assertions:
- Artifact identifier and digest matching what was tested and promoted.
- Test results for the candidate, with failing or quarantined tests listed and justified.
- Canary or staged metrics compared against a stated baseline: error rate, latency percentile, and saturation signals. Set thresholds before rollout.
- Migration dry run result against a production-like copy, with duration measured.
- Rollback rehearsal result or a dated statement that it was not rehearsed, with reason.

Quality checks for the workflow itself:
- Median commit-to-production time and change failure rate are measured, not estimated. Report both with the measurement window.
- Flaky-test quarantine count is tracked and trending down; no test stays quarantined beyond an agreed period.
- Zero manual edits to artifacts between build and production.

Do not state benchmark figures, DORA tier placements, or compliance guarantees unless the user supplies the measured data.

## Failure handling

- Check failure on candidate: stop promotion, do not waive. Route to owner with failing evidence.
- Metric regression during rollout: halt traffic increase, execute the classified rollback, preserve logs and artifact identifiers.
- Migration fails midway: stop, do not retry destructively; assess whether the application can run on current schema, then escalate for approval.
- Missing rollback path discovered late: block release until one exists or the change is reclassified and approved.
- Ambiguous tool behavior: record the uncertainty and the documentation to verify; do not guess flags or syntax.

## Deliverable contract

Produce a single document containing:
1. Current-state map with measured stage durations and the identified bottleneck.
2. Recommended branching, merge, versioning, and promotion policy with rationale tied to cadence.
3. Per-release checklist with reversibility class, gate status, named owners, and window.
4. Approval requests, listed separately, for every action in the escalation list.
5. Evidence index linking artifact digest, test results, migration dry run, and rollout metrics.
6. Assumptions list and items marked for verification against current official documentation.
7. Release notes draft, breaking changes first.

Do not produce: unverified tool commands, invented metrics, or a plan that deploys unbuilt or untested artifacts.