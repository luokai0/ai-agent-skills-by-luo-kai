---
name: private-equity-expert
description: Expert-level private equity knowledge. Use when working with LBO analysis, deal sourcing, due diligence, portfolio company management, exit strategies, fund structure, carried interest, capital calls, or venture capital. Also use when the user mentions 'LBO', 'private equity', 'buyout', 'portfolio company', 'carried interest', 'IRR', 'MOIC', 'capital call', 'dry powder', 'deal flow', 'due diligence', 'add-on acquisition', or 'exit multiple'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Private Equity Expert

You are a world-class private equity professional with deep expertise in LBO analysis, deal sourcing, due diligence, portfolio company value creation, exit strategies, fund economics, and the full private equity investment lifecycle.

## Before Starting

1. **Focus** — Deal analysis, fund structure, portfolio management, or exits?
2. **Strategy** — Buyout, growth equity, venture, distressed, or real assets?
3. **Stage** — Sourcing, diligence, execution, ownership, or exit?
4. **Size** — Small cap (<$100M EV), mid-market ($100M-$1B), or large cap (>$1B)?
5. **Goal** — IRR analysis, deal structuring, value creation, or fund economics?

---

## Core Expertise Areas

- **LBO Analysis**: deal structure, debt capacity, returns modeling
- **Deal Sourcing**: proprietary deal flow, intermediary relationships
- **Due Diligence**: commercial, financial, legal, operational
- **Value Creation**: operational improvements, bolt-on M&A, multiple expansion
- **Exit Strategies**: IPO, strategic sale, secondary buyout, recapitalization
- **Fund Structure**: LP/GP economics, carried interest, waterfall
- **Venture Capital**: term sheets, cap tables, dilution, portfolio construction
- **Portfolio Monitoring**: KPIs, board governance, management alignment

---

## LBO Analysis Framework
```python
import numpy as np
import pandas as pd

def lbo_entry_analysis(company_data, deal_assumptions):
    """
    Full LBO entry analysis — can we make money on this deal?
    """
    # ── PURCHASE PRICE ────────────────────────────────────────
    ltm_ebitda      = company_data['ltm_ebitda']
    entry_multiple  = deal_assumptions['entry_ev_ebitda']
    entry_ev        = ltm_ebitda * entry_multiple
    net_debt        = company_data['net_debt']
    equity_value    = entry_ev - net_debt
    transaction_costs = entry_ev * 0.02  # 2% fees

    # ── DEBT CAPACITY ─────────────────────────────────────────
    max_leverage    = deal_assumptions['max_debt_ebitda']
    total_debt      = min(ltm_ebitda * max_leverage,
                          entry_ev * deal_assumptions['max_debt_pct_ev'])

    debt_tranches   = {
        'Senior Secured TLB': {
            'amount': total_debt * 0.60,
            'rate':   deal_assumptions['tlb_rate'],
            'amort':  0.01,  # 1% annual mandatory amort
            'cash_sweep': True
        },
        'Senior Notes': {
            'amount': total_debt * 0.30,
            'rate':   deal_assumptions['notes_rate'],
            'amort':  0.00,  # bullet
            'cash_sweep': False
        },
        'Mezzanine': {
            'amount': total_debt * 0.10,
            'rate':   deal_assumptions['mezz_rate'],
            'amort':  0.00,
            'cash_sweep': False
        }
    }

    equity_check    = entry_ev - total_debt + transaction_costs
    equity_pct      = equity_check / entry_ev

    return {
        'entry_ev':          round(entry_ev, 0),
        'entry_multiple':    entry_multiple,
        'total_debt':        round(total_debt, 0),
        'equity_check':      round(equity_check, 0),
        'equity_pct':        round(equity_pct * 100, 1),
        'leverage_turns':    round(total_debt / ltm_ebitda, 2),
        'debt_tranches':     {k: round(v['amount'], 0)
                              for k, v in debt_tranches.items()},
        'feasibility':       'Feasible' if equity_pct > 0.25 else
                             'Highly Leveraged' if equity_pct > 0.15 else
                             'Too Leveraged'
    }

def lbo_returns_model(entry_data, operating_projections, exit_assumptions):
    """
    Model PE returns across hold period.
    """
    hold_years      = exit_assumptions['hold_period']
    entry_ev        = entry_data['entry_ev']
    equity_check    = entry_data['equity_check']
    initial_debt    = entry_data['total_debt']

    # Project EBITDA
    ebitda          = [entry_data['entry_ebitda']]
    for g in operating_projections['ebitda_growth_rates']:
        ebitda.append(ebitda[-1] * (1 + g))
    exit_ebitda     = ebitda[hold_years]

    # Debt paydown (simplified)
    fcf_conversion  = operating_projections['fcf_to_ebitda']
    annual_fcf      = [e * fcf_conversion for e in ebitda[1:hold_years+1]]
    debt_paydown    = sum(annual_fcf) * operating_projections['debt_sweep_pct']
    exit_debt       = max(0, initial_debt - debt_paydown)

    # Exit
    exit_multiple   = exit_assumptions['exit_ev_ebitda']
    exit_ev         = exit_ebitda * exit_multiple
    exit_equity     = exit_ev - exit_debt
    moic            = exit_equity / equity_check

    # IRR calculation
    cash_flows      = [-equity_check] + [0]*(hold_years-1) + [exit_equity]
    irr             = np.irr(cash_flows) if hasattr(np, 'irr') else (
                      moic**(1/hold_years) - 1)

    # Value creation attribution
    ebitda_growth_val = (exit_ebitda - ebitda[0]) * exit_multiple
    multiple_exp_val  = ebitda[0] * (exit_multiple - entry_ev/ebitda[0])
    debt_paydown_val  = debt_paydown

    return {
        'exit_ebitda':       round(exit_ebitda, 0),
        'exit_ev':           round(exit_ev, 0),
        'exit_debt':         round(exit_debt, 0),
        'exit_equity':       round(exit_equity, 0),
        'moic':              round(moic, 2),
        'irr':               round(irr * 100, 1),
        'value_creation': {
            'ebitda_growth':  round(ebitda_growth_val, 0),
            'multiple_exp':   round(multiple_exp_val, 0),
            'debt_paydown':   round(debt_paydown_val, 0)
        },
        'returns_quality':   'Excellent' if irr > 0.25 else
                             'Good'      if irr > 0.20 else
                             'Acceptable'if irr > 0.15 else 'Poor'
    }

def irr_sensitivity_table(exit_ebitda, initial_debt_paydown,
                           equity_check, exit_multiples, hold_periods):
    """PE returns sensitivity: exit multiple vs hold period."""
    results = {}
    for mult in exit_multiples:
        row = {}
        for period in hold_periods:
            exit_equity = exit_ebitda * mult - initial_debt_paydown
            moic        = exit_equity / equity_check
            irr         = (moic**(1/period) - 1) * 100
            row[f"{period}yr"] = f"{irr:.1f}%"
        results[f"{mult}x"] = row
    return pd.DataFrame(results).T
```

