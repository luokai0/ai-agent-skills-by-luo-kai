---
name: gtm-strategy
description: Use when planning, reviewing, or rewriting a go-to-market strategy for a product, service, or market entry, including ICP definition, channel selection, pricing-to-channel fit, launch sequencing, and GTM metrics.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Gtm Strategy

## Purpose and boundaries

This skill produces or audits a go-to-market (GTM) strategy: who the offer is for, why they buy now, how they will hear about it, how they will buy, who sells and supports it, and how success is measured. It covers B2B and B2C offers, new products, new segments, and new geographies.

Out of scope: brand identity design, legal review of contracts or regulated claims, financial audits, and executing paid campaigns or outbound sends. The skill recommends; a human owner approves and executes.

## Inputs and assumptions

Collect these before drafting. Mark any missing item as an explicit assumption with an owner and a validation date.

1. Offer: what is sold, price points, delivery model, and what is not included.
2. Evidence of demand: pipeline, waitlist, pilot results, win/loss notes, retention data. Distinguish stated interest from paid commitment.
3. Target market: candidate segments, firmographic or demographic criteria, and known exclusions.
4. Constraints: budget, headcount, sales cycle length, regulatory limits on claims or outreach, and deadline.
5. Competitive alternatives: what buyers use today, including "do nothing" and spreadsheets.
6. Unit economics: target CAC, payback period, gross margin, and average contract or order value.

If demand evidence is only opinion, label the strategy "hypothesis-stage" and limit commitments to tests.

## Operating workflow

1. **State the wedge in one sentence.** Format: "For [segment with a specific trigger], [offer] replaces [current alternative] by [measurable difference]." If you cannot write it, stop and return to segmentation.
2. **Define the ICP with disqualifiers.** List 3 to 5 firmographic or behavioral criteria and 2 disqualifiers. Example: "Logistics firms with 200–1,000 employees running more than one warehouse management system; disqualify those with an in-house platform team of 10+."
3. **Map buying committee and trigger events.** Name the economic buyer, champion, and blocker. List 2 to 4 triggers (new regulation, funding round, failed vendor, hiring spike) that move a prospect from passive to active.
4. **Select 2 to 3 primary channels** by scoring each candidate (1–5) on: reach into the ICP, expected CAC, time to first revenue, and control over timing. Drop any channel scoring below 3 on reach.
5. **Set pricing-to-channel fit.** Self-serve channels need low-friction prices and trial paths; enterprise channels need procurement-ready packaging and a discount floor. Do not sell an enterprise contract through a checkout flow.
6. **Sequence the launch in three phases:**
   - Pilot (4–8 weeks): 5–15 design partners, paid where possible, with a written success definition.
   - Controlled expansion (1–2 quarters): one channel scaled with weekly conversion review.
   - Broad availability: only after payback and retention thresholds in the gates below are met.
7. **Assign sales and support motions.** Specify who handles inbound, qualification, demo, close, onboarding, and expansion, with handoff criteria between them.
8. **Define metrics and review cadence.** Required metrics: qualified pipeline created per week, stage conversion rates, CAC by channel, win rate, sales cycle days, 90-day retention, and net revenue retention for recurring offers.

## Decision gates

Advance only when each gate is met with evidence.

- **Gate A, Problem:** At least 10 ICP interviews or 5 signed pilots show the problem is ranked top-3 by the buyer. Fail if the majority cite "nice to have."
- **Gate B, Channel:** One channel produces qualified opportunities at a cost within 1.5x target CAC for 6 consecutive weeks. Fail if no channel meets this after two test cycles; re-examine the ICP before adding spend.
- **Gate C, Economics:** Projected payback is within the agreed period using observed conversion, not planned conversion. Require a sensitivity check at 50% of expected win rate.
- **Gate D, Scale:** Pilot retention or usage meets the pre-agreed threshold and support load per customer is documented.

## Verification and evidence

- Every numeric claim in the strategy cites its source (CRM export, interview log, experiment ID) or is labeled an assumption.
- Test each channel assumption with a named experiment: hypothesis, metric, sample size, stop rule, and result.
- Check the ICP against actual closed-won accounts: at least 70% should match the stated criteria. If not, the ICP is wrong, not the buyers.
- Cross-check pricing against the three most common alternatives a buyer would consider.
- Re-verify any platform, tool, or ad-policy constraint against current official documentation before recommending it, since these change frequently.

## Failure handling

- **Low conversion:** Separate lead-quality problems (ICP mismatch) from offer problems (value unclear) from process problems (slow follow-up). Diagnose from stage-level data before changing anything.
- **Conflicting stakeholder priorities:** Surface the trade-off in writing with options and their metric impact; escalate to the decision owner. Do not silently pick one.
- **Missing data:** Replace the metric with a dated assumption and a collection plan. Do not infer numbers from comparable companies without labeling them as borrowed.
- **Gate failure:** Return to the earlier step the failed gate depends on. Do not skip ahead to spend more.

## Deliverable contract

The output is a single document containing, in order:

1. Wedge statement and ICP with disqualifiers.
2. Buying committee and trigger list.
3. Channel scorecard with selected channels and rationale.
4. Pricing and packaging mapped to each channel.
5. Three-phase launch plan with dates relative to start, owners, and gate criteria.
6. Metrics table: definition, target, source system, owner, review frequency.
7. Assumptions register: each assumption, confidence level, validation method, due date.
8. Risks and kill criteria.

Length: as long as needed to be executable, usually 4 to 8 pages. Every section must name an owner.

## What not to do

- Do not claim market size, growth rates, or competitor figures without a cited source.
- Do not recommend spend on a channel before the ICP is validated.
- Do not promise outcomes such as revenue, conversion, or compliance status.
- Do not launch outbound sends, paid campaigns, pricing changes, or customer communications without explicit human approval; these are external and often irreversible.
- Do not delete or overwrite existing CRM records, pipeline data, or prior strategy versions; create new versions instead.
- Do not present GTM tooling features, API parameters, or platform limits from memory; mark them for verification against current vendor documentation.