---
name: cloud-security-and-compliance
description: Use when assessing, hardening, or auditing cloud accounts, tenants, or workloads for security posture and compliance control mapping, including IAM review, network exposure, encryption, logging, and evidence collection for frameworks such as CIS benchmarks, SOC 2, ISO 27001, or PCI DSS.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Cloud Security And Compliance

## Purpose and boundaries

This skill covers reviewing cloud environments (IaaS, PaaS, managed Kubernetes, serverless, SaaS configuration tied to cloud identity) for security misconfigurations, mapping findings to compliance controls, and producing remediation plans and evidence packages.

In scope: identity and access policy review, network exposure analysis, data encryption and key management checks, logging and audit trail coverage, backup and resilience settings, vulnerability and secret exposure triage, and control-to-evidence mapping.

Out of scope: legal determination of compliance, certification sign-off (only an accredited auditor can attest), incident response execution beyond initial triage, penetration testing against systems without written authorization, and designing new application cryptography.

## Inputs and assumptions

Required inputs before starting:
- Cloud provider(s), account/subscription/project identifiers, and environment tier (prod, staging, dev).
- The target framework and version, and the specific control set in scope.
- Read-only access scope granted to the reviewer (preferably audit or security-reader roles).
- Architecture summary: workload inventory, data classification, internet-facing entry points.
- Date of the review and the audit period, if evidence must cover a window.

Assumptions to state explicitly in the report: configuration snapshots reflect the moment of capture; the reviewer has not verified application logic; provider-managed controls are accepted per the provider's shared responsibility documentation.

If any required input is missing, record it as a gap rather than guessing.

## Operating workflow

1. **Scope the control set.** Map the framework's controls to cloud domains (identity, network, data, logging, workload, change management). Record which controls are in scope and which are inherited from the provider.
2. **Collect configuration state read-only.** Use provider-native inventory and posture tooling, or export policy documents. Save raw exports with timestamps and hashes. Do not modify resources during collection.
3. **Analyze identity first.** Enumerate human and workload identities, privileged roles, long-lived access keys, MFA enforcement on console and CLI paths, cross-account trust, and wildcard permissions in policies.
4. **Analyze exposure.** Identify publicly reachable compute, storage, databases, management ports, and API endpoints. Trace routing and security group or firewall rules to confirm actual reachability, not just rule presence.
5. **Analyze data protection.** Confirm encryption at rest and in transit for storage, databases, and queues; check key ownership, rotation policy, and key access policies.
6. **Analyze logging and detection.** Confirm control-plane audit logs, data-plane access logs where applicable, and centralized retention. Verify log integrity protections and that logs cannot be disabled by the monitored principals.
7. **Triage findings.** Score each finding by exploitability, exposure, data sensitivity, and blast radius. Discard duplicates and provider-default-safe items.
8. **Map to controls and draft remediation.** Each finding maps to one or more control identifiers, has an owner, a fix recommendation, and a verification step.
9. **Package evidence.** Assemble the deliverable described below.

## Decision gates

Stop and request explicit human approval before:
- Any change to production IAM, network, encryption, or logging configuration, including "safe" hardening.
- Disabling, rotating, or deleting keys, secrets, snapshots, or log sinks.
- Running active scans, exploit checks, or any traffic against systems outside the authorized scope.
- Sharing evidence containing credentials, personal data, or internal topology outside the review team.
- Declaring a control "compliant" or "passed" for an external auditor.
- Accepting a risk on behalf of the business.

Proceed without approval only for read-only enumeration within the granted role.

Severity decision criteria:
- **Critical:** Publicly reachable admin or database interface with no authentication, or credentials exposed in a readable location.
- **High:** Privileged role assignable without MFA, unencrypted sensitive data store reachable from the internet, audit logging disabled in production.
- **Medium:** Overly broad but not wildcard permissions, missing key rotation within policy, logs retained below required period.
- **Low:** Hygiene issues without a demonstrated exposure path.

## Verification and evidence

Every finding must include: resource identifier, configuration excerpt or export reference, timestamp, the control mapped, and a reproducible check command or console path. Verify each finding twice: once by policy document, once by effective state (for example, effective permissions or reachability), since policies can be overridden by boundaries, conditions, or other rules.

Measurable quality checks before delivery:
- 100% of in-scope controls have a status: pass, fail, not applicable with reason, or insufficient evidence.
- Zero findings without a resource identifier and evidence reference.
- Every critical and high finding has a named owner and a target remediation date set by the business.
- Raw exports are hashed and retained in the evidence store.
- Provider feature behavior cited in the report is checked against current official documentation on the review date.

Mark version-sensitive details (API field names, default settings, supported algorithms, service limits) with the note "verify against current provider documentation" rather than stating them as fact.

## Failure handling

- **Insufficient permissions:** Record the blocked control as "insufficient evidence." Do not escalate privileges to fill the gap.
- **Conflicting data between tools:** Trust the provider's control-plane export over third-party summaries, and note the discrepancy.
- **Resource appears misconfigured but is unreachable or disabled:** Downgrade severity and document the reason; recheck after the review window.
- **Discovered active compromise indicators:** Stop the review, preserve current state, and escalate to the incident response owner. Do not attempt remediation.
- **Scope ambiguity:** Pause and request clarification on account boundaries before analyzing.

## Deliverable contract

The output is a single report containing, in order:
1. Scope statement, assumptions, and input gaps.
2. Control matrix: control ID, framework, status, evidence reference, reviewer note.
3. Findings register: ID, severity, resource, description, control mapping, evidence, remediation, owner, verification step.
4. Remediation plan grouped by owner, with items requiring approval marked.
5. Evidence index with export names, capture times, and hashes.
6. Limitations and version-sensitivity notes.

Do not include raw secrets, full access keys, or unredacted personal data in the report; reference their location instead.

Do not claim the environment is "secure" or "compliant." State findings and control status only.

## Ultron routing contract

**Choose this skill when:** reviewing a real cloud environment for security configuration defects and mapping technical findings to the organization's control framework, with remediation and evidence planning.

**Choose security-governance when:** the task is to define security requirements, control ownership, access review policy, exception handling, or organization-wide security standards rather than inspect a particular environment.

**Handoff contract:** receive the control objectives, approved risk thresholds, and evidence requirements from governance. Return the resource-level observations, technical proof, severity, remediation plan, and any control that cannot be evaluated. Send unresolved policy conflicts or exception requests back to governance with scope and impact.

**Why the boundary exists:** a cloud configuration scan cannot decide the organization's policy, and a written policy cannot prove that a cloud resource is configured correctly.
