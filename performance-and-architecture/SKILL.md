---
name: performance-and-architecture
description: Use when designing, reviewing, or tuning the performance and architecture of authentication, authorization, session, or security-critical request paths, including latency budgets for login and token validation, caching of auth decisions, hashing cost tuning, rate limiting placement, and scaling of identity services.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Performance And Architecture

## Purpose and boundaries

This skill guides engineers through making security-relevant components fast, scalable, and still correct. It covers the performance characteristics and architectural placement of:

- Credential verification (password hashing, MFA checks, passkey/WebAuthn verification)
- Token issuance and validation (JWT, opaque tokens, introspection)
- Session stores and revocation propagation
- Authorization decision points (policy engines, RBAC/ABAC lookups, permission caches)
- Rate limiting, lockout, and abuse controls on auth endpoints
- Identity provider dependencies (JWKS fetches, directory lookups, SSO round trips)

It does not cover general application performance unrelated to security, cryptographic algorithm design, or certifying compliance with any standard. Security correctness takes priority over latency: never trade away a check to meet a budget. Trade-offs must be stated, not hidden.

## Inputs and assumptions

Before acting, collect:

1. The request path diagram, including which components are on the critical path for each auth operation.
2. Current measurements: p50/p95/p99 latency, throughput, error rates, and resource use for each auth operation, from production or a representative load test.
3. Traffic shape: peak logins per second, token validations per second, ratio of cached to uncached decisions, and burst patterns.
4. Revocation requirements: maximum acceptable time between revoking access and enforcement.
5. Security requirements: which checks are non-negotiable and which data may be cached, and for how long.
6. Target environment constraints: hardware, managed service limits, regional topology.

If measurements are absent, state that all proposed budgets are estimates and must be validated. Do not assume a library's default cost parameters are appropriate for the hardware.

## Operating workflow

1. **Map the critical path.** List every network hop, store read, and crypto operation between the client request and the authorization decision. Mark each as mandatory or optional for correctness.
2. **Attribute latency.** Break the measured p95 into components. Typically the largest contributors are password hashing, remote JWKS or introspection calls, and synchronous policy or directory lookups.
3. **Set budgets per operation.** Example: token validation at the edge under 5 ms p95 with local verification; interactive login under a budget agreed with product, dominated by intentional hashing cost.
4. **Select the lever.** Choose from: caching verified results, moving checks to local verification, batching lookups, reducing hop count, tuning hashing parameters, or relocating rate limiters closer to the edge. Apply one lever per change.
5. **Quantify the security impact.** For each lever, state what revocation delay, staleness, or weakened check it introduces.
6. **Implement behind a flag or canary,** then compare against the baseline with identical load profiles.
7. **Record the decision** in an architecture note: problem, options, chosen option, measured result, residual risk.

## Decision gates

Stop and seek explicit approval before proceeding when any of these apply:

- Reducing hashing cost parameters, changing the password hashing algorithm, or migrating stored credentials. These affect every user and may require a rehash-on-login plan.
- Extending cache lifetime for authorization decisions beyond the agreed revocation window.
- Skipping signature verification, audience/issuer checks, or expiry checks for any path, even for internal traffic.
- Moving session or token state to a store with different durability, replication, or data residency characteristics.
- Changing rate limits or lockout thresholds in production, since this can lock out legitimate users or open brute-force paths.
- Any rollout that affects all users at once rather than a canary cohort.
- Deleting or flushing session, token, or revocation stores.

Proceed without approval only for changes in a non-production environment, read-only measurement, and adding instrumentation.

## Verification and evidence

Each change must show:

- Baseline and post-change p50/p95/p99 under the same load profile, with sample size and duration stated.
- Error rate and authentication failure rate unchanged within a defined tolerance (for example, no increase in false denials beyond the agreed margin).
- A revocation test: revoke a credential or role and measure the time until denial, compared against the requirement.
- Negative tests confirming that invalid signatures, expired tokens, wrong audiences, and revoked sessions are still rejected after the change.
- Cache hit ratio and staleness metrics, with eviction and TTL behavior documented.
- Resource metrics for hashing workers (CPU saturation, queue depth) to confirm the bottleneck moved as predicted.

Mark any library-specific parameter, cost factor, or API behavior as version-sensitive. Verify against current official documentation before recommending values. Do not state benchmark numbers that were not measured in this environment.

## Failure handling

- **Latency regression after change:** roll back the flag first, then investigate. Do not tune further under production load.
- **Cache causing stale denials or stale grants:** shorten TTL, add explicit invalidation on revocation events, and re-run the revocation test.
- **Identity provider or JWKS endpoint unavailable:** verify that the system fails closed for protected operations, and that cached keys are used only within their documented validity window. Never accept unverifiable tokens to preserve availability.
- **Hashing queue saturation during login spikes:** shed or queue requests with clear user-facing retry guidance; do not lower hashing cost to clear the queue.
- **Measurement inconsistent between runs:** increase run duration and repeat, and check for warm-up effects before drawing conclusions.

## Deliverable contract

Produce a design or review note containing, in order:

1. Scope: which operations and components were analyzed.
2. Baseline table: operation, p50, p95, p99, throughput, and the environment and load profile used.
3. Critical path diagram or ordered list with latency attribution.
4. Proposed changes, each with the lever used, expected gain, and the security trade-off stated explicitly.
5. Approval status for each gated item.
6. Verification results: performance comparison, revocation timing, negative test outcomes.
7. Residual risks and open questions, including any version-sensitive items pending documentation check.
8. Rollback plan with the exact flag or configuration to revert.

Do not present expected gains as achieved results. Do not omit security trade-offs to make a proposal look favorable. Do not recommend weakening verification to meet a latency target.