---
name: real-estate-investing-expert
description: Expert-level real estate investing knowledge. Use when working with property valuation, rental yield, cap rates, cash-on-cash returns, REITs, mortgage financing, property analysis, real estate development, or portfolio building. Also use when the user mentions 'cap rate', 'NOI', 'cash flow', 'rental yield', 'LTV', 'DSCR', 'REITs', 'cash-on-cash', 'appreciation', 'house hacking', 'BRRRR', 'commercial real estate', or 'property management'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Real Estate Investing Expert

You are a world-class real estate investor and analyst with deep expertise in residential and commercial property analysis, valuation, financing, portfolio construction, REITs, development, and building long-term wealth through real estate.

## Before Starting

1. **Property type** — Residential, multifamily, commercial, industrial, or REITs?
2. **Strategy** — Buy and hold, fix and flip, BRRRR, development, or REITs?
3. **Goal** — Cash flow, appreciation, tax benefits, or diversification?
4. **Market** — Local market, national, or international?
5. **Capital** — Available equity, financing capacity, and target returns?

---

## Core Expertise Areas

- **Property Valuation**: income approach, sales comparison, cost approach
- **Cash Flow Analysis**: NOI, cap rate, cash-on-cash, IRR
- **Financing**: mortgages, LTV, DSCR, creative financing
- **Residential Investing**: single family, multifamily, house hacking
- **Commercial Real Estate**: office, retail, industrial, multifamily
- **REITs**: structure, valuation, FFO, sectors
- **Development**: pro forma, construction, entitlement
- **Tax Benefits**: depreciation, 1031 exchange, cost segregation

---

## Core Metrics
```python
def property_analysis(income_data, expense_data, purchase_data):
    """
    Complete property investment analysis.
    """
    # ── INCOME ────────────────────────────────────────────────
    gross_rents         = income_data['monthly_rent'] * 12
    vacancy_loss        = gross_rents * income_data['vacancy_rate']
    other_income        = income_data.get('other_income', 0)
    effective_gross_income = gross_rents - vacancy_loss + other_income

    # ── EXPENSES ──────────────────────────────────────────────
    property_tax        = expense_data['property_tax']
    insurance           = expense_data['insurance']
    maintenance         = expense_data.get('maintenance',
                           gross_rents * 0.05)
    property_mgmt       = effective_gross_income * expense_data.get(
                           'mgmt_fee_pct', 0.08)
    capex_reserve       = gross_rents * expense_data.get('capex_pct', 0.05)
    utilities           = expense_data.get('utilities', 0)
    hoa                 = expense_data.get('hoa', 0)

    total_expenses      = (property_tax + insurance + maintenance +
                           property_mgmt + capex_reserve +
                           utilities + hoa)

    # ── NOI & CAP RATE ────────────────────────────────────────
    noi                 = effective_gross_income - total_expenses
    purchase_price      = purchase_data['purchase_price']
    cap_rate            = noi / purchase_price

    # ── CASH FLOW ─────────────────────────────────────────────
    down_payment        = purchase_price * purchase_data['down_payment_pct']
    loan_amount         = purchase_price - down_payment
    closing_costs       = purchase_price * purchase_data.get(
                           'closing_cost_pct', 0.03)
    total_cash_in       = down_payment + closing_costs + \
                          purchase_data.get('repairs', 0)

    # Monthly mortgage payment
    monthly_rate        = purchase_data['interest_rate'] / 12
    n_payments          = purchase_data['loan_term_years'] * 12
    monthly_mortgage    = loan_amount * (
        monthly_rate * (1+monthly_rate)**n_payments /
        ((1+monthly_rate)**n_payments - 1)
    )
    annual_debt_service = monthly_mortgage * 12
    annual_cash_flow    = noi - annual_debt_service

    # ── RETURNS ───────────────────────────────────────────────
    cash_on_cash        = annual_cash_flow / total_cash_in
    grm                 = purchase_price / gross_rents  # gross rent multiplier
    dscr                = noi / annual_debt_service
    ltv                 = loan_amount / purchase_price

    return {
        'income': {
            'gross_rents':     round(gross_rents, 0),
            'vacancy_loss':    round(vacancy_loss, 0),
            'egi':             round(effective_gross_income, 0)
        },
        'expenses': {
            'total_expenses':  round(total_expenses, 0),
            'expense_ratio':   round(total_expenses/effective_gross_income*100, 1)
        },
        'noi':                 round(noi, 0),
        'financing': {
            'loan_amount':     round(loan_amount, 0),
            'monthly_payment': round(monthly_mortgage, 0),
            'annual_ds':       round(annual_debt_service, 0)
        },
        'returns': {
            'cap_rate':        round(cap_rate * 100, 2),
            'cash_on_cash':    round(cash_on_cash * 100, 2),
            'grm':             round(grm, 2),
            'dscr':            round(dscr, 2),
            'ltv':             round(ltv * 100, 1),
            'total_cash_in':   round(total_cash_in, 0),
            'annual_cf':       round(annual_cash_flow, 0),
            'monthly_cf':      round(annual_cash_flow/12, 0)
        },
        'verdict': {
            'cap_rate_check':  'Good' if cap_rate > 0.06 else 'Low',
            'dscr_check':      'Safe' if dscr > 1.25 else 'Tight',
            'coc_check':       'Good' if cash_on_cash > 0.08 else 'Low'
        }
    }

def cap_rate_benchmarks():
    return {
        'Single Family':      '4-6% (appreciation markets), 6-10% (cash flow markets)',
        'Small Multifamily':  '5-7%',
        'Large Multifamily':  '4-6% (class A), 6-9% (class C)',
        'Retail':             '5-7% (grocery anchored), 7-10% (unanchored)',
        'Office':             '5-8% (CBD), 7-10% (suburban)',
        'Industrial':         '4-6% (logistics), 5-8% (flex)',
        'Self Storage':       '5-7%',
        'Hotel':              '7-10%',
        'interpretation': {
            'Low cap rate':   'Low risk, high demand market — less cash flow',
            'High cap rate':  'Higher risk or lower demand — more cash flow',
            'compression':    'Cap rates fall = values rise (like bond prices)'
        }
    }
```

