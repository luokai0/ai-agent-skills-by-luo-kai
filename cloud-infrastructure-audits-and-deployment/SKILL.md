---
name: cloud-infrastructure-audits-and-deployment
description: Use when auditing an existing cloud environment (accounts, networks, identity, compute, storage, data stores, cost, logging) or planning and executing an infrastructure deployment change that must be verified, reviewed, and reversible.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Cloud Infrastructure Audits And Deployment

## Purpose and boundaries

This skill covers two linked activities: (1) read-only audits that establish what exists, how it is configured, and where it deviates from stated requirements; and (2) controlled deployments that change infrastructure through reviewed, reversible steps. It applies to any major provider, and to infrastructure-as-code (IaC) and console-driven environments alike.

In scope: inventory, configuration review, identity and access review, network exposure, encryption and secrets handling, backup and recovery posture, logging and monitoring coverage, cost anomalies, plan-and-apply deployments, post-deployment verification, and rollback planning.

Out of scope: application code review, penetration testing or active exploitation, incident response during a live breach (hand off to the incident owner), compliance certification (this skill produces evidence, not attestations), and procurement or contract decisions.

## Inputs and assumptions

Before starting, confirm and record:

- Target scope: account or subscription identifiers, regions, projects, environments (prod, staging, dev), and explicit exclusions.
- Objective: audit question, or the change being deployed, with its success criteria.
- Access level granted: read-only roles for audits; for deployments, the named change owner and the approving party.
- Source of truth: IaC repository and commit, or "console-only" if none exists. Drift between the two is a finding in itself.
- Requirements baseline: internal standards, data classification, and any external framework the owner wants referenced. Do not assume a framework applies.
- Change window and freeze calendar.

Assumptions must be written down and labeled. If a provider feature, CLI flag, or quota behavior is version-sensitive, mark it "verify against current official documentation" and do not rely on memory for exact names or limits.

## Operating workflow

### Audit track

1. Snapshot inventory. Enumerate resources per scope using read-only listing or export tools. Record counts by type, region, and owner tag. Save the raw output with a timestamp.
2. Identity review. List human and workload principals, privileged role assignments, long-lived credentials, unused principals (no activity in 90 days is a common starting threshold, adjust to policy), and cross-account trust.
3. Network exposure. Identify every resource reachable from the public internet: load balancers, public IPs, storage with public access settings, databases with public endpoints, and management ports. Trace each to a justified owner and purpose.
4. Data protection. Check encryption at rest and in transit settings, key ownership and rotation policy, backup enablement, backup retention, and whether restore has ever been tested (look for evidence, not claims).
5. Observability. Confirm audit/control-plane logging is enabled in all regions and retained to a location the workload team cannot alter. Confirm alerts exist for root or break-glass usage and for security-group or policy changes.
6. Cost and capacity. Flag unattached volumes, idle reserved capacity, oversized instances with sustained low utilization, and untagged spend. Report as observations; do not recommend termination without owner confirmation.
7. Classify findings using the severity table in Decision gates, then write the report.

### Deployment track

1. Write the change request: target state, affected resources, dependencies, expected downtime (state "none" only if verified), and rollback procedure.
2. Produce a plan or dry run with the IaC tool or provider's preview mechanism. Save the full plan output.
3. Review the plan line by line. Every destroy, replace, or IAM/network-policy change requires explicit mention in the request.
4. Stage in a non-production environment first when one exists that mirrors the target configuration. Record differences that make staging non-representative.
5. Obtain approval (see gates), then apply the exact reviewed plan artifact. Never re-plan silently between review and apply; if the plan changed, return to step 3.
6. Verify (see Verification and evidence), then monitor for the agreed soak period before closing.
7. Record outcome, deviations, and any manual steps taken.

## Decision gates

Stop and obtain explicit written approval from the named owner before:

- Deleting, replacing, or resizing any stateful resource (databases, volumes, object buckets, key vaults, DNS zones).
- Changing IAM policies, role trust, or key material.
- Opening any inbound path to the internet or widening an existing one.
- Disabling logging, backups, encryption, or deletion protection, even temporarily.
- Any action affecting resources outside the approved scope, or that sends data to a new external party.
- Any apply performed outside a change window or during a freeze.
- Any action where rollback is partial or unknown.

Severity classification for audit findings:

- Critical: publicly reachable stateful data with no authentication, or privileged credentials exposed in plaintext. Escalate immediately.
- High: privileged access without MFA or review, logging disabled in a production account, backups absent for production data.
- Medium: overbroad but authenticated access, missing encryption-at-rest settings on non-sensitive stores, unowned resources.
- Low: tagging gaps, naming inconsistency, unused non-sensitive resources.

Proceed autonomously only with read-only inventory, plan generation, and report drafting.

## Verification and evidence

Every claim in a report needs a source: a command output, export file, or console screenshot reference, with timestamp and account identifier. Unsourced claims are excluded.

Deployment checks, all required before closing:

- Plan artifact applied matches the reviewed plan (hash or stored artifact ID recorded).
- Resource state matches the declared configuration on a fresh read, not the apply output alone.
- Health checks pass on every changed endpoint for the soak window.
- Security configuration re-audited: exposure, IAM, encryption, and logging for changed resources.
- Backup or snapshot taken before the change exists and is restorable (confirm restore metadata; a full restore test is required for stateful changes).
- Drift check: IaC source and live state agree; any manual change is either codified or reverted.

Audit quality bar: at least 95% of inventoried resources have an assigned owner tag or a recorded "unowned" finding; every critical or high finding has reproduction evidence and a named remediation owner.

## Failure handling

- Permission denied during audit: record the gap as a coverage limitation. Do not escalate privileges to fill it.
- Plan shows unexpected destroy: halt, do not apply, return to change owner with the diff.
- Apply partially fails: stop further changes, capture state and error output, and follow the pre-written rollback. If no rollback exists, escalate before any corrective action.
- Health check fails after apply: roll back if the rollback is verified and within window; otherwise escalate.
- Evidence conflicts (console versus IaC disagree): report both, treat live state as authoritative for risk, and do not "fix" either side without approval.
- Rate limits or timeouts: pause, record progress, resume from the last recorded checkpoint.

## Deliverable contract

Audit report, in this order:

1. Scope, timestamp, and access level used.
2. Coverage statement: what was checked, what was not, and why.
3. Findings table: ID, severity, resource, evidence reference, owner, recommended action.
4. Assumptions and version-sensitive items flagged for verification.
5. Recommended next actions requiring approval, listed separately.

Deployment record:

1. Change request and approvals with names and dates.
2. Plan artifact reference and reviewed summary of destroy/replace/IAM/network changes.
3. Apply result, verification evidence, and soak outcome.
4. Rollback procedure status and any deviations or manual steps.

Do not state that a system is compliant, secure, or fully recovered. State only what the evidence shows.