---
name: growth-marketing-customer-ops
description: Use when a growth marketing or customer operations task requires matching, enriching, validating, or segmenting customer or prospect records against external registries (business registers, licensing bodies, identifier registries, partner directories), or when registry data drives campaign eligibility, suppression, or account routing.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Growth Marketing Customer Ops

## Purpose and boundaries

This skill governs how customer records are reconciled with external registries for marketing and customer operations: matching records to registry entries, appending registry attributes, validating status (active, dissolved, suspended, lapsed), and producing segments or suppression lists for campaigns.

In scope: match design, confidence scoring, enrichment field mapping, status validation, segment definition, change logging, and reconciliation reports.

Out of scope: legal determinations about a company's standing, credit or risk decisions, scraping registries in ways their terms prohibit, altering the system of record for registry data, and sending any outreach. Registry data is evidence for a marketing decision, not a substitute for legal or compliance review.

## Inputs and assumptions

Before starting, confirm:

1. Source extract: row count, date pulled, owner, and fields available (name, address, country, identifier, domain, contact role).
2. Registry sources: which registries are authorized, their jurisdiction, access method, and their stated refresh frequency. Record the timestamp of every pull.
3. Use case: campaign eligibility, deduplication, account routing, or suppression. Each use case has different tolerance for false matches.
4. Consent and lawful-basis rules that apply to the target market. Do not assume a registry record permits marketing contact.
5. Retention rules for enriched data.

Assume registry fields are incomplete, stale, and sometimes in local-language or non-standard formats. Assume duplicate legal entities exist under trading names.

## Operating workflow

1. Normalize inputs: trim whitespace, standardize country codes, lowercase domains, strip legal-form suffixes into a separate field, and preserve the original value.
2. Match in tiers: exact identifier match first, then normalized name plus postcode or country, then fuzzy name with address corroboration. Never match on name alone for an outreach segment.
3. Assign each match a confidence tier (High, Medium, Low) with the rule that produced it. Only High matches flow to automated segments.
4. Validate status against the registry record for each High match. Flag dissolved, suspended, or merged entities for suppression review.
5. Append only the agreed field list. Do not append personal data about individuals beyond what the use case and lawful basis allow.
6. Write a change log: record ID, field changed, old value, new value, source, pull timestamp, and rule ID.
7. Produce the segment with exclusion counts broken down by reason.

## Decision gates

Stop and request explicit approval before:

- Overwriting any field in the system of record, or deleting records.
- Sending any campaign or external message to a segment.
- Sharing registry-derived data with a third party or moving it across jurisdictions.
- Using a matching rule with expected false-match rate above the threshold the owner set. If no threshold exists, request one.
- Running bulk registry queries above the quota or rate limits in the source's current terms, which you must verify against the registry's official documentation.
- Enriching individual-level personal data.

## Verification and evidence

- Sample at least 50 High matches (or all, if fewer) and manually verify identifier and address agreement. Report the observed false-match rate with the sample size.
- Confirm row counts reconcile: input = matched + unmatched + excluded, with no unexplained gap.
- Check that every appended value carries a source and timestamp.
- Confirm suppression lists contain zero records that are also in the active send list.
- Cross-check segment size against the prior run; investigate any change above 10% without a documented cause.
- Mark any statement about registry coverage, update frequency, or API limits as "verify against current official documentation" unless you have checked it in this session.

## Failure handling

- Registry unavailable or rate-limited: pause, record the partial state, and resume from the last checkpoint. Do not substitute cached data without labeling its age.
- Conflicting registry values: keep both, mark the record Low confidence, and exclude it from automated segments.
- Matching produces unexpected concentration (for example, many customers mapped to one entity): halt and review; this often indicates a join error or a parent-subsidiary issue.
- Discovered personal data outside scope: stop enrichment on that field, report it, and do not propagate it.

## Deliverable contract

Return:

1. Run summary: sources, pull timestamps, input count, match tier counts, exclusion counts by reason.
2. Segment file or list with confidence tier and rule ID per row.
3. Change log as specified above.
4. Verification results: sample size, observed false-match rate, reconciliation totals.
5. Open items requiring approval, listed by gate.

Do not state that a segment is compliant or lawful. State only what was checked and what remains for review.