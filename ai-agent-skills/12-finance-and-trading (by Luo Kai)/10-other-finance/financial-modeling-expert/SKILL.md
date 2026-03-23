---
author: luo-kai
name: financial-modeling-expert
description: Expert-level financial modeling and valuation. Use when building financial models, LBO models, DCF models, merger models, three-statement models, scenario analysis, sensitivity tables, or forecasting financial statements. Also use when the user mentions 'financial model', 'LBO', 'merger model', 'DCF', 'three statement model', 'sensitivity analysis', 'scenario analysis', 'Excel model', 'forecast', 'assumptions', 'waterfall', or 'returns analysis'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Financial Modeling Expert

You are a world-class financial modeler with deep expertise in three-statement models, DCF valuation, LBO analysis, merger models, scenario analysis, and building institutional-quality financial models in Excel and Python.

## Before Starting

1. **Model type** — Three-statement, DCF, LBO, merger, or operating model?
2. **Purpose** — Investment decision, fundraising, M&A, or internal planning?
3. **Company stage** — Early stage, growth, or mature/stable?
4. **Time horizon** — 3-year, 5-year, or 10-year forecast?
5. **Tool** — Excel, Python, or both?

---

## Core Expertise Areas

- **Three-Statement Models**: income statement, balance sheet, cash flow integration
- **DCF Valuation**: FCF projection, WACC, terminal value, sensitivity
- **LBO Models**: debt structure, returns analysis, IRR, exit multiples
- **Merger Models**: accretion/dilution, synergies, pro forma financials
- **Operating Models**: revenue build, cost structure, KPI drivers
- **Scenario Analysis**: base/bull/bear cases, sensitivity tables
- **Returns Analysis**: IRR, MOIC, equity waterfall, carried interest
- **Python Modeling**: pandas-based models, Monte Carlo, automation

---

