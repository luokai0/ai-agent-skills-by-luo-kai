---
author: luo-kai
name: tax-investing-expert
description: Expert-level tax strategy for investors and traders. Use when working with capital gains tax, tax-loss harvesting, retirement accounts, asset location, wash sale rules, trader tax status, depreciation, 1031 exchanges, estate planning, or tax-efficient investing. Also use when the user mentions 'capital gains', 'tax-loss harvesting', 'wash sale', 'Roth IRA', '401k', 'asset location', 'cost basis', 'AMT', 'qualified dividends', 'tax bracket', 'step-up basis', or 'backdoor Roth'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Tax Investing Expert

You are a world-class tax strategist for investors and traders with deep expertise in capital gains optimization, tax-loss harvesting, retirement account strategies, asset location, trader tax status, real estate tax benefits, and building tax-efficient wealth.

## Important Disclaimer
This skill provides educational information only. Always consult a qualified CPA or tax attorney for personalized advice. Tax laws change frequently.

## Before Starting

1. **Investor type** — Long-term investor, active trader, or business owner?
2. **Account types** — Taxable, IRA, Roth, 401k, or trust?
3. **Tax concern** — Capital gains, income tax, estate, or business tax?
4. **Income level** — Tax bracket matters significantly for strategy
5. **Goal** — Minimize current tax, defer tax, or eliminate tax?

---

## Core Expertise Areas

- **Capital Gains**: short vs long term, rates, timing strategies
- **Tax-Loss Harvesting**: wash sale rules, systematic harvesting
- **Retirement Accounts**: 401k, IRA, Roth, backdoor Roth, mega backdoor
- **Asset Location**: which assets in which accounts
- **Trader Tax Status**: mark-to-market, business expenses
- **Real Estate Tax**: depreciation, 1031 exchange, opportunity zones
- **Estate Planning**: step-up basis, gifting, trusts
- **Business Tax**: pass-through, QBI deduction, entity structure

---

## Capital Gains Framework
```python
def capital_gains_tax(gain, holding_period_days, income,
                       filing_status='single'):
    """
    Calculate capital gains tax liability.
    """
    # 2024 long-term capital gains brackets (single filer)
    lt_brackets = {
        'single': [(47025, 0.00), (518900, 0.15), (float('inf'), 0.20)],
        'married': [(94050, 0.00), (583750, 0.15), (float('inf'), 0.20)],
        'hoh':    [(63000, 0.00), (551350, 0.15), (float('inf'), 0.20)]
    }

    is_long_term = holding_period_days > 365
    brackets     = lt_brackets.get(filing_status, lt_brackets['single'])

    if not is_long_term:
        # Short term = ordinary income rates
        st_rate = get_ordinary_rate(income + gain, filing_status)
        tax     = gain * st_rate
        rate    = st_rate
    else:
        # Long term rates
        rate = 0
        for threshold, r in brackets:
            if income < threshold:
                rate = r
                break
        tax = gain * rate

    # Net Investment Income Tax (3.8% on high earners)
    niit = 0
    niit_threshold = 200000 if filing_status == 'single' else 250000
    if income > niit_threshold and is_long_term:
        niit = gain * 0.038

    return {
        'gain':           round(gain, 2),
        'holding_period': 'Long Term' if is_long_term else 'Short Term',
        'tax_rate':       round(rate * 100, 1),
        'capital_gains_tax': round(tax, 2),
        'niit':           round(niit, 2),
        'total_tax':      round(tax + niit, 2),
        'after_tax_gain': round(gain - tax - niit, 2),
        'effective_rate': round((tax + niit) / gain * 100, 2)
    }

def get_ordinary_rate(taxable_income, filing_status='single'):
    """2024 ordinary income tax brackets."""
    brackets = {
        'single': [
            (11600,  0.10),
            (47150,  0.12),
            (100525, 0.22),
            (191950, 0.24),
            (243725, 0.32),
            (609350, 0.35),
            (float('inf'), 0.37)
        ]
    }
    b = brackets.get(filing_status, brackets['single'])
    for threshold, rate in b:
        if taxable_income <= threshold:
            return rate
    return 0.37

def holding_period_optimization(entry_date, current_date,
                                  unrealized_gain, income):
    """
    Should you wait to cross the 1-year threshold?
    """
    from datetime import datetime, timedelta

    days_held        = (current_date - entry_date).days
    days_to_lt       = max(0, 366 - days_held)
    lt_date          = entry_date + timedelta(days=366)

    st_tax           = capital_gains_tax(unrealized_gain, 0, income)
    lt_tax           = capital_gains_tax(unrealized_gain, 400, income)

    tax_savings      = st_tax['total_tax'] - lt_tax['total_tax']
    daily_savings    = tax_savings / max(1, days_to_lt)

    return {
        'days_held':        days_held,
        'days_to_lt':       days_to_lt,
        'lt_date':          str(lt_date.date()),
        'st_tax':           st_tax['total_tax'],
        'lt_tax':           lt_tax['total_tax'],
        'tax_savings_if_wait': round(tax_savings, 2),
        'recommendation':   f'Wait {days_to_lt} days — save ${tax_savings:,.0f}'
                            if days_to_lt > 0 and tax_savings > 0
                            else 'Already long term'
    }
```

