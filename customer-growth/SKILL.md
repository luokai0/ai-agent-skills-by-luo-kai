---
name: customer-growth
description: Use when planning, diagnosing, or executing customer acquisition, activation, retention, expansion, or referral work for a product or service business, including funnel analysis, churn investigation, pricing-tier and onboarding changes, and growth experiment design.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Customer Growth

## Purpose and boundaries

This skill turns customer growth questions into measured hypotheses, prioritized experiments, and decision-ready recommendations. It covers the lifecycle: acquisition, activation, retention, expansion, and referral. It produces analysis and plans; it does not itself launch campaigns, change live pricing, message customers, or alter production systems.

Out of scope: legal review of marketing claims, tax or accounting treatment, individual credit or financial advice, and guaranteed revenue forecasts. Refer those to the appropriate owner.

## Inputs and assumptions

Required before analysis:
- Business model (self-serve, sales-led, marketplace, subscription, transactional) and unit of growth (account, seat, household, order).
- Lifecycle definitions: what counts as signed up, activated, retained, churned, expanded. If undefined, propose definitions and mark them as assumptions.
- Time window, cohort granularity, and data source names.
- Current baseline metrics, with the date range and known data gaps.
- Constraints: budget, team capacity, contractual or regulatory limits on messaging, and brand rules.

State every assumption explicitly in the deliverable. Do not treat missing data as zero.

## Operating workflow

1. **Define the question.** Rewrite the request as one decision: for example, "Why did 90-day retention for trial-to-paid accounts fall 6 points in Q3?" Reject vague goals such as "grow revenue" until decomposed.
2. **Build the metric tree.** Decompose the outcome multiplicatively or additively (e.g., revenue = accounts × activation rate × conversion × ARPA). Identify which branch changed.
3. **Segment before concluding.** Split by channel, plan, region, acquisition cohort, company size, and product version. A blended change often hides one segment's shift. Require at least two segments to show the same pattern before calling it systemic.
4. **Separate correlation from mechanism.** For each candidate cause, list the observable it predicts and the observable that would falsify it. Check release dates, pricing changes, outages, and campaign timing against the metric curve.
5. **Generate and rank hypotheses.** Score each on expected impact, confidence, and cost (ICE or equivalent). Keep at most five active hypotheses.
6. **Design the test.** For each hypothesis: primary metric, guardrail metrics (e.g., support tickets, refund rate, unsubscribe rate), minimum detectable effect, sample size estimate, duration, and stop rule. Use randomized allocation where feasible; otherwise document a quasi-experimental design and its threats to validity.
7. **Recommend and hand off.** Provide the ranked plan, owners, and approval requests for any gated action.

## Decision gates

Stop and obtain explicit human approval before:
- Changing live prices, plan limits, or contract terms.
- Sending messages to customers or prospects, including win-back, re-engagement, or price-change notices.
- Launching paid acquisition spend above a stated threshold or changing bidding rules.
- Deleting, merging, or exporting customer records, or sharing personal data outside its approved scope.
- Any experiment that withholds a paid feature or discount from customers who would otherwise receive it.
- Any action with contractual, regulatory, or reputational consequences, including referral incentives involving payments.

Proceed without a gate only for read-only analysis, drafting, and proposing experiments in a document.

## Verification and evidence

Every quantitative claim must cite its source query, dataset, date range, and cohort definition. Before reporting a lift:
- Confirm sample sizes per arm meet the pre-registered minimum.
- Check for sample ratio mismatch in randomized tests; if present, halt interpretation.
- Compare the effect against guardrails and seasonality from the prior year or matched periods.
- Report confidence intervals or uncertainty ranges, not point estimates alone.
- Recheck that the metric definition did not change mid-window.

Mark any vendor-platform setting, analytics tool feature, or API detail as "verify against current official documentation" unless the user has supplied it in this session.

## Failure handling

- **Missing or inconsistent data:** Report the gap, quantify its likely effect on conclusions, and request the specific field or extract. Do not impute silently.
- **Metric conflicts across tools:** Identify the definitional difference (timezone, deduplication, attribution window) and present both values with the reconciled one labeled.
- **Inconclusive test:** Report the interval, state what effect size is now ruled out, and recommend either extension (only if pre-planned) or closing the hypothesis.
- **Guardrail breach:** Recommend halting the variant pending review, regardless of primary metric gains.
- **Insufficient evidence for a causal claim:** Downgrade the language to "associated with" and list the test that would establish causation.

## Deliverable contract

Produce a document with these sections, in order:

1. **Question and decision** (one sentence each)
2. **Baseline and metric tree** (table with values, periods, and sources)
3. **Findings** (segmented, each with evidence reference and confidence level: high, medium, low)
4. **Ranked hypotheses** (table: hypothesis, predicted observable, ICE score, cost)
5. **Experiment plan** (primary metric, guardrails, MDE, sample size, duration, stop rule, owner)
6. **Approval requests** (each gated action, the reason, and the requested decision)
7. **Assumptions and open data gaps**
8. **Next review date** and the metric that will trigger it

Quality check before delivery: every finding traces to a stated source; no hypothesis lacks a falsifiable prediction; no gated action is written as already done; all version-sensitive tool details are flagged.

## What not to do

- Do not report averages across segments that differ materially in size or behavior.
- Do not declare winners from peeking at unfinished tests.
- Do not recommend discounts or dark patterns (hidden fees, forced cancellation friction) as retention levers.
- Do not fabricate benchmark figures for "industry averages"; request the user's own history or cite a verified source.
- Do not expand scope into unrelated brand, product roadmap, or hiring decisions without flagging the boundary.

## Ultron routing contract

**Choose this skill when:** turning a customer growth objective into a measurable strategy and experiment plan across acquisition, activation, retention, expansion, and referral.

**Choose growth-marketing-customer-ops when:** the task is operationally reconciling and enriching customer/company records with external registry data, defining registry-derived segments or suppression lists, and maintaining provenance for those fields.

**Handoff contract:** this skill defines the growth hypothesis, target cohort, success metric, experiment design, and decision threshold. The customer-ops skill returns the available verified attributes, match confidence, status changes, and segment limitations. Do not treat a registry match as proof of customer intent or as permission to contact someone.

**Why the boundary exists:** growth strategy decides what should be tested; customer operations determines which records can be reliably and lawfully used to implement that test.