---

## Property Valuation Methods
```python
def income_approach_valuation(noi, market_cap_rate):
    """
    Income Approach: Value = NOI / Cap Rate
    Most common for income-producing properties.
    """
    value = noi / market_cap_rate
    return {
        'noi':            round(noi, 0),
        'market_cap_rate':f"{market_cap_rate*100:.2f}%",
        'estimated_value': round(value, 0),
        'note':           '10bps cap rate change = ~1.5-2% value change'
    }

def sales_comparison_approach(subject_property, comps):
    """
    Sales comparison: adjust comp sales for differences.
    Most common for residential.
    """
    adjusted_prices = []
    for comp in comps:
        adj_price = comp['sale_price']

        # Adjust for differences
        sqft_diff = subject_property['sqft'] - comp['sqft']
        adj_price += sqft_diff * comp.get('price_per_sqft', 150)

        bed_diff   = subject_property['beds'] - comp['beds']
        adj_price += bed_diff * 5000

        bath_diff  = subject_property['baths'] - comp['baths']
        adj_price += bath_diff * 3000

        if subject_property.get('garage') and not comp.get('garage'):
            adj_price += 15000
        if subject_property.get('pool') and not comp.get('pool'):
            adj_price += 20000

        adjusted_prices.append(adj_price)

    indicated_value = sum(adjusted_prices) / len(adjusted_prices)
    return {
        'comp_values':      [round(p, 0) for p in adjusted_prices],
        'indicated_value':  round(indicated_value, 0),
        'value_range':      (round(min(adjusted_prices), 0),
                             round(max(adjusted_prices), 0))
    }

def gross_rent_multiplier(purchase_price, monthly_rent):
    """
    GRM = Price / Annual Rent
    Quick filter — lower GRM = better deal.
    Typical: 8-12x for residential.
    """
    annual_rent = monthly_rent * 12
    grm = purchase_price / annual_rent
    return {
        'grm':          round(grm, 2),
        'benchmark':    'Good' if grm < 10 else 'Average' if grm < 14 else 'High',
        'implied_price_per_rent': round(purchase_price / monthly_rent, 0)
    }
```

---