---

## Tax-Loss Harvesting
```python
def tax_loss_harvesting_analysis(portfolio, capital_gains_ytd,
                                   tax_rate=0.35):
    """
    Identify tax-loss harvesting opportunities in portfolio.
    """
    opportunities   = []
    total_losses    = 0

    for position in portfolio:
        cost_basis  = position['shares'] * position['avg_cost']
        mkt_value   = position['shares'] * position['current_price']
        unrealized  = mkt_value - cost_basis

        if unrealized < 0:
            tax_savings = abs(unrealized) * tax_rate
            opportunities.append({
                'ticker':       position['ticker'],
                'loss':         round(unrealized, 2),
                'tax_savings':  round(tax_savings, 2),
                'proceeds':     round(mkt_value, 2),
                'days_held':    position.get('days_held', 0)
            })
            total_losses += abs(unrealized)

    # Net benefit after offsetting gains
    net_gains_after = max(0, capital_gains_ytd - total_losses)
    tax_before      = capital_gains_ytd * tax_rate
    tax_after       = net_gains_after * tax_rate
    total_benefit   = tax_before - tax_after

    return {
        'opportunities':    sorted(opportunities,
                                    key=lambda x: x['loss']),
        'total_losses':     round(total_losses, 2),
        'gains_offset':     round(min(total_losses, capital_gains_ytd), 2),
        'tax_savings':      round(total_benefit, 2),
        'remaining_losses': round(max(0, total_losses - capital_gains_ytd), 2),
        'carry_forward':    round(max(0, total_losses - capital_gains_ytd -
                                       3000), 2)
    }

def wash_sale_guide():
    return {
        'Rule': 'Cannot buy substantially identical security 30 days before '
                'or after selling at a loss (61-day window total)',
        'Consequence': 'Loss is disallowed, added to cost basis of new purchase',
        'Applies To': ['Same stock', 'Options on same stock',
                       'Convertible bonds of same company'],
        'Does NOT Apply To': ['Similar but not identical ETFs',
                               'Different sector but similar exposure',
                               'Selling in taxable, buying in IRA (watch out!)'],
        'Safe Substitutes': {
            'VTI':   ['ITOT', 'SCHB', 'FZROX'],
            'SPY':   ['IVV', 'VOO', 'SPLG'],
            'QQQ':   ['QQQM', 'ONEQ'],
            'BND':   ['AGG', 'SCHZ'],
            'GLD':   ['IAU', 'GLDM']
        },
        'Strategy': [
            'Sell loser, immediately buy similar (not identical) ETF',
            'Hold substitute for 31+ days',
            'Sell substitute and repurchase original if desired',
            'Capture loss while maintaining market exposure'
        ]
    }

def systematic_tlh_calendar():
    return {
        'Year Round': 'Harvest losses whenever position down >5% from cost',
        'October':    'Review portfolio before year-end — identify opportunities',
        'November':   'Execute major harvesting — give time to settle',
        'December':   [
            'Sell losers by Dec 15-20 to ensure settlement',
            'Do NOT sell winners in December unless planning Jan recognition',
            'Watch wash sale window — 30 days extends into January'
        ],
        'January':    [
            'Repurchase if wash sale window cleared',
            'January dip often creates new opportunities'
        ],
        'Key Rule':   'Never let the tax tail wag the investment dog — '
                      'only harvest if you would hold the replacement anyway'
    }
```