## Three-Statement Model
```python
import pandas as pd
import numpy as np

def build_three_statement_model(assumptions):
    """
    Integrated three-statement financial model.
    Income Statement -> Cash Flow -> Balance Sheet
    """
    years   = assumptions['forecast_years']
    periods = list(range(1, years + 1))

    # ── INCOME STATEMENT ──────────────────────────────────────
    revenue = []
    base_rev = assumptions['base_revenue']
    for i, period in enumerate(periods):
        growth = assumptions['revenue_growth'][i]
        base_rev = base_rev * (1 + growth)
        revenue.append(base_rev)

    gross_profit   = [r * assumptions['gross_margin']    for r in revenue]
    ebitda         = [r * assumptions['ebitda_margin']   for r in revenue]
    da             = [r * assumptions['da_pct_revenue']  for r in revenue]
    ebit           = [e - d for e, d in zip(ebitda, da)]
    interest       = []  # filled in after debt schedule
    ebt            = []
    tax            = []
    net_income     = []

    # ── WORKING CAPITAL ───────────────────────────────────────
    ar             = [r * assumptions['ar_days'] / 365    for r in revenue]
    inventory      = [r * assumptions['inv_days'] / 365   for r in revenue]
    ap             = [r * assumptions['ap_days'] / 365    for r in revenue]
    nwc            = [a + i - p for a, i, p in zip(ar, inventory, ap)]
    delta_nwc      = [nwc[0] - assumptions['base_nwc']] + [
                      nwc[i] - nwc[i-1] for i in range(1, years)]

    # ── CAPEX & FIXED ASSETS ─────────────────────────────────
    capex          = [r * assumptions['capex_pct_revenue'] for r in revenue]
    gross_ppe      = [assumptions['base_ppe']]
    for i in range(years):
        gross_ppe.append(gross_ppe[-1] + capex[i])
    gross_ppe      = gross_ppe[1:]

    accum_dep      = [assumptions['base_accum_dep']]
    for i in range(years):
        accum_dep.append(accum_dep[-1] + da[i])
    accum_dep      = accum_dep[1:]
    net_ppe        = [g - a for g, a in zip(gross_ppe, accum_dep)]

    # ── DEBT SCHEDULE ─────────────────────────────────────────
    debt_balance   = [assumptions['base_debt']]
    for i in range(years):
        amort = min(assumptions['annual_amortization'], debt_balance[-1])
        debt_balance.append(debt_balance[-1] - amort)
    debt_balance   = debt_balance[1:]

    for i in range(years):
        avg_debt = (([assumptions['base_debt']] + debt_balance)[i] +
                    ([assumptions['base_debt']] + debt_balance)[i+1]) / 2
        interest.append(avg_debt * assumptions['interest_rate'])
        ebt_val = ebit[i] - interest[-1]
        ebt.append(ebt_val)
        tax.append(max(0, ebt_val * assumptions['tax_rate']))
        net_income.append(ebt_val - tax[-1])

    # ── CASH FLOW STATEMENT ───────────────────────────────────
    cfo            = [ni + d - dnwc
                      for ni, d, dnwc
                      in zip(net_income, da, delta_nwc)]
    cfi            = [-c for c in capex]
    debt_repayment = [assumptions['annual_amortization']] * years
    cff            = [-d for d in debt_repayment]
    net_cash_flow  = [o + i + f for o, i, f in zip(cfo, cfi, cff)]
    fcf            = [o + i for o, i in zip(cfo, cfi)]

    # ── BALANCE SHEET ─────────────────────────────────────────
    cash           = [assumptions['base_cash']]
    for cf in net_cash_flow:
        cash.append(max(0, cash[-1] + cf))
    cash           = cash[1:]

    total_assets   = [c + a + i + p
                      for c, a, i, p
                      in zip(cash, ar, inventory, net_ppe)]
    total_debt_bs  = debt_balance
    equity         = [assumptions['base_equity'] + sum(net_income[:i+1])
                      for i in range(years)]
    total_liab_eq  = [d + e + p_ap
                      for d, e, p_ap
                      in zip(total_debt_bs, equity, ap)]

    return {
        'revenue':      [round(r, 0) for r in revenue],
        'gross_profit': [round(g, 0) for g in gross_profit],
        'ebitda':       [round(e, 0) for e in ebitda],
        'ebit':         [round(e, 0) for e in ebit],
        'net_income':   [round(n, 0) for n in net_income],
        'fcf':          [round(f, 0) for f in fcf],
        'total_debt':   [round(d, 0) for d in total_debt_bs],
        'cash':         [round(c, 0) for c in cash],
        'equity':       [round(e, 0) for e in equity],
        'check':        [round(a - l, 0)
                         for a, l in zip(total_assets, total_liab_eq)]
    }

# Example assumptions
model_assumptions = {
    'forecast_years':    5,
    'base_revenue':      100_000_000,
    'revenue_growth':    [0.15, 0.12, 0.10, 0.08, 0.07],
    'gross_margin':      0.60,
    'ebitda_margin':     0.25,
    'da_pct_revenue':    0.05,
    'capex_pct_revenue': 0.06,
    'ar_days':           45,
    'inv_days':          30,
    'ap_days':           40,
    'base_nwc':          8_000_000,
    'base_ppe':          50_000_000,
    'base_accum_dep':    20_000_000,
    'base_debt':         60_000_000,
    'annual_amortization':5_000_000,
    'interest_rate':     0.07,
    'tax_rate':          0.25,
    'base_cash':         10_000_000,
    'base_equity':       40_000_000
}
```

---

