---
name: cicd-and-progressive-delivery
description: Use when designing, reviewing, or troubleshooting CI/CD pipelines and progressive delivery rollouts (canary, blue-green, feature-flag gating, automated rollback) for services deployed to cloud or container platforms.
author: Luo Kai
provenance: original
version: 1.0.0
---

# CI/CD and Progressive Delivery

## Purpose and boundaries

This skill guides the design and review of build, test, and deployment pipelines and the staged rollout of changes to production traffic. It covers:

- Pipeline stage structure, artifact promotion, and environment parity.
- Rollout strategies: rolling, blue-green, canary, and percentage or cohort-based feature flags.
- Metric-driven promotion and automated or manual rollback decisions.

It does not cover: application architecture, infrastructure provisioning internals (see infrastructure-as-code skills), incident command, or security tooling selection. Tool-specific syntax must be checked against current vendor documentation; this skill does not assert exact flags, field names, or versions.

## Inputs and assumptions

Before proposing changes, collect:

1. Service inventory: runtime, deployment target (Kubernetes, VM fleet, serverless, managed PaaS), statefulness, and dependency graph.
2. Current pipeline definition and the last 20 run outcomes with durations.
3. Existing SLIs and SLOs (error rate, latency percentiles, saturation) and their data source.
4. Database and schema change history; whether migrations are backward compatible.
5. Traffic profile: request volume, peak windows, and minimum volume needed for statistically meaningful canary comparison.
6. Rollback mechanism currently available and its measured time to execute.

If any input is missing, state the assumption explicitly in the deliverable. Do not assume zero-downtime capability, schema compatibility, or metric coverage without evidence.

## Operating workflow

1. **Map the path to production.** List every stage from commit to full traffic. Mark each stage as automated, manual, or gated, and record its median duration.
2. **Verify artifact immutability.** Build once; promote the same digest or artifact through environments. Rebuilding per environment is a finding.
3. **Check test placement.** Unit and static checks run on every commit; integration and contract tests run before artifact promotion; end-to-end smoke tests run after each deploy. Flag suites that run only nightly on a path that ships daily.
4. **Classify each change.** Label as stateless code, configuration, schema migration, or infrastructure. Each class has a different rollout ceiling (see Decision gates).
5. **Select a strategy per service tier.** Match the strategy to blast radius and rollback speed.
6. **Define promotion metrics before rollout.** Write the thresholds in the plan: for example, canary error rate no more than baseline plus a stated margin, p99 latency within a stated ratio of baseline, and no new error signatures in logs. Thresholds must be derived from observed baseline data, not chosen arbitrarily.
7. **Specify rollback triggers and procedure.** Automated rollback on hard SLO breach; human decision on soft signals. Record the expected rollback duration and test it.
8. **Produce the rollout plan** using the deliverable contract below.

## Decision gates

- **Canary sizing:** Do not conclude a canary comparison until the canary cohort has accumulated enough requests to detect the target regression at the chosen confidence level. If volume is too low, extend the observation window or use synthetic traffic, and say so.
- **Schema changes:** Require expand-then-contract sequencing. A deploy that removes or renames a column used by the previous version must not proceed without an explicit approval gate and a verified rollback path.
- **Feature flags:** Flags introduced for rollout must have an owner and a removal date. Flags controlling data-writing paths require the same review as schema changes.
- **Blue-green:** Permitted only when the environment doubles cost acceptably and session or cache state is shared or drainable.
- **Full promotion:** Requires that the canary or first cohort met all promotion thresholds for the defined window, with no unexplained error signatures.
- **Approval required (human, explicit):** Any production deployment outside the normal change window, any action that deletes data or environments, any rollback of a schema migration, any change affecting external customers or partners, and any step that touches credentials, secrets, or access policies.

## Verification and evidence

Each recommendation must cite evidence:

- Pipeline timing from actual run history, not estimates.
- Baseline metrics over at least one representative traffic cycle (for example, one full weekday peak).
- Canary comparison results showing both cohorts, the metric, the window, and sample sizes.
- Rollback rehearsal result with measured duration.

Quality checks:
- Every promotion threshold names a metric, a comparison baseline, a window, and an action.
- Artifact digest or version is identical across all promoted environments.
- Every stage has an owner and a failure action.
- No gate depends on a manual step that has no documented timeout or escalation.

## Failure handling

- **Failed promotion metric:** Halt the rollout at current percentage; do not auto-advance. Roll back if the breach is a hard SLO violation; otherwise hold and request review.
- **Inconclusive canary (insufficient data):** Extend the window once; if still inconclusive, report it as inconclusive rather than passing it.
- **Rollback failure:** Escalate immediately to the on-call owner. Do not attempt a second untested rollback path without approval.
- **Flaky tests blocking promotion:** Quarantine the test with a tracked ticket and an expiry; do not disable the gate globally.
- **Metric pipeline outage:** Treat as failed verification. Pause promotions; do not infer health from absence of alerts.

## Deliverable contract

The output must contain:

1. **Current-state summary:** stages, durations, strategy per service, and identified gaps.
2. **Change classification** for the proposed release.
3. **Rollout plan table:** step, traffic percentage, duration or sample requirement, promotion thresholds, rollback trigger.
4. **Assumptions register:** each unverified assumption with the verification owner.
5. **Approval requests:** list of actions requiring explicit human approval, with the risk and reversibility stated.
6. **Version-sensitive items:** any tool features, flags, or API behaviors referenced, marked "verify against current official documentation" with the vendor name.
7. **Open risks** ranked by impact.

Do not state that a deployment is safe, compliant, or guaranteed to meet any SLO. State what was measured and what remains unverified.

## What not to do

- Do not rebuild artifacts between environments.
- Do not set canary thresholds without baseline data.
- Do not advance a rollout on elapsed time alone.
- Do not run destructive operations (environment deletion, data rollback, forced database changes) without explicit approval.
- Do not disable failing gates to unblock a release.
- Do not present unverified tool behavior as fact.