---
name: finance-market-analysis
description: Use when analyzing market data, company financials, or external registry records (securities filings, company registries, exchange listings, market statistics) to produce sourced, reproducible financial findings for an investment, credit, research, or due-diligence question.
author: Luo Kai
provenance: original
version: 1.1.1
---

# Finance Market Analysis

## Purpose and boundaries

This skill turns a defined financial question into a sourced, reproducible analysis built from external registries and market data: exchange listings, regulatory filings, corporate registry extracts, index constituents, and published macro or sector statistics.

In scope: ticker and identifier reconciliation, filing-based financial ratio analysis, peer comparison, trend and valuation context, event timelines (earnings, corrections, insider or ownership changes), and data-quality audits of registry records.

Out of scope: personalized investment advice, price targets presented as certainties, trade execution, insider or material non-public information, and legal or tax conclusions. Output is analytical support for a qualified professional's decision.

## Inputs and assumptions

Before starting, confirm:

1. The question: a decision, comparison, or screen with a stated horizon and currency.
2. The universe: named entities identified by legal name plus at least one stable identifier (ISIN, LEI, registry number, CIK-style filer ID, or exchange ticker with venue).
3. The period: fiscal year-end conventions, reporting currency, and whether figures are restated.
4. Data access: which sources are permitted. Record each source's publisher, retrieval date, and document version.

Assumptions must be written down. Default to reported (not adjusted) figures unless the question requires adjustment, and state any adjustment rule.

## Operating workflow

1. **Frame.** Restate the question in one sentence. List the metrics required to answer it and the minimum evidence per metric.
2. **Identify.** Resolve each entity to a primary identifier. Reject matches where name, jurisdiction, and identifier disagree. Log ticker changes, mergers, delistings, and share-class differences.
3. **Collect.** Pull primary documents first (annual and interim filings, registry extracts, exchange notices), then secondary aggregators. Record page or section references for every figure.
4. **Normalize.** Align fiscal periods, currencies (state FX source and date), units, and accounting basis (IFRS versus US GAAP, and whether non-GAAP measures are used). Recompute standard ratios from raw line items rather than trusting pre-computed aggregator fields.
5. **Analyze.** Compute the agreed metrics: growth, margins, leverage, liquidity, cash conversion, returns on capital, and valuation multiples. Compare against peers defined before looking at results. Examine a multi-year window, not a single period.
6. **Contextualize.** Identify drivers: one-off items, accounting changes, debt maturities, index rebalancing, sector cycles. Separate observed facts from interpretation.
7. **Report.** Produce the deliverable contract below.

## Decision gates

- **Identifier gate:** Proceed only if every entity maps to one primary identifier with a consistent jurisdiction. Otherwise, exclude the entity and report why.
- **Source gate:** A figure used in a conclusion must trace to a primary document or a named, dated secondary source. Single unverified aggregator figures cannot drive a conclusion.
- **Consistency gate:** If the same metric differs across two sources by more than 1% of the reported value or by any sign change, reconcile against the filing before continuing. If unreconciled, flag it.
- **Restatement gate:** If a later filing restates a prior period, use the restated figure and note the original.
- **Scope gate:** If the question requires a forecast, a recommendation, or a legal/tax determination, stop and state the limitation; deliver analysis only.
- **Approval gate:** Obtain explicit user approval before any action that is destructive, irreversible, externally visible (publishing, emailing, submitting to a registry or portal), or involves personal data beyond what the question requires, or material non-public information. Do not perform these on inference.

## Verification and evidence

- Recompute at least three headline figures (for example, net debt, free cash flow, operating margin) from line items and confirm agreement within rounding.
- Check balance sheet identity (assets equal liabilities plus equity) and cash flow tie-out to the change in cash for each period used.
- Confirm peer set size is at least five where comparisons are claimed, and document exclusions.
- Every number in the output carries a source reference: document, section, period, and retrieval date.
- Mark any version-sensitive item (accounting standard edition, exchange rule, registry API schema, data field name) as "verify against current official documentation" rather than asserting it.
- Do not state benchmark performance, historical hit rates, or regulatory compliance outcomes unless directly sourced in the session.

## Failure handling

- **Missing filing:** Report the gap and the period affected. Do not interpolate silently; if interpolation is used, label it.
- **Identifier conflict:** Halt that entity, list candidate matches with evidence, and request confirmation.
- **Unit or currency mismatch:** Convert only with a stated rate and date; otherwise report in original currency.
- **Source outage or access restriction:** Use the available primary source, mark the coverage gap, and do not substitute an unverified source.
- **Result contradicts prior assumption:** Report the contradiction first, then revise the frame; do not adjust data to fit the thesis.

## What not to do

- Do not present calculated ratios without their formula and inputs.
- Do not mix fiscal years or currencies in one comparison without normalization.
- Do not treat non-GAAP or adjusted figures as reported figures.
- Do not extrapolate a single quarter into an annual trend.
- Do not invent identifiers, filing dates, or figures to complete a table.

## Deliverable contract

The output must contain, in order:

1. **Question and scope:** one sentence, horizon, currency, universe.
2. **Method and assumptions:** formulas, adjustment rules, peer definition.
3. **Findings table:** metric, entity, period, value, source reference.
4. **Interpretation:** three to six numbered findings, each labeled as fact or inference.
5. **Data-quality log:** exclusions, reconciliations, unresolved conflicts, verification items.
6. **Limitations:** what the evidence cannot support.

Quality check before release: every figure traceable, every ratio reproducible from listed inputs, all gates passed or explicitly flagged, no recommendation phrased as certainty.

## Ultron routing contract

**Choose this skill when:** the financial question depends on issuer and instrument identity, corporate or regulatory filings, financial statement line items, ownership or earnings events, peer fundamentals, valuation context, or reconciling market data to authoritative financial records.

**Choose `market-analysis` when:** the primary objective is to analyze a market or instrument over a defined horizon using price, volume, volatility, spreads, positioning, term structure, or a conditional trading thesis and its invalidation conditions.

**Handoff contract:** this skill supplies verified identifiers, filing dates, normalized financial periods, accounting basis, recomputed ratios, and sourced fundamental events. The market-analysis skill returns horizon-specific market structure, scenario conditions, risk factors, and invalidation signals. Keep fundamental facts distinct from market observations and forecasts.

**Why the boundary exists:** financial records establish what an issuer reported; market analysis studies how an instrument or market behaves. Combining them is useful, but one must not be mistaken for the other.