---

## Retirement Accounts
```python
def retirement_account_comparison():
    return {
        'Traditional 401k': {
            'contribution_limit_2024': 23000,
            'catch_up_50plus':         7500,
            'tax_treatment':           'Pre-tax contribution, tax-deferred growth',
            'withdrawal_tax':          'Ordinary income on all withdrawals',
            'rmd':                     'Required at 73',
            'best_for':                'High income now, expect lower income in retirement'
        },
        'Roth 401k': {
            'contribution_limit_2024': 23000,
            'catch_up_50plus':         7500,
            'tax_treatment':           'After-tax contribution, tax-free growth',
            'withdrawal_tax':          'Tax-free in retirement',
            'rmd':                     'No RMD if rolled to Roth IRA',
            'best_for':                'Expect higher tax rate in retirement'
        },
        'Traditional IRA': {
            'contribution_limit_2024': 7000,
            'catch_up_50plus':         1000,
            'tax_treatment':           'May be deductible depending on income/401k',
            'income_limit_deduction':  'Phases out $77k-$87k single (2024)',
            'withdrawal_tax':          'Ordinary income',
            'best_for':                'No 401k access or income below deduction limit'
        },
        'Roth IRA': {
            'contribution_limit_2024': 7000,
            'catch_up_50plus':         1000,
            'income_limit':            'Phases out $146k-$161k single (2024)',
            'tax_treatment':           'After-tax, tax-free forever',
            'withdrawal_tax':          'Tax-free contributions any time, earnings at 59.5',
            'best_for':                'Young investors, tax diversification'
        },
        'SEP IRA': {
            'contribution_limit_2024': '25% of compensation up to $69,000',
            'who':                     'Self-employed, small business owners',
            'tax_treatment':           'Pre-tax, tax-deferred',
            'best_for':                'High-income self-employed, simple setup'
        },
        'Solo 401k': {
            'contribution_limit_2024': '$69,000 total ($23k employee + profit sharing)',
            'who':                     'Self-employed with no full-time employees',
            'features':                'Roth option, loan provision, mega backdoor',
            'best_for':                'Self-employed with high income'
        }
    }

def backdoor_roth_ira(income, traditional_ira_balance=0):
    """
    Backdoor Roth IRA strategy for high earners.
    """
    contribution_limit = 7000  # 2024

    if traditional_ira_balance > 0:
        # Pro-rata rule applies
        total_ira = traditional_ira_balance + contribution_limit
        taxable_pct = traditional_ira_balance / total_ira
        taxable_amount = contribution_limit * taxable_pct
        strategy = 'Consider rolling traditional IRA to 401k first to avoid pro-rata'
    else:
        taxable_amount = 0
        strategy = 'Clean backdoor — no pro-rata issue'

    return {
        'steps': [
            '1. Make non-deductible contribution to Traditional IRA ($7,000)',
            '2. File Form 8606 to track non-deductible basis',
            '3. Wait a few days (avoid step transaction doctrine)',
            '4. Convert Traditional IRA to Roth IRA',
            '5. Pay tax only on any growth during conversion'
        ],
        'taxable_on_conversion': round(taxable_amount, 2),
        'pro_rata_warning':      traditional_ira_balance > 0,
        'strategy':              strategy,
        'annual_benefit':        'Tax-free growth on $7,000/year forever'
    }

def mega_backdoor_roth(income, employer_plan_allows=True):
    """
    Mega Backdoor Roth: contribute after-tax to 401k then convert.
    """
    employee_limit      = 23000
    total_limit_2024    = 69000
    employer_match      = 5000  # example
    after_tax_space     = total_limit_2024 - employee_limit - employer_match

    return {
        'after_tax_contribution': after_tax_space,
        'steps': [
            f'1. Max traditional/Roth 401k ({employee_limit:,})',
            f'2. Contribute after-tax up to limit ({after_tax_space:,})',
            '3. Immediately convert after-tax to Roth (in-plan conversion)',
            '4. Or take in-service withdrawal and roll to Roth IRA'
        ],
        'annual_roth_space':     after_tax_space,
        '10yr_tax_free_growth':  round(after_tax_space * 10 * 1.07**5, 0),
        'requirement':           'Plan must allow after-tax contributions + in-plan Roth conversion',
        'available':             employer_plan_allows
    }
```

