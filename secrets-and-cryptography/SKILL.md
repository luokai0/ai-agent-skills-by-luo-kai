---
name: secrets-and-cryptography
description: Use when designing, reviewing, or troubleshooting how an application or infrastructure stores, distributes, rotates, or uses secrets, keys, certificates, or cryptographic primitives, including key management, TLS configuration, hashing, encryption at rest, and secret leakage remediation.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Secrets And Cryptography

## Purpose and boundaries

This skill guides professional work on secret handling and applied cryptography: credential and key lifecycle, secret storage and injection, encryption design choices, certificate and TLS posture, password and token hashing, and response to exposed secrets.

In scope: reviewing code and configuration for hardcoded or leaked secrets; choosing vetted primitives and modes; designing key hierarchies and rotation; evaluating secret managers and injection paths; assessing TLS and certificate settings; planning revocation after exposure.

Out of scope: inventing custom cryptographic algorithms or protocols; defeating access controls on systems you do not own; producing working exploit code against third-party systems; certifying compliance with any framework.

## Inputs and assumptions

Gather before advising:
- Asset type (API key, database credential, signing key, TLS certificate, user password, encryption key, session token).
- Data sensitivity and who or what must access it.
- Current storage location, injection method, and rotation practice.
- Runtime environment, language, and libraries in use.
- Threat model: insider, external attacker, lost device, leaked repository, compromised dependency.
- Recovery requirements: can data be re-encrypted, can keys be destroyed, what is the outage tolerance.

State assumptions explicitly. If a critical input is missing, stop and request it rather than guessing.

## Operating workflow

1. Inventory secrets. List every secret, key, and certificate with owner, location, consumers, and expiry. Search version history, not only current files, for exposed material.
2. Classify each item by sensitivity and blast radius.
3. Trace the lifecycle: generation, storage, distribution, use, rotation, revocation, destruction.
4. Check generation. Keys and tokens must come from a cryptographically secure random source provided by the platform or a vetted library. Human-chosen values are not secrets.
5. Check storage. Secrets belong in a dedicated secret store or a hardware-backed key facility. Environment variables are acceptable for injection only when the platform restricts their exposure; they are never a storage location.
6. Check use. Verify secrets are not logged, echoed in error messages, placed in URLs, cached in client code, or passed in query strings.
7. Check primitives. Prefer authenticated encryption with associated data, and established password hashing functions with work factors tuned to current guidance. Confirm the exact algorithm, mode, and parameters against the library's current official documentation.
8. Define rotation: trigger events, overlap window for dual-valid credentials, and automated versus manual steps.
9. Produce findings and remediation in priority order.

## Decision gates

Stop and request explicit human approval before any of the following:
- Rotating or revoking a production credential, certificate, or signing key.
- Re-encrypting or migrating data stores in place.
- Destroying or disabling any key, including keys believed to be compromised but still protecting live data.
- Changing TLS or authentication settings on externally reachable services.
- Publishing, disclosing, or transmitting exposed secret values outside the organization.
- Running any test that sends real credentials to a third-party endpoint.

Proceed without approval only for read-only analysis, local reasoning, and drafting remediation plans.

Choose the primitive by purpose:
- Confidentiality with integrity: authenticated encryption with a unique nonce per message under one key.
- Message integrity between parties sharing a key: keyed MAC.
- Signatures: asymmetric signature scheme with the key held by a single controlled signer.
- Password storage: slow, salted, memory-hard or adaptive password hash. Never a general-purpose hash alone.
- Random identifiers that need unguessability: cryptographically secure random generator, not a time-seeded or sequential source.

## Verification and evidence

Each finding must cite the file, line, configuration key, or system record that shows it. Quality checks:
- Secret scan of the repository history and build artifacts reports zero live secrets after remediation, using a scanner whose version and rules you have confirmed.
- Every key has a recorded owner, creation date, and next rotation date.
- Rotation has been rehearsed in a non-production environment with both old and new credentials verified to behave as specified during the overlap window.
- TLS configuration is checked with an approved scanner or a documented manual handshake test; certificate chain validates and hostname matches.
- Encryption round-trip test passes, and tampered ciphertext is rejected with an error rather than producing output.
- Logs sampled from the last defined period contain no secret patterns.

Mark any statement about algorithm strength, library defaults, or protocol versions as requiring confirmation against current official documentation. Do not assert compliance with a standard.

## Failure handling