## Investment Strategies
```python
def brrrr_analysis(purchase_price, rehab_cost, arv,
                    rental_income, expenses, refi_ltv=0.75,
                    refi_rate=0.07, refi_term=30):
    """
    BRRRR Strategy: Buy, Rehab, Rent, Refinance, Repeat
    Goal: Pull out most/all of initial capital after refinance.
    """
    # Initial investment
    total_invested     = purchase_price + rehab_cost
    initial_equity     = total_invested  # assume all cash purchase

    # After rehab value
    forced_appreciation = arv - purchase_price
    equity_created      = arv - total_invested

    # Refinance
    refi_loan_amount    = arv * refi_ltv
    cash_out            = refi_loan_amount - total_invested
    remaining_equity    = arv - refi_loan_amount

    # Monthly mortgage on refi
    monthly_rate        = refi_rate / 12
    n_payments          = refi_term * 12
    monthly_mortgage    = refi_loan_amount * (
        monthly_rate * (1+monthly_rate)**n_payments /
        ((1+monthly_rate)**n_payments - 1)
    )

    # Cash flow after refi
    noi                 = rental_income * 12 - expenses
    annual_ds           = monthly_mortgage * 12
    annual_cf           = noi - annual_ds
    cash_left_in        = max(0, total_invested - refi_loan_amount)

    # Returns
    coc = annual_cf / cash_left_in if cash_left_in > 0 else float('inf')

    return {
        'buy_and_rehab': {
            'purchase':         purchase_price,
            'rehab':            rehab_cost,
            'total_invested':   total_invested
        },
        'after_rehab': {
            'arv':              arv,
            'equity_created':   round(equity_created, 0),
            'forced_appreciation': round(forced_appreciation, 0)
        },
        'refinance': {
            'loan_amount':      round(refi_loan_amount, 0),
            'cash_out':         round(cash_out, 0),
            'monthly_payment':  round(monthly_mortgage, 0),
            'cash_left_in':     round(cash_left_in, 0)
        },
        'returns': {
            'annual_cash_flow': round(annual_cf, 0),
            'cash_on_cash':     round(coc * 100, 2) if cash_left_in > 0 else 'Infinite',
            'equity_remaining': round(remaining_equity, 0),
            'strategy_verdict': 'Excellent' if cash_out > 0 else
                               'Good'      if cash_left_in < total_invested * 0.20 else
                               'Marginal'
        }
    }

def house_hacking_analysis(purchase_price, units, rent_per_unit,
                             owner_unit_market_rent, down_payment_pct=0.035):
    """
    House hacking: live in one unit, rent out others.
    Use FHA (3.5%) or conventional with owner-occupied financing.
    """
    down_payment        = purchase_price * down_payment_pct
    loan_amount         = purchase_price - down_payment
    monthly_rate        = 0.07 / 12
    n_payments          = 360
    monthly_mortgage    = loan_amount * (
        monthly_rate * (1+monthly_rate)**n_payments /
        ((1+monthly_rate)**n_payments - 1)
    )

    rental_units        = units - 1  # owner occupies one
    monthly_rent        = rental_units * rent_per_unit
    effective_housing_cost = monthly_mortgage - monthly_rent

    return {
        'purchase_price':         purchase_price,
        'down_payment':           round(down_payment, 0),
        'monthly_mortgage':       round(monthly_mortgage, 0),
        'rental_income':          round(monthly_rent, 0),
        'effective_housing_cost': round(effective_housing_cost, 0),
        'market_rent_savings':    round(owner_unit_market_rent -
                                        effective_housing_cost, 0),
        'verdict':                'Excellent' if effective_housing_cost < 500 else
                                  'Good'      if effective_housing_cost < 1000 else
                                  'Marginal'
    }

def fix_and_flip_analysis(purchase_price, rehab_cost, arv,
                           hold_months=6, financing_rate=0.12):
    """
    Fix and flip profit analysis.
    """
    # Costs
    purchase_costs      = purchase_price * 0.02  # closing costs
    financing_cost      = (purchase_price + rehab_cost) * \
                          financing_rate * (hold_months/12)
    holding_costs       = purchase_price * 0.01 * (hold_months/12)  # taxes, insurance
    selling_costs       = arv * 0.06  # agent commission + closing

    total_costs         = (purchase_price + rehab_cost + purchase_costs +
                           financing_cost + holding_costs + selling_costs)
    gross_profit        = arv - total_costs
    roi                 = gross_profit / (purchase_price + rehab_cost)
    annualized_roi      = roi * (12 / hold_months)

    mao = arv * 0.70 - rehab_cost  # Maximum Allowable Offer (70% rule)

    return {
        'arv':              arv,
        'total_costs':      round(total_costs, 0),
        'gross_profit':     round(gross_profit, 0),
        'roi':              round(roi * 100, 2),
        'annualized_roi':   round(annualized_roi * 100, 2),
        'mao_70_rule':      round(mao, 0),
        'paid_vs_mao':      'Good' if purchase_price <= mao else 'Overpaid',
        'cost_breakdown': {
            'purchase':     purchase_price,
            'rehab':        rehab_cost,
            'financing':    round(financing_cost, 0),
            'holding':      round(holding_costs, 0),
            'selling':      round(selling_costs, 0)
        }
    }
```

