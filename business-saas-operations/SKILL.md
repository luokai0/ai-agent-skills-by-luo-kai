---
name: business-saas-operations
description: Use when administering, auditing, or changing business SaaS tool configurations (CRM, helpdesk, HR, finance, collaboration suites) that are reached through external registries, marketplaces, or app directories, including vendor onboarding, app listing reviews, integration setup, and access reconciliation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Business SaaS Operations

## Purpose and boundaries

This skill guides operators through the lifecycle of business SaaS tools that are discovered, installed, or connected via external registries: vendor marketplaces, app directories, package feeds for SaaS extensions, and third-party integration catalogs. It covers vetting listings, planning installs, configuring integrations, reconciling access, and documenting the result.

In scope: listing and publisher review, permission-scope analysis, sandbox trials, configuration changes in non-production tenants, access-role mapping, integration runbooks, and operational handoff.

Out of scope: writing vendor code, negotiating contracts, legal compliance determinations, and production changes that have not passed the decision gates below.

## Inputs and assumptions

Before acting, collect:
- Tool name, vendor, registry source, and the exact listing or identifier.
- Business owner and the process the tool supports.
- Target environment (sandbox, staging, production) and tenant identifiers.
- Requested permissions or scopes, and the data categories they would touch (customer PII, financial records, employee data, credentials).
- Current access-control model: roles, groups, admin owners.
- Change window and rollback owner.

Assume nothing about a listing's safety, publisher identity, or currency of documentation. Treat vendor claims as unverified until checked against the vendor's own official documentation.

## Operating workflow

1. **Record the request.** Write a one-paragraph statement: what the tool does for the business, who uses it, and what data it will touch.
2. **Verify the source.** Confirm the registry is the vendor's official marketplace or a vetted directory. Check publisher verification status, listing ownership history, and install counts only as weak signals. Note the listing's last-updated date.
3. **Map permissions.** List every requested scope or permission. For each, state the reason it is needed and the minimum alternative. Flag any scope granting write access to records, admin rights, or unrestricted data export.
4. **Assess data flow.** Draw the path: source system to tool to destination. Identify where data is stored, which region, and what retention the vendor documents. Mark anything the vendor does not document as unknown.
5. **Trial in a non-production tenant.** Install with the narrowest scope. Use synthetic or anonymized data. Record every API call, webhook, and outbound domain observed during the trial.
6. **Compare trial against declared behavior.** Any undeclared outbound destination, scope use beyond the stated purpose, or unexpected data volume is a stop condition.
7. **Draft the production change plan.** Include steps, owner, rollback procedure, role mapping, and monitoring checks.
8. **Obtain approval** at Gate C, then execute during the agreed window.
9. **Reconcile post-change.** Confirm access lists match the approved role map and remove trial credentials.

## Decision gates

- **Gate A (source):** Proceed only if the listing is from the vendor or a publisher the organization has already vetted. Unverified publishers require security review before any trial.
- **Gate B (scope):** Proceed to trial only if every scope maps to a documented business need. Reject or narrow any scope granting admin, bulk export, or cross-tenant access.
- **Gate C (production):** Requires explicit written approval from the business owner and the system administrator, plus a security reviewer for any tool touching customer, financial, or employee data. Approval must name the scopes, environment, and change window.
- **Stop condition:** Halt immediately on undeclared network destinations, credential requests outside the approved flow, or unexplained data volume spikes.

Example: a helpdesk add-in requests "read all tickets and all attachments" for a reporting need that only requires ticket status and category. Narrow the scope or reject; do not approve the broad request and rely on later policy.

## Verification and evidence

Each gate must produce a retained artifact:
- Listing review record: URL, publisher, verification status, capture date.
- Permission matrix: scope, justification, minimum alternative, decision.
- Trial log: observed endpoints, data fields sent, error rates.
- Approval record: approver names, date, scopes, environment.
- Post-change reconciliation: diff of expected versus actual role assignments, showing zero unexplained entries.

Quality checks:
- 100% of requested scopes have a documented justification.
- Zero undeclared outbound domains in trial logs.
- Access reconciliation shows no orphaned trial accounts after 24 hours.
- Rollback procedure has been rehearsed in the non-production tenant at least once.

Version-sensitive details (API scope names, permission identifiers, marketplace policies, vendor data-residency terms, and certification claims) must be checked against the vendor's current official documentation at the time of review. Record the documentation URL and access date. Do not rely on memory or on cached listing text.

## Failure handling

- **Trial fails:** Capture the error, the scope or endpoint involved, and the vendor's documented behavior. Do not broaden scopes to make the trial pass. Escalate to the vendor or reject the tool.
- **Undeclared behavior found:** Stop, preserve logs, notify the security reviewer, and disable the integration credential. Do not delete logs.
- **Production change causes errors:** Execute the rollback plan at once. Notify the business owner. Record the timeline.
- **Listing changes after approval:** Re-run Gates A and B before any further update.
- **Approver unavailable during window:** Postpone. Do not self-approve.

## Deliverable contract

Each engagement ends with a single review package containing:
1. Summary (under 150 words): tool, purpose, decision, and residual risk.
2. Listing review record and permission matrix.
3. Data flow diagram or table with unknowns explicitly marked.
4. Trial log summary and comparison to declared behavior.
5. Approval record and change plan with rollback steps.
6. Post-change reconciliation result.
7. Open items with named owners and due dates.

What not to do:
- Do not install from unverified listings or sideload packages into production.
- Do not grant admin or bulk-export scopes as a convenience.
- Do not test with real customer or employee records.
- Do not store vendor credentials in tickets, chat, or documentation; reference the secrets manager entry instead.
- Do not treat registry ratings or install counts as evidence of security.
- Do not state that a tool is compliant with any regulation or certification unless the vendor's current documentation and your internal assessment confirm it.