---
name: business-finance-erp
description: Use when validating, enriching, or reconciling finance ERP master data (vendors, customers, legal entities, tax IDs, bank accounts) against external business registries, tax authority lookups, or identifier registries such as LEI or VAT databases.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Business Finance ERP

## Purpose and boundaries

This skill governs how finance master data is checked against external registries and how the results are applied inside an ERP. It covers: confirming legal names, registration numbers, tax identifiers, registered addresses, and entity status; matching ERP records to registry entries; flagging discrepancies for finance review; and documenting the evidence behind each change.

It does not cover: making payments, changing bank details in production without dual approval, sanctions or AML screening decisions (hand these to compliance), tax filing, or credit decisions.

## Inputs and assumptions

Required inputs:
- Export or list of master records to check (ERP ID, legal name, country, registration number, tax ID, address, bank account reference, status).
- Access to the approved registry sources for each country or identifier type, with the access method the organization has authorized.
- The ERP's current field definitions and mandatory-field rules.

Assumptions to state explicitly in the output:
- Registry data may be stale, partial, or differently formatted by jurisdiction. Registry status is evidence, not proof of legal standing.
- Registry query methods, rate limits, and data licensing terms change. Verify current endpoints, field names, and terms against each registry's official documentation before running a batch.
- Personal data in sole-trader records requires the organization's data-protection basis; do not extract beyond the fields needed.

## Operating workflow

1. Scope the batch: record count, countries, identifier types, and the ERP fields allowed to change. Read-only mode is the default.
2. Normalize inputs: trim whitespace, standardize country codes to ISO 3166-1 alpha-2, strip punctuation from tax IDs per the jurisdiction's format, and record the original value alongside the normalized one.
3. Query registries using the identifier first (registration number, tax ID), then name plus country only as a fallback. Name-only matches are never sufficient for an update.
4. Score each match: identifier exact match plus legal-name similarity above your documented threshold plus active status = auto-confirm candidate. Any other combination = review.
5. Compare field by field: legal name, registration number, tax ID, registered address, entity status, date of incorporation where available.
6. Classify each record: CONFIRMED, DISCREPANCY (specify field), INACTIVE_OR_DISSOLVED, NOT_FOUND, AMBIGUOUS.
7. Produce a change proposal. Do not write to the ERP in this step.

## Decision gates

- **Gate 1, before any query:** Confirm the registry is authorized for this data purpose and jurisdiction. If not, stop.
- **Gate 2, before applying changes:** Any change to legal name, tax ID, or address requires a named approver from the finance master-data owner role. Changes affecting bank account details require a second approver independent of the requester and must be verified through a channel separate from the record itself (for example, a call-back to a number already on file).
- **Gate 3, external impact:** Sending correction requests to vendors or customers, or notifying third parties, requires explicit approval for each batch.
- **Gate 4, deactivation:** Blocking or deactivating a vendor because the registry shows dissolution requires approval. Open invoices and payments must be listed before the block is proposed.

Never auto-apply DISCREPANCY, INACTIVE_OR_DISSOLVED, or AMBIGUOUS results.

## Verification and evidence

Each proposed change must carry:
- Registry name, query timestamp (UTC), identifier used, and the registry's returned record reference.
- Before and after values for each field.
- Match score and the threshold applied.
- Reviewer identity and decision for gated items.

Quality checks, measured per batch:
- Identifier-matched rate: report it; a low rate signals poor source data, not a success.
- Zero auto-applied changes outside the confirmed class.
- Sample audit: re-check at least 5% of CONFIRMED records, or 20 records if fewer, against the registry manually. Any mismatch fails the batch.
- Reconciliation: count of input records equals the sum of all output classes.

## Failure handling

- Registry unavailable or rate-limited: pause, record the last completed index, resume later. Do not retry in a tight loop.
- Schema or field change returned by the registry: stop the batch and flag for verification against current documentation.
- Conflicting results from two registries: classify AMBIGUOUS and escalate.
- ERP write error mid-batch: halt writes, produce a rollback list from the before-values, and obtain approval before reversing.

## Deliverable contract

Return:
1. Batch summary: records in, records per class, identifier-matched rate, sample audit result.
2. Change proposal table: ERP ID, field, current value, proposed value, source reference, class, gate required.
3. Escalation list: every item needing approval, with the approver role.
4. Assumptions and unverified items, including any registry endpoint or field detail not confirmed against current official documentation.

Do not: invent registry field names; state that a vendor is legally compliant or creditworthy; apply bank changes from registry data; merge duplicate vendors without a separate approved merge review; or represent registry data as guaranteed accurate.