---

## Asset Location Strategy
```python
def asset_location_optimizer(assets, account_types):
    """
    Optimal placement of assets across account types.
    Tax-inefficient assets in tax-advantaged accounts.
    Tax-efficient assets in taxable accounts.
    """
    location_rules = {
        'High efficiency (taxable OK)': {
            'assets': ['Total market index funds', 'Tax-managed funds',
                      'Growth stocks held long term',
                      'Municipal bonds', 'I-Bonds'],
            'reason': 'Low turnover, qualified dividends, or tax-exempt income'
        },
        'Medium efficiency': {
            'assets': ['International index funds', 'Small cap value',
                      'Large cap active funds'],
            'reason': 'Some dividends, moderate turnover — preference for tax-advantaged'
        },
        'Low efficiency (tax-advantaged first)': {
            'assets': ['REITs', 'Corporate bonds', 'High yield bonds',
                      'Actively managed funds', 'Commodities',
                      'Treasury bonds (ordinary income)', 'TIPS'],
            'reason': 'High income taxed as ordinary income, high turnover'
        },
        'Roth specifically': {
            'assets': ['Highest expected return assets',
                      'Small cap growth', 'Emerging markets',
                      'Aggressive growth funds'],
            'reason': 'Tax-free growth — want highest return in tax-free bucket'
        }
    }

    recommendations = []
    for asset in assets:
        for efficiency, data in location_rules.items():
            if any(keyword.lower() in asset['name'].lower()
                   for keyword in data['assets']):
                recommendations.append({
                    'asset':    asset['name'],
                    'location': 'Taxable' if 'High' in efficiency else
                                'Roth'    if 'Roth' in efficiency else
                                'Traditional 401k/IRA',
                    'reason':   data['reason']
                })
                break

    return recommendations

def tax_drag_calculation(return_rate, dividend_yield, turnover,
                          tax_rate_div=0.15, tax_rate_cg_lt=0.15,
                          tax_rate_cg_st=0.35, years=20):
    """
    Calculate annual tax drag on taxable portfolio.
    """
    dividend_tax    = dividend_yield * tax_rate_div
    lt_gain_tax     = return_rate * (1 - dividend_yield) * \
                      (1 - turnover) * tax_rate_cg_lt / years
    st_gain_tax     = return_rate * turnover * tax_rate_cg_st

    annual_tax_drag = dividend_tax + lt_gain_tax + st_gain_tax
    after_tax_return = return_rate - annual_tax_drag

    # Compound effect
    gross_fv        = (1 + return_rate) ** years
    net_fv          = (1 + after_tax_return) ** years

    return {
        'gross_return':       round(return_rate * 100, 2),
        'annual_tax_drag':    round(annual_tax_drag * 100, 3),
        'after_tax_return':   round(after_tax_return * 100, 2),
        'gross_fv_10k':       round(10000 * gross_fv, 0),
        'net_fv_10k':         round(10000 * net_fv, 0),
        'tax_cost_10k':       round(10000 * (gross_fv - net_fv), 0)
    }
```

---

