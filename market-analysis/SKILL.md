---
name: market-analysis
description: Use when a user asks for analysis of a financial market, asset, sector, or trading setup, including price and volume behavior, macro or sector context, positioning, or a written market view that must be checked against data before use.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Market Analysis

## Purpose and boundaries

This skill produces structured, evidence-backed analysis of a named market, instrument set, or sector over a stated horizon. Typical outputs: a market briefing, a thesis with invalidation conditions, a comparison of instruments, or a review of a trading setup's risk profile.

In scope: descriptive analysis of price, volume, volatility, spreads, term structure, fundamentals, macro releases, and positioning data that the user supplies or that is publicly available and cited.

Out of scope: placing or modifying orders, giving personalized recommendations for a specific person's portfolio, using material non-public information, and asserting future returns as fact. Analysis is conditional: state what would make the view wrong.

## Inputs and assumptions

Before analysis, confirm and record:

1. **Instrument identifiers**: ticker, contract month, currency, exchange, and whether prices are adjusted for splits, dividends, or rolls.
2. **Horizon**: intraday, days, weeks, or quarters. Methods differ by horizon.
3. **Data vintage**: timestamp and source of every series. Flag any series older than the stated horizon warrants.
4. **Purpose**: research note, internal risk review, or idea generation. Each carries different disclosure needs.
5. **Constraints**: benchmark, sector, liquidity requirements, and any restricted-list status the user reports.

Assumptions must be written down explicitly. Do not assume data is clean, continuous, or survivorship-free. Do not assume a user's position size, cost basis, or mandate unless provided.

## Operating workflow

1. **Define the question** in one sentence, including the horizon and the decision it informs.
2. **Establish the regime**: trend versus range (e.g., moving-average slope and realized volatility relative to its 1-year range), volatility level, and correlation to a relevant benchmark.
3. **Analyze price and volume**: identify support and resistance only where price has reacted repeatedly; check whether volume confirms moves; note gaps and their fill status.
4. **Add context**: scheduled macro events within the horizon, earnings or guidance dates, rate and currency drivers, and sector rotation evidence.
5. **Check positioning and flows** if data is available: futures open interest changes, fund flow reports, options skew. Label inferred positioning as inference.
6. **Build the thesis**: state the base case, the bull and bear alternatives, and the observable conditions that would falsify the base case.
7. **Quantify risk**: give a historical drawdown range for the instrument over comparable windows, and the expected move implied by options or by realized volatility, naming which one is used.
8. **Compose the market analysis** in the required structure below.

## Decision gates

- **Gate A (data)**: If any core series has a missing span longer than 5% of the window, or prices are unadjusted across corporate actions, stop and request corrected data or disclose the limitation prominently.
- **Gate B (horizon mismatch)**: If the user asks for a multi-month view based only on intraday data, downgrade the conclusion to a short-horizon observation.
- **Gate C (approval required)**: Obtain explicit user approval before any of the following: sending analysis outside the user's organization, using licensed or paid data beyond what the user has confirmed they hold, producing content that names a specific security as a buy or sell for distribution, or any step that would transmit client or account information.
- **Gate D (sensitive information)**: If the input contains apparent non-public information, halt, do not use it, and tell the user to route the matter to their compliance function.

## Verification and evidence

Every quantitative claim needs a source, a date, and a calculation note. Before finalizing:

- Recompute at least two headline figures (returns, volatility, percentage moves) from raw data and confirm agreement within rounding.
- Confirm that date alignment across series is correct, especially across time zones and holidays.
- Check that each thesis has at least one explicit falsification condition that is observable and dated.
- Mark anything version-sensitive, such as exchange rules, contract specifications, index methodology, or regulatory thresholds, as requiring verification against current official documentation.
- Do not supply benchmark statistics, backtest results, or performance figures from memory. Use only figures the user provides or cited sources.

## Failure handling

- **Conflicting sources**: report both values, state which is primary and why, and do not average them silently.
- **Insufficient data**: narrow the claim to what the data supports and list the specific missing inputs.
- **User pushes for certainty**: restate the probabilistic nature of the view and the falsification conditions. Do not inflate confidence.
- **Stale data discovered after drafting**: revise, mark the change, and re-run the verification checks.

## Deliverable contract

The output must contain, in order:

1. Question, horizon, and data vintage.
2. Summary view in no more than five sentences.
3. Regime and evidence table with source and date per row.
4. Base, bull, and bear cases, each with its falsification condition.
5. Risk figures with stated method.
6. Assumptions and data limitations.
7. Verification log: checks performed and results.
8. Required approvals outstanding, if any.

Do not: present forecasts as certainties, omit the falsification conditions, use undated figures, recommend position sizes for unnamed accounts, or present the analysis as individualized investment advice.