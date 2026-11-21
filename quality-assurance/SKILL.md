---
name: quality-assurance
description: Use when planning, executing, or reviewing quality assurance for authentication and security controls, including login, session, MFA, password reset, token handling, authorization checks, and security regression testing.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Quality Assurance

## Purpose and boundaries

This skill defines how to test authentication and security-relevant functionality so that defects are found, reproduced, classified, and verified with evidence. It covers test design, execution, triage, and sign-off for:

- Credential login, lockout, and rate limiting
- Multi-factor enrollment, challenge, and recovery
- Password reset, account recovery, and email or phone verification
- Session creation, expiry, rotation, and logout invalidation
- Token issuance, validation, audience, expiry, and revocation
- Authorization boundaries (object-level and function-level access)
- Security headers, cookie attributes, and transport settings as observed by a tester

It does not cover writing production code, performing penetration tests against systems without written authorization, or certifying compliance. Compliance statements require the owning compliance function.

## Inputs and assumptions

Before testing, confirm:

1. A written scope naming environments, hostnames, accounts, and permitted test types.
2. Test accounts with defined roles, created for testing only. Do not use real customer or employee credentials.
3. Requirements or acceptance criteria. If none exist, record assumed behavior and mark it as assumed.
4. The version or build under test, and the current official documentation for any protocol, library, or identity provider involved. Version-sensitive behavior must be checked against that documentation; do not rely on memory.

If any input is missing, stop and request it.

## Operating workflow

1. **Map the surface.** List every entry point for the feature: UI flows, API endpoints, redirects, callbacks, and admin paths. Record each as a row in a test matrix.
2. **Derive cases from threats and requirements.** For each row, write cases for the expected path, each documented failure path, and at least these abuse cases: credential stuffing response, replayed tokens or codes, expired session reuse, parameter tampering, missing-authorization access, and user enumeration through response differences or timing.
3. **Assign priority.** Rate each case by impact and likelihood: P1 for authentication bypass, account takeover, or privilege escalation; P2 for information disclosure or weakened controls; P3 for hardening gaps.
4. **Execute in a controlled order.** Run positive baseline tests first, then negative tests, then abuse tests. Record environment, build, account, timestamp, and request or screen evidence for each result.
5. **Reproduce before reporting.** Every failure must reproduce at least twice from a clean state.
6. **Triage and report.** Classify each defect, attach evidence, and state the expected and observed behavior.
7. **Verify fixes.** Retest the original case plus adjacent cases in the same control family.

## Decision gates

- **Gate A (scope):** Proceed only if scope is written and covers the target. Otherwise halt.
- **Gate B (data):** Proceed only with test accounts. If production data appears in responses, stop, record the exposure, and escalate.
- **Gate C (destructive or external actions):** Requires explicit named approval before: account lockout of shared accounts, mass login attempts beyond the agreed rate limit, testing against third-party identity providers, sending real emails or SMS to non-test recipients, deleting or modifying user records, rotating shared secrets or signing keys, or any action that could affect other users or external parties.
- **Gate D (severity escalation):** Any confirmed authentication bypass, exposed credential, or cross-account data access is escalated immediately to the named security owner, before the full report is complete.
- **Gate E (sign-off):** Release is recommended only when all P1 cases pass, no open P2 defects lack an accepted risk record, and retests are complete.

## Verification and evidence

Each result must include:

- Case ID, priority, environment, build, account role
- Exact steps and inputs (credentials redacted to role labels)
- Expected result with source reference
- Observed result with timestamped evidence (status code, response shape, screen capture with secrets masked)
- Pass, fail, blocked, or not-applicable with reason

Quality measures for the test cycle:

- 100% of P1 cases executed and passed or formally waived.
- Every failure reproduced twice.
- Every defect has a severity, a single root-cause hypothesis, and a retest result.
- Test matrix covers 100% of listed entry points; uncovered entry points are reported as gaps.

## Failure handling

- **Environment instability:** Record it, pause, and do not count results from unstable runs.
- **Account lockout during testing:** Stop, record, and request unlock through the approved process (Gate C).
- **Unexpected production impact:** Stop immediately, notify the owner, and document the timeline.
- **Ambiguous requirement:** Mark the case blocked and request a decision. Do not invent expected behavior.
- **Tool or library behavior differs from documentation:** Record the discrepancy with the version, and verify against current official documentation before filing.

## Deliverable contract

Deliver a single report containing:

1. Scope, environments, builds, and test accounts (by role)
2. Test matrix with case IDs, priorities, and results
3. Defect list ordered by severity, each with reproduction steps and evidence
4. Coverage gaps and assumptions
5. Gate decisions taken and approvals obtained, with dates
6. Release recommendation: approve, approve with accepted risks (named owner), or reject

Do not include in the report: raw passwords, tokens, session identifiers, private keys, or real personal data. Mask all secrets as role labels or truncated hashes.

## What not to do

- Do not test beyond the written scope or against unauthorized systems.
- Do not declare a control "secure" or "compliant"; report only what was tested.
- Do not state tool flags, API names, or library versions from memory; verify them against current official documentation.
- Do not run credential guessing against real accounts.
- Do not mark a P1 case as passed without retest evidence.