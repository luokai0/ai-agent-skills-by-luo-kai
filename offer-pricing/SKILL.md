---
name: offer-pricing
description: Use when setting, revising, or stress-testing the price, packaging, discount rules, or tier structure of a product, service, or subscription offer for a business or entrepreneurial venture.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Offer Pricing

## Purpose and boundaries

This skill produces a defensible price and package structure for a single offer (one product, service, or subscription family), with the reasoning, assumptions, and test plan needed to validate it. It covers value-based price anchoring, tier design, discount governance, and pilot-based price testing.

Out of scope: tax or accounting treatment, legal terms of sale, consumer-protection disclosures, securities or investment pricing, regulated pricing (utilities, healthcare reimbursement, controlled goods), and any price change that will be communicated to existing customers without human approval.

## Inputs and assumptions

Collect before modeling. Mark any missing input as an explicit assumption with a stated confidence level.

- Target customer segment and the job the offer completes for them
- Current unit cost: variable cost per unit or per delivered hour, plus allocated fixed cost per unit at expected volume
- Alternatives the buyer actually uses: status quo, competitor offers, in-house effort, doing nothing; include their approximate prices
- Quantified value: time saved, revenue gained, cost avoided, risk reduced, with source or basis
- Sales channel and expected discount pressure
- Volume estimate and churn or repeat-purchase assumptions for subscriptions
- Minimum acceptable gross margin and payback target set by the owner

Assume nothing about willingness to pay without evidence. If evidence is absent, the output is a hypothesis, not a recommendation.

## Operating workflow

1. **Define the floor.** Compute cost-to-serve per unit. Set the absolute floor price at cost-to-serve plus the minimum contribution needed to cover fixed costs at target volume. Reject any proposed price below this floor unless the owner records a strategic reason and an end date.
2. **Quantify the value ceiling.** Estimate the buyer's value from the job, for example hours saved multiplied by loaded hourly cost, minus adoption effort. Discount this by your confidence (a 50% confidence on a value claim halves its weight). The ceiling is the value you can credibly claim, not the value you wish to claim.
3. **Identify the reference price.** Pick the most likely comparison the buyer makes. Price relative to that anchor, not relative to your cost.
4. **Set a target between floor and ceiling.** A common starting point is a price capturing 20–40% of the credible value gap, adjusted for differentiation proof. Document why.
5. **Design tiers only if buyers differ in need.** Use at most three tiers. Each tier must differ in a buyer-visible job, not only in volume quota. Anchor the highest tier to make the middle tier the default choice only when the middle tier is actually the target.
6. **Define discount rules.** Specify who may discount, maximum percentage, required trade (term length, prepayment, case-study, referral), and expiry. Discounts must be exchanged for something; none are unconditional.
7. **Build a sensitivity table.** Compute contribution margin, customer count needed to hit fixed-cost recovery, and revenue at price points 15% below and 15% above target, under low, base, and high conversion assumptions.
8. **Plan a controlled test.** Specify a price test with a fixed sample, a holdout or sequential design, a minimum observation window, and a predefined success metric (conversion, average revenue per account, or contribution). Do not declare a winner before reaching the sample size.

## Decision gates

- **Gate A (floor):** If target price is below the cost floor, stop and escalate. Do not proceed to tiering.
- **Gate B (value):** If the credible value ceiling is below the reference price, the offer cannot win on price. Recommend changing the value proposition or segment rather than cutting price.
- **Gate C (discount depth):** Any proposed discount above 25% of list, or any discount without an exchanged concession, requires owner approval.
- **Gate D (external change):** Any change visible to existing customers, any public price publication, or any change to contracted terms requires explicit human approval before drafting for release.
- **Gate E (test launch):** Pilot pricing shown to real prospects requires approval of the test design, the affected segment, and a rollback plan.

## Verification and evidence

Each recommendation must include:

- Cost floor calculation with each input listed and its source
- Value ceiling worksheet showing each claim, its basis, and its confidence weight
- Reference price with the source or the stated assumption behind it
- Sensitivity table covering at least three price points and three conversion scenarios
- Pass criteria: contribution margin at or above the owner's threshold in the base case, and no scenario where the offer loses money at expected volume
- Test success metric and minimum sample size, with the formula or tool used stated and flagged for verification against current documentation if it is version-specific

Quality checks: every number traces to an input or a stated assumption; no tier differs only by quantity without a stated reason; discount rules name the exchange given.

## Failure handling

- **Missing cost data:** Halt modeling of margin. Present a range using the best available bounds and label it provisional.
- **Conflicting value claims:** Report both, use the lower credible figure as the ceiling, and list what evidence would resolve the conflict.
- **No reference competitor:** Use the buyer's status quo cost as the reference and state that the anchor is weaker.
- **Test shows no clear winner:** Keep the current price, record the result, and do not extrapolate.
- **Owner requests a price below floor:** Document the trade-off, quantify the margin loss per period, and require approval with an end date.

## Deliverable contract

Return a single structured document with these sections in order:

1. Recommendation (one price per tier, with currency and billing period)
2. Floor, ceiling, and reference table
3. Tier definitions with buyer-visible differences
4. Discount policy with exchanged concessions and expiry
5. Sensitivity table
6. Test plan with success metric, sample size basis, and duration
7. Open assumptions ranked by impact, each with the evidence that would resolve it
8. Approvals required before any external action

Do not output a price without the floor and ceiling shown beside it. Do not state willingness-to-pay as fact; state it as an estimate with its basis.