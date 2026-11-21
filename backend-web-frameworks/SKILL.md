---
name: backend-web-frameworks
description: Use when designing, building, reviewing, or debugging server-side web applications or HTTP APIs in a backend framework, including routing, middleware, request validation, data access wiring, authentication hooks, and deployment-readiness checks.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Backend Web Frameworks

## Purpose and boundaries

This skill covers choosing, structuring, and reviewing server-side web code built on a backend framework: request lifecycle, routing, middleware or interceptors, validation, error mapping, configuration, and the seams to databases, caches, queues, and identity providers. It does not cover frontend rendering, infrastructure provisioning, or language-level design beyond what the framework requires. Treat framework-specific names, flags, and versions as unverified until checked against the current official documentation for the exact version in use.

## Inputs and assumptions

Before acting, establish:

- Language, framework, and exact version from the lockfile or manifest, not from memory.
- Runtime target (container, serverless, long-running process) and expected concurrency model.
- Existing conventions: router style, error envelope, logging format, test harness.
- Traffic and latency expectations, if stated. If absent, state that performance claims are unmeasured.
- Data sensitivity: personal data, credentials, payment data, or regulated records.

If any of these are missing and they change the design, ask rather than assume.

## Operating workflow

1. Map the request path: entry point, global middleware, route matching, authentication, validation, handler, data call, response serialization, error handler.
2. Identify the framework's documented extension points (middleware, guards, dependency injection, lifecycle hooks) and place each concern in exactly one of them.
3. Define input contracts first: schema for path, query, headers, and body, with explicit maximum sizes and rejection of unknown fields where the API is strict.
4. Keep handlers thin. Business rules belong in plain functions or services that can be tested without starting the server.
5. Centralize error mapping so that internal exceptions never reach clients with stack traces, SQL text, or secret values.
6. Set timeouts on outbound calls and database operations. Make them configurable and document defaults.
7. Confirm graceful shutdown: stop accepting new requests, drain in-flight work, close pools.
8. Add structured logs with request identifiers; exclude credentials, tokens, and personal fields.

## Decision gates

- **Sync vs. offloaded work:** If an operation exceeds the request timeout budget or depends on an unreliable third party, move it to a queue or background job with idempotency keys. Do not extend timeouts to hide it.
- **Middleware vs. handler logic:** Cross-cutting behavior (auth, rate limits, tracing) goes in middleware. Resource-specific authorization stays with the resource.
- **Framework upgrade:** Before changing major versions, read the migration notes for every breaking change touching used features, then run the full test suite on a branch.
- **Custom vs. built-in:** Use the framework's built-in parser, validator, or session support unless it is documented as unable to meet a stated requirement.
- **Stop and request approval** before: deleting or rewriting migrations, altering authentication or authorization logic, changing public API contracts, modifying production configuration, rotating secrets, or deploying. These require explicit human approval with the diff or plan shown first.

## Verification and evidence

- Run the project's existing test and lint commands; report exact output summaries, not paraphrased success.
- For each new endpoint: test success, validation failure, unauthenticated access, unauthorized access, and oversized input.
- Confirm that error responses match the documented envelope and contain no internal details, checked with a deliberately failing request.
- Verify timeouts with a test that exceeds them, and confirm the resulting status code.
- Check that secrets are read from the environment or a secret store, and that no literal credentials appear in the diff.
- Any performance statement must cite a measurement with method, load shape, and environment. Otherwise write "not measured."
- Confirm compatibility claims against the pinned framework version's official documentation.

## Failure handling

- If a framework behavior contradicts its documentation, pin the version, record the observed behavior with a minimal reproduction, and report it rather than working around it silently.
- If tests fail after a change, revert the smallest unit that caused it and explain the cause before retrying.
- If required documentation is unavailable, mark the affected design decision as unverified and list it in the deliverable.
- If a security-relevant defect is found, stop feature work, document it, and escalate for approval before fixing.

## Deliverable contract

Every result must include:

1. A short summary of the change and its affected routes or modules.
2. The request-path map, with the extension point used for each concern.
3. Test and lint results with exact commands and outcomes.
4. A list of assumptions, unverified version-specific details, and unmeasured claims.
5. Explicit approval requests for any gated action not yet approved.
6. Known limitations and follow-up items, each with an owner or "unassigned" stated plainly.

Do not claim production readiness, compliance, or security guarantees. Do not invent library names, configuration keys, or benchmark figures.