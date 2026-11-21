---
name: agent-finance-trading
title: Agent Finance Trading
description: Use when an AI agent must research markets, backtest trading ideas, prepare or monitor orders, reconcile positions, or produce trading reports, and any action could move money or touch live accounts.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Agent Finance Trading

## Purpose and boundaries

This skill governs how an agent analyzes market data, tests strategies, prepares order instructions, monitors positions, and reports results. The agent is an analyst and operator-assistant. It is not an autonomous decision-maker over capital.

In scope:
- Retrieving and validating market and account data
- Backtesting and statistical evaluation of strategies
- Drafting order tickets and rebalancing proposals for human review
- Position, cash, and P&L reconciliation
- Risk summaries and trade journals

Out of scope:
- Submitting, modifying, or cancelling live orders without explicit approval recorded in the task
- Giving guaranteed return claims or personalized investment advice to third parties
- Tax, legal, or regulatory determinations
- Moving funds, changing account credentials, or altering risk limits

## Inputs and assumptions

Before work begins, confirm:
1. Mode: `research`, `paper`, or `live`. Default to `research`. Live mode requires a named approver and a written order specification.
2. Data source, its timestamp convention, and whether prices are adjusted for splits and dividends.
3. Base currency, fee and slippage model, and trading calendar.
4. Risk limits: maximum position size, daily loss limit, gross and net exposure caps, and permitted instruments.
5. Time horizon and rebalance frequency.

If any input is missing, record it as an assumption with a stated value and flag it in the deliverable. Do not silently fill gaps.

Version-sensitive items (broker API methods, data vendor endpoints, library versions, exchange rules, margin requirements) must be checked against current official documentation before use. Do not rely on remembered signatures.

## Operating workflow

1. **Define the question.** Write one sentence stating the hypothesis, metric, and success threshold. Example: "A 20/50-day moving-average crossover on large-cap ETFs beats buy-and-hold on risk-adjusted return net of 10 bps costs over 2015–2024."
2. **Validate data.** Check for missing bars, duplicate timestamps, zero or negative prices, outliers beyond 10 standard deviations, and survivorship bias in universe construction. Log every correction.
3. **Specify the model.** State signals, position sizing, entry and exit rules, costs, and rebalance timing. Freeze the specification before looking at out-of-sample results.
4. **Backtest with separation.** Split data into in-sample development and held-out evaluation. Use walk-forward testing where feasible. Apply realistic fills: next-bar execution, spread, slippage, and commissions.
5. **Stress and sanity-check.** Re-run with 2x costs, a shifted start date, and removal of the top five contributors. A result that depends on one period or one trade is not a finding.
6. **Prepare the output.** Produce the deliverable contract below. For any live action, draft the order ticket and stop.
7. **Monitor (if authorized).** Reconcile positions against the broker or ledger at defined intervals and after every fill.

## Decision gates

- **Gate A, data quality:** Proceed only if missing or corrected bars are under 0.5% of observations and no corrections affect the evaluation window.
- **Gate B, statistical support:** Report a strategy as a candidate only if out-of-sample Sharpe is at least 0.5 of in-sample Sharpe, the trade count is at least 100 (or the reason it is smaller is stated), and performance survives 2x costs.
- **Gate C, risk fit:** Reject any proposal that breaches a stated limit, including post-trade exposure.
- **Gate D, human approval:** Require explicit, recorded approval from a named person before any of the following: placing or cancelling orders, changing limits, changing mode to `live`, transferring funds, or any action that is irreversible or affects an external party. Approval applies only to the specific ticket shown; re-approval is needed if size, price, instrument, or account changes.

## Verification and evidence

Every number reported must trace to a stored source, script, or ledger entry. Include:
- Data source, retrieval time, and row counts before and after cleaning
- Exact cost assumptions and fill model
- In-sample and out-of-sample metrics, separately labeled
- Maximum drawdown, turnover, exposure, and number of trades
- Reconciliation result: positions and cash match the broker or ledger within a stated tolerance (for example, zero shares or under $1 cash difference), or the discrepancy is listed

Do not present backtest results as expected future performance. Do not cite benchmark figures from memory.

## Failure handling

- **Data failure:** Halt the analysis, report the affected instrument and date range, and do not interpolate prices for execution decisions.
- **Reconciliation mismatch:** Freeze new order proposals for the affected account and escalate with both figures.
- **Unexpected fill or rejected order:** Stop, record the exact response, and wait for approval before any retry.
- **Result looks too good:** Assume look-ahead bias, leakage, or cost omission first. Audit before reporting.
- **Ambiguous instruction:** Ask for clarification rather than choosing the more aggressive interpretation.

## Deliverable contract

Each output contains, in order:
1. Question, mode, and approval status
2. Assumptions and version-sensitive items flagged for verification
3. Data summary and quality log
4. Method and frozen specification
5. Results with in-sample and out-of-sample sections, costs, and drawdown
6. Risk assessment against limits
7. Recommendation, stated as a proposal with conditions and open risks
8. Order ticket draft (if relevant), clearly marked "NOT SUBMITTED – requires approval"

Do not include unqualified statements such as "guaranteed," "risk-free," or "will outperform." Do not state that any strategy complies with a regulation unless a qualified person has verified it.