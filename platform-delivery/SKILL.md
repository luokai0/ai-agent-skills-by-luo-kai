---
name: platform-delivery
description: Use when shipping, promoting, or rolling back a frontend application through build, preview, staging, and production environments, including CI/CD pipeline changes, asset hosting, cache and CDN configuration, environment variables, and release verification for web apps.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Platform Delivery

## Purpose and boundaries

This skill covers getting a frontend build from a commit to users safely: build configuration, artifact creation, environment promotion, static hosting and CDN behavior, cache invalidation, feature exposure, and rollback. It applies to single-page apps, server-rendered frontends, and static sites.

It does not cover application feature logic, backend API design, database migrations, or infrastructure provisioning beyond the frontend's own hosting. Hand those to the owning skill or team.

## Inputs and assumptions

Collect before acting:

- Target platform (static host, CDN, container, edge runtime, or SSR server) and its current documentation version.
- Build tool and framework versions from the lockfile. Do not assume them from memory.
- Environment matrix: which variables differ per environment and which are build-time versus runtime.
- Current production artifact identifier and the last known-good release.
- Caching rules: asset hashing scheme, HTML cache headers, CDN TTLs, service worker presence.
- Who owns approval for production promotion.

If any item is unknown, state the assumption in the delivery record and mark it unverified.

## Operating workflow

1. **Freeze the candidate.** Identify the exact commit and lockfile. Confirm the build is reproducible: a clean install and build from the lockfile must produce the same asset manifest hashes twice in succession, or differences must be explained.
2. **Audit configuration diffs.** Compare environment variables and build flags against the previous release. List every changed key. Flag any secret-looking value that appears in client bundles.
3. **Build once, promote many.** Produce one immutable artifact and deploy the same bytes to preview, staging, and production. Rebuilding per environment is forbidden unless the difference is strictly runtime configuration.
4. **Deploy to preview or staging.** Verify routing, asset paths, base URL, and `index.html` cache headers.
5. **Run verification** (see below) against staging.
6. **Request promotion approval** with the evidence bundle.
7. **Promote** using the platform's atomic alias or pointer switch, not file-by-file copies.
8. **Post-release watch.** Monitor error rates, failed asset loads, and core web vitals for a defined window before closing the release.

## Decision gates

- **Gate A, build reproducibility:** Hash mismatch on a clean rebuild blocks release until explained.
- **Gate B, bundle hygiene:** Any secret in a client bundle, or any new source map published to a public location, blocks release.
- **Gate C, cache correctness:** Hashed assets must be served with long-lived immutable caching. The HTML entry point and any non-hashed files must revalidate. Violations block release.
- **Gate D, compatibility:** If the release changes a cached contract (service worker scope, localStorage schema, API client shape), a migration or fallback must exist. Otherwise require explicit approval with a stated risk.
- **Gate E, production promotion:** Requires named human approval. Automated pipelines may deploy to staging but must not promote to production without an approval record.

## Verification and evidence

Run and record:

- Asset manifest diff between current and candidate releases. Expected changes should match the commit scope.
- Smoke test of critical routes: load, authenticated shell, one primary user action per major feature. Record status codes and console error counts.
- Header check on `index.html`, one hashed JS chunk, and one non-hashed public file. Record `Cache-Control` values as observed.
- Client-side route fallback: a deep link returns the app shell with a 200 status, not a 404.
- Error budget comparison: client error rate and failed chunk loads for a bounded window after promotion, against the prior baseline. Set the window and threshold before release.
- Performance regression check on a representative page using the team's agreed metric set. Compare against the stored baseline; do not claim improvement without the baseline.

Mark any tool flags, header names, or platform features you cite as requiring confirmation against current vendor documentation for the version in use.

## Failure handling

- **Failed smoke test on staging:** Stop. Do not promote. Diagnose from build logs and the asset manifest before retrying.
- **Elevated client errors after promotion:** Roll back to the prior pointer immediately if the threshold is breached. Rollback is pre-approved only when the runbook explicitly says so; otherwise escalate to the approver with the recommendation.
- **Stale users on old chunks:** Confirm old assets remain available for the retention window. Do not delete previous release artifacts until the window passes.
- **Cache poisoning suspicion** (wrong content served under a hashed URL): Purge affected paths, verify origin content, and treat as an incident.
- **Partial deploy:** Re-run the atomic promotion. Do not hand-patch individual files on the host.

## Deliverable contract

Each release produces a delivery record containing:

- Commit SHA, lockfile hash, artifact identifier, and build timestamp.
- Environment variable diff with secrets redacted by name only.
- Gate results A through E, each marked pass, fail, or waived with the approver's name.
- Verification outputs listed above, including observed headers.
- Rollback target identifier and the exact rollback command or pointer switch as documented for the platform.
- Open assumptions and items marked for documentation verification.
- Post-release watch outcome and a close or rollback decision.

## What not to do

- Do not rebuild separately per environment.
- Do not put secrets in client-side configuration or source maps served publicly.
- Do not set long cache lifetimes on `index.html` or unhashed entry files.
- Do not delete prior release artifacts during the rollback window.
- Do not promote to production, purge global caches, change DNS, or alter production headers without explicit approval.
- Do not state performance, uptime, or compliance outcomes without measured evidence.
- Do not invent configuration keys, CLI flags, or version numbers. Verify them against current official documentation.