---

## Due Diligence Framework
```python
def due_diligence_checklist():
    return {
        'Commercial DD': {
            'Market': [
                'Total addressable market size and growth rate',
                'Market share trends — gaining or losing?',
                'Competitive dynamics — fragmented or consolidated?',
                'Customer concentration — top 10 customers as % of revenue',
                'Pricing power — ability to pass through cost increases'
            ],
            'Business Quality': [
                'Revenue quality — recurring vs transactional',
                'Customer retention and NRR (if SaaS/subscription)',
                'Sales cycle length and win rates',
                'Product differentiation vs commoditization',
                'Management team depth and retention'
            ],
            'Risks': [
                'Key man dependency — what if CEO leaves?',
                'Technology disruption risk',
                'Regulatory risk',
                'Customer concentration (>20% in single customer)',
                'Supplier concentration and pricing power'
            ]
        },
        'Financial DD': {
            'Quality of Earnings': [
                'Normalize EBITDA — remove non-recurring items',
                'Verify revenue recognition policy',
                'Analyze working capital trends',
                'Validate FCF conversion vs net income',
                'Assess off-balance sheet liabilities'
            ],
            'Historical Analysis': [
                'Revenue growth consistency (3-5 years)',
                'Margin trends — expanding or compressing?',
                'Capex intensity and maintenance vs growth split',
                'Working capital seasonality',
                'Debt covenant headroom'
            ],
            'Projections': [
                'Management case vs independent case',
                'Sensitivity to key revenue assumptions',
                'Breakeven analysis',
                'Liquidity runway under stress',
                'Debt service coverage ratios'
            ]
        },
        'Legal DD': [
            'Material contracts and change of control provisions',
            'Litigation and contingent liabilities',
            'IP ownership — patents, trademarks, trade secrets',
            'Employment agreements and non-competes',
            'Regulatory compliance and licenses',
            'Environmental liabilities',
            'Tax structure and outstanding obligations'
        ],
        'Operational DD': [
            'IT systems and technology infrastructure',
            'Supply chain resilience',
            'Key operational metrics and benchmarks',
            'Management incentive alignment',
            'ESG compliance and risks',
            'Integration complexity (for add-ons)'
        ]
    }

def quality_of_earnings_adjustments(reported_ebitda, adjustments):
    """
    Normalize EBITDA for non-recurring and non-cash items.
    """
    adjusted = reported_ebitda
    breakdown = {'reported': reported_ebitda}

    for item, amount in adjustments.items():
        adjusted += amount
        breakdown[item] = amount

    breakdown['adjusted_ebitda'] = adjusted
    breakdown['adjustment_total'] = adjusted - reported_ebitda
    breakdown['adjustment_pct']   = round(
        (adjusted - reported_ebitda) / reported_ebitda * 100, 1)

    return breakdown

# Common EBITDA adjustments
common_adjustments = {
    'owner_compensation_excess':  +500_000,   # normalize to market rate
    'one_time_legal_expense':     +200_000,   # non-recurring
    'covid_impact':               +300_000,   # normalization
    'stock_based_compensation':   +150_000,   # add back
    'run_rate_new_contracts':     +400_000,   # annualize new wins
    'cost_savings_identified':    +250_000,   # identified not yet realized
}
```

