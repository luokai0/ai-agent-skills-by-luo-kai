---
name: auth-implementation
description: Use when designing, implementing, reviewing, or migrating authentication flows (login, sessions, tokens, MFA, password reset, OAuth/OIDC client or resource-server integration) in an application or service.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Auth Implementation

## Purpose and boundaries

This skill guides implementation of authentication: verifying who a user or client is, and establishing and maintaining that identity across requests. It covers credential storage, login and logout, session or token issuance and validation, multi-factor enrollment and verification, account recovery, and integration with external identity providers using OAuth 2.0 or OpenID Connect.

It does not cover authorization policy design (what an authenticated principal may do), network perimeter security, key management infrastructure, or cryptographic primitive invention. Route those to the relevant skill or to a security owner. Never design custom cryptography; use vetted libraries and platform facilities.

## Inputs and assumptions

Collect before writing code:

1. Client types: browser SPA, server-rendered web, mobile, machine-to-machine, third-party API consumers.
2. Existing identity source: local user table, corporate IdP, social login, or migration from a legacy system.
3. Required assurance level: password-only, password plus second factor, or phishing-resistant factors.
4. Session model constraints: stateful server sessions, signed tokens, or mixed. Note revocation requirements.
5. Compliance or contractual obligations. State them as requirements to verify, not guarantees you provide.
6. Language, framework, and deployment platform, with exact versions.

If any input is missing, state the assumption explicitly in the deliverable. Do not guess at identity provider endpoints, client secrets, or tenant identifiers.

## Operating workflow

1. **Map the flows.** List every entry point: sign-up, login, step-up, logout, password change, reset, email change, MFA enroll and recover, token refresh, and service-to-service calls.
2. **Select the mechanism per flow.** Prefer delegating credential handling to an established IdP for user login. Use local credentials only when a delegated option is infeasible, and document why.
3. **Design credential storage.** Hash passwords with a memory-hard or adaptive algorithm from a maintained library (for example Argon2id or scrypt); verify current parameter recommendations in official library and OWASP documentation. Store per-user salts through the library's default mechanism. Never log, echo, or return credentials.
4. **Design session or token handling.** Set cookie attributes (Secure, HttpOnly, SameSite) explicitly. Rotate session identifiers on login and privilege change. For tokens, validate issuer, audience, expiry, signature algorithm (pin the expected algorithm, reject `none`), and clock skew tolerance.
5. **Implement recovery and MFA.** Reset tokens are single-use, high-entropy, short-lived, and stored hashed. Respond identically whether or not an account exists. Require re-authentication for MFA changes.
6. **Add abuse controls.** Rate-limit per account and per source, with lockout or backoff that does not enable trivial denial of service.
7. **Write tests** covering each flow's success and failure paths (see Verification).
8. **Produce the deliverable** per the contract below.

## Decision gates

Stop and obtain explicit approval before:

- Deleting or migrating existing user credentials, sessions, or tokens, or changing hashing parameters that force re-hash of stored passwords at scale.
- Rotating signing keys or client secrets in any shared or production environment.
- Changing redirect URIs, allowed origins, or identity provider registrations, since these affect external parties.
- Disabling MFA, widening token lifetimes, or accepting an additional identity provider.
- Running any test or script against production identity systems or real user data.
- Sending emails, SMS, or webhooks to real recipients.

Proceed without approval only for local code changes, unit tests, and fixtures using synthetic identities.

## Verification and evidence

Quality checks, each with a measurable outcome:

- Every auth endpoint has tests for: valid credentials, wrong password, unknown user (same response shape and comparable timing), locked or rate-limited state, expired or reused token, and missing or malformed input.
- Token validation tests reject: wrong issuer, wrong audience, expired token, altered signature, algorithm mismatch, and `alg=none`.
- Session cookies are verified in a response-header assertion: Secure, HttpOnly, and SameSite present with the intended values.
- Session ID changes after successful login (assert different value before and after).
- Reset tokens fail on second use and after expiry.
- No credential, token, or reset secret appears in logs; run a grep-style assertion over captured test logs.
- Password hashing parameters are recorded in the deliverable and checked against current official guidance, with the verification date stated.
- OAuth/OIDC flows use the authorization code flow with PKCE for public clients; the `state` and `nonce` parameters are generated per request and validated.

Evidence to attach: test names and pass counts, a list of flows covered, and any unverified items.

## Failure handling

- If a library or framework API is unfamiliar or its version is uncertain, do not invent method names or flags. Mark the detail as "verify against current official documentation for version X" and proceed with the rest.
- If a test reveals a credential or token leak, stop, redact the evidence, and escalate to the security owner before continuing.
- If an IdP integration fails in a non-test environment, roll back the configuration change and report; do not retry repeatedly against live endpoints.
- If requirements conflict (for example, long-lived sessions versus strict revocation), present two options with tradeoffs and wait for a decision.
- Never weaken a control to make a test pass.

## Deliverable contract

Return:

1. **Flow inventory**: table of flows, mechanism chosen, and rationale.
2. **Assumptions and open questions**: each with an owner.
3. **Implementation changes**: files changed and a summary of each security-relevant decision (storage, cookie attributes, token validation rules).
4. **Verification results**: tests run, outcomes, and checklist status against the Verification section, with unverified items labeled.
5. **Version-sensitive items**: every library, framework, or standard detail flagged for confirmation against official documentation, with the version it applies to.
6. **Approval log**: each decision gate triggered, the approval requested, and the outcome.

Do not claim the system is secure, compliant, or audited. State only what was implemented and tested.