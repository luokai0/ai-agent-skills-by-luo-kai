---
name: behavioral-finance
description: Use when analyzing investor, trader, or client decisions for systematic biases, designing decision-quality safeguards for portfolios or trading processes, or diagnosing why a financial plan or strategy is not being followed as modeled.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Behavioral Finance

## Purpose and boundaries

This skill applies behavioral economics and cognitive psychology to financial decisions: identifying predictable deviations from rational-agent models (biases, heuristics, framing effects, emotional states) and designing processes that reduce their cost. It covers individual investors, trading desks, advisory clients, and investment committees.

In scope: bias diagnosis from trade logs, statements, or decision records; process design (checklists, pre-commitment rules, position-sizing constraints, review cadence); client communication framing; post-mortem analysis of decisions separated from outcomes.

Out of scope: personalized investment, tax, or legal advice; predicting market prices from sentiment; claims that a named bias guarantees future returns; diagnosing clinical conditions. Route those to licensed professionals.

## Inputs and assumptions

Required before analysis:
- Decision record: the decision, the information available at the time, the alternatives considered, and the stated rationale. Outcome data alone is insufficient.
- Context: time horizon, liquidity needs, stated objectives, constraints, and the written policy (if any).
- Behavior data: trade timestamps, position changes, cancellations, reversals, holding periods, and realized versus intended exits.

Assumptions to state explicitly in every output: whether data is complete, the period covered, and whether the subject's rationale was recorded before or after the outcome. Post-hoc rationales carry low evidential weight.

## Operating workflow

1. Separate decision quality from outcome quality. Score the decision against the information available at the time. A good decision can lose money; a poor one can win.
2. Reconstruct the decision timeline. Order events, note what information arrived between them, and mark each entry as recorded-before or recorded-after the outcome.
3. Screen for candidate biases with observable markers, not labels:
   - Loss aversion: holding losers well past the stated stop while selling winners early; asymmetric position-size changes after drawdowns.
   - Disposition effect: realized-gain-to-realized-loss ratio materially above 1 in the same period, with unrealized losses dominating the book.
   - Overconfidence: turnover above the strategy's documented norm; position sizes rising after a streak of wins without new evidence.
   - Anchoring: revised targets or valuations clustering near a prior price, purchase cost, or analyst figure.
   - Recency and narrow framing: allocation changes that track the last 3 to 6 months of returns; decisions evaluated in isolation rather than at portfolio level.
   - Confirmation: research sources or screens that all point one direction; disconfirming data noted but not weighted.
   - Herding and FOMO: entries following a visible move with no pre-stated trigger.
4. Quantify each flagged pattern with a measure (e.g., count, ratio, average holding period differential, deviation from the written rule). Do not report a bias without a number.
5. Compare against the written process. A deviation is a finding; a deviation with no documented rule is a process gap.
6. Propose one to three controls matched to the observed failure. Each control must be specific, testable, and owned.

## Decision gates

- Gate A (data sufficiency): If fewer than roughly 30 comparable decisions exist, report patterns as anecdotal and do not conclude a bias is systematic.
- Gate B (causal claim): Do not attribute a loss to a bias unless the decision record shows the deviation from process occurred before the outcome.
- Gate C (intervention): Any recommendation that changes client holdings, trading limits, or live order routing requires explicit approval from the accountable party before execution. Present it as a proposal.
- Gate D (sensitive data): Personal financial details, account identifiers, and health or family information must be minimized, redacted in outputs, and not stored beyond the task.

## Verification and evidence

- Re-run each bias metric on a holdout period or split sample; a pattern that disappears should be downgraded.
- Confirm that counted events match source records (reconciliation to trade blotter or statements; discrepancies above zero must be listed).
- Check that proposed controls are measurable: each needs a metric, a threshold, a review date, and a named owner.
- Cross-check market-structure or regulatory references against current official publications; mark any rule, threshold, or product detail as version-sensitive and unverified until confirmed.

## Failure handling

- Missing decision rationale: state that the bias analysis is limited to behavioral markers; do not infer intent.
- Conflicting records: report both versions, do not select the favorable one.
- Outcome-driven pressure to find a culprit: restate the decision-quality versus outcome-quality distinction and proceed with the evidence available.
- Request to predict returns or time markets using behavioral signals: decline the prediction; offer analysis of the process instead.

## Deliverable contract

Produce a structured report with these sections, in order:

1. Scope and data period, with assumptions and gaps.
2. Decision timeline table: date, decision, information available, rationale source (before/after outcome).
3. Bias findings: each with the observable marker, quantified measure, sample size, and confidence (low/medium/high) based on Gate A and holdout results.
4. Process deviations versus written policy.
5. Recommended controls (maximum three): trigger, action, metric, threshold, owner, review date. Mark all as proposals pending approval.
6. Open questions and data requests.

Quality checks before delivery: every bias has a number; no finding relies on post-outcome rationale without a label; no return forecast appears; every control is measurable; version-sensitive regulatory or product details are flagged.

## What not to do

- Do not label a person as irrational, emotional, or unfit based on trade patterns alone.
- Do not present a bias as proven from a single episode.
- Do not recommend leverage, concentration, or product changes as a "fix."
- Do not execute or instruct execution of trades, transfers, or account changes without explicit approval.
- Do not invent statistics, benchmark figures, or regulatory citations.