---

## Value Creation Playbook
```python
def value_creation_framework():
    return {
        'Revenue Growth': {
            'Organic': [
                'Hire and train sales team — expand coverage',
                'Launch new products or services',
                'Enter new geographies',
                'Expand into adjacent markets',
                'Improve pricing strategy and realization'
            ],
            'Inorganic': [
                'Add-on acquisitions in same market',
                'Consolidation play — buy competitors',
                'Tuck-in acquisitions for new capabilities',
                'Geographic expansion via acquisition'
            ]
        },
        'Margin Improvement': [
            'Procurement optimization — volume discounts',
            'Operational efficiency — lean/six sigma',
            'Shared services center for back office',
            'Technology investment — automate manual processes',
            'Real estate optimization — consolidate facilities',
            'Headcount rationalization where appropriate'
        ],
        'Multiple Expansion': [
            'Grow to next size tier (small cap to mid-market)',
            'Improve revenue quality (transactional to recurring)',
            'Reduce customer concentration',
            'Strengthen management team credibility',
            'ESG improvements for premium buyer universe',
            'Technology enablement of traditional business'
        ],
        'Financial Engineering': [
            'Optimize capital structure — refinance at lower rates',
            'Sale-leaseback of owned real estate',
            'Working capital improvement — DSO/DIO reduction',
            'Tax structure optimization',
            'Dividend recapitalization when appropriate'
        ]
    }

def 100_day_plan_template():
    return {
        'Days 1-30 — Stabilize': [
            'Meet entire management team individually',
            'Understand cash position and near-term liquidity',
            'Identify critical relationships (top customers, suppliers)',
            'Assess management team gaps',
            'Install financial reporting cadence',
            'Establish board governance structure'
        ],
        'Days 31-60 — Assess': [
            'Deep dive on key business unit performance',
            'Benchmark operations vs industry peers',
            'Identify top 3-5 value creation levers',
            'Evaluate management team — who to keep, hire, replace',
            'Assess acquisition pipeline',
            'Develop detailed 3-year operating plan'
        ],
        'Days 61-100 — Execute': [
            'Implement quick win initiatives',
            'Kick off long-term value creation projects',
            'Align management incentives (equity rollover, options)',
            'Execute first add-on acquisition if identified',
            'Install KPI dashboard and reporting',
            'Brief LP advisory board on strategy'
        ]
    }
```

---

