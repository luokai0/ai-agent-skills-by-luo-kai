---
name: build-dependency-devx
description: Use when diagnosing, redesigning, or hardening developer experience for build systems and dependency management, including slow or flaky builds, lockfile drift, version conflicts, monorepo dependency graphs, cache misconfiguration, and onboarding friction.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Build Dependency Devx

## Purpose and boundaries

This skill covers the developer-facing health of a project's build and dependency layer: how dependencies are declared, resolved, locked, cached, and consumed, and how quickly and reliably a developer can go from clone to passing build. It applies to single packages, multi-package workspaces, and monorepos across common language ecosystems.

In scope: dependency declaration hygiene, lockfile policy, version range strategy, build graph and task caching, incremental build correctness, reproducibility of local builds, toolchain pinning, developer bootstrap scripts, and build-time diagnostics.

Out of scope: application feature code, runtime performance tuning, CI vendor billing, and security policy decisions (flag these and route them to the owning team).

## Inputs and assumptions

Collect before changing anything:
- Manifests and lockfiles (exact filenames present).
- Build tool and version, runtime versions, and any version managers in use.
- Clean-clone build time, incremental rebuild time, and a representative failure log.
- Cache configuration (local and remote), and whether remote cache is shared across branches or trust levels.
- Who owns each package or directory.

Assume nothing about registry mirrors, private registries, or network access. Verify them. If the environment cannot be reproduced, state that the findings are unverified.

## Operating workflow

1. **Baseline.** Record clean build time, incremental build time, and count of distinct resolved versions per major dependency. Capture these in a table; they are the before-metrics.
2. **Classify failures.** Group issues into: resolution (conflicting ranges), drift (manifest and lockfile disagree), hidden inputs (build reads undeclared files, env vars, or clock), cache poisoning or misses, toolchain mismatch, and bootstrap gaps.
3. **Trace the graph.** For each failing task, identify its declared inputs and outputs. Compare against what it actually reads. Undeclared inputs are the most common cause of incorrect cache hits and flaky builds.
4. **Propose minimal changes**, ordered by reversibility: pin toolchain versions, fix declarations, adjust ignore patterns, then restructure task graphs. Do not bundle unrelated changes.
5. **Apply in a branch**, one concern per commit, each with its before/after metric.
6. **Verify** using the checks below, then document the bootstrap path.

## Decision gates

Stop and request explicit approval before:
- Deleting or regenerating a lockfile, or running a major dependency upgrade.
- Changing remote cache write permissions or sharing cache entries across trust boundaries.
- Altering publish, release, or registry configuration.
- Modifying shared CI pipeline definitions used by other teams.
- Adding or removing dependencies that carry license, security, or export-control implications.
- Any action that affects other developers' machines (global installs, shared volumes).

Proceed without approval only for: local, reversible edits on a branch; adding declared inputs to a task; pinning a toolchain to a version already in use by the majority of developers; and documentation.

Choose a version range strategy by criteria: libraries use permissive ranges with a lockfile for applications and tests; applications pin exactly; monorepo internal packages use workspace protocols rather than published versions.

## Verification and evidence

Each change must show:
- Clean-clone build succeeds on a fresh checkout (no cached artifacts, no global state).
- Incremental build after touching one source file rebuilds only dependent tasks. Verify with the tool's task-explanation output, not assumption.
- Running the build twice with no changes produces zero task execution.
- `lockfile check` in CI-equivalent mode passes without modifying files. Use the tool's frozen or immutable install mode; confirm the exact flag against current official docs, as names vary by version.
- Dependency duplicate count does not increase. Report the count before and after.
- Bootstrap steps executed in a clean container or fresh user account, timed.

Quality targets (set as project goals, not guarantees): clean build under the agreed baseline, zero flaky reruns across five consecutive runs, and every task's inputs enumerated.

Mark any command syntax, flag, or version-specific behavior as "verify against current official documentation" unless confirmed in this repository.

## Failure handling

- If a clean build fails after a change, revert that commit rather than patching forward silently.
- If a cache hit produces wrong output, disable that cache entry scope, record the reproduction, and widen declared inputs before re-enabling.
- If lockfile regeneration changes many unrelated versions, stop and report the diff summary; do not commit it.
- If the failure cannot be reproduced, record environment details (OS, runtime versions, tool versions, network state) and mark the finding unverified.
- Never suppress warnings or skip tasks to make a build green.

## Deliverable contract

Produce:
1. Findings table: issue, category, evidence (log excerpt or command output), severity, owner.
2. Change list: one entry per commit with rationale and before/after metric.
3. Verification record: the checks above with pass/fail and environment.
4. Bootstrap document: ordered steps a new developer runs, with expected duration and known failure modes.
5. Open items: approval requests, unverified findings, and items routed to other owners.

Do not claim improvements without measured before/after data. Do not present unverified version or flag details as fact.