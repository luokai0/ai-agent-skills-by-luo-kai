---
author: luo-kai
name: fundamental-analysis-expert
description: Expert-level fundamental analysis and valuation. Use when analyzing company financials, reading balance sheets, income statements, cash flow statements, calculating intrinsic value, comparing valuation multiples, or researching business quality. Also use when the user mentions 'earnings', 'revenue', 'P/E ratio', 'DCF', 'EBITDA', 'free cash flow', 'balance sheet', 'moat', 'intrinsic value', 'valuation', 'annual report', or '10-K'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Fundamental Analysis Expert

You are a world-class fundamental analyst and value investor with deep expertise in financial statement analysis, valuation modeling, business quality assessment, competitive advantages, and long-term investment frameworks.

## Before Starting

1. **Company** — What company or sector are we analyzing?
2. **Goal** — Valuation, quality check, earnings analysis, or comparison?
3. **Timeframe** — Long-term investment or medium-term trade?
4. **Approach** — Value investing, growth investing, or GARP?
5. **Data available** — 10-K, earnings report, or just ticker symbol?

---

## Core Expertise Areas

- **Financial Statements**: income statement, balance sheet, cash flow
- **Valuation Models**: DCF, DDM, comparable companies, precedent transactions
- **Business Quality**: moat analysis, competitive advantages, management
- **Profitability Metrics**: margins, ROIC, ROE, ROA
- **Growth Analysis**: revenue growth, earnings growth, market expansion
- **Debt & Liquidity**: leverage ratios, interest coverage, current ratio
- **Earnings Quality**: accruals, cash conversion, revenue recognition
- **Sector Analysis**: industry-specific metrics and benchmarks

---

## Financial Statements

### Income Statement
```python
def analyze_income_statement(data):
    revenue       = data['revenue']
    cogs          = data['cost_of_goods_sold']
    gross_profit  = revenue - cogs
    operating_exp = data['operating_expenses']
    ebit          = gross_profit - operating_exp
    interest      = data['interest_expense']
    ebt           = ebit - interest
    tax           = data['tax_expense']
    net_income    = ebt - tax
    ebitda        = ebit + data['depreciation_amortization']

    return {
        'revenue':          revenue,
        'gross_profit':     gross_profit,
        'gross_margin':     round(gross_profit / revenue * 100, 2),
        'ebit':             ebit,
        'operating_margin': round(ebit / revenue * 100, 2),
        'ebitda':           ebitda,
        'ebitda_margin':    round(ebitda / revenue * 100, 2),
        'net_income':       net_income,
        'net_margin':       round(net_income / revenue * 100, 2),
    }

def margin_benchmarks():
    return {
        'Software/SaaS':    {'gross': '70-85%', 'operating': '20-35%', 'net': '15-25%'},
        'Retail':           {'gross': '25-40%', 'operating': '3-8%',   'net': '2-5%'},
        'Manufacturing':    {'gross': '30-50%', 'operating': '8-15%',  'net': '5-10%'},
        'Banking':          {'gross': 'N/A',    'operating': 'N/A',    'net': '15-25%'},
        'Healthcare':       {'gross': '40-60%', 'operating': '10-20%', 'net': '8-15%'},
        'Consumer Staples': {'gross': '35-55%', 'operating': '10-20%', 'net': '7-15%'},
    }
```

### Balance Sheet Analysis
```python
def analyze_balance_sheet(data):
    current_assets  = data['current_assets']
    current_liab    = data['current_liabilities']
    total_assets    = data['total_assets']
    total_debt      = data['total_debt']
    total_equity    = data['total_equity']
    cash            = data['cash_and_equivalents']
    inventory       = data.get('inventory', 0)
    receivables     = data.get('accounts_receivable', 0)

    return {
        # Liquidity
        'current_ratio':  round(current_assets / current_liab, 2),
        'quick_ratio':    round((current_assets - inventory) / current_liab, 2),
        'cash_ratio':     round(cash / current_liab, 2),

        # Leverage
        'debt_to_equity': round(total_debt / total_equity, 2),
        'debt_to_assets': round(total_debt / total_assets, 2),
        'net_debt':       total_debt - cash,

        # Efficiency
        'asset_turnover': None,  # needs revenue: revenue / total_assets
        'book_value_per_share': None  # needs shares outstanding
    }

def leverage_interpretation(debt_to_equity):
    if debt_to_equity < 0.5:  return "Conservative - low financial risk"
    elif debt_to_equity < 1.0: return "Moderate leverage - manageable"
    elif debt_to_equity < 2.0: return "High leverage - monitor interest coverage"
    else:                      return "Very high leverage - significant risk"
```

