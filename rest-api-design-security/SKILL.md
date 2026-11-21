---
name: rest-api-design-security
description: Use when designing, reviewing, or hardening REST API endpoints for authentication, authorization, input validation, rate limiting, data exposure, or transport security before implementation or release.
author: Luo Kai
provenance: original
version: 1.1.0
---

# REST API Design Security

## Purpose and boundaries

This skill covers the security design of HTTP/JSON REST APIs: resource modeling as it affects access control, authentication and authorization, input validation, response shaping, error handling, rate limiting, transport configuration, and logging of API traffic.

It does not cover: GraphQL or gRPC specifics, front-end XSS, infrastructure hardening beyond the API boundary, cryptographic protocol design, or formal compliance certification. Where a finding touches those areas, record it and hand it off.

## Inputs and assumptions

Collect before reviewing:
- Endpoint inventory: method, path, request and response schemas, and caller type (end user, service, partner, public).
- Authentication mechanism in use or proposed (session, bearer token, API key, mutual TLS, OAuth 2.x flows).
- Data classification for each resource (public, internal, personal, financial, credentials).
- Existing gateway, WAF, or rate-limit configuration, if any.
- Deployment topology: which endpoints are internet-facing.

Assumptions must be stated explicitly in the deliverable. If an input is missing, mark the affected checks as "not verified" rather than passing them.

## Operating workflow

1. **Map trust boundaries.** List each entry point and the identity it accepts. Flag any endpoint callable without authentication.
2. **Enumerate resources and actions.** For every endpoint, record the object it reads or mutates and the owner relationship (user, tenant, organization).
3. **Check authorization per object.** For each endpoint that accepts an identifier, confirm the server verifies that the authenticated principal may access that specific object, not just the route. Test for broken object-level authorization by substituting identifiers belonging to other principals.
4. **Check authorization per function.** Confirm administrative and privileged operations require a distinct role or scope, and that role fields cannot be set by the client.
5. **Validate input.** Verify schema-level validation: types, lengths, enumerations, ranges, and maximum body size. Reject unknown fields on write endpoints unless explicitly allowed. Check that path, query, and header values are validated and never interpolated into queries, shell commands, or file paths.
6. **Shape responses.** Confirm responses return only fields the caller needs. Flag fields such as password hashes, internal IDs of other tenants, stack traces, internal hostnames, and full database records.
7. **Review errors.** Errors must not disclose whether a resource exists to unauthorized callers. Use consistent status codes for authentication failure and for not-found-or-forbidden cases where existence is sensitive.
8. **Check rate limiting and abuse controls.** Identify endpoints for login, password reset, token issuance, search, file upload, and expensive queries. Each needs a documented limit keyed to an appropriate identity (account, token, IP with caveats).
9. **Check transport and token handling.** Confirm TLS for all endpoints, tokens not placed in URLs, secure cookie attributes where cookies are used, and short token lifetimes with a revocation path.
10. **Check logging.** Logs must record authentication events and authorization denials with correlation IDs, and must not record secrets, tokens, or full request bodies containing personal data.

## Decision gates

- **Gate A (authentication):** If any state-changing or data-returning endpoint lacks authentication, stop and require an explicit justification signed off by the owner before proceeding.
- **Gate B (object access):** If an identifier-based endpoint does not verify ownership or tenancy, classify as high severity. Do not accept a "the UI prevents it" argument.
- **Gate C (sensitive change):** Changes to authentication flows, token signing, key management, CORS policy on credentialed routes, or public exposure of an internal endpoint require explicit approval from the system owner before implementation or deployment.
- **Gate D (testing against live systems):** Do not send attack traffic, fuzzing, or credential-guessing tests against production or third-party systems without written approval naming the target, window, and rate limit.
- **Gate E (data handling):** Do not copy real personal or credential data into test artifacts, tickets, or reports. Use redacted or synthetic samples.

## Verification and evidence

For each finding, record:
- Endpoint, method, and affected parameter.
- Reproduction steps using a test account pair (principal A owns object X; principal B attempts access).
- Observed status code and response excerpt with sensitive values redacted.
- Expected behavior and the rule violated.

Quality checks before closing a review:
- 100% of endpoints in the inventory have an authentication classification and an authorization rule recorded.
- Every identifier-accepting endpoint has at least one cross-principal test result.
- Every write endpoint has a documented schema with rejection of unknown fields, or a recorded exception.
- Rate-limit values for authentication endpoints are documented and tested for a lockout or throttle response.
- No secret, token, or personal data appears in the deliverable.

Version-sensitive items (framework middleware names, OAuth grant availability, TLS version defaults, header recommendations, library behavior) must be marked "verify against current official documentation" and must not be stated as fact from memory.

## Failure handling

- If a test environment is unavailable, perform static review of the schemas and code paths, and label every finding as "static, unconfirmed."
- If reproduction is ambiguous, report the uncertainty and the next test needed; do not upgrade severity or downgrade it without evidence.
- If a fix would break a known client, propose a versioned migration with a deprecation window rather than an in-place breaking change, and request approval (Gate C).
- If you discover an active exploitation indicator or exposed secret, stop, do not attempt further probing, and escalate to the system owner immediately.

## Deliverable contract

Produce a single report containing:
1. Scope, assumptions, and inputs received, with missing inputs listed.
2. Endpoint inventory table: endpoint, auth requirement, object scope, rate limit, sensitivity.
3. Findings ordered by severity, each with evidence fields above, a rule reference, and a concrete remediation.
4. Approval requests raised under the decision gates, with status.
5. Verification status for each quality check: passed, failed, or not verified, with reason.
6. Version-sensitive items flagged for documentation verification.

Do not: approve a design on partial inventory; use live third-party systems for testing; propose security through obscurity (hidden routes, unguessable paths) as the control; state that an API is "secure" or "compliant" as a conclusion; or omit negative results.

## Ultron routing contract

**Choose this skill when:** the task is to secure or review an existing HTTP/JSON REST API boundary, especially resource authorization, authentication, validation, response exposure, error behavior, rate limits, transport, and API-specific logging.

**Choose api-design-security-and-app-scaffolding when:** the work starts with a new API or requires a complete API contract plus an application skeleton that implements it.

**Handoff contract:** return endpoint/resource findings, abuse cases, authorization and validation requirements, safe response rules, rate-limit policy, and negative security tests. The scaffold skill owns implementation of any required new application structure; this skill independently verifies the resulting API boundary.

**Why the boundary exists:** a secure REST API review should not silently become a full application scaffolding project, and a scaffold generator should not be treated as independent security assurance.
