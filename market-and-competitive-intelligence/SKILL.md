---
name: market-and-competitive-intelligence
description: Use when researching markets, competitors, pricing, vendor positioning, or AI/data product landscapes and need a sourced, dated, decision-ready brief with explicit confidence levels.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Market And Competitive Intelligence

## Purpose and boundaries

This skill produces sourced, dated, decision-oriented analysis of markets, competitors, and product landscapes in the data and AI domain: data platforms, analytics tools, ML/AI model providers, MLOps tooling, data infrastructure vendors, and AI application categories.

In scope: market sizing logic, competitor feature and positioning comparison, pricing and packaging analysis, go-to-market signals, partnership and integration mapping, hiring and roadmap signals drawn from public sources, and identification of gaps or threats.

Out of scope: non-public information obtained through deception, pretexting, or access to systems you are not authorized to use; reverse engineering of proprietary code; contacting competitor employees or customers under a false identity; investment or legal advice; guaranteed forecasts.

## Inputs and assumptions

Before starting, confirm:
- The decision the brief supports (e.g., enter a segment, price a tier, pick a partner, prioritize a feature).
- The geography, buyer segment (SMB, mid-market, enterprise, public sector), and time horizon.
- The competitor set. Ask for it if not given; propose a candidate set of 5 to 10 with reasons for inclusion and exclusion.
- Permitted sources: public websites, documentation, filings, pricing pages, changelogs, job postings, conference talks, analyst summaries the user has access to, and user-provided internal data.

Assumptions must be written down with a label. Pricing, feature availability, and certifications change frequently; treat any value captured more than 90 days ago as stale unless re-verified.

## Operating workflow

1. Define the question in one sentence and the decision it feeds. Reject open-ended "tell me about the market" requests until narrowed.
2. Build the competitor set. Include direct competitors, adjacent platforms that could expand into the segment, open-source alternatives, and the buyer's status quo (in-house build, spreadsheets, incumbent suite).
3. Create a fact register: one row per claim with columns for claim, value, source URL, capture date, and confidence (high: primary source and recent; medium: secondary or older than 90 days; low: inferred or single unverified source).
4. Collect across dimensions: target customer, core use case, architecture and deployment model (cloud, self-hosted, hybrid), integrations, data residency options, pricing model and published tiers, support and SLA terms as published, roadmap signals, partnerships, and customer proof points.
5. Triangulate. Any claim that drives a recommendation needs at least two independent sources or one primary source plus a dated corroborating signal.
6. Analyze: map positioning against buyer criteria, identify where competitors are weak or crowded, estimate sizing using explicit bottom-up inputs with stated ranges, and list threats with likelihood and impact.
7. Write the brief using the deliverable contract below.

## Decision gates

- Gate A (scope): Stop if the decision, segment, or geography is undefined. Do not proceed on assumptions alone.
- Gate B (sources): Stop before analysis if more than a third of decision-relevant claims are low confidence. Collect more sources or downgrade the conclusions.
- Gate C (sensitive collection): Require explicit user approval before accessing any login-gated competitor material, using scraping at volume, contacting third parties, or handling customer or employee personal data.
- Gate D (external use): Require explicit approval before publishing, sharing outside the requesting team, or sending the brief to vendors, partners, or investors.
- Gate E (pricing actions): Do not present a recommended price as final. Require approval from the accountable owner before any external pricing change.

## Verification and evidence

Quality checks, all required:
- Every quantitative claim has a source URL and capture date.
- Every competitor feature claim cites the vendor's current documentation or a dated changelog entry, not marketing copy alone.
- Each claim in the recommendations section maps to at least one fact register row.
- Sizing shows formula, inputs, ranges, and sensitivity to the largest input.
- Version-sensitive details (model names, tier limits, supported regions, certifications, API features) are marked "verify against current official documentation" unless confirmed in the last 30 days.
- No figures are rounded in a way that changes the conclusion.
- The brief distinguishes observed facts, vendor claims, and analyst inference.

## Failure handling

- Paywalled or unavailable source: record the gap, mark dependent claims low confidence, and do not infer the content.
- Conflicting figures: report both with sources, explain the likely reason (scope, date, currency, definition), and do not average them silently.
- Vendor pricing "contact sales": record as undisclosed. Do not estimate without flagging it as a model assumption.
- Stale data discovered mid-analysis: re-capture or downgrade confidence; do not patch with memory.
- Insufficient evidence for a recommendation: say so and state what evidence would change the conclusion.

## Deliverable contract

The brief contains, in order:
1. Decision and question (one paragraph).
2. Bottom line (three to five sentences, with confidence level).
3. Competitor set with inclusion rationale.
4. Comparison table: dimensions by competitor, each cell tied to a fact register ID.
5. Findings, each with evidence IDs and confidence.
6. Sizing, if requested, with formulas and ranges.
7. Risks and open questions, including what would change the conclusion.
8. Fact register appendix with source, date, and confidence per row.
9. Verification log: which checks passed, which items are pending re-verification.

State what not to do: do not treat marketing claims as capability proof, do not present estimates as measured figures, do not omit dates, and do not describe a competitor's internal intent as established fact.

## Ultron routing contract

**Choose this skill when:** researching a commercial market and its competitive landscape: market sizing, vendor positioning, features, pricing, packaging, integrations, customer segments, public roadmap signals, and opportunity/threat mapping in data and AI domains.

**Choose market-analysis when:** the subject is a financial instrument, asset set, or sector and the question concerns price, volume, volatility, spreads, positioning, term structure, or a conditional market/trading thesis over a stated horizon.

**Handoff contract:** this skill supplies sourced company/product identities, dated competitive facts, pricing observations, market structure assumptions, and uncertainty. The market-analysis skill may use relevant public sector or macro context, but must keep commercial positioning distinct from market-price evidence and must state the time horizon and invalidation conditions.

**Why the boundary exists:** commercial competition and financial market behavior can influence each other, but they require different data, methods, and conclusions.