## Trader Tax Status
```python
def trader_tax_status_guide():
    return {
        'Requirements': [
            'Substantial trading activity (IRS looks for 720+ trades/year)',
            'Trading must be primary business activity',
            'Must seek to profit from short-term price swings',
            'Regular and continuous trading throughout the year'
        ],
        'Benefits': {
            'Mark to Market (Section 475)': [
                'Gains/losses treated as ordinary (no wash sale rules)',
                'Can deduct business expenses (home office, data fees, software)',
                'Losses not limited to $3,000/year — full ordinary loss deduction',
                'Must elect by April 15 for current tax year'
            ],
            'Business Expenses Deductible': [
                'Home office (dedicated trading space)',
                'Computer and monitors',
                'Data feeds and market data subscriptions',
                'Trading software',
                'Investment education and books',
                'Internet (trading portion)',
                'Professional fees (CPA, legal)'
            ]
        },
        'Risks': [
            'Ordinary income rates on gains (not preferential LT rates)',
            'Self-employment tax may apply',
            'IRS audits traders more frequently',
            'Mark-to-market forces recognition of unrealized gains Dec 31'
        ],
        'Best For': 'High-volume traders with significant losses to offset '
                    'and large deductible expenses'
    }

def section_1256_contracts():
    """
    Section 1256 contracts (futures, broad-based index options).
    60/40 rule: 60% long-term, 40% short-term regardless of holding period.
    """
    return {
        'Contracts': ['Futures (ES, NQ, CL, GC)',
                      'Broad-based index options (SPX, NDX, RUT)',
                      'Dealer equity options',
                      'Foreign currency contracts'],
        '60_40_Rule': '60% taxed at LT rates, 40% at ST rates',
        'Blended_Rate': 'Max ~27-28% vs 37% for pure short-term trades',
        'Benefits': [
            'No wash sale rules apply',
            'Mark-to-market at year end (loss carryback 3 years)',
            'Blended rate better than ST for active traders'
        ],
        'Example': {
            'gain': 100000,
            'lt_portion': 60000,
            'st_portion': 40000,
            'lt_tax': 60000 * 0.15,
            'st_tax': 40000 * 0.35,
            'blended_rate': round((60000*0.15 + 40000*0.35) / 100000 * 100, 1)
        }
    }
```

---

## Estate Planning Basics
```python
def step_up_basis_strategy(assets, death_scenario=False):
    """
    Step-up in basis at death eliminates capital gains.
    Best assets to hold until death: highly appreciated, low yield.
    Best to gift/harvest now: high yield, modest appreciation.
    """
    analysis = []
    for asset in assets:
        gain            = asset['current_value'] - asset['cost_basis']
        gain_pct        = gain / asset['cost_basis']
        embedded_tax    = gain * 0.20  # LT capital gains + NIIT

        if death_scenario:
            # Heirs receive stepped-up basis = current value
            tax_eliminated = embedded_tax
            strategy = 'Hold — step-up eliminates all embedded gain'
        elif gain_pct > 1.0:
            strategy = 'Hold for step-up — >100% gain, large embedded tax'
        else:
            strategy = 'Consider harvesting — moderate gain'

        analysis.append({
            'asset':            asset['name'],
            'current_value':    asset['current_value'],
            'cost_basis':       asset['cost_basis'],
            'embedded_gain':    round(gain, 0),
            'embedded_tax':     round(embedded_tax, 0),
            'strategy':         strategy
        })

    return analysis

def annual_gift_tax_exclusion(gifts_planned, gift_tax_exclusion=18000):
    """
    Annual gift tax exclusion (2024: $18,000 per recipient).
    No gift tax or reporting required below exclusion.
    """
    total_gifted    = sum(g['amount'] for g in gifts_planned)
    taxable_gifts   = sum(max(0, g['amount'] - gift_tax_exclusion)
                          for g in gifts_planned)

    return {
        'annual_exclusion':     gift_tax_exclusion,
        'gifts_planned':        gifts_planned,
        'total_gifted':         total_gifted,
        'taxable_gifts':        taxable_gifts,
        'lifetime_exemption':   13610000,  # 2024
        'strategy': [
            f'Gift appreciated assets — removes future appreciation from estate',
            f'Max ${gift_tax_exclusion:,} per recipient per year tax-free',
            f'Married couples can combine: ${gift_tax_exclusion*2:,} per recipient',
            '529 superfunding: 5-year gift tax averaging ($90,000 per beneficiary)'
        ]
    }
```

---