---

## Commercial Real Estate
```python
def commercial_re_analysis(property_type, noi, purchase_price,
                             loan_amount, interest_rate, loan_term):
    """
    Commercial RE underwriting.
    """
    cap_rate            = noi / purchase_price
    loan_constant       = (interest_rate / 12 * (1 + interest_rate/12)**
                           (loan_term*12)) / ((1+interest_rate/12)**
                           (loan_term*12) - 1) * 12
    annual_ds           = loan_amount * loan_constant
    dscr                = noi / annual_ds
    cash_flow           = noi - annual_ds
    equity_invested     = purchase_price - loan_amount
    coc                 = cash_flow / equity_invested
    ltv                 = loan_amount / purchase_price

    return {
        'cap_rate':         round(cap_rate * 100, 2),
        'dscr':             round(dscr, 2),
        'ltv':              round(ltv * 100, 1),
        'cash_on_cash':     round(coc * 100, 2),
        'annual_noi':       round(noi, 0),
        'annual_ds':        round(annual_ds, 0),
        'annual_cf':        round(cash_flow, 0),
        'lender_criteria': {
            'dscr_min':     '1.20-1.25x typical minimum',
            'ltv_max':      '65-75% typical for commercial',
            'dscr_status':  'Lendable' if dscr >= 1.20 else 'Below threshold'
        }
    }

def commercial_property_types():
    return {
        'Multifamily': {
            'cap_rates':    '4-6% class A, 6-9% class C',
            'drivers':      'Employment, population growth, housing supply',
            'metrics':      'Rent per unit, occupancy, rent growth',
            'financing':    'Agency (Fannie/Freddie) for 5+ units',
            'pro':          'Recession resistant — people always need housing'
        },
        'Industrial': {
            'cap_rates':    '4-6% logistics, 5-8% flex',
            'drivers':      'E-commerce growth, supply chain reshoring',
            'metrics':      'Clear height, dock doors, truck court depth',
            'financing':    'CMBS, life insurance, bank',
            'pro':          'Fastest growing CRE sector, low maintenance'
        },
        'Retail': {
            'cap_rates':    '5-7% grocery anchored, 7-10%+ unanchored',
            'drivers':      'Consumer spending, e-commerce threat',
            'metrics':      'Sales per sq ft, occupancy cost ratio',
            'financing':    'CMBS, bank, depends on credit of tenants',
            'risk':         'E-commerce disruption, anchor tenant risk'
        },
        'Office': {
            'cap_rates':    '5-8% CBD, 7-10% suburban',
            'drivers':      'Employment, remote work trends',
            'metrics':      'Occupancy, WALT (weighted avg lease term)',
            'financing':    'CMBS, bank',
            'risk':         'WFH secular headwind, high TI/LC costs'
        },
        'Self Storage': {
            'cap_rates':    '5-7%',
            'drivers':      'Life events — moves, divorce, downsizing',
            'metrics':      'Physical and economic occupancy, ECRI',
            'pro':          'Low maintenance, recession resistant'
        }
    }
```

---

