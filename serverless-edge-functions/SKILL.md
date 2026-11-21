---
name: serverless-edge-functions
description: Use when designing, writing, deploying, or debugging serverless functions that run at CDN or edge locations, including request rewriting, auth gating, header and cache logic, A/B routing, and lightweight API responses under strict CPU, memory, and latency limits.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Serverless Edge Functions

## Purpose and boundaries

Use this skill to produce edge function code and its deployment plan: request inspection, routing, header and cache manipulation, auth gating, redirects, and small synthesized responses that execute close to the user. It covers design trade-offs, runtime constraints, testing, and rollout.

Out of scope: long-running jobs, large data processing, stateful transactional writes to primary databases from the edge, and full origin-replacing application logic. If the task needs those, recommend a regional function or origin service instead.

## Inputs and assumptions

Collect before writing code:

1. Target platform and runtime (for example, a specific edge provider's worker or isolate model). Treat its limits as version-sensitive.
2. Trigger points: viewer request, origin request, origin response, viewer response, or equivalent.
3. Latency budget, expected request volume, and cache hit ratio goal.
4. Data needed: headers, cookies, geo fields, and any external calls. Note which are available at the edge and which are not.
5. Existing cache keys, cache TTLs, and origin behavior.
6. Security requirements: which paths need auth, which tokens or keys are involved, and where secrets are stored.

Assumptions must be written down. If the platform's CPU time, memory, subrequest count, bundle size, or header limits are not confirmed, mark them "verify against current official documentation" and do not state numbers.

## Operating workflow

1. **Define the single responsibility.** One function, one job (for example, "normalize locale redirects"). Reject bundles that mix auth, caching, and personalization without separation.
2. **Map the trigger.** Select the earliest stage that satisfies the need. Header normalization belongs on the viewer request; cache key adjustments usually belong before cache lookup; origin-specific header injection belongs on the origin request.
3. **Write a pure core.** Put routing and decision logic in a function that takes a plain request descriptor and returns an action (pass, redirect, rewrite, respond). Keep platform bindings in a thin adapter.
4. **Bound all work.** No unbounded loops, no recursive parsing of untrusted input, and no external fetch without a timeout and a fallback path.
5. **Handle failure explicitly.** Any error in the edge path must either pass the request through unchanged or return a defined error response. Never leave the response undefined.
6. **Test locally** with fixtures covering: missing headers, malformed cookies, oversized URLs, unicode paths, duplicate query keys, and boundary geo values.
7. **Stage the rollout:** deploy to a non-production route, compare responses against the baseline on sampled traffic, then increase exposure in steps.

## Decision gates

- **Gate A: Is edge the right place?** Proceed only if the logic is stateless or reads cacheable data, and needs to run before origin. If it needs a consistent write or heavy compute, stop and escalate.
- **Gate B: Does it touch secrets or auth?** Requires explicit approval from the service owner before implementation. Verify tokens with asymmetric signatures or platform-provided key stores; never embed secrets in source.
- **Gate C: Does it alter cache keys or vary headers?** Requires approval because it can cause cache poisoning or fragmentation. Show the before and after cache key for three sample requests.
- **Gate D: Does it change redirects or status codes for production paths?** Requires approval and a rollback plan with the previous configuration preserved.
- **Gate E: Does it call an external service?** Requires approval for the destination, timeout, retry policy, and data sent. Forwarding user identifiers or personal data needs a documented justification.

## Verification and evidence

Each deliverable must include:

- Unit tests for the pure core, covering every decision branch.
- A fixture table: input request, expected action, actual result.
- Measured or estimated bundle size, checked against the platform's current documented limit.
- A cache behavior check: the same URL requested twice, confirming hit or miss status as expected, with the vary and key settings noted.
- A canary result: error rate, p95 added latency, and status-code distribution compared against baseline. If no canary has run, state "not yet measured" and do not claim improvement.

Do not report performance gains without a measured baseline.

## Failure handling

- **Runtime exception:** return pass-through to origin if the request is safe to forward; otherwise return a static 500 with no internal detail.
- **Timeout on external call:** use the cached or default decision defined in the design; log the event with a request identifier.
- **Unexpected input shape:** treat as untrusted, reject with 400 for API paths, or pass through for content paths. Do not throw.
- **Rollback trigger:** error rate above the baseline threshold agreed in the plan, or any auth bypass observed. Roll back first, then diagnose.

## Deliverable contract

Return:

1. Function purpose statement (one sentence).
2. Trigger stage and platform assumptions, with version-sensitive items marked.
3. Source code: pure core and adapter, separated.
4. Configuration: route patterns, cache key settings, and environment variable names (no values).
5. Test suite and fixture table.
6. Gate status: which of A–E applied, and what approval is still pending.
7. Rollout and rollback steps with thresholds.

Do not include real secrets, invented platform flags, unverified benchmark numbers, or statements of compliance certification. Do not deploy to production paths, modify live cache rules, or alter auth behavior without explicit approval from the named owner.