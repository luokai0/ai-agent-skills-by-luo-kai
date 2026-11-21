---
name: security-governance
description: Use when defining, reviewing, or auditing security policies, access control models, authentication standards, secrets handling, or security exception processes for a system, team, or organization, and when translating security requirements into enforceable controls with owners, evidence, and review cadence.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Security Governance

## Purpose and boundaries

This skill governs how security requirements are decided, assigned, implemented, verified, and retired. It covers authentication and authorization policy, identity lifecycle, privileged access, secrets management policy, security exception handling, and control ownership mapping.

In scope: writing or reviewing security standards; mapping requirements to controls; defining access reviews; approving or rejecting exceptions; producing audit-ready evidence checklists.

Out of scope: performing live penetration tests, rotating production credentials, changing identity provider configuration, or making legal or regulatory compliance determinations. Those require the named owner and explicit approval (see Decision gates).

## Inputs and assumptions

Before acting, confirm:

1. System or scope name, owner, and data classification (public, internal, confidential, restricted).
2. Existing policy documents, control inventory, and identity provider or access tooling in use.
3. The requirement source (internal standard, customer contract, regulation). Record it verbatim; do not paraphrase it into a stronger or weaker claim.
4. Current state evidence: access lists, configuration exports, review records, incident history for the scope.
5. Named approvers for risk acceptance.

If any item is missing, record it as an open question and proceed only with analysis that does not depend on it. Do not assume a control exists because a policy mentions it.

## Operating workflow

1. **Scope the asset.** List systems, identities (human, service, workload), and data classes in scope. Exclude nothing silently; list exclusions with reasons.
2. **Extract requirements.** Convert each source statement into a numbered requirement with a single testable condition. Example: "Admin access requires MFA" becomes "All accounts holding role `admin` in the production tenant must have an enrolled phishing-resistant or app-based second factor, verified at login policy level."
3. **Map to controls.** For each requirement, identify the preventive control (policy setting, technical enforcement), the detective control (review, log alert), and the owner. A requirement with no owner is not accepted.
4. **Assess current state.** Compare the control to observed configuration or records. Classify each as Met, Partially Met, Not Met, or Unverifiable.
5. **Prioritize gaps.** Rank by data classification and exposure: internet-reachable, privileged, or restricted-data paths first.
6. **Draft remediation.** For each gap, state the change, the rollback path, the owner, and the target review date. Do not set dates you cannot justify from capacity.
7. **Record exceptions.** Any unmet requirement not remediated in the window becomes an exception with compensating controls, expiry date, and approver.
8. **Schedule verification.** Define the evidence to be collected and the next review date.

## Decision gates

Stop and obtain explicit written approval from the named owner before:

- Any change to production identity providers, MFA enforcement, conditional access, or SSO configuration.
- Revoking, disabling, or deleting accounts, service principals, keys, or certificates in use.
- Rotating or revoking production secrets, or changing secret storage locations.
- Granting standing privileged access or expanding an existing role.
- Accepting risk, granting an exception, or extending an exception beyond its approved expiry.
- Communicating policy changes or findings to external parties, customers, or regulators.
- Any action whose effect cannot be reversed within the agreed rollback window.

Proceed without a gate only for read-only analysis, drafting documents, and proposing changes marked as pending approval.

Exception criteria: approve only when (a) the business reason is documented, (b) a compensating control is verified to operate, (c) expiry is 90 days or less unless the approver records a justified longer term, and (d) the risk owner, not the implementing team, signs.

## Verification and evidence

Every rating must cite evidence. Acceptable evidence: configuration export with timestamp, access review sign-off, log sample covering a stated period, ticket with approval record. Unacceptable: verbal confirmation, policy text alone, or "believed to be enabled."

Quality checks:

- Every requirement has exactly one owner and one testable condition.
- Every Met rating references evidence dated within the last review cycle.
- Access reviews cover 100% of privileged accounts and at least the sampled percentage agreed for standard accounts; record the sample method.
- Each exception has an expiry date, approver, and compensating control reference.
- No orphaned exceptions: none past expiry without renewal approval.
- Secrets policy checks confirm no credentials appear in source repositories, build logs, or tickets, using the team's approved scanning tool. Name the tool and version as verified against its current documentation.

Version-sensitive items (identity provider feature names, scanner rule sets, regulatory citations, cryptographic algorithm recommendations) must be marked "verify against current official documentation" when cited, and not stated from memory.

## Failure handling

- **Evidence unavailable:** Mark the control Unverifiable, not Met. Open a collection task with an owner and date.
- **Conflicting sources:** Report both verbatim, identify the stricter reading as provisional, and escalate for a decision. Do not silently choose.
- **Control found broken during review:** Stop the review of that control, record the finding with timestamp and affected scope, and escalate under the incident process. Do not attempt a fix without a gate approval.
- **Owner unresponsive past the agreed date:** Escalate one level. Do not close the item as accepted.
- **Scope expands mid-review:** Pause, re-run Scope step, and re-confirm inputs.

## Deliverable contract

Produce a governance report containing, in order:

1. Scope statement with inclusions and exclusions.
2. Requirements register: ID, source text, testable condition, control, owner, status, evidence reference.
3. Gap list ranked by exposure, with remediation, rollback, and target date.
4. Exception register: ID, reason, compensating control, expiry, approver, status.
5. Pending approvals: each gated action, the approver, and the decision needed.
6. Open questions and unverifiable items with collection owners.
7. Next review date and evidence to be collected.

Do not present the report as a compliance certification or assurance statement. State that it reflects the evidence listed, as of the stated date.

## What not to do

- Do not record a control as Met based on policy wording or intent.
- Do not include secret values, tokens, or full credential strings in any output; reference them by identifier only.
- Do not grant or approve exceptions on behalf of an owner.
- Do not invent tool names, configuration keys, or version numbers.
- Do not perform changes to live systems during a governance review.
- Do not merge distinct requirements to shorten the register.