## REITs
```python
def reit_valuation(reit_data):
    """
    REIT-specific valuation metrics.
    """
    # FFO = Net Income + D&A - Gains on Property Sales
    ffo     = (reit_data['net_income'] +
               reit_data['depreciation'] -
               reit_data['gains_on_sales'])

    # AFFO = FFO - Recurring Capex - Straight Line Rent
    affo    = ffo - reit_data['recurring_capex'] - \
              reit_data.get('straight_line_rent', 0)

    shares  = reit_data['shares_outstanding']
    price   = reit_data['share_price']
    mkt_cap = price * shares

    ffo_per_share   = ffo / shares
    affo_per_share  = affo / shares
    price_to_ffo    = price / ffo_per_share
    price_to_affo   = price / affo_per_share
    dividend_yield  = reit_data['annual_dividend'] / price
    payout_ratio    = reit_data['annual_dividend'] / affo_per_share

    # NAV approach
    nav             = reit_data['noi'] / reit_data['market_cap_rate']
    nav_per_share   = (nav - reit_data['total_debt'] +
                       reit_data['cash']) / shares
    premium_to_nav  = (price - nav_per_share) / nav_per_share

    return {
        'ffo_per_share':    round(ffo_per_share, 2),
        'affo_per_share':   round(affo_per_share, 2),
        'price_to_ffo':     round(price_to_ffo, 2),
        'price_to_affo':    round(price_to_affo, 2),
        'dividend_yield':   round(dividend_yield * 100, 2),
        'payout_ratio':     round(payout_ratio * 100, 1),
        'nav_per_share':    round(nav_per_share, 2),
        'premium_to_nav':   round(premium_to_nav * 100, 1),
        'valuation':        'Cheap'     if premium_to_nav < -0.10 else
                            'Fair'      if premium_to_nav < 0.10 else
                            'Expensive'
    }

def reit_sectors():
    return {
        'Data Centers':     'EQIX, DLR — AI/cloud demand driver',
        'Industrial':       'PLD, REXR — e-commerce logistics',
        'Residential':      'EQR, AVB, MAA — apartment REITs',
        'Self Storage':     'PSA, EXR, CUBE',
        'Healthcare':       'WELL, VTR — senior housing, medical office',
        'Net Lease':        'O, NNN — single tenant, long leases',
        'Office':           'BXP, SLG — headwind from WFH',
        'Retail Mall':      'SPG, MAC — challenged by e-commerce',
        'Hotel':            'HST, PK — cyclical, COVID risk',
        'Mortgage REITs':   'AGNC, NLY — interest rate sensitive'
    }
```

---

## Tax Benefits
```python
def tax_benefits_analysis(property_value, land_value_pct=0.20,
                           annual_income=50_000, tax_rate=0.37,
                           hold_years=5):
    """
    Real estate tax benefits analysis.
    """
    building_value      = property_value * (1 - land_value_pct)
    annual_depreciation = building_value / 27.5  # residential
    tax_shield          = annual_depreciation * tax_rate
    total_depreciation  = annual_depreciation * hold_years

    return {
        'annual_depreciation':  round(annual_depreciation, 0),
        'annual_tax_shield':    round(tax_shield, 0),
        'total_tax_savings':    round(tax_shield * hold_years, 0),
        'effective_yield_boost': round(tax_shield / property_value * 100, 2),
        'note':                 'Depreciation recaptured at 25% on sale — plan accordingly'
    }

def exchange_1031_analysis(sale_price, adjusted_basis, new_property_price,
                             capital_gains_rate=0.20, depreciation_recapture=0.25):
    """
    1031 Exchange: defer capital gains by reinvesting in like-kind property.
    """
    gain                = sale_price - adjusted_basis
    depreciation_taken  = adjusted_basis * 0.30  # approximate
    recapture_tax       = depreciation_taken * depreciation_recapture
    capital_gains_tax   = (gain - depreciation_taken) * capital_gains_rate
    total_tax_without   = recapture_tax + capital_gains_tax

    # With 1031 — defer all taxes
    additional_buying_power = total_tax_without

    return {
        'sale_price':           sale_price,
        'adjusted_basis':       adjusted_basis,
        'total_gain':           round(gain, 0),
        'tax_without_1031':     round(total_tax_without, 0),
        'tax_with_1031':        0,
        'tax_deferral':         round(total_tax_without, 0),
        'buying_power_preserved':round(sale_price, 0),
        'buying_power_without': round(sale_price - total_tax_without, 0),
        'rules': [
            '45 days to identify replacement property',
            '180 days to close on replacement',
            'Must be like-kind property',
            'Must use qualified intermediary',
            'New property must be >= sale price'
        ]
    }
```

---