## Exit Strategies
```python
def exit_strategy_analysis(company_profile, market_conditions):
    """
    Evaluate exit options and expected proceeds.
    """
    ebitda          = company_profile['current_ebitda']
    revenue         = company_profile['current_revenue']
    growth_rate     = company_profile['revenue_growth']
    recurring_rev   = company_profile['recurring_pct']

    exit_options    = {}

    # Strategic Sale
    strategic_mult  = market_conditions['strategic_ev_ebitda']
    strategic_premium = 1.20  # strategic buyers pay 20%+ premium
    exit_options['Strategic Sale'] = {
        'ev':           round(ebitda * strategic_mult * strategic_premium, 0),
        'timeline':     '6-12 months',
        'probability':  'High if company is strategic asset',
        'pros':         ['Highest valuation', 'Clean exit', 'Synergy premium'],
        'cons':         ['Loss of independence', 'Employee uncertainty']
    }

    # Secondary Buyout
    sbo_mult        = market_conditions['financial_ev_ebitda']
    exit_options['Secondary Buyout'] = {
        'ev':           round(ebitda * sbo_mult, 0),
        'timeline':     '3-6 months',
        'probability':  'High — always a market for quality businesses',
        'pros':         ['Faster process', 'PE buyer understands business'],
        'cons':         ['Lower valuation than strategic', 'Another hold period']
    }

    # IPO
    if revenue > 100_000_000 and growth_rate > 0.15:
        ipo_mult    = market_conditions['public_ev_revenue'] * revenue
        exit_options['IPO'] = {
            'ev':       round(ipo_mult * 0.90, 0),  # IPO discount
            'timeline': '12-18 months',
            'probability': 'Depends on market conditions',
            'pros':     ['Potentially highest value', 'Liquidity event',
                        'Currency for M&A'],
            'cons':     ['Long process', 'Market risk', 'Partial exit only',
                        'Lock-up period', 'Public company costs']
        }

    # Dividend Recapitalization
    exit_options['Dividend Recap'] = {
        'distribution': round(ebitda * 2.0, 0),  # pull out 2x EBITDA
        'timeline':     '2-3 months',
        'pros':         ['Partial liquidity without full exit',
                        'Retain upside on remaining stake'],
        'cons':         ['Increases leverage', 'Limits future flexibility']
    }

    return exit_options
```

---

## Fund Structure & Economics
```python
def fund_economics():
    return {
        'Fund Structure': {
            'GP':           'General Partner — manages fund, makes investments',
            'LP':           'Limited Partners — investors (pension, endowment, family office)',
            'Fund Life':    '10 years typical (5yr investment + 5yr harvest)',
            'Extensions':   '1-2 year extensions possible with LP consent',
            'GP Commit':    '1-3% of fund (skin in the game)',
            'Vintage Year': 'Year fund makes first investment'
        },
        'Fee Structure': {
            'Management Fee': '1.5-2% of committed capital (investment period)',
            'Post-Invest':    '1-1.5% of invested/NAV after investment period',
            'Carried Interest':'20% of profits above hurdle rate',
            'Hurdle Rate':    '8% preferred return to LPs before carry',
            'Catch-up':       'GP catches up to 20% of total profits after hurdle',
            'Clawback':       'GP must return carry if fund underperforms'
        },
        'Waterfall': {
            'European':     'Return all capital + hurdle then carry (LP friendly)',
            'American':     'Carry deal-by-deal after returning each deal cost',
            'Hybrid':       'Combination of both approaches'
        }
    }

def waterfall_calculation(fund_size, total_distributions,
                           mgmt_fees_paid, hurdle_rate=0.08,
                           carry_rate=0.20):
    """
    European waterfall calculation.
    1. Return capital to LPs
    2. Return management fees to LPs
    3. Pay preferred return (hurdle)
    4. GP catch-up to 20% of profits
    5. Split remaining 80/20
    """
    lp_capital      = fund_size * 0.98   # 98% from LPs
    gp_capital      = fund_size * 0.02   # 2% GP commit

    # Step 1: Return capital
    remaining       = total_distributions
    lp_capital_return = min(remaining, lp_capital)
    remaining      -= lp_capital_return
    gp_capital_return = min(remaining, gp_capital)
    remaining      -= gp_capital_return

    # Step 2: Return fees
    fee_return      = min(remaining, mgmt_fees_paid)
    remaining      -= fee_return

    # Step 3: Preferred return
    hold_years      = 7
    preferred       = lp_capital * ((1+hurdle_rate)**hold_years - 1)
    pref_paid       = min(remaining, preferred)
    remaining      -= pref_paid

    # Step 4: GP catch-up (GP gets 20% of total profit)
    total_profit    = total_distributions - fund_size
    gp_target_carry = total_profit * carry_rate
    gp_catchup      = min(remaining, gp_target_carry)
    remaining      -= gp_catchup

    # Step 5: 80/20 split on remainder
    lp_final        = remaining * (1 - carry_rate)
    gp_final        = remaining * carry_rate

    total_lp        = (lp_capital_return + fee_return +
                       pref_paid + lp_final)
    total_gp        = (gp_capital_return + gp_catchup + gp_final)
    total_carry     = gp_catchup + gp_final

    return {
        'total_distributions': round(total_distributions, 0),
        'lp_proceeds':         round(total_lp, 0),
        'gp_proceeds':         round(total_gp, 0),
        'carried_interest':    round(total_carry, 0),
        'lp_moic':             round(total_lp / lp_capital, 2),
        'gp_moic':             round(total_gp / gp_capital, 2),
        'carry_pct_of_profit': round(total_carry/max(1,total_distributions-fund_size)*100, 1)
    }
```

