---
name: fundamentals-valuation
description: Use when estimating the intrinsic value of a listed or private company from financial statements, building or reviewing DCF, comparable-company, or residual-income models, or checking whether a stated price target is supported by its assumptions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Fundamentals Valuation

## Purpose and boundaries

This skill produces a documented, auditable valuation of an operating company (or a specific equity/enterprise claim) from its financial fundamentals. It covers: normalizing historical financials, forecasting free cash flow or residual income, selecting discount rates, cross-checking with relative multiples, and stating a value range with its sensitivities.

It does not cover: trade execution, position sizing, portfolio construction, options or derivatives pricing, real-estate appraisal, bank-regulatory capital analysis, or giving personalized investment advice. Output is analysis for a qualified professional to review; it is not a recommendation to buy or sell.

## Inputs and assumptions

Required inputs, in order of priority:
1. Three to five years of audited annual statements (income statement, balance sheet, cash flow statement) and the most recent interim filing.
2. Share count (basic and diluted), net debt components, and minority interests, preferred equity, and pension deficits.
3. Market data as of a stated date: share price, risk-free rate reference, and peer multiples.
4. Management guidance and consensus estimates, labeled as third-party inputs.

Record every assumption in an assumptions register: value, source, date, and owner. Treat unlabeled numbers as unsupported. If a required input is missing, mark the dependent output "provisional" rather than filling it with an estimate silently.

Do not assume the company's reporting follows a single standard without checking. Flag any reliance on non-GAAP or non-IFRS adjusted measures and reconcile them to statutory figures.

## Operating workflow

1. **Define the claim.** State the value being estimated (equity value per share, enterprise value, or a specific business unit) and the valuation date.
2. **Normalize historicals.** Remove one-offs (impairments, restructuring, litigation, disposal gains). Separate operating from non-operating assets and liabilities. Capitalize or expense leases consistently with the reporting standard in force; verify the treatment against current accounting standard text.
3. **Compute invested capital and returns.** Calculate return on invested capital (NOPAT divided by average invested capital) for each historical year. Use this to test whether growth creates or destroys value.
4. **Build the forecast.** Drive revenue by segment or volume × price where possible. Forecast margins, reinvestment rate (net capex plus working-capital change divided by NOPAT), and the fade toward a terminal state. Link growth to reinvestment: implied growth equals reinvestment rate × return on new capital.
5. **Set the discount rate.** Build cost of capital from a stated risk-free rate, equity risk premium, and beta from a documented method. Show the sensitivity of beta to leverage. Use a target capital structure, not the current one, unless justified.
6. **Compute terminal value.** Use a perpetuity growth rate that does not exceed long-run nominal economic growth for the relevant currency. Cross-check the implied exit multiple against sector history.
7. **Cross-check with relative value.** Select peers by business model, growth, and returns, not by sector label alone. Use normalized multiples (EV/EBITDA after lease treatment, P/E on normalized earnings). Report the median and interquartile range.
8. **Reconcile to per-share value.** Subtract net debt and equity claims, divide by diluted shares using the treasury stock method where options are material.
9. **Run sensitivities.** Vary discount rate, terminal growth, and the margin path. Identify which single input moves value most.
10. **Write the conclusion as a range** with the central case, bear and bull cases, and the assumptions that drive the gap.

## Decision gates

- **Gate A (inputs):** Proceed only if audited statements, share count, and net debt are sourced. Otherwise output "provisional" and list the blocking items.
- **Gate B (normalization):** If one-offs exceed 10% of operating profit in any forecast base year, document each adjustment before forecasting.
- **Gate C (terminal value):** If terminal value exceeds 80% of enterprise value, require an explicit explanation and a sensitivity table with a reduced terminal growth case.
- **Gate D (discount rate):** If the discount rate is below the cost of debt after tax, or the terminal growth rate is at or above the discount rate, stop and correct before reporting.
- **Gate E (external use):** Any valuation intended for distribution to third parties, use in a transaction, fairness opinion, regulatory filing, or client-facing price target requires explicit human approval and review by a credentialed professional. Do not produce such material as final.

## Verification and evidence

Quality checks, each must pass or be explained:
- Forecast reinvestment and growth are internally consistent (implied return on new capital is within a stated, defended range relative to historical ROIC).
- Balance sheet reconciles: forecast net debt roll-forward equals cash flow after distributions.
- Per-share value recomputes from enterprise value within rounding tolerance.
- Peer set has at least five companies with documented selection criteria, or the relative cross-check is labeled weak.
- Sensitivity table covers at least a ±1 percentage point discount rate range and ±0.5 percentage point terminal growth range.
- Every number traces to a source row in the assumptions register.

Tax rates, accounting rules, and regulatory thresholds change. Mark each such detail "verify against current official documentation" with the document name and date checked.

## Failure handling

- **Missing data:** Stop the affected line item, mark it provisional, and list the data request. Do not back-solve figures from the target price.
- **Conflicting sources:** Prefer audited filings over press summaries; prefer the primary filing over derived databases. Record the conflict.
- **Target-price anchoring:** If the result is reached by adjusting inputs toward a known market price or a desired outcome, discard the model and restart from the assumptions register.
- **Sudden model break** (negative invested capital, sign errors, circular references): freeze output, identify the first failing cell or step, and fix before continuing.

## Deliverable contract

Deliver a single document containing, in order:
1. Valuation date, claim, and status (final draft or provisional).
2. Assumptions register table (item, value, source, date).
3. Normalized historical summary with one-off adjustments listed.
4. Forecast table with explicit drivers and reinvestment link.
5. Discount rate build-up.
6. Valuation output: enterprise value, equity value, value per share, with bear/central/bull range.
7. Relative cross-check with peer list and criteria.
8. Sensitivity tables.
9. Open items, gate results, and items marked for verification against current documentation.

Do not include buy, sell, or hold language. Do not present a point estimate without its range and drivers. Do not state that the model is "accurate," "guaranteed," or "compliant."