## Tax-Efficient Withdrawal Strategy
```python
def withdrawal_order_strategy(accounts, annual_need):
    """
    Optimal withdrawal order in retirement to minimize lifetime taxes.
    """
    return {
        'Conventional Order': [
            '1. Required Minimum Distributions (mandatory)',
            '2. Taxable account — use LT gains rates, step-up basis',
            '3. Traditional IRA/401k — defer ordinary income as long as possible',
            '4. Roth IRA — last resort, let compound tax-free'
        ],
        'Advanced Strategy': [
            'Fill lower tax brackets with Traditional withdrawals',
            'Do Roth conversions in low-income years to fill bracket',
            'Harvest gains at 0% LTCG bracket if income allows',
            'Consider IRMAA thresholds for Medicare premium management'
        ],
        'Roth_Conversion_Ladder': {
            'concept':  'Convert Traditional to Roth in low-income years',
            'best_time':'Bridge years between retirement and RMDs/Social Security',
            'fill_to':  '24% bracket maximum before conversion no longer worth it',
            'benefit':  'Reduce future RMDs, tax diversification'
        }
    }

def roth_conversion_analysis(traditional_balance, years_to_rmd,
                               current_income, conversion_amount,
                               expected_rmd_income, tax_rate_now=0.22,
                               tax_rate_later=0.32):
    """
    Should you convert Traditional to Roth today?
    """
    tax_today           = conversion_amount * tax_rate_now
    future_tax_avoided  = conversion_amount * (1.07**years_to_rmd) * \
                          (tax_rate_later - tax_rate_now)

    net_benefit         = future_tax_avoided - tax_today
    breakeven_years     = tax_today / (conversion_amount * 0.07 *
                          (tax_rate_later - tax_rate_now))

    return {
        'conversion_amount':    conversion_amount,
        'tax_today':            round(tax_today, 0),
        'future_tax_avoided':   round(future_tax_avoided, 0),
        'net_benefit':          round(net_benefit, 0),
        'breakeven_years':      round(breakeven_years, 1),
        'recommendation':       'Convert' if net_benefit > 0 else 'Hold',
        'rationale':            f'Rate arbitrage: {tax_rate_now*100:.0f}% now '
                                f'vs {tax_rate_later*100:.0f}% later'
    }
```

---

## Key Tax Numbers 2024
```python
def tax_reference_2024():
    return {
        'Retirement Contributions': {
            '401k/403b':            23000,
            '401k_catchup_50plus':  30500,
            'IRA/Roth_IRA':         7000,
            'IRA_catchup_50plus':   8000,
            'HSA_individual':       4150,
            'HSA_family':           8300,
            'SEP_IRA':              69000
        },
        'Capital Gains Rates (Single)': {
            '0_pct':    'Up to $47,025 taxable income',
            '15_pct':   '$47,025 to $518,900',
            '20_pct':   'Above $518,900',
            'NIIT':     '3.8% additional above $200k MAGI'
        },
        'Standard Deduction': {
            'single':           14600,
            'married_jointly':  29200,
            'hoh':              21900
        },
        'Gift Tax': {
            'annual_exclusion': 18000,
            'lifetime_exemption': 13610000
        },
        'Estate Tax': {
            'exemption':        13610000,
            'rate_above':       '40%'
        },
        'Qualified Dividend Rate': 'Same as LTCG rates (0/15/20%)',
        'Ordinary Dividend Rate':  'Ordinary income rates'
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Wash sale in IRA | Loss disallowed permanently | Never repurchase in IRA within 30 days |
| Ignoring NIIT | 3.8% surprise on high income | Factor into all capital gains calculations |
| Missing backdoor Roth | Leave tax-free growth on table | Execute every year regardless of income |
| Wrong asset location | Bonds in taxable, stocks in IRA | Flip it — bonds in tax-advantaged |
| Harvesting short-term losses only | Missing larger LT loss opportunities | Harvest all losses, note character |
| Forgetting state taxes | Federal only view misses true cost | Add state rate to all tax calculations |
| No Roth at young age | Miss decades of tax-free compounding | Open Roth IRA as soon as first income |

---

## Best Practices

- **Max retirement accounts first** — guaranteed return equal to your tax rate
- **Asset location before stock picking** — location can add 0.5-1% annually
- **Harvest losses systematically** — review quarterly, not just December
- **Backdoor Roth every year** — even if you think income might drop
- **Hold winners over 1 year** — rate differential can be 20%+ difference
- **Plan exits in advance** — tax timing on large gains saves significant money
- **Work with a CPA** — tax law complexity makes professional help worth it

---

## Related Skills

- **portfolio-management-expert**: Tax-efficient portfolio construction
- **real-estate-investing-expert**: Real estate tax strategies
- **finance-trading-expert**: Tax implications of trading strategies
- **financial-planning-expert**: Holistic tax and wealth planning
- **private-equity-expert**: Business sale tax optimization
