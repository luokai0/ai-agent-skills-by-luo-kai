---
name: reliability-and-debugging
description: Use when diagnosing intermittent or failing authentication, authorization, session, token, MFA, or SSO behavior in production or staging, or when fixing reliability in auth components without weakening security controls.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Reliability And Debugging

## Purpose and boundaries

Locate, reproduce, and fix faults in authentication and authorization paths: login, MFA, token issuance and validation, session lifecycle, federation, password reset, account recovery, rate limiting, and lockout. Preserve every security property while restoring correct behavior.

Out of scope: designing new cryptographic primitives, bypassing controls to make a flow pass, and testing systems without owner authorization.

A fix that restores availability by weakening verification is a failed fix. Examples: disabling signature checks, widening accepted issuers or audiences, extending token lifetimes without justification, or removing lockout.

## Inputs and assumptions

Required before work begins:
- Symptom statement: affected population, error text or code, first-seen time, failure rate, environment.
- Component map: identity provider, gateway, application, session store, key source, time sources.
- Recent changes: deployments, configuration, certificate or key rotations, dependency upgrades, IdP tenant changes.
- Access: read-only logs and metrics by default.

Assumptions to state explicitly: clocks are NTP-synchronized unless shown otherwise; logs use UTC; user-facing errors are generic while internal logs are detailed.

## Operating workflow

1. Write one falsifiable sentence: "For [population], [operation] fails with [observable] since [time]." Refuse vague reports until narrowed.
2. Establish a baseline of success and failure rates by client, region, IdP, and build.
3. Trace one failing request end to end using correlation identifiers. Record each hop's decision and timestamp.
4. Classify the fault (see Decision gates) and form one hypothesis.
5. Reproduce in staging or a local harness using synthetic accounts only.
6. Test the hypothesis by changing one variable at a time. Log every change.
7. Apply the smallest fix that restores correct behavior, not merely a passing request.
8. Verify, deploy through a canary or flag where available, and compare against the baseline.

High-yield checks:
- "Not yet valid" or "expired" errors: compare issuer and verifier clocks, and confirm the configured skew tolerance and its unit.
- Intermittent 401s across replicas: signing key sets differ between instances, or a key cache did not refresh after rotation.
- Redirect loops: cookie attributes (domain, path, Secure, SameSite) or redirect URI mismatch after a host or proxy change. Check forwarded headers.
- SSO failing for some tenants: metadata or claim mapping differences. Compare claim names and structure, never claim values.
- Lockout spikes: a retry storm from one client, or shared NAT addresses hitting per-IP limits.

## Decision gates

- Gate 1, security-relevant? Any change to validation, key handling, token lifetime, redirect rules, or rate limits requires security review and explicit approval before deployment.
- Gate 2, reversible? Code and configuration rollbacks need a tested rollback path. Key deletion, mass session revocation, bulk lockout resets, schema migrations, and IdP setting changes require explicit approval with a stated blast radius.
- Gate 3, externally visible? Changes affecting relying parties, tenant settings, or customer notifications require approval from the system owner.
- Gate 4, evidence sufficient? If the hypothesis is not reproduced after two focused attempts, stop and collect targeted telemetry instead of guessing.

## Verification and evidence

Acceptance requires all of the following:
- The reproduced failure now succeeds, and at least one control case per affected client type succeeds.
- Negative cases still fail: expired token, wrong audience, wrong issuer, bad signature, replayed authorization code, locked account.
- Failure rate returns to baseline within the agreed window (for example, 30 minutes on canary) with no new error classes.
- Logs contain no tokens, passwords, secrets, raw assertions, or full personal identifiers.
- Any product- or library-specific setting cited in the fix is verified against current official documentation for the deployed version before it is relied on.

## Failure handling

- If the fix increases security-relevant signals (accepted invalid tokens, successful logins from unexpected sources), roll back immediately and open a security incident.
- If rollback is unavailable, disable only the changed component and notify the owner.
- Do not repeatedly trigger production authentication flows to reproduce a bug. Use labeled test accounts with rate limits.
- If root cause is unknown after the evidence gate, report the narrowed scope and open an investigation item rather than shipping a speculative change.

## Deliverable contract

Produce:
1. Defect summary: symptom, population, time window, root cause, confidence level.
2. Evidence: correlation identifiers, timestamps, redacted log excerpts.
3. Change record: code or configuration diff reference, rollback procedure, named approvers.
4. Verification results mapped to the acceptance checklist.
5. Residual risk and follow-up items, each with an owner.

What not to do:
- Do not disable signature, audience, issuer, expiry, or lockout checks as a diagnostic step in production.
- Do not paste secrets, tokens, or raw assertions into tickets, chat, or commits.
- Do not claim a compliance outcome from a debugging fix.
- Do not invent flag names, parameters, or version behavior. Verify them first.

## Ultron routing contract

**Choose this skill when:** an authentication or authorization path is failing, flaky, slow, or inconsistent and the task requires reproduction, trace analysis, root-cause isolation, a minimal repair, and regression proof.

**Choose `quality-assurance` when:** the task is to define or run a systematic test plan for authentication/security behavior, establish coverage, or produce formal verification and sign-off evidence rather than diagnose one known defect.

**Handoff contract:** accept a reproducible case or observed symptom. Return the causal chain, affected state transitions, smallest safe fix, regression test, and explicit evidence that signatures, issuers, audiences, expiry, MFA, lockout, and authorization checks remain enforced as applicable. Send the repaired case back to QA for broader suite validation.

**Why the boundary exists:** incident diagnosis and test assurance are complementary. Do not make the debugger invent broad release coverage or ask QA to guess at root cause.
