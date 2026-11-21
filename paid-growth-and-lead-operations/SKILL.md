---
name: paid-growth-and-lead-operations
description: Use when designing, auditing, or troubleshooting paid acquisition data flows, conversion tracking, lead scoring pipelines, CRM lead routing, or attribution reporting for paid media campaigns.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Paid Growth And Lead Operations

## Purpose and boundaries

This skill covers the data operations behind paid acquisition: campaign taxonomy, conversion event definitions, lead capture and deduplication, lead scoring and routing, offline conversion uploads, and performance reporting that ties spend to downstream revenue.

In scope: tracking-plan review, UTM and naming conventions, lead-to-CRM mapping, qualification rules, conversion-value logic, reconciliation between ad platforms and the CRM, and diagnosis of discrepancies.

Out of scope: creative strategy, bid-strategy selection as a marketing decision, legal sign-off on consent language, and any direct change to live ad accounts or CRM records. This skill produces analysis, specifications, and change proposals; a human operator executes them.

## Inputs and assumptions

Request these before analysis:

1. Campaign inventory export: platform, campaign, ad group, UTM parameters, start and end dates, daily spend.
2. Lead records: unique ID, created timestamp, source fields, form or event type, consent status, qualification status, opportunity linkage.
3. Conversion definitions currently configured in each platform, with their trigger, value, and attribution window.
4. The CRM stage history for a sample of leads, including timestamps and owner changes.
5. The revenue or pipeline figure the business treats as truth, and its date basis.

Assumptions to state explicitly in every output: time zone used, currency and FX rate source, attribution model, and whether platform-reported and CRM-reported numbers are compared on the same date basis. If any assumption is unverified, label it as such.

## Operating workflow

1. **Define the question.** Write one sentence: what decision depends on this analysis (budget shift, channel cut, routing fix, tracking repair).
2. **Build the taxonomy map.** List every campaign source value and map it to a canonical channel. Count unmapped values; do not guess mappings for values that lack clear evidence.
3. **Audit conversion events.** For each platform event, record trigger, value logic, and window. Flag events that fire on page load rather than confirmed submission, events that double-fire, and values that are constant placeholders.
4. **Reconcile leads.** Deduplicate on normalized email or phone plus a time window (state the window used). Compare platform lead counts to CRM lead counts by day and by source. Accept a gap only if it is explained by a named cause such as consent suppression, spam filtering, or late CRM sync.
5. **Evaluate lead scoring and routing.** Check that every scoring rule references a field that is populated for at least 90 percent of leads in the sample; otherwise the rule is measuring data completeness, not lead quality. Confirm routing rules have a default owner for unmatched records.
6. **Test offline conversion matching.** For uploaded conversions, verify the match key type, the timestamp used (click or conversion time), and the share of records successfully matched. Report match rate as a number, not an adjective.
7. **Produce the reconciliation and recommendations.** Separate findings by confidence: confirmed (reproduced in data), probable (consistent with data, not reproduced), and hypothesis (requires a test).

## Decision gates

- **Gate A, before any recommendation to change spend:** reconciled lead or conversion gap is under 10 percent per source, or the gap has a named, quantified cause. If not, the output is limited to a tracking repair plan.
- **Gate B, before recommending a scoring change:** a holdout or historical back-test shows the new rule separates later-qualified from unqualified leads better than the current rule. Report both metrics.
- **Gate C, before proposing offline conversion uploads:** match rate is measured on a sample and consent basis is confirmed by the data owner.
- **Gate D, mandatory approval:** any action that deletes or merges CRM records, alters live conversion tracking, changes routing for active leads, uploads personal data to an external platform, or modifies budgets. Present the exact change, scope, affected record count, and rollback method, then stop until a named human approves.

## Verification and evidence

Every finding must cite the data slice it came from (table, date range, filter). Required checks before publishing:

- Row counts before and after each join or deduplication, with the number of dropped rows and the reason.
- Totals per source sum to the overall total within rounding.
- Date basis is identical across compared systems.
- Spot-check at least 10 individual leads end to end, from ad click to CRM stage, and record the outcome.

Platform-specific field names, event parameters, API endpoints, and upload formats change between versions. Mark any such detail as "verify against current official documentation" and do not state it as fact without that check.

## Failure handling

- **Mismatched totals:** stop, list the top three contributors to the gap by source and date, and state which system is considered authoritative. Do not average the two figures.
- **Missing key fields:** report the null rate per field and exclude affected rules from recommendations.
- **Ambiguous attribution:** present results under at least two attribution models and state that the choice changes the ranking.
- **Sample too small:** if fewer than 200 leads or 30 conversions per segment exist, report directional findings only.
- **Conflicting consent flags:** treat the record as non-contactable and escalate to the data owner.

Do not fill gaps with assumed values. Do not present a single-day spike as a trend.

## Deliverable contract

Return a document with these sections in order:

1. Decision supported and scope.
2. Assumptions with verification status.
3. Data sources and slices used, with row counts.
4. Findings table: finding, evidence, confidence level, estimated impact with units.
5. Reconciliation summary: platform versus CRM counts by source and date, gap percentage, named cause.
6. Recommended actions, each tagged with its gate status and whether human approval is required.
7. Open questions and the data needed to close them.
8. Version-sensitive items to verify against official documentation.

Do not include unverified benchmark figures, industry averages presented as targets, or claims of regulatory compliance. Do not recommend moving personal data between systems without naming the lawful basis as confirmed by the data owner.\n\n## Ultron routing contract

**Choose this skill when:** the question is about paid acquisition measurement and the path from ad spend to qualified leads or revenue: campaign taxonomy, attribution, conversion events, offline conversion matching, lead-source reconciliation, and paid-channel performance diagnostics.

**Choose `saas-crm-marketing-automation` when:** the work changes or designs contact lifecycle behavior inside the CRM: deduplication, segmentation, scoring, nurture enrollment, suppression, lifecycle stages, ownership, and sales handoff.

**Handoff contract:** this skill defines the paid-source and conversion data contract, including campaign IDs, event names, attribution windows, value semantics, consent constraints, and reconciliation gaps. The CRM skill maps that contract to contact/account fields and automation rules. Any live spend, tracking, personal-data upload, or CRM mutation remains subject to its explicit approval gate.

**Why the boundary exists:** acquisition measurement determines where leads and revenue came from; CRM automation determines what happens to a contact after capture. A shared contact record does not make those responsibilities interchangeable.
