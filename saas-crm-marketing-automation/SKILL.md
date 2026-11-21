---
name: saas-crm-marketing-automation
description: Use when designing, auditing, or building marketing automation on a SaaS CRM, including lead capture, lifecycle stages, segmentation, lead scoring, nurture sequences, and sync rules, especially when an AI agent will read or write CRM or marketing records.
author: Luo Kai
provenance: original
version: 1.0.0
---

# SaaS CRM Marketing Automation

## Purpose and boundaries

This skill covers designing, reviewing, and changing marketing automation that moves contacts, accounts, and opportunities through a SaaS CRM: capture, deduplication, lifecycle staging, segmentation, scoring, nurture sequencing, and sales handoff.

Out of scope: legal determination of consent or lawful basis (refer to counsel), paid media buying, product analytics instrumentation, and data-warehouse modeling beyond reconciling counts.

## Inputs and assumptions

Required before work begins:
- Platform names and the workspace or account identifiers the user owns.
- Lifecycle definitions with entry and exit criteria and a named owner per stage.
- Field dictionary for contact, account, and lead objects, including required fields and allowed picklist values.
- Consent and suppression fields, and the source of each consent record.
- A sample export of current records, minimized to the columns needed.
- Success metrics with a current baseline.

Record every assumption. If a platform feature, limit, or API behavior affects the design, mark it "verify against current vendor documentation." Do not state endpoint names, rate limits, or plan entitlements unless the user supplied them from current documentation.

## Operating workflow

1. **Map current state.** List every entry point (forms, imports, integrations, API writes), every stage transition, and every automated action. Record the system of record for each field.
2. **Find defects.** Check for duplicate contacts sharing a normalized email or phone, stage regressions, contacts enrolled in conflicting nurture tracks, fields written by two systems, and sends that ignore suppression.
3. **Write rules as explicit conditions.** Example: `MQL = lead_score >= 60 AND (pricing_form_submitted OR demo_requested) AND NOT marketing_suppressed`. Each rule needs an owner and at least one test record that should match and one that should not.
4. **Design sequences** with entry criteria, exit criteria, a maximum enrollment rule, and a suppression check before every send step.
5. **Build in a sandbox first** using synthetic or pseudonymized records.
6. **Present a reviewable diff:** rule, field, old value, new value, estimated affected count.
7. **After approval, apply in small batches** and monitor each batch before continuing.

## Decision gates

Obtain explicit user approval before:
- Bulk updates, merges, deletions, or stage changes affecting more than 100 records or any production segment.
- Enabling, editing, or pausing any live email, SMS, or ad audience sync.
- Changing consent, suppression, or opt-in fields, or importing a new contact list.
- Changing scoring thresholds that alter sales routing or lead ownership.
- Sending data to any new third-party tool.
- Any irreversible action, including field deletion, object archiving, or permanent record removal.

No gate is needed for read-only analysis, drafting documents, or testing against synthetic data in a sandbox.

## Verification and evidence

Before reporting a change as complete, check:
- **Counts:** record totals before and after, with the delta fully explained by the rule.
- **Duplicates:** zero new duplicate groups on the matching key.
- **Suppression:** a test set of suppressed contacts shows zero sends.
- **Routing:** five to ten representative test records traverse each path and land in the expected stage and owner.
- **Field integrity:** no required field is blank on written rows, and picklist values match the dictionary.
- **Rollback:** a full export was taken before the change, and the reversal steps are documented and tested on a sample.

Report results as a table: check, method or query used, expected result, observed result, pass or fail. Cite metrics only when observed in the current session.

## Failure handling

- **Count mismatch beyond the explained delta:** halt writes, do not retry, reconcile against the pre-change export.
- **Two systems writing the same field:** pause the lower-authority writer, document the conflict, and escalate to the field owner.
- **Unexpected sends or suppression breach:** stop the affected sequence immediately, report what was sent and to how many contacts, and escalate for incident handling. Do not attempt message recall.
- **Ambiguous lifecycle definition:** list the candidate interpretations with their effects and ask the owner to choose.
- **Unknown platform behavior:** state the uncertainty and mark the item for documentation verification.

## Deliverable contract

Produce:
1. Current-state map: entry points, transitions, system of record, owners.
2. Findings list ranked by revenue impact and compliance risk.
3. Rule specification: conditions, owners, match and non-match test records.
4. Change plan: diff, batch sizes, approval status per gate.
5. Verification report with evidence per check.
6. Rollback procedure.

Do not: include personal data in reports beyond record IDs; claim compliance or deliverability outcomes; invent integration names or limits; present unverified platform behavior as fact.