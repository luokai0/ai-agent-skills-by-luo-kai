---
name: api-design-security-and-app-scaffolding
description: Use when designing or reviewing an HTTP API, generating a new application scaffold, or hardening an existing service's authentication, authorization, input validation, and configuration before code is written or merged.
author: Luo Kai
provenance: original
version: 1.1.0
---

# API Design, Security, and App Scaffolding

## Purpose and boundaries

This skill covers three linked tasks: (1) specifying an HTTP API contract, (2) producing a secure application skeleton that implements that contract, and (3) reviewing the security posture of the contract and skeleton. It applies to REST and JSON-over-HTTP services, and to scaffolds for web backends that expose them.

It does not cover: frontend UI design, infrastructure provisioning in live cloud accounts, penetration testing of systems you do not own, compliance certification (SOC 2, PCI, HIPAA, and similar, which require auditors), or choosing business logic. Where a task crosses those lines, produce the artifact within scope and flag the rest for a human owner.

## Inputs and assumptions

Before working, collect or state explicitly:

- Consumers of the API (first-party, partner, public) and their trust level.
- Data classification of each resource: public, internal, personal, or regulated.
- Authentication method in use or required (for example, OAuth 2.0 / OpenID Connect via an existing identity provider, or API keys for machine clients).
- Expected scale, latency targets, and rate-limit needs, stated as numbers if known.
- Target language and framework. Record the exact version. Do not assume a framework's current API surface; mark any version-sensitive call for verification against its current official documentation.
- Deployment target (container, serverless, VM), since it changes secret handling and logging.

If any item is missing and affects security or data handling, mark it as an assumption in the deliverable and list it under open questions. Do not silently default to permissive behavior.

## Operating workflow

1. **Model resources and actions.** List nouns (resources), their identifiers, and the operations on them. Map each operation to the minimum role or scope that may invoke it.
2. **Write the contract first.** Use an OpenAPI-style description. For every operation define: path, method, request schema, response schemas for success and each error class, idempotency behavior for unsafe methods, pagination for collections, and authentication requirement.
3. **Define errors uniformly.** Use one error envelope across the service with a stable machine-readable code, a human message that never echoes secrets or stack traces, and a correlation ID. Map validation failures to 400 or 422 consistently, authentication failures to 401, authorization failures to 403, and avoid leaking existence of resources a caller cannot see (return 404 where appropriate).
4. **Specify authorization per object.** Authentication alone is insufficient. For each resource-scoped operation, state the ownership or tenancy check performed against the server-side record, not against client-supplied fields.
5. **Specify validation at the boundary.** Enforce maximum body size, maximum string length, allowed character sets, numeric ranges, enum membership, and rejection of unknown fields for write operations. Validate content type; reject mismatches.
6. **Generate the scaffold.** Structure: entry point, configuration loader, router, middleware chain (request ID, authentication, authorization helpers, validation, rate limiting, structured logging, error handler), service layer, data access layer, tests. Load secrets from the environment or a secret manager; never from committed files.
7. **Apply secure defaults.** TLS terminated at the edge with redirect from plaintext; security headers set; CORS restricted to an explicit origin list; debug mode disabled by default; parameterized queries only; passwords and tokens hashed or stored by the identity provider, never logged.
8. **Add tests alongside.** Write tests for each authorization rule (allowed and denied cases), each validation rule, and each error path.

## Decision gates

Stop and obtain explicit human approval before proceeding when any of the following applies:

- The change deletes or migrates data, alters a schema in place, or rotates credentials.
- The change exposes a new public endpoint, changes an existing public contract in a breaking way, or alters CORS or authentication rules.
- The change stores or transmits regulated or personal data in a new location or to a third party.
- The change would call an external production system, send messages, or trigger payments.
- The chosen authentication scheme is custom rather than a standard protocol implementation.

Proceed without a gate only for additive, internal, reversible work that stays within the declared scope.

## Verification and evidence

Each deliverable must include evidence for these checks. Report the result, not an assumption:

- Every operation in the contract has an explicit auth requirement; zero operations are marked "none" without justification.
- Every resource-scoped read and write has a server-side ownership or role check, with a test for a denied cross-tenant request.
- Validation tests cover oversize input, unknown fields, wrong content type, and out-of-range values; each returns the uniform error envelope.
- No secret literals appear in the repository; run a secret-scanning tool and record its version and output summary.
- Dependencies are pinned to versions recorded in the lockfile; known-vulnerability scan results are attached with the tool name and date.
- Logs for a sample failing request contain the correlation ID and no tokens, passwords, or full personal data.
- Rate limits and body-size limits are configured with stated numeric values, and a test demonstrates rejection beyond the limit.

Do not state performance figures, throughput, or compliance status unless measured in the stated environment.

## Failure handling

- If a required input is missing and it affects security, halt and ask. Otherwise record the assumption.
- If a framework feature needed is uncertain in the pinned version, mark it "verify against current official documentation" and write the smallest verifiable alternative.
- If a test or scan fails, do not weaken the test. Fix the cause or report it as an open defect with severity.
- If an authorization rule cannot be expressed cleanly, default to deny and escalate.

## Deliverable contract

Deliver exactly these items:

1. OpenAPI-style contract covering all operations, with auth, errors, pagination, and idempotency specified.
2. Scaffold file tree and the code for entry point, configuration, middleware chain, error handler, and one fully implemented resource with its authorization and validation.
3. Test suite covering the verification checks above.
4. Configuration reference listing each environment variable, its purpose, its default, and whether it is a secret. Do not invent variables beyond those the code reads.
5. Security notes: assumptions, decision gates triggered and their approval status, open risks with severity, and items requiring verification against current official documentation.

Do not present the output as production-ready until every verification check is either passed with evidence or listed as an open risk with an owner.

## Ultron routing contract

**Choose this skill when:** the deliverable combines an HTTP API contract with a secure application skeleton that implements it. It owns resource and endpoint shape, request/response conventions, initial application structure, and the security posture of that contract and scaffold.

**Choose rest-api-design-security when:** the API already exists or the task is specifically to assess its HTTP/JSON security boundary: authentication, authorization, validation, response shaping, rate limits, transport, and logging.

**Handoff contract:** provide the API schema, trust boundaries, identity assumptions, scaffold implementation, and known risks. The REST security skill returns prioritized boundary findings and controls; this skill integrates required contract/scaffold changes and reruns the end-to-end API contract checks.

**Why the boundary exists:** creating a usable API skeleton and independently reviewing an API's security properties are related but different deliverables.
