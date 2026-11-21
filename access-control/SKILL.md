---
name: access-control
description: Use when designing, reviewing, or auditing who can access which resources (authorization models, RBAC/ABAC policies, IAM roles, least-privilege reviews, access requests, or permission revocation) in applications or cloud/infrastructure environments.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Access Control

## Purpose and boundaries

This skill guides the design, review, and verification of authorization: deciding and enforcing which principals (users, services, workloads, API clients) may perform which actions on which resources, under which conditions. It covers application-level checks, identity and cloud policy (roles, grants, resource policies), access-request and review processes, and revocation.

It does not cover: authentication mechanics (credential storage, MFA enrollment, session token issuance), network perimeter design, cryptographic key management, or legal compliance determinations. Where these touch access decisions, flag the dependency and hand off.

## Inputs and assumptions

Collect before acting:

- Protected resources and their owners, with sensitivity classification.
- Principal types in scope (human, service account, CI job, third party) and the identity provider that asserts them.
- Current permission model (roles, groups, attributes, ACLs, policy documents) and where it is enforced (application code, gateway, cloud IAM, database).
- Required business rules expressed as who/what/when/where statements.
- Environment: production vs. non-production, tenant boundaries.

Assumptions must be written down. If the identity source of truth or resource inventory is unknown, stop and request it rather than inferring.

## Operating workflow

1. **Inventory.** List resources, actions, and current grants. Export the actual state (role assignments, policy documents, group memberships) rather than relying on design docs.
2. **Model.** Choose the simplest model that meets requirements: RBAC for stable job functions; ABAC or relationship-based checks when decisions depend on resource ownership, tenant, or attributes. Define roles or attributes as a closed vocabulary.
3. **Derive least privilege.** For each principal, map required actions to the minimum resource scope and duration. Remove wildcards on actions and resources unless a documented reason exists.
4. **Locate enforcement.** Each protected action must have exactly one authoritative check point per layer, default-deny on error or missing rule. Check that object-level checks exist, not just route-level.
5. **Diff.** Compare derived minimum against actual grants. Classify each excess as stale, unjustified, or justified-with-owner.
6. **Propose changes** as an ordered set: additive grants before removals, with rollback steps for each.
7. **Verify** (see below), then obtain approval before applying.

## Decision gates

Stop and obtain explicit human approval before:

- Removing or modifying grants for production principals, or any change that could lock out an operator or break a running service.
- Granting administrative, owner, or wildcard privileges.
- Changes to cross-account, cross-tenant, or third-party access.
- Disabling audit logging or altering retention.
- Bulk revocation or any action affecting more than one team.
- Any action that touches live identity providers, cloud consoles, or production data.

Proceed without a gate only for read-only analysis and drafting proposals in a non-production copy.

Escalate to a security owner when: an excess grant reaches sensitive data, a broken object-level check is found in production code, or an access pattern suggests compromise.

## Verification and evidence

Each change must have:

- **Positive tests:** the intended principal performs each permitted action (one test per role-action pair).
- **Negative tests:** each non-permitted principal is denied, including cross-tenant and unauthenticated cases, and an object ID belonging to another owner.
- **Default-deny test:** an unknown role, missing attribute, or policy evaluation error results in denial.
- **Drift check:** exported grants match the approved model after the change.
- **Audit check:** denials and grant changes are logged with principal, action, resource, and decision.

Quality targets: zero wildcard grants without a recorded exception; 100% of protected endpoints have a mapped permission in the inventory; every standing privileged grant has a named owner and review date no more than 90 days out (a local policy choice; adjust to your governance standard).

Record evidence as: the exported before/after grant set, test names and results, approver identity and timestamp, and rollback command or procedure.

## Failure handling

- **Test failure after change:** halt further changes, revert to the prior state using the recorded rollback, and document the failing case.
- **Lockout or service outage:** prioritize restoring a break-glass path using the pre-approved emergency procedure; do not improvise new admin grants.
- **Unknown principal or resource discovered:** treat as unauthorized until owner is identified; do not grant it access to resolve the ambiguity.
- **Conflicting rules:** the more restrictive rule wins; surface the conflict to the owner.
- **Cloud or IdP behavior uncertain:** verify against current official documentation for the specific product version before acting. Mark any version-sensitive syntax or flag as unverified until confirmed.

## Deliverable contract

Produce a single report containing:

1. Scope and assumptions (listed explicitly).
2. Model summary: roles/attributes, enforcement points, and default-deny confirmation.
3. Findings table: principal, resource, current grant, minimum required, classification (stale / excess / justified / missing), severity.
4. Ordered change plan with per-step rollback.
5. Gate list: each change requiring approval, marked pending.
6. Verification plan and results (or explicit "not yet run" status).
7. Open questions and owner assignments.

Do not claim a control is effective without the test evidence above. Do not state that a configuration satisfies any regulatory or framework requirement; state only what was checked.

## What not to do

- Do not grant broad access to unblock a task; grant the narrowest scope and document it.
- Do not treat authenticated as authorized.
- Do not rely on client-side hiding of UI elements as a control.
- Do not apply changes directly to production from analysis output.
- Do not copy permissions from one principal to another without re-deriving need.
- Do not invent role names, policy syntax, or API calls; confirm against current documentation.