## Market Analysis
```python
def market_analysis_framework():
    return {
        'Macro Indicators': [
            'Population growth rate (>1% = strong)',
            'Job growth and employment diversity',
            'Median household income trends',
            'Net migration (in vs out)',
            'GDP growth of metro area'
        ],
        'Supply Indicators': [
            'Building permits (high = oversupply risk)',
            'Vacancy rates by property type',
            'Months of housing supply',
            'Construction costs vs rents',
            'Zoning regulations (supply restrictions)'
        ],
        'Demand Indicators': [
            'Rent growth rates (YoY)',
            'Absorption rate of new units',
            'Home price appreciation',
            'Rental vs ownership cost comparison',
            'Employer announcements'
        ],
        'Best Markets to Watch': {
            'Sunbelt':      'High migration, job growth, relatively affordable',
            'Secondary':    'Less competition, higher cap rates, emerging growth',
            'Avoid':        'High vacancy, population outflow, single employer towns'
        }
    }

def rent_vs_buy_comparison(rent, purchase_price, down_payment_pct=0.20,
                             mortgage_rate=0.07, appreciation=0.03,
                             hold_years=7):
    """
    Rent vs buy financial comparison.
    """
    # Buying costs
    down_payment        = purchase_price * down_payment_pct
    loan                = purchase_price - down_payment
    monthly_rate        = mortgage_rate / 12
    n                   = 30 * 12
    monthly_mortgage    = loan * (monthly_rate*(1+monthly_rate)**n /
                                   ((1+monthly_rate)**n-1))
    property_tax        = purchase_price * 0.012 / 12
    insurance           = purchase_price * 0.005 / 12
    maintenance         = purchase_price * 0.01 / 12
    monthly_own_cost    = monthly_mortgage + property_tax + insurance + maintenance

    # Renting costs
    monthly_rent_cost   = rent

    # Net worth after hold_years
    future_value        = purchase_price * (1+appreciation)**hold_years
    remaining_loan      = loan * ((1+monthly_rate)**(n) - (1+monthly_rate)**(hold_years*12)) / \
                          ((1+monthly_rate)**n - 1)
    home_equity         = future_value - remaining_loan - down_payment
    rent_savings        = (monthly_own_cost - monthly_rent_cost) * 12 * hold_years
    investment_return   = rent_savings * (1.07**hold_years)  # if invested

    return {
        'monthly_own_cost':     round(monthly_own_cost, 0),
        'monthly_rent':         round(monthly_rent_cost, 0),
        'monthly_difference':   round(monthly_own_cost - monthly_rent_cost, 0),
        'home_equity_built':    round(home_equity, 0),
        'break_even_years':     round(down_payment / (monthly_own_cost - rent) / 12, 1)
                                if monthly_own_cost > rent else 'Immediate',
        'verdict':              'Buy' if home_equity > investment_return else 'Rent'
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Underestimating expenses | Negative cash flow surprises | Use 50% rule as quick check |
| Ignoring vacancy | Assume 100% occupancy | Always model 5-8% vacancy minimum |
| Over-leveraging | Rate rise or vacancy kills cash flow | DSCR > 1.25, stress test rates |
| Skipping due diligence | Hidden repairs, legal issues | Always inspect, title search, environmental |
| Emotional buying | Overpay for nice property | Numbers must work — never fall in love |
| Ignoring market cycles | Buy at peak, forced to sell at bottom | Study local market supply/demand |
| Self-managing too many | Time cost kills returns | Hire property management at scale |

---

## Best Practices

- **Cash flow first** — appreciation is a bonus, not a plan
- **50% rule quick filter** — expenses typically 50% of gross rent
- **DSCR above 1.25** — leave room for vacancies and rate increases
- **Location drives appreciation** — jobs, schools, infrastructure
- **Screen tenants thoroughly** — evictions cost $3,000-$10,000+
- **Build reserves** — 3-6 months expenses in liquid reserve
- **Scale systematically** — master one market before expanding

---

## Related Skills

- **finance-trading-expert**: REIT trading and analysis
- **financial-modeling-expert**: Real estate pro forma models
- **risk-management-expert**: Portfolio risk and leverage
- **macro-economics-expert**: Interest rate impact on real estate
- **portfolio-management-expert**: Real estate in overall portfolio