## DCF Valuation Model
```python
def dcf_model(financials, assumptions):
    """
    Full DCF valuation with sensitivity analysis.
    """
    fcfs            = financials['fcf']
    wacc            = assumptions['wacc']
    terminal_growth = assumptions['terminal_growth_rate']
    net_debt        = financials['total_debt'][-1] - financials['cash'][-1]
    shares          = assumptions['shares_outstanding']

    # Discount FCFs to present value
    pv_fcfs = [fcf / (1 + wacc)**t
               for t, fcf in enumerate(fcfs, 1)]

    # Terminal value — Gordon Growth Model
    terminal_fcf    = fcfs[-1] * (1 + terminal_growth)
    terminal_value  = terminal_fcf / (wacc - terminal_growth)
    pv_terminal     = terminal_value / (1 + wacc)**len(fcfs)

    # Enterprise and equity value
    ev              = sum(pv_fcfs) + pv_terminal
    equity_value    = ev - net_debt
    price_per_share = equity_value / shares

    return {
        'pv_fcfs':          round(sum(pv_fcfs), 0),
        'terminal_value':   round(terminal_value, 0),
        'pv_terminal':      round(pv_terminal, 0),
        'terminal_pct_ev':  round(pv_terminal / ev * 100, 1),
        'enterprise_value': round(ev, 0),
        'net_debt':         round(net_debt, 0),
        'equity_value':     round(equity_value, 0),
        'price_per_share':  round(price_per_share, 2)
    }

def dcf_sensitivity_table(fcfs, net_debt, shares,
                           wacc_range, tgr_range):
    """
    Two-variable sensitivity table: WACC vs Terminal Growth Rate.
    """
    table = {}
    for wacc in wacc_range:
        row = {}
        for tgr in tgr_range:
            pv_fcfs     = sum(fcf / (1+wacc)**t
                              for t, fcf in enumerate(fcfs, 1))
            tv          = fcfs[-1] * (1+tgr) / (wacc - tgr)
            pv_tv       = tv / (1+wacc)**len(fcfs)
            price       = (pv_fcfs + pv_tv - net_debt) / shares
            row[f"TGR={tgr:.1%}"] = round(price, 2)
        table[f"WACC={wacc:.1%}"] = row
    return pd.DataFrame(table).T

def wacc_calculation(equity_value, debt_value, cost_of_equity,
                      cost_of_debt, tax_rate):
    """Calculate WACC from capital structure."""
    total   = equity_value + debt_value
    we      = equity_value / total
    wd      = debt_value / total
    wacc    = we * cost_of_equity + wd * cost_of_debt * (1 - tax_rate)
    return {
        'wacc':             round(wacc * 100, 3),
        'equity_weight':    round(we * 100, 1),
        'debt_weight':      round(wd * 100, 1),
        'after_tax_kd':     round(cost_of_debt * (1-tax_rate) * 100, 3)
    }
```

---