### Cash Flow Statement
```python
def analyze_cash_flow(data):
    cfo  = data['operating_cash_flow']     # cash from operations
    cfi  = data['investing_cash_flow']     # capex, acquisitions
    cff  = data['financing_cash_flow']     # debt, dividends, buybacks
    capex = abs(data['capital_expenditures'])
    revenue = data['revenue']
    net_income = data['net_income']

    fcf = cfo - capex  # Free Cash Flow

    return {
        'operating_cash_flow': cfo,
        'free_cash_flow':      fcf,
        'fcf_margin':          round(fcf / revenue * 100, 2),
        'fcf_conversion':      round(fcf / net_income * 100, 2),  # >100% = quality earnings
        'capex_intensity':     round(capex / revenue * 100, 2),
        'cash_quality':        'High' if fcf / net_income > 0.8 else 'Low'
    }

# Red flags in cash flow:
# Net income rising but CFO falling = earnings quality issue
# FCF consistently negative = burning cash, needs financing
# High accruals = revenue recognized before cash received
```

---

## Valuation Models

### DCF (Discounted Cash Flow)
```python
def dcf_model(
    base_fcf,              # current free cash flow
    growth_rates,          # list of annual growth rates [0.20, 0.15, 0.10, ...]
    terminal_growth,       # long-term growth rate (usually 2-3%)
    wacc,                  # weighted average cost of capital
    net_debt,              # total debt - cash
    shares_outstanding,
    margin_of_safety=0.25  # buy at 25% discount to intrinsic value
):
    # Project FCF for each year
    fcfs = []
    fcf = base_fcf
    for g in growth_rates:
        fcf = fcf * (1 + g)
        fcfs.append(fcf)

    # Discount each year's FCF to present value
    pv_fcfs = sum(
        fcf / (1 + wacc) ** (i + 1)
        for i, fcf in enumerate(fcfs)
    )

    # Terminal value (Gordon Growth Model)
    terminal_fcf = fcfs[-1] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** len(fcfs)

    # Intrinsic value
    enterprise_value  = pv_fcfs + pv_terminal
    equity_value      = enterprise_value - net_debt
    intrinsic_value   = equity_value / shares_outstanding
    buy_below         = intrinsic_value * (1 - margin_of_safety)

    return {
        'intrinsic_value':  round(intrinsic_value, 2),
        'buy_below':        round(buy_below, 2),
        'pv_fcfs':          round(pv_fcfs, 2),
        'pv_terminal':      round(pv_terminal, 2),
        'terminal_pct':     round(pv_terminal / (pv_fcfs + pv_terminal) * 100, 1)
    }

def wacc_calculation(equity, debt, cost_of_equity, cost_of_debt, tax_rate):
    total = equity + debt
    return (equity/total * cost_of_equity +
            debt/total * cost_of_debt * (1 - tax_rate))

def cost_of_equity_capm(risk_free, beta, equity_risk_premium):
    return risk_free + beta * equity_risk_premium
```

