---
name: trading-psychology
description: Use when reviewing a trader's decision process, journal, or behavior patterns; designing pre-trade and post-trade checklists; diagnosing revenge trading, overtrading, or rule drift; or building discipline controls for a discretionary or systematic trading practice.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Trading Psychology

## Purpose and boundaries

This skill turns trading behavior into observable evidence and then into concrete process changes. It covers: decision-quality review, emotional-state and behavior logging, rule-adherence auditing, pre-trade and post-trade checklists, and written discipline protocols for discretionary or systematic traders.

It does not provide clinical diagnosis, treatment, or mental-health advice. It does not recommend specific securities, entries, exits, position sizes, or return targets. If behavior suggests addiction, severe distress, or self-harm risk, stop the analysis and direct the user to qualified professional support.

## Inputs and assumptions

Request these before analysis:
- Trade log: timestamp, instrument, side, size, entry, exit, stop, target, realized P&L, and the stated reason for entry.
- Rule set: the written plan, including risk per trade, maximum daily loss, allowed setups, and session hours.
- Context notes: market conditions, news exposure, sleep or fatigue notes if the user volunteers them, and any account events (drawdowns, withdrawals, prop-firm limits).
- Time window: at least 30 trades or 20 trading days for pattern claims. Fewer trades support only anecdotal observations; label them as such.

Assume the logs are accurate unless reconciliation shows otherwise. Do not assume intent. Describe behavior, not character.

## Operating workflow

1. Reconcile the log against the rule set. Flag every trade with missing stop, size above the stated risk limit, entry outside allowed setups, or trades after the daily loss limit.
2. Compute process metrics, not just P&L: percent of trades with a predefined stop, percent of trades meeting all entry criteria, average risk per trade versus plan, trades per session, and time from loss to next entry.
3. Segment by state. Compare outcomes for trades taken within 15 minutes of a loss, after two or more consecutive losses, after a winning streak, and in the final hour of the session.
4. Test for specific patterns:
   - Revenge: next-trade size above baseline within 30 minutes of a loss.
   - Overtrading: trade count more than 1.5 times the session median with declining setup quality.
   - Loss aversion: losers held materially longer than winners, or stops moved away from entry.
   - Premature exit: winners closed well before target with no rule trigger.
5. Rank findings by estimated cost (sum of rule-violating losses) and by frequency.
6. Propose at most three interventions, each with a trigger, an action, and a measurable test.

## Decision gates

- Gate A (sample sufficiency): if fewer than 30 trades, report observations only and do not recommend rule changes.
- Gate B (causal caution): describe correlations between state and outcome as associations. Do not claim a feeling caused a loss.
- Gate C (intervention approval): any change to position limits, live-account permissions, risk settings, or broker configuration requires explicit written approval from the account owner before the user applies it. Do not modify live settings yourself.
- Gate D (sensitive content): if the user discloses financial distress, debt, or personal crisis, pause the performance analysis and ask whether they want to address that separately with appropriate professional help.

## Verification and evidence

Every finding must cite the trade IDs or dates supporting it. Provide counts and the calculation used. Before presenting an intervention, check:
- It targets a finding with at least 5 supporting instances.
- It has a binary, loggable trigger (for example, "two consecutive losses" rather than "feeling frustrated").
- It defines a review horizon (for example, 20 sessions) and a success metric (for example, rule-violation rate below 5 percent).

Do not claim statistical significance without naming the test and its assumptions. Do not cite published research findings unless the user supplies the source and you can verify it.

## Failure handling

- Incomplete logs: list missing fields, quantify the affected trades, and exclude them from metrics with a stated count.
- Contradictory data (P&L not reconciling with fills): stop and request broker statements. Do not estimate.
- User requests a guaranteed-profit system or a pitch for a specific instrument: decline that part and continue with the process review.
- User asks for a plan to recover losses quickly: refuse the sizing escalation and redirect to the loss-limit protocol.

## Deliverable contract

Return a report with these sections, in order:
1. Summary (three sentences maximum, stating the highest-cost violation).
2. Data quality (trade count, date range, excluded records).
3. Process metrics table (metric, value, plan target, status).
4. Findings (ranked, each with evidence IDs and calculation).
5. Interventions (maximum three; trigger, action, metric, review date, approval status).
6. Open questions for the user.

Do not include motivational language, guarantees of future performance, or unverified claims about market behavior.