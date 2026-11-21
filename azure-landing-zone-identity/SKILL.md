---
name: azure-landing-zone-identity
description: Use when designing, reviewing, or troubleshooting identity foundations for an Azure landing zone, including Microsoft Entra ID tenant structure, RBAC role assignments, management group scope, managed identities, privileged access, and break-glass accounts.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Azure Landing Zone Identity

## Purpose and boundaries

This skill guides the identity layer of an Azure landing zone: who can act, at what scope, with which privilege, and how that is proven and audited. It covers Microsoft Entra ID (tenant and directory configuration relevant to Azure access), Azure RBAC at management group, subscription, and resource scope, managed identities, workload identity, privileged access, and emergency access.

It does not cover network topology, policy-as-code authoring beyond identity-related policies, workload application auth design, or on-premises AD federation internals beyond the trust boundary. Hand those to the relevant skills.

## Inputs and assumptions

Collect before acting:

- Management group hierarchy (exported, not recalled from memory).
- Subscription inventory with owners, environment tags, and workload classification.
- Current role assignments at each management group and subscription, exported to a file.
- Entra ID licensing tier, since PIM, conditional access, and access reviews depend on it. Verify feature availability against current Microsoft documentation.
- Identity sources: cloud-only, synced, or federated users, and any external identities.
- Compliance obligations stated by the organization. Do not assume a framework is in scope; ask.

Assumptions must be written down in the deliverable. Any version-sensitive behavior (role names, portal labels, CLI syntax, licensing requirements) must be marked "verify against current official documentation" unless you have confirmed it in this session.

## Operating workflow

1. **Baseline.** Export management group tree, role assignments (including inherited and deny assignments where readable), Entra directory roles, and service principals with credentials. Store exports as evidence.
2. **Classify principals.** Group every principal as human user, group, service principal, managed identity, or external guest. Flag any principal with Owner or User Access Administrator above subscription scope.
3. **Map intent to scope.** For each required capability, choose the narrowest scope that serves the workload. Prefer resource group scope for application teams, subscription scope for platform operations, and management group scope only for cross-cutting governance roles.
4. **Select built-in roles first.** Use a built-in role whose actions match the need. Create a custom role only when no built-in role fits and document the exact action list and its owner.
5. **Assign through groups.** Bind roles to Entra groups, not individual users. Group names encode scope, function, and environment, for example `az-sub-prod-network-contributor`.
6. **Replace standing privilege.** Make elevated roles eligible rather than active where licensing allows, with justification, approval, and time limits.
7. **Use managed identities.** Replace stored secrets for Azure-hosted workloads with managed identities. Where a service principal is unavoidable, record its owner, purpose, credential type, and expiry.
8. **Configure break-glass.** Two or more cloud-only emergency accounts, excluded from routine conditional access only as documented, with credentials held under dual control and sign-in monitored.
9. **Validate and hand off.** Run the checks in the verification section and produce the deliverable.

## Decision gates

Stop and obtain explicit human approval before proceeding if any step would:

- Delete, move, or re-parent management groups or subscriptions.
- Remove role assignments, disable accounts, or delete service principals that may be in use.
- Grant Owner, User Access Administrator, Global Administrator, or any tenant-wide role.
- Change conditional access policies or exclusions that could lock out administrators.
- Rotate or revoke credentials for production workloads.
- Alter external sharing, guest invitation, or cross-tenant settings.
- Touch emergency access accounts.
- Apply changes to a production scope from a non-production analysis.

Approval must name the specific change, scope, and rollback step. A general "go ahead" is not sufficient for gates on irreversible actions. Read-only exports and analysis do not require approval.

## Verification and evidence

Each finding and change must be backed by evidence:

- **Least privilege check:** Count principals holding Owner or User Access Administrator at management group and subscription scope. Target: each count justified in writing, with zero unexplained entries.
- **Standing privilege check:** Percentage of elevated assignments that are eligible rather than active. Report the baseline and the target.
- **Secret exposure check:** Number of service principals with password or certificate credentials older than the organization's rotation standard. Report by owner.
- **Orphan check:** Role assignments whose principal no longer exists or is disabled. Target: zero.
- **Break-glass check:** Confirm at least two emergency accounts exist, have been tested in a sign-in exercise within the last review period, and that the test is logged.
- **Drift check:** Compare the current export against the approved baseline; every difference must map to a ticket or approval.

Record the date, tool, command or portal path, and operator for each check. Do not report a check as passed unless its output was reviewed.

## Failure handling

- **Export incomplete or permission denied:** Stop the affected analysis, record the gap, and do not infer missing assignments. Request the reader role needed.
- **Assignment cannot be removed due to dependency:** Document the dependent resource and owner, add a remediation item, and do not force removal.
- **Lockout risk discovered:** Halt changes to conditional access or role removal affecting administrators. Escalate to the tenant owner.
- **Conflicting requirements between teams:** Present the options with scope, risk, and cost; decision belongs to the accountable owner.
- **Unverifiable version behavior:** Mark the item as unverified in the deliverable instead of asserting a behavior.

## Deliverable contract

Produce a single report containing:

1. Scope statement and assumptions list.
2. Principal and role inventory summary with counts per scope.
3. Findings table: finding, scope, evidence reference, risk rating, proposed action, approval required (yes/no).
4. Ordered remediation plan with rollback step for each change.
5. Verification results for each check in the verification section, with status and evidence location.
6. Open items, including every unverified version-sensitive detail.

Do not include secrets, credential values, tokens, or full tenant identifiers in the report; reference them by a stable internal label.

## What not to do

- Do not assign Owner as a convenience to unblock a team.
- Do not assign roles to individual users when a group exists or should exist.
- Do not create a shared account for administrators.
- Do not store secrets in pipelines, scripts, or documents when a managed identity or federated credential is available.
- Do not remove emergency access or change its exclusions without approval.
- Do not state licensing, compliance, or feature availability as fact without verifying it against current Microsoft documentation.\n\n## Ultron routing contract

**Choose this skill when:** the question concerns Azure identity and authorization foundations across tenants, management groups, subscriptions, and resources: Entra directory roles, Azure RBAC, managed identities, workload identities, privileged access, emergency accounts, and identity governance.

**Choose `azure-app-and-data-services` when:** the work is configuring or operating a particular application host or managed data service and only needs a workload-specific identity decision.

**Handoff contract:** receive the workload's exact resource scope, required actions, environment, principal lifecycle, and operational owner. Return the narrowest viable principal and role assignment, approval requirements, and verification evidence. Avoid granting subscription- or tenant-wide authority for a resource-level workload need.

**Why the boundary exists:** identity policy is a shared security foundation; application services are consumers of that foundation and must not create their own exceptions without governance.