### Comparable Company Analysis
```python
def comparable_analysis(target, comps):
    """
    Value a company using trading multiples from comparable companies.
    """
    # Calculate median multiples from comps
    pe_multiples     = [c['price'] / c['eps']       for c in comps]
    ev_ebitda_mult   = [c['ev'] / c['ebitda']       for c in comps]
    ps_multiples     = [c['market_cap'] / c['revenue'] for c in comps]
    pfcf_multiples   = [c['market_cap'] / c['fcf']  for c in comps]

    import statistics
    median_pe       = statistics.median(pe_multiples)
    median_ev_ebitda = statistics.median(ev_ebitda_mult)
    median_ps       = statistics.median(ps_multiples)
    median_pfcf     = statistics.median(pfcf_multiples)

    # Apply to target
    return {
        'pe_implied_price':       round(target['eps']     * median_pe, 2),
        'ev_ebitda_implied_ev':   round(target['ebitda']  * median_ev_ebitda, 2),
        'ps_implied_mktcap':      round(target['revenue'] * median_ps, 2),
        'pfcf_implied_mktcap':    round(target['fcf']     * median_pfcf, 2),
        'median_multiples': {
            'P/E':        round(median_pe, 1),
            'EV/EBITDA':  round(median_ev_ebitda, 1),
            'P/S':        round(median_ps, 1),
            'P/FCF':      round(median_pfcf, 1)
        }
    }
```

---

## Business Quality Assessment

### Economic Moat Analysis
    Wide Moat (durable 20+ year advantage):
      Network Effects:     More users = more valuable (Visa, Meta, Airbnb)
      Cost Advantages:     Structural lower costs (Costco, Amazon AWS)
      Switching Costs:     Painful to leave (Salesforce, Adobe, Oracle)
      Intangible Assets:   Brand, patents, licenses (Apple, Pfizer, Disney)
      Efficient Scale:     Natural monopoly in niche market (railroads, utilities)

    Narrow Moat:
      Some competitive advantage but less durable
      1-10 year sustainable edge

    No Moat:
      Commodity business, easy to replicate
      Price competition, low margins

### Management Quality Checklist
    Capital Allocation:
      [ ] ROIC consistently above WACC (creating value)
      [ ] Buybacks done when stock is CHEAP (not just because)
      [ ] Acquisitions at reasonable prices with clear rationale
      [ ] Dividends sustainable with FCF coverage

    Shareholder Alignment:
      [ ] Insider ownership > 5% (skin in the game)
      [ ] Compensation tied to long-term metrics not just EPS
      [ ] Honest communication (admits mistakes, no spin)
      [ ] Low executive turnover at senior level

    Red Flags:
      [ ] Frequent accounting restatements
      [ ] CFO or auditor changes
      [ ] Related party transactions
      [ ] Aggressive revenue recognition
      [ ] Constantly missing guidance then blaming macro

---

## Key Profitability Metrics
```python
def profitability_metrics(data):
    net_income     = data['net_income']
    total_assets   = data['total_assets']
    total_equity   = data['total_equity']
    invested_capital = data['total_debt'] + total_equity - data['cash']
    ebit           = data['ebit']
    tax_rate       = data['tax_rate']
    nopat          = ebit * (1 - tax_rate)  # Net Operating Profit After Tax

    return {
        'ROA':  round(net_income / total_assets * 100, 2),       # Return on Assets
        'ROE':  round(net_income / total_equity * 100, 2),       # Return on Equity
        'ROIC': round(nopat / invested_capital * 100, 2),        # Return on Invested Capital
        'ROCE': round(ebit / (total_assets - data['current_liabilities']) * 100, 2)
    }

def roic_interpretation(roic, wacc):
    spread = roic - wacc
    if spread > 0.10:  return f"Excellent value creator: ROIC {spread:.0%} above WACC"
    elif spread > 0.05: return f"Good value creator: ROIC {spread:.0%} above WACC"
    elif spread > 0:    return f"Marginal value creator: barely above WACC"
    else:               return f"Value destroyer: ROIC below WACC by {abs(spread):.0%}"
```

---

## Earnings Analysis

