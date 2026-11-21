---
name: data-analytics-modeling
description: Use when building, reviewing, or validating analytical or statistical models over external registry data (government, public-sector, licensing, corporate, clinical, or standards registries), including entity resolution, dimensional modeling, forecasting, and metric definition from registry extracts.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Data Analytics Modeling

## Purpose and boundaries

This skill governs analytical modeling performed on data pulled from external registries: public company filings, business licence rolls, professional certification lists, product or device registrations, vehicle or land registers, and similar authoritative-but-uncontrolled sources. The work covers source profiling, entity resolution, conformed modeling, metric definition, model fitting, and validation.

In scope: schema mapping, identifier reconciliation, slowly changing dimensions, cohort and survival framing, rate and count models, anomaly screening, and reproducible reporting.

Out of scope: operating or altering the registry itself, scraping against terms of service, re-identifying individuals in de-identified extracts, producing eligibility or enforcement decisions about named persons without a human owner, and legal conclusions about compliance.

## Inputs and assumptions

Before modeling, collect and record:

1. Source description: publisher, extract date, retrieval method, licence or usage terms, and update cadence.
2. Data dictionary: field definitions as published; note any fields whose meaning is inferred.
3. Analytical question stated as a decision or measurable outcome.
4. Grain: one row represents what (a filing, a licence, a registrant-year)?
5. Known gaps: late filings, retroactive corrections, deregistered records, duplicate issuance.

Assumptions must be written down with an owner and a test that would falsify them. Treat registry status codes as provisional until confirmed against documentation.

## Operating workflow

1. Snapshot the raw extract as received. Store checksum, row count, and extract timestamp. Never overwrite it.
2. Profile each field: null rate, distinct count, format pattern, min/max, and out-of-domain values. Record results as a table.
3. Build the identifier strategy. Prefer the registry's own stable key. Where none exists, resolve entities with normalized name plus jurisdiction plus a secondary attribute, and report the match precision on a labelled sample (target at least 200 pairs, reviewed by two people where feasible).
4. Model time explicitly. Separate event date, effective date, and recorded date. Use validity intervals for status changes rather than overwriting.
5. Define each metric in a single versioned specification: numerator, denominator, population filter, time window, and handling of reversals.
6. Fit the simplest model that answers the question. Use counts with exposure offsets (Poisson or negative binomial) for event rates across unequal registry coverage; use survival framing for time-to-event questions about registration duration.
7. Run the validation set in the verification section before any result leaves the working environment.
8. Publish with the snapshot identifier, code version, and assumption register attached.

## Decision gates

Stop and escalate if any of the following holds:

- Entity match precision on the labelled sample is below 95%, or recall is unknown.
- Null or out-of-domain rate for a key field exceeds 5% and the cause is unexplained.
- The source licence does not clearly permit the intended use.
- The result would be used to make a decision about an identifiable person or entity (approval, denial, sanction, flagging).
- A metric changes definition between extract versions without a documented reason.
- Backtest error exceeds the tolerance agreed in the analytical question, or results are unstable across reasonable window choices (more than 10% relative change).

Proceed only when each gate is passed or a named owner accepts the documented residual risk.

## Verification and evidence

Each deliverable must include:

- Reconciliation: row counts from raw to modeled tables, with every drop explained by a filter.
- Uniqueness test: the declared grain key is unique (zero duplicates) in each conformed table.
- Referential test: every foreign key resolves; report orphan counts.
- Temporal test: no validity interval overlaps for the same entity and attribute; no event precedes its registration date unless flagged as a correction.
- Sensitivity: report the metric under at least two alternative window and filter choices.
- Calibration or fit check: for predictive models, hold out the most recent period and report error against a naive baseline.
- Reproducibility: a fresh run from the snapshot reproduces headline figures exactly.

Mark any statement about current registry rules, field semantics, or library behaviour as requiring verification against the publisher's current official documentation. Do not cite benchmark figures or accuracy claims that were not produced in this work.

## Failure handling

- Checksum mismatch on re-read: halt, quarantine the extract, and request a re-pull.
- Sudden change in volume (beyond three standard deviations of the trailing series): treat as a possible publication change; investigate before modeling.
- Matching failure concentrated in one jurisdiction: segment the match rules for that jurisdiction rather than loosening global thresholds.
- Model fails the naive-baseline comparison: report the baseline result and do not ship the model.
- Unresolvable definition conflict: escalate to the metric owner with both definitions and the affected row count.

## Deliverable contract

A completed engagement delivers:

1. Methodology note (maximum two pages): question, grain, sources, metric specifications, and model choice with justification.
2. Assumption register: each entry with owner, evidence, and falsification test.
3. Data quality report: profiling tables, reconciliation, and the verification results above.
4. Reproducible pipeline and a run manifest recording snapshot ID, code revision, and run timestamp.
5. Results with uncertainty intervals and sensitivity ranges; no point estimates without spread.
6. Open-issues list with severity and owner.

Do not: overwrite raw snapshots; merge entities on name alone; report results without the denominator; present registry status as verified fact without a source date; or perform any deletion, bulk export, external transmission, or publication of record-level data without explicit written approval from the data owner.