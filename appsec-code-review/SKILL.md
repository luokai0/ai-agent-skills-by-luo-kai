---
name: appsec-code-review
description: Use when reviewing application source code, pull requests, diffs, or modules for security and authentication flaws, including session handling, access control, credential storage, token validation, and input handling in web and API services.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Appsec Code Review

## Purpose and boundaries

This skill guides a security-focused review of application code, with emphasis on authentication (who the caller is) and authorization (what they may do), plus the input and data handling that those controls depend on.

In scope: authentication flows, session and token lifecycle, password and secret handling, authorization checks on every data access path, input validation and output encoding at trust boundaries, cryptographic API misuse, and insecure defaults in configuration that ships with the code.

Out of scope: running live exploits against systems, infrastructure or cloud posture review, penetration testing, dependency license review, and compliance attestation. Do not claim that code is "secure" or "compliant"; report what was reviewed, what was found, and what was not checked.

## Inputs and assumptions

Required inputs: the diff or file set, the language and framework, and the intended trust model (public, authenticated users, tenants, admins, service-to-service).

Ask for missing items before concluding. If the trust model is unknown, state the assumption explicitly in the report.

Assume nothing about runtime configuration. Where behavior depends on deployment settings, mark the finding as conditional and list the setting to verify.

## Operating workflow

1. Map entry points. List every route, RPC handler, message consumer, and CLI entry touched by the change. Record which ones require authentication.
2. Trace identity. Follow how the caller's identity is established: header, cookie, bearer token, client certificate, or session store. Note where it is trusted and where it is first checked.
3. Check authorization per object. For each read, write, and delete, confirm the code verifies the caller's rights to that specific object, not just the route. Look for identifiers taken from the request and used directly in queries.
4. Review credential and secret handling. Check hashing algorithm and parameters, comparison method, logging of secrets, storage location, and hardcoded values.
5. Review token and session logic. Check signature verification, algorithm pinning, expiry, audience and issuer checks, revocation on logout and password change, and cookie attributes.
6. Review input and output boundaries. Check parameterization of queries, path and command construction, deserialization of untrusted data, redirect targets, and template output encoding.
7. Review error and logging paths. Confirm failures do not reveal account existence, stack traces, or tokens, and that security events are logged without sensitive values.
8. Record each finding with evidence before classifying severity.

## Decision gates

Gate A, scope: Stop and request clarification if the change touches authentication code but the trust model is unknown.

Gate B, severity: Rate a finding High when it allows unauthenticated access, cross-tenant or cross-user data access, privilege escalation, credential disclosure, or token forgery. Rate Medium when exploitation requires an existing authenticated session plus an unusual condition. Rate Low for defense-in-depth gaps with no demonstrated path to impact.

Gate C, confidence: Mark a finding Confirmed only when the code path from input to impact is traced in the reviewed source. Mark it Suspected when a dependency, middleware, or config value outside the diff determines the outcome.

Gate D, external action: Do not run tests against shared, staging, or production environments, send requests to live systems, rotate credentials, or open tickets in external trackers without explicit user approval. Propose the action and wait.

Gate E, sensitive material: If the code contains real-looking secrets, keys, or personal data, do not reproduce them in the report. Redact to the first four characters and the location.

## Verification and evidence

Every finding must cite file path, line range, the relevant code, and the specific condition that makes it exploitable. Where possible, supply a local unit test or reasoning trace showing the failing behavior, executed only in an isolated local environment.

Verify version-sensitive claims (library defaults, algorithm recommendations, framework middleware behavior) against current official documentation. Mark anything unverified as "requires verification" rather than asserting it.

Quality checks before delivery:
- Every High and Medium finding has a file-and-line citation and a stated trigger condition.
- No finding restates a framework default without checking the version in use.
- The list of reviewed entry points matches the list of entry points touched by the diff, with no silent omissions.
- Each route that requires authentication shows an identity check on the path.
- Coverage statement lists files read, files not read, and assumptions made.

## Failure handling

If the diff is incomplete or context is missing, report the gap and list the files needed. Do not infer the content of unseen functions.

If a finding cannot be confirmed, downgrade it to Suspected and state the missing evidence.

If a test or tool fails to run, record the exact error and do not substitute a claimed result.

If you discover evidence of an active compromise, such as unexpected credentials or exfiltration code, stop the review, report it immediately, and do not attempt remediation or further interaction with the affected system.

## Deliverable contract

Produce a report with these sections in order:

1. Summary: reviewed scope, trust model assumed, count of findings by severity and confidence.
2. Findings: each with ID, title, severity, confidence, location, trigger condition, impact, and recommended fix.
3. Positive controls observed: specific checks that were correctly implemented.
4. Coverage and gaps: files read, files not read, unverified assumptions, items requiring verification against official documentation.
5. Approval requests: any actions that need explicit user approval before proceeding.

Recommended fixes must be specific to the code shown and must not introduce new unverified APIs. Do not declare the code free of vulnerabilities.

## Ultron routing contract

**Choose this skill when:** reviewing application code for security defects at identity and data trust boundaries, especially authentication, authorization, session/token lifecycle, secrets, input validation, output encoding, cryptographic API use, and insecure shipped defaults.

**Choose software-quality-and-security-review when:** the requested review spans broader correctness, reliability, maintainability, design quality, and security rather than being primarily an application-security assessment.

**Handoff contract:** this skill returns security-specific findings, exploit preconditions, affected principals/resources, data exposure or privilege impact, and focused regression cases. The broader review skill may integrate those findings with non-security defects but must preserve their severity and evidence.

**Why the boundary exists:** security review needs threat-oriented reasoning and abuse cases; broad code review also evaluates correctness and maintainability. A general review must not dilute a security-critical finding.