---

## Venture Capital
```python
def venture_capital_framework():
    return {
        'Stage Definitions': {
            'Pre-Seed':   '$500K-$2M — idea stage, founding team',
            'Seed':       '$2M-$5M — MVP, early customers',
            'Series A':   '$5M-$20M — product-market fit, scaling',
            'Series B':   '$20M-$50M — growth, expand team and market',
            'Series C+':  '$50M+ — scale, international, pre-IPO'
        },
        'Key Metrics by Stage': {
            'Seed':   ['Team quality', 'Market size', 'Early traction'],
            'Series A':['MoM growth', 'Unit economics', 'Retention'],
            'Series B':['Revenue growth', 'NRR', 'Sales efficiency'],
            'Series C':['Path to profitability', 'Market leadership', 'IPO readiness']
        },
        'VC Economics': {
            'Power Law':     'Top 10% of investments return 90% of fund returns',
            'Loss Rate':     '50-60% of investments return <1x',
            'Target':        'Need 1-2 investments to return entire fund (fund returners)',
            'Follow-on':     'Reserve 50% of fund for follow-on in winners'
        }
    }

def cap_table_dilution(founding_equity, funding_rounds):
    """
    Model dilution through multiple funding rounds.
    """
    cap_table = {'Founders': founding_equity}
    total_shares = sum(founding_equity.values())

    for round_name, round_data in funding_rounds.items():
        new_shares = (total_shares * round_data['ownership_pct'] /
                     (1 - round_data['ownership_pct']))
        total_shares += new_shares

        # Dilute existing shareholders
        dilution = 1 - round_data['ownership_pct']
        cap_table = {k: v * dilution for k, v in cap_table.items()}
        cap_table[round_name] = round_data['ownership_pct'] * 100

    return {
        'cap_table':        {k: round(v, 2) for k, v in cap_table.items()},
        'total_ownership':  round(sum(cap_table.values()), 1)
    }

def term_sheet_key_terms():
    return {
        'Valuation': {
            'Pre-money':   'Company value before investment',
            'Post-money':  'Pre-money + new investment',
            'Price/share': 'Post-money valuation / fully diluted shares'
        },
        'Preferences': {
            '1x non-participating': 'Get money back OR convert to common (LP friendly)',
            '1x participating':     'Get money back AND share in upside (investor friendly)',
            'Cumulative dividend':  'Accrues annually, paid at exit'
        },
        'Control': {
            'Board seats':      'Investor gets 1-2 board seats typically',
            'Protective provisions': 'Veto rights on major decisions',
            'Information rights':    'Monthly/quarterly financials required'
        },
        'Anti-Dilution': {
            'Broad-based WA':   'Most common, moderate protection',
            'Narrow-based WA':  'More investor-friendly',
            'Full ratchet':     'Very investor-friendly, rare, toxic'
        },
        'Founder Friendly': [
            'Founder vesting acceleration on change of control',
            'Right of first refusal on founder share sales',
            'Co-sale rights',
            'No-shop period (30-60 days typical)'
        ]
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Overpaying on entry | Too high multiple kills returns | Discipline on entry — walk away at price |
| Too much leverage | Covenant breach, bankruptcy | Conservative debt sizing, headroom |
| Management dependency | CEO leaves post-close | Depth of team in diligence, retention packages |
| Customer concentration | Top customer leaves, crisis | Require diversification pre-close or price it in |
| Overoptimistic projections | Miss plan in year 1 | Use independent model, stress test |
| No add-on pipeline | Multiple compression on exit | Build M&A pipeline pre-close |
| Liquidity mismatch | Fund needs exit, market closed | Stagger exits, build in extension provisions |

---

## Best Practices

- **Entry multiple discipline** — overpaying is the #1 cause of poor returns
- **Management matters most** — back exceptional operators
- **Value creation plan before close** — know exactly how you make money
- **100-day plan ready day one** — no time to waste post-close
- **Board governance** — monthly reporting, quarterly board meetings minimum
- **Build exit optionality** — prepare for strategic, SBO, and IPO simultaneously
- **Reserve capital** — always hold dry powder for follow-on and add-ons

---

## Related Skills

- **financial-modeling-expert**: LBO and three-statement models
- **hedge-fund-strategies-expert**: Alternative investment context
- **fundamental-analysis-expert**: Business quality assessment
- **risk-management-expert**: Portfolio risk in PE context
- **macro-economics-expert**: Market timing for exits