## LBO Model
```python
def lbo_model(entry_assumptions, operating_assumptions, exit_assumptions):
    """
    Leveraged Buyout model — private equity returns analysis.
    """
    # ── ENTRY ─────────────────────────────────────────────────
    entry_ebitda    = entry_assumptions['ltm_ebitda']
    entry_multiple  = entry_assumptions['ev_ebitda_multiple']
    entry_ev        = entry_ebitda * entry_multiple
    equity_check    = entry_assumptions['equity_contribution']
    total_debt      = entry_ev - equity_check
    debt_tranches   = entry_assumptions['debt_tranches']

    # ── OPERATING PROJECTION ──────────────────────────────────
    years           = operating_assumptions['hold_period']
    ebitda          = [entry_ebitda]
    for g in operating_assumptions['ebitda_growth']:
        ebitda.append(ebitda[-1] * (1 + g))
    ebitda          = ebitda[1:]

    revenue         = [e / operating_assumptions['ebitda_margin']
                       for e in ebitda]
    da              = [r * operating_assumptions['da_pct']
                       for r in revenue]
    ebit            = [e - d for e, d in zip(ebitda, da)]

    # ── DEBT SCHEDULE ─────────────────────────────────────────
    debt_schedule   = []
    cash_sweep      = []
    debt_bal        = {t['name']: t['amount'] for t in debt_tranches}

    for year in range(years):
        interest_total = sum(
            bal * t['rate']
            for t, bal in zip(debt_tranches,
                               [debt_bal[t['name']] for t in debt_tranches])
        )
        nopat    = ebit[year] * (1 - operating_assumptions['tax_rate'])
        capex    = revenue[year] * operating_assumptions['capex_pct']
        delta_nwc= revenue[year] * operating_assumptions['nwc_pct_change']
        fcf      = nopat + da[year] - capex - delta_nwc - interest_total

        # Mandatory amortization first
        for t in debt_tranches:
            amort = min(t.get('annual_amort', 0), debt_bal[t['name']])
            debt_bal[t['name']] -= amort

        # Cash sweep on revolving/term loan B
        cash_available = max(0, fcf)
        for t in debt_tranches:
            if t.get('cash_sweep', False):
                sweep = min(cash_available, debt_bal[t['name']])
                debt_bal[t['name']] -= sweep
                cash_available      -= sweep

        total_debt_yr   = sum(debt_bal.values())
        debt_schedule.append({
            'year':       year + 1,
            'ebitda':     round(ebitda[year], 0),
            'interest':   round(interest_total, 0),
            'total_debt': round(total_debt_yr, 0),
            'leverage':   round(total_debt_yr / ebitda[year], 2),
            'fcf':        round(fcf, 0)
        })

    # ── EXIT ──────────────────────────────────────────────────
    exit_ebitda     = ebitda[-1]
    exit_multiple   = exit_assumptions['ev_ebitda_multiple']
    exit_ev         = exit_ebitda * exit_multiple
    exit_debt       = sum(debt_bal.values())
    exit_equity     = exit_ev - exit_debt

    # ── RETURNS ───────────────────────────────────────────────
    moic            = exit_equity / equity_check
    irr             = (moic ** (1/years)) - 1

    # IRR using cash flows
    cash_flows      = [-equity_check] + [0] * (years - 1) + [exit_equity]
    irr_precise     = np.irr(cash_flows) if hasattr(np, 'irr') else irr

    return {
        'entry': {
            'ev':               round(entry_ev, 0),
            'equity_check':     round(equity_check, 0),
            'total_debt':       round(total_debt, 0),
            'entry_leverage':   round(total_debt / entry_ebitda, 2)
        },
        'exit': {
            'exit_ebitda':      round(exit_ebitda, 0),
            'exit_ev':          round(exit_ev, 0),
            'exit_debt':        round(exit_debt, 0),
            'exit_equity':      round(exit_equity, 0)
        },
        'returns': {
            'moic':             round(moic, 2),
            'irr':              round(irr * 100, 1),
            'hold_period':      years
        },
        'debt_schedule':        debt_schedule
    }

def irr_sensitivity(entry_ev, equity_check, exit_ebitda,
                     exit_multiples, hold_periods):
    """IRR sensitivity table: exit multiple vs hold period."""
    table = {}
    for mult in exit_multiples:
        row = {}
        for period in hold_periods:
            exit_equity = exit_ebitda * mult - (entry_ev - equity_check)
            moic        = exit_equity / equity_check
            irr         = (moic ** (1/period) - 1) * 100
            row[f"{period}yr"] = f"{irr:.1f}%"
        table[f"{mult}x exit"] = row
    return pd.DataFrame(table).T
```

---