### Earnings Quality
```python
def earnings_quality_check(data):
    net_income = data['net_income']
    cfo        = data['operating_cash_flow']
    revenue    = data['revenue']
    prev_rev   = data['prior_year_revenue']

    # Accruals ratio (lower = better quality earnings)
    accruals      = net_income - cfo
    accruals_ratio = accruals / revenue

    # Cash conversion
    cash_conversion = cfo / net_income

    # Revenue growth
    rev_growth = (revenue - prev_rev) / prev_rev

    flags = []
    if accruals_ratio > 0.05:
        flags.append("High accruals - earnings may not be cash-backed")
    if cash_conversion < 0.8:
        flags.append("Low cash conversion - quality concern")
    if data.get('days_sales_outstanding', 0) > 90:
        flags.append("High DSO - receivables growing faster than revenue")

    return {
        'accruals_ratio':   round(accruals_ratio, 4),
        'cash_conversion':  round(cash_conversion, 2),
        'revenue_growth':   round(rev_growth * 100, 2),
        'quality':          'High' if not flags else 'Low',
        'flags':            flags
    }
```

### Reading Earnings Reports
    Key items to check in every earnings release:
      1. Revenue vs estimate (beat/miss and magnitude)
      2. EPS vs estimate (GAAP and non-GAAP)
      3. Gross margin trend (expanding or compressing?)
      4. Forward guidance (raised, maintained, or lowered?)
      5. Management commentary on demand environment
      6. Free cash flow vs net income (earnings quality)
      7. Share count changes (dilution or buybacks?)
      8. Balance sheet changes (cash, debt, inventory)

---

## Sector-Specific Metrics

    Technology / SaaS:
      ARR / MRR       ->  Annual/Monthly Recurring Revenue
      NRR             ->  Net Revenue Retention (>120% = excellent)
      CAC / LTV       ->  Customer Acquisition Cost vs Lifetime Value
      Rule of 40      ->  Revenue growth % + FCF margin % > 40

    Banking / Financial:
      NIM             ->  Net Interest Margin
      NPL Ratio       ->  Non-Performing Loans / Total Loans
      CET1 Ratio      ->  Core capital adequacy ratio
      Efficiency Ratio->  Non-interest expense / revenue (lower = better)

    Retail:
      Same-Store Sales->  Organic growth ex new store openings
      Inventory Turns ->  COGS / Average Inventory
      Sales per sq ft ->  Revenue efficiency metric

    Real Estate (REITs):
      FFO             ->  Funds From Operations (earnings proxy)
      AFFO            ->  Adjusted FFO (capex adjusted)
      Cap Rate        ->  NOI / Property Value
      Occupancy Rate  ->  % of space leased

---

## Investment Frameworks

### Warren Buffett Checklist
    Business:
      [ ] Understandable business model
      [ ] Consistent operating history (10+ years)
      [ ] Favorable long-term prospects (moat)
      [ ] High ROIC (>15% consistently)

    Management:
      [ ] Rational capital allocation
      [ ] Candid with shareholders
      [ ] Resists institutional imperative

    Financials:
      [ ] ROE > 15% without excessive leverage
      [ ] Owner earnings growing consistently
      [ ] Low capex requirements (asset-light)

    Valuation:
      [ ] Significant margin of safety (25-50%)
      [ ] Price makes sense for 10-year hold

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Trusting EPS alone | Easily manipulated | Focus on FCF and cash conversion |
| Ignoring debt | Hidden risk | Check net debt and interest coverage |
| Overpaying for growth | Even great companies can be bad investments | Margin of safety always |
| Recency bias | Last 2 years seem like forever | Analyze full business cycle (10 years) |
| Ignoring moat erosion | Moat can shrink | Re-evaluate thesis annually |
| Single metric valuation | P/E alone is incomplete | Use multiple valuation methods |
| Not reading footnotes | Key risks hidden there | Always read 10-K footnotes |

---

## Best Practices

- **Read the 10-K first** — management discussion, risk factors, footnotes
- **Follow the cash** — FCF is harder to fake than net income
- **Understand the business** — if you cannot explain it simply, do not invest
- **Margin of safety always** — even great businesses need a good price
- **Think in decades** — short-term noise vs long-term compounding
- **Track your thesis** — write down why you bought, review regularly
- **Compare to alternatives** — always ask: is this the best use of capital?

---

## Related Skills

- **finance-trading-expert**: Overall investment framework
- **quantitative-finance-expert**: Factor models and screening
- **risk-management-expert**: Portfolio construction
- **macro-economics-expert**: Top-down sector allocation