- Secret found in version control: treat as compromised regardless of repository visibility. Recommend revocation and replacement first, history rewriting second, and request approval for both.
- Scanner false positive: document the pattern and reason; do not suppress rules broadly.
- Missing consumer information during rotation planning: halt rotation, enumerate known consumers, and request owner confirmation.
- Rotation breaks a consumer: roll back to the overlap credential if the window is still open; otherwise escalate.
- Ambiguous cryptographic requirement: list the candidate primitives with tradeoffs and ask the owner to choose.
- Conflicting guidance between sources: prefer the current official documentation of the specific library or platform and note the discrepancy.

## Deliverable contract

Return a document containing, in order:
1. Scope and assumptions, including unanswered inputs.
2. Secret and key inventory table: item, type, location, owner, consumers, expiry, status.
3. Findings ranked by severity, each with evidence reference, risk, and specific remediation.
4. Proposed rotation or migration plan with ordered steps, rollback point, and approval gates marked.
5. Verification checklist with the checks above marked pass, fail, or not yet run.
6. Open questions and items requiring version confirmation.

Do not include actual secret values in the output. Redact to the first four characters at most, or describe the value by type and fingerprint.

## Agent credential broker and token exchange (v1.1)

An agent should request an authorized operation, not receive the credentials that make every operation possible. Put vendor credentials, OAuth refresh tokens, signing keys, and service secrets behind a credential broker or narrowly scoped egress gateway.

### Broker responsibilities
The broker is a trusted security component outside the model context and outside untrusted tool output. It should:
1. Authenticate the calling workload and verify the task authorization envelope.
2. Confirm that the requested destination, operation, tenant, and resource are allowed by policy.
3. Obtain or exchange a credential for that destination using a managed identity or approved OAuth flow.
4. Restrict the credential to the minimum audience, scopes, resource set, and lifetime supported by the provider.
5. Attach the credential to the outbound request without returning it to the agent.
6. Record a redacted audit event linking the agent, task, initiating subject, credential class, destination, and decision.
7. Revoke or invalidate broker-side grants when the task, user consent, or upstream authorization is withdrawn.

### Delegated OAuth and workload credentials
Keep service authority and user-delegated authority distinct. A service-to-service credential represents the workload; a delegated OAuth credential represents a user-approved grant. Do not silently substitute one for the other.

For delegated access:
- Use the provider's supported authorization-code and consent flow, with PKCE where applicable.
- Store refresh tokens only in the approved secret store or broker vault.
- Exchange or refresh tokens inside the broker, not in model-visible code or prompts.
- Validate issuer, signature, expiry, authorized party, audience, scopes, tenant, and token binding where supported.
- Do not accept a token merely because it is syntactically valid or was returned by a tool.
- Never pass a token issued for one API audience to a different resource server.
- Do not forward inbound user tokens to downstream services as a shortcut. Perform an explicit, policy-checked exchange.

### Credential isolation
- Give each integration a separate credential identity and policy.
- Avoid a single global API key shared by unrelated agents, tenants, or tasks.
- Keep credentials out of command arguments, URLs, browser-visible storage, source code, traces, crash dumps, and generated artifacts.
- Prefer short-lived credentials and managed identity over long-lived static secrets.
- Use per-task or per-tenant credential caches only when the cache key includes every authorization dimension; never reuse a broader cached token for a narrower request.
- Make secret retrieval an explicit broker action with a policy decision, not a general-purpose file read exposed to the agent.

### Rotation and incident response
Track owner, provider, scopes, audience, consumers, expiry, last use, and revocation method for every brokered credential. Support overlapping rotation windows only as long as needed, then revoke the old credential. On suspected exposure, revoke at the provider, invalidate broker caches, inspect use logs, identify affected tasks and tenants, and rotate dependent credentials. Do not assume deleting a secret from the current repository removes copies from history, logs, caches, or build artifacts.

### Broker acceptance tests
Verify that:
- The model and agent process cannot read the broker's stored refresh token or static secret.
- A credential for service A is rejected by service B.
- A read-only task cannot obtain a write-scoped credential.
- Revoked consent prevents future refresh and new outbound calls.
- A cached token cannot cross tenant, subject, audience, or task boundaries.
- Broker logs contain enough evidence to investigate use but no reusable secret material.

If the upstream provider cannot express the required scope or resource restriction, enforce it in the broker and egress policy, and document the remaining blast radius.