## Merger Model (M&A)
```python
def merger_model(acquirer, target, deal_assumptions):
    """
    Merger accretion/dilution analysis.
    Tests whether deal is EPS accretive or dilutive.
    """
    # ── DEAL STRUCTURE ────────────────────────────────────────
    purchase_price  = target['share_price'] * target['shares_outstanding']
    cash_portion    = purchase_price * deal_assumptions['cash_pct']
    stock_portion   = purchase_price * (1 - deal_assumptions['cash_pct'])
    new_shares      = stock_portion / acquirer['share_price']
    debt_raised     = cash_portion * deal_assumptions['debt_pct_of_cash']
    cash_used       = cash_portion - debt_raised

    # ── PRO FORMA INCOME STATEMENT ───────────────────────────
    combined_revenue   = acquirer['revenue'] + target['revenue']
    revenue_synergies  = combined_revenue * deal_assumptions['revenue_synergy_pct']
    cost_synergies     = deal_assumptions['cost_synergies']
    combined_ebitda    = (acquirer['ebitda'] + target['ebitda'] +
                          cost_synergies + revenue_synergies *
                          deal_assumptions['synergy_margin'])
    combined_da        = acquirer['da'] + target['da'] + \
                         deal_assumptions['incremental_da']
    combined_ebit      = combined_ebitda - combined_da
    incremental_interest = debt_raised * deal_assumptions['debt_rate']
    combined_ebt       = (acquirer['ebt'] + target['ebt'] +
                          cost_synergies - incremental_interest +
                          revenue_synergies * deal_assumptions['synergy_margin'])
    combined_tax       = combined_ebt * deal_assumptions['tax_rate']
    combined_ni        = combined_ebt - combined_tax

    # ── EPS ANALYSIS ──────────────────────────────────────────
    pro_forma_shares   = acquirer['shares_outstanding'] + new_shares
    acquirer_standalone_eps = acquirer['net_income'] / acquirer['shares_outstanding']
    pro_forma_eps          = combined_ni / pro_forma_shares
    accretion_dilution_pct = (pro_forma_eps - acquirer_standalone_eps) / \
                              acquirer_standalone_eps * 100

    # ── GOODWILL ─────────────────────────────────────────────
    target_book_value  = target['total_equity']
    purchase_premium   = purchase_price - target_book_value
    identified_intangibles = deal_assumptions.get('identified_intangibles', 0)
    goodwill           = purchase_premium - identified_intangibles

    return {
        'deal_structure': {
            'purchase_price':   round(purchase_price, 0),
            'cash_paid':        round(cash_used, 0),
            'debt_raised':      round(debt_raised, 0),
            'new_shares':       round(new_shares, 0),
            'premium_pct':      round((purchase_price /
                                        (target['share_price'] *
                                         target['shares_outstanding']) - 1) * 100, 1)
        },
        'pro_forma': {
            'combined_revenue': round(combined_revenue + revenue_synergies, 0),
            'combined_ebitda':  round(combined_ebitda, 0),
            'combined_ni':      round(combined_ni, 0),
            'pro_forma_shares': round(pro_forma_shares, 0)
        },
        'eps_analysis': {
            'standalone_eps':       round(acquirer_standalone_eps, 4),
            'pro_forma_eps':        round(pro_forma_eps, 4),
            'accretion_dilution':   round(accretion_dilution_pct, 2),
            'verdict':              'Accretive' if accretion_dilution_pct > 0
                                    else 'Dilutive'
        },
        'goodwill':             round(goodwill, 0)
    }
```

---

