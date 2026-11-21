---
name: secrets-and-cryptography
description: Use when designing, reviewing, or troubleshooting how an application or infrastructure stores, distributes, rotates, or uses secrets, keys, certificates, or cryptographic primitives, including key management, TLS configuration, hashing, encryption at rest, and secret leakage remediation.
author: Luo Kai
provenance: original
version: 1.0.0
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