## Scenario & Sensitivity Analysis
```python
def scenario_analysis(model_fn, base_assumptions, scenarios):
    """
    Run model under multiple scenarios.
    scenarios: dict of {name: {assumption_overrides}}
    """
    results = {}

    for scenario_name, overrides in scenarios.items():
        assumptions = {**base_assumptions, **overrides}
        output      = model_fn(assumptions)
        results[scenario_name] = output

    return results

def tornado_chart_data(model_fn, base_assumptions,
                        variable_ranges, output_key):
    """
    Tornado chart data — rank variables by output impact.
    Shows which assumptions matter most.
    """
    base_output = model_fn(base_assumptions)[output_key]
    impacts     = []

    for var, (low_val, high_val) in variable_ranges.items():
        low_assumptions  = {**base_assumptions, var: low_val}
        high_assumptions = {**base_assumptions, var: high_val}

        low_output  = model_fn(low_assumptions)[output_key]
        high_output = model_fn(high_assumptions)[output_key]

        impacts.append({
            'variable':    var,
            'low_output':  round(low_output, 2),
            'high_output': round(high_output, 2),
            'range':       round(abs(high_output - low_output), 2),
            'low_value':   low_val,
            'high_value':  high_val
        })

    return sorted(impacts, key=lambda x: x['range'], reverse=True)

# Standard scenario set
standard_scenarios = {
    'Base Case': {
        'revenue_growth': [0.10, 0.10, 0.08, 0.07, 0.06],
        'ebitda_margin':  0.25,
        'wacc':           0.10,
        'exit_multiple':  10
    },
    'Bull Case': {
        'revenue_growth': [0.18, 0.15, 0.13, 0.11, 0.10],
        'ebitda_margin':  0.28,
        'wacc':           0.09,
        'exit_multiple':  12
    },
    'Bear Case': {
        'revenue_growth': [0.05, 0.04, 0.03, 0.03, 0.02],
        'ebitda_margin':  0.20,
        'wacc':           0.12,
        'exit_multiple':  8
    },
    'Stress Case': {
        'revenue_growth': [-0.05, 0.00, 0.02, 0.03, 0.04],
        'ebitda_margin':  0.15,
        'wacc':           0.14,
        'exit_multiple':  6
    }
}
```

---

## Model Best Practices
```python
def modeling_best_practices():
    return {
        'Structure': [
            'Separate inputs (blue), calculations (black), outputs (green)',
            'One assumption per cell — never hardcode numbers in formulas',
            'Flow left to right, top to bottom — logical reading order',
            'Balance sheet must balance — build in check row',
            'Circular references: use iterative calculation for interest on debt'
        ],
        'Assumptions': [
            'All assumptions on single dedicated tab',
            'Source every assumption — note where it came from',
            'Use historical averages as anchor for forecasts',
            'Stress-test every key assumption individually',
            'Document what would need to be true for bull/bear cases'
        ],
        'Error Prevention': [
            'Balance check: assets = liabilities + equity (should = 0)',
            'Cash flow check: ending cash = beginning cash + net change',
            'Ratio sanity: margins, leverage, coverage in reasonable range',
            'Cross-check DCF equity value vs comparable company multiples',
            'Audit trail: trace any output back to source assumption'
        ],
        'Outputs': [
            'Executive summary page: key outputs on one page',
            'Scenario comparison table: base/bull/bear side by side',
            'Sensitivity tables for key value drivers',
            'IRR/MOIC waterfall for returns models',
            'Football field chart: range of values across methodologies'
        ]
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Circular references | Model crashes or gives wrong answer | Use iterative calc or stub interest |
| Hardcoded numbers | Cannot run scenarios | All numbers in assumptions tab |
| Balance sheet imbalance | Model is wrong | Build check row, debug systematically |
| Overcomplicating model | Garbage in garbage out | Simple model with clean assumptions beats complex broken one |
| No sensitivity analysis | Miss key value drivers | Always build sensitivity tables |
| Optimistic assumptions | Model always shows good returns | Run bear case first |
| Terminal value dominates | 80%+ of DCF value in terminal value | Test terminal value sensitivity heavily |

---

## Best Practices

- **Keep it simple** — a clean 3-statement model beats a complex broken one
- **Assumptions drive everything** — spend most time on assumption quality
- **Always build bear case first** — forces honest thinking about downside
- **Terminal value sensitivity** — if TV is >70% of DCF value, be very careful
- **Cross-check valuation** — DCF vs comps vs precedents should bracket a range
- **Document your work** — someone else should be able to understand your model
- **Version control** — save dated versions before major changes

---

## Related Skills

- **fundamental-analysis-expert**: Financial statement interpretation
- **quantitative-finance-expert**: Statistical modeling in Python
- **private-equity-expert**: LBO modeling in PE context
- **risk-management-expert**: Scenario and stress testing
- **macro-economics-expert**: Top-down assumption setting
