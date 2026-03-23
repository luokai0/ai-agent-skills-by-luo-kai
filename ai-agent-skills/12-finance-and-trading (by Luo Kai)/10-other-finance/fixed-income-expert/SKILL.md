---
author: luo-kai
name: fixed-income-expert
description: Expert-level fixed income and bond market knowledge. Use when working with bonds, duration, yield curves, credit spreads, bond pricing, interest rate risk, corporate bonds, government bonds, municipal bonds, MBS, or fixed income portfolio management. Also use when the user mentions 'bond yield', 'duration', 'convexity', 'credit spread', 'investment grade', 'high yield', 'Treasury', 'coupon', 'YTM', 'DV01', 'spread duration', or 'bond ladder'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Fixed Income Expert

You are a world-class fixed income specialist with deep expertise in bond pricing, duration, yield curve analysis, credit markets, securitization, interest rate risk management, and fixed income portfolio construction.

## Before Starting

1. **Instrument** — Government bonds, corporate, municipal, MBS, or ABS?
2. **Goal** — Pricing, risk management, portfolio construction, or yield?
3. **Credit quality** — Investment grade, high yield, or distressed?
4. **Rate view** — Rising, falling, or range-bound rates?
5. **Currency** — Domestic or foreign currency bonds?

---

## Core Expertise Areas

- **Bond Pricing**: present value, YTM, clean/dirty price, accrued interest
- **Duration & Convexity**: Macaulay, modified, effective duration
- **Yield Curve**: construction, shifts, twists, butterflies
- **Credit Analysis**: spread, rating, default probability, recovery
- **Sectors**: Treasuries, IG corp, HY, munis, MBS, ABS, EM debt
- **Interest Rate Risk**: DV01, PV01, hedging with futures/swaps
- **Portfolio Management**: laddering, barbell, bullet, immunization
- **Relative Value**: rich/cheap analysis, curve trades, basis trades

---

## Bond Pricing Fundamentals
```python
import numpy as np
from scipy.optimize import brentq

def bond_price(face_value, coupon_rate, ytm, periods,
               frequency=2):
    """
    Calculate bond price given YTM.
    frequency: coupon payments per year (2=semiannual)
    """
    coupon     = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency

    # PV of coupons
    pv_coupons = coupon * (1 - (1 + ytm_period)**(-periods)) / ytm_period

    # PV of face value
    pv_face    = face_value / (1 + ytm_period)**periods

    return round(pv_coupons + pv_face, 4)

def yield_to_maturity(face_value, coupon_rate, price,
                       periods, frequency=2):
    """Calculate YTM using numerical solver."""
    coupon = face_value * coupon_rate / frequency

    def price_diff(ytm_period):
        pv_c = coupon * (1-(1+ytm_period)**(-periods)) / ytm_period
        pv_f = face_value / (1+ytm_period)**periods
        return pv_c + pv_f - price

    ytm_period = brentq(price_diff, 0.0001, 1.0)
    return round(ytm_period * frequency, 6)

def accrued_interest(face_value, coupon_rate, days_since_coupon,
                      days_in_period, frequency=2):
    """
    Accrued interest between coupon dates.
    Dirty price = Clean price + Accrued interest
    """
    coupon = face_value * coupon_rate / frequency
    accrued = coupon * (days_since_coupon / days_in_period)
    return round(accrued, 4)

def current_yield(annual_coupon, price):
    """Simple current yield = annual coupon / price."""
    return round(annual_coupon / price * 100, 4)

def bond_equivalent_yield(discount_rate, days_to_maturity):
    """Convert T-bill discount rate to bond equivalent yield."""
    bey = (360 * discount_rate) / (360 - discount_rate * days_to_maturity)
    return round(bey * 100, 4)
```

---

## Duration & Convexity
```python
def macaulay_duration(face_value, coupon_rate, ytm,
                       periods, frequency=2):
    """
    Macaulay Duration: weighted average time to receive cash flows.
    Measures interest rate sensitivity in years.
    """
    coupon     = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency
    price      = bond_price(face_value, coupon_rate, ytm, periods, frequency)

    weighted_cf = 0
    for t in range(1, periods + 1):
        cf = coupon if t < periods else coupon + face_value
        pv = cf / (1 + ytm_period)**t
        weighted_cf += (t / frequency) * pv

    duration = weighted_cf / price
    return round(duration, 4)

def modified_duration(macaulay_dur, ytm, frequency=2):
    """
    Modified Duration = Macaulay / (1 + YTM/frequency)
    % price change ≈ -Modified Duration * yield change
    """
    mod_dur = macaulay_dur / (1 + ytm / frequency)
    return round(mod_dur, 4)

def convexity(face_value, coupon_rate, ytm, periods, frequency=2):
    """
    Convexity: second-order price sensitivity to yield changes.
    Positive convexity = price rises more than duration predicts on rally
    """
    coupon     = face_value * coupon_rate / frequency
    ytm_period = ytm / frequency
    price      = bond_price(face_value, coupon_rate, ytm, periods, frequency)

    conv_sum = 0
    for t in range(1, periods + 1):
        cf = coupon if t < periods else coupon + face_value
        pv = cf / (1 + ytm_period)**t
        conv_sum += pv * t * (t + 1)

    conv = conv_sum / (price * (1 + ytm_period)**2 * frequency**2)
    return round(conv, 4)

def price_change_estimate(mod_duration, convexity, yield_change):
    """
    Estimate bond price change for given yield change.
    dP/P ≈ -ModDur * dy + 0.5 * Convexity * dy^2
    """
    duration_effect  = -mod_duration * yield_change
    convexity_effect = 0.5 * convexity * yield_change**2
    total_change     = duration_effect + convexity_effect

    return {
        'duration_effect':  round(duration_effect * 100, 4),
        'convexity_effect': round(convexity_effect * 100, 4),
        'total_pct_change': round(total_change * 100, 4),
        'note': 'Convexity always helps — adds to gains, reduces losses'
    }

def dv01(face_value, coupon_rate, ytm, periods, frequency=2):
    """
    DV01: Dollar Value of 1 basis point.
    How much bond value changes for 1bp yield move.
    """
    price_up   = bond_price(face_value, coupon_rate, ytm + 0.0001,
                             periods, frequency)
    price_down = bond_price(face_value, coupon_rate, ytm - 0.0001,
                             periods, frequency)
    dv01_val   = (price_down - price_up) / 2
    return round(dv01_val, 4)
```

---

## Yield Curve
```python
def yield_curve_shapes():
    return {
        'Normal (Upward Sloping)': {
            'description': 'Short rates < Long rates',
            'signal':      'Healthy economy, inflation expected over time',
            'strategy':    'Receive long end, pay short end in rates'
        },
        'Inverted (Downward Sloping)': {
            'description': 'Short rates > Long rates',
            'signal':      'Recession predictor — bond market pricing rate cuts',
            'strategy':    'Long duration bonds — expect rates to fall'
        },
        'Flat': {
            'description': 'Short rates ≈ Long rates',
            'signal':      'Late cycle, transition between regimes',
            'strategy':    'Barbell — own short and long, avoid middle'
        },
        'Humped': {
            'description': 'Medium rates highest, short and long lower',
            'signal':      'Transitory rate hike expectations',
            'strategy':    'Butterfly trade — short belly, long wings'
        }
    }

def curve_trades():
    return {
        'Steepener': {
            'trade':    'Long short-end + Short long-end (2s10s steepener)',
            'profits':  'Yield curve steepens (long rates rise more or fall less)',
            'trigger':  'Early cycle, Fed cutting, growth improving',
            'example':  'Long 2yr Treasury futures, Short 10yr Treasury futures'
        },
        'Flattener': {
            'trade':    'Short short-end + Long long-end',
            'profits':  'Yield curve flattens (short rates rise more)',
            'trigger':  'Late cycle, Fed hiking, recession risk building',
            'example':  'Short 2yr, Long 10yr — duration neutral'
        },
        'Butterfly': {
            'trade':    'Long wings (2yr + 30yr) + Short belly (10yr)',
            'profits':  'Belly richens (curve humps)',
            'neutral':  'Duration neutral — hedges parallel shifts'
        },
        'Roll Down': {
            'trade':    'Buy bond that will roll down steep curve',
            'profits':  'As time passes, 10yr becomes 9yr at lower yield',
            'best':     'Steep curve + stable rate environment'
        }
    }

def bootstrapping_yield_curve(maturities, par_yields):
    """
    Bootstrap zero-coupon curve from par yields.
    """
    zero_rates   = []
    discount_factors = []

    for i, (mat, par_yield) in enumerate(zip(maturities, par_yields)):
        coupon = par_yield / 2  # semiannual

        if i == 0:
            # First period: simple calculation
            z = par_yield
        else:
            # Bootstrap using previous discount factors
            sum_df = sum(coupon * df for df in discount_factors)
            df_n   = (1 - sum_df) / (1 + coupon)
            z      = (1 / df_n) ** (1 / mat) - 1
            discount_factors.append(df_n)

        zero_rates.append(round(z * 100, 4))

    return dict(zip(maturities, zero_rates))
```

---

## Credit Analysis
```python
def credit_spread_analysis(corp_yield, treasury_yield, maturity):
    """Analyze corporate bond credit spread."""
    spread_bps = (corp_yield - treasury_yield) * 10000

    if maturity <= 2:
        benchmarks = {'AAA': 20, 'AA': 40, 'A': 70,
                      'BBB': 120, 'BB': 250, 'B': 450, 'CCC': 900}
    else:
        benchmarks = {'AAA': 40, 'AA': 70, 'A': 100,
                      'BBB': 160, 'BB': 300, 'B': 550, 'CCC': 1100}

    implied_rating = 'CCC'
    for rating, bench_spread in benchmarks.items():
        if spread_bps <= bench_spread:
            implied_rating = rating
            break

    return {
        'corp_yield':     corp_yield,
        'treasury_yield': treasury_yield,
        'spread_bps':     round(spread_bps, 1),
        'implied_rating': implied_rating,
        'classification': 'Investment Grade' if spread_bps < 300 else 'High Yield'
    }

def default_probability_from_spread(spread_bps, recovery_rate=0.40,
                                     years=5):
    """Estimate cumulative default probability from credit spread."""
    annual_pd = (spread_bps / 10000) / (1 - recovery_rate)
    cumulative_pd = 1 - (1 - annual_pd) ** years
    return {
        'annual_pd':      round(annual_pd * 100, 3),
        'cumulative_5yr': round(cumulative_pd * 100, 2),
        'recovery_assumed': f"{recovery_rate*100:.0f}%"
    }

def bond_credit_checklist():
    return {
        'Quantitative': [
            'Interest coverage ratio (EBIT/Interest) > 3x for IG',
            'Debt/EBITDA < 3x for IG, < 5x for BB, < 6x for B',
            'Free cash flow consistently positive',
            'Liquidity: cash + revolver covers 12 months of needs',
            'Debt maturity profile — no near-term wall'
        ],
        'Qualitative': [
            'Business model durability — recession resistant?',
            'Competitive position — pricing power?',
            'Management track record with debt',
            'Industry trends — secular headwinds or tailwinds?',
            'Covenant protection — investor friendly terms?'
        ],
        'Structural': [
            'Seniority — senior secured, unsecured, subordinated?',
            'Collateral — what assets back the bonds?',
            'Call provisions — when can issuer redeem early?',
            'Change of control put — bondholder protection on M&A',
            'Cross-default provisions'
        ]
    }
```

---

## Bond Sectors
```python
def bond_sectors_overview():
    return {
        'US Treasuries': {
            'issuer':    'US Federal Government',
            'credit':    'Risk-free (AAA)',
            'types':     'T-Bills (< 1yr), T-Notes (2-10yr), T-Bonds (20-30yr)',
            'liquidity': 'Highest in world',
            'use':       'Risk-free benchmark, safe haven, duration management'
        },
        'TIPS': {
            'issuer':    'US Treasury',
            'feature':   'Principal adjusts with CPI inflation',
            'real_yield': 'TIPS yield = nominal yield - breakeven inflation',
            'use':       'Inflation hedge, real return lock-in'
        },
        'Investment Grade Corps': {
            'rating':    'BBB- or above (S&P), Baa3 or above (Moody\'s)',
            'spread':    'Typically 50-200bps over Treasuries',
            'liquidity': 'Good but less than Treasuries',
            'use':       'Yield pickup over Treasuries with manageable credit risk'
        },
        'High Yield': {
            'rating':    'BB+ or below',
            'spread':    'Typically 300-800bps over Treasuries',
            'default':   'Higher default risk, more equity-like behavior',
            'use':       'Enhanced yield, economic growth bet'
        },
        'Municipal Bonds': {
            'issuer':    'State and local governments',
            'tax':       'Interest exempt from federal (often state) income tax',
            'taxable_equivalent': 'Muni yield / (1 - tax rate)',
            'use':       'High income investors seeking tax efficiency'
        },
        'Agency MBS': {
            'issuer':    'Fannie Mae, Freddie Mac, Ginnie Mae',
            'backing':   'Residential mortgage pools',
            'risk':      'Prepayment risk — homeowners refinance in falling rates',
            'spread':    '50-150bps over Treasuries',
            'use':       'Yield pickup with implicit government backing'
        },
        'EM Sovereign': {
            'issuers':   'Developing country governments',
            'index':     'JPMorgan EMBI+',
            'risk':      'Currency, political, credit risk',
            'spread':    'Wide range: 100-1000bps+ over Treasuries',
            'use':       'Diversification, high yield in EM growth cycle'
        }
    }
```

---

## Portfolio Strategies
```python
def bond_portfolio_strategies():
    return {
        'Bullet': {
            'structure':  'Concentrate maturities around single target date',
            'use':        'Match specific liability, minimize reinvestment risk',
            'risk':       'Concentrated in one part of curve'
        },
        'Barbell': {
            'structure':  'Combine short-term + long-term bonds, avoid middle',
            'use':        'Hedge against curve flattening or steepening',
            'advantage':  'Higher convexity than bullet at same duration',
            'risk':       'Underperforms if curve humps in belly'
        },
        'Ladder': {
            'structure':  'Equal allocation across maturities (1yr to 10yr)',
            'use':        'Regular reinvestment, reduce timing risk',
            'advantage':  'Simple, diversified, reinvestment at various rates',
            'best_for':   'Individual investors, income-focused portfolios'
        },
        'Immunization': {
            'structure':  'Match portfolio duration to liability duration',
            'use':        'Pension funds, insurance companies',
            'goal':       'Portfolio value tracks liability regardless of rate moves',
            'requirement':'Rebalance as duration drifts'
        },
        'Total Return': {
            'structure':  'Active management for price appreciation + income',
            'tools':      'Duration tilts, sector rotation, credit selection',
            'benchmark':  'Bloomberg Aggregate Bond Index',
            'use':        'Maximize risk-adjusted total return'
        }
    }

def bond_ladder_construction(total_investment, maturities, current_yields):
    """Build a bond ladder portfolio."""
    allocation_per_rung = total_investment / len(maturities)
    ladder = []

    for mat, yield_rate in zip(maturities, current_yields):
        annual_income = allocation_per_rung * yield_rate
        ladder.append({
            'maturity_years': mat,
            'allocation':     round(allocation_per_rung, 2),
            'yield':          round(yield_rate * 100, 2),
            'annual_income':  round(annual_income, 2)
        })

    total_income = sum(r['annual_income'] for r in ladder)
    blended_yield = total_income / total_investment

    return {
        'rungs':          ladder,
        'total_income':   round(total_income, 2),
        'blended_yield':  round(blended_yield * 100, 3),
        'avg_duration':   round(sum(maturities) / len(maturities), 1)
    }
```

---

## Interest Rate Risk Management
```python
def rate_risk_hedging(portfolio_dv01, target_dv01,
                       hedge_instrument_dv01):
    """
    Calculate hedge ratio to achieve target DV01.
    Use Treasury futures or interest rate swaps as hedge.
    """
    dv01_to_hedge  = portfolio_dv01 - target_dv01
    contracts_needed = dv01_to_hedge / hedge_instrument_dv01

    return {
        'portfolio_dv01':    round(portfolio_dv01, 2),
        'target_dv01':       round(target_dv01, 2),
        'dv01_to_hedge':     round(dv01_to_hedge, 2),
        'contracts_needed':  round(contracts_needed, 2),
        'action':            'Short futures' if dv01_to_hedge > 0
                             else 'Long futures'
    }

def scenario_analysis(bonds, yield_shifts):
    """
    Analyze portfolio P&L under different yield curve scenarios.
    """
    results = {}

    for scenario, shifts in yield_shifts.items():
        total_pnl = 0
        for bond in bonds:
            dur_effect  = -bond['mod_duration'] * shifts.get(
                bond['maturity_bucket'], 0)
            conv_effect = 0.5 * bond['convexity'] * shifts.get(
                bond['maturity_bucket'], 0)**2
            pnl = (dur_effect + conv_effect) * bond['market_value']
            total_pnl += pnl

        results[scenario] = round(total_pnl, 2)

    return results

# Common yield curve scenarios
yield_scenarios = {
    'Parallel +100bps':     {'2yr': 0.01,  '5yr': 0.01,  '10yr': 0.01,  '30yr': 0.01},
    'Parallel -100bps':     {'2yr': -0.01, '5yr': -0.01, '10yr': -0.01, '30yr': -0.01},
    'Bear Steepener':       {'2yr': 0.005, '5yr': 0.01,  '10yr': 0.02,  '30yr': 0.03},
    'Bull Flattener':       {'2yr': -0.02, '5yr': -0.015,'10yr': -0.01, '30yr': -0.005},
    'Short End Spike':      {'2yr': 0.05,  '5yr': 0.02,  '10yr': 0.005, '30yr': 0.00},
}
```

---

## Key Fixed Income Metrics
```python
def fixed_income_metrics_guide():
    return {
        'YTM':              'Total annualized return if held to maturity',
        'YTC':              'Yield to call — if bond called at first call date',
        'YTW':              'Yield to worst — lowest of YTM, YTC, YTP',
        'Current Yield':    'Annual coupon / Current price',
        'Z-Spread':         'Constant spread over entire swap curve',
        'OAS':              'Option-Adjusted Spread — removes embedded option value',
        'DV01':             'Dollar value of 1 basis point move',
        'PVBP':             'Price value of basis point (same as DV01)',
        'Duration':         'Price sensitivity to yield change (in years)',
        'Convexity':        'Second-order price sensitivity — always positive for bonds',
        'Breakeven':        'Nominal yield - TIPS yield = inflation expectation',
        'Spread Duration':  'Price sensitivity to credit spread change',
        'Treasury Basis':   'Difference between cash Treasury and futures price'
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Ignoring duration | Rate rise wipes out years of coupon | Always know your duration exposure |
| Chasing yield | High yield = high risk | Understand what drives the spread |
| Ignoring call risk | Bond called when rates fall | Always calculate YTW not just YTM |
| Concentration in one issuer | Default wipes position | Diversify across issuers and sectors |
| Ignoring liquidity | Cannot sell at fair price in stress | Size positions based on liquidity |
| Misunderstanding MBS | Prepayment shortens duration in rally | Model prepayment scenarios |
| Tax on munis | Wrong investor type | Munis only valuable to high-tax investors |

---

## Best Practices

- **Know your duration** before any rate view or portfolio construction
- **Yield to worst always** — never evaluate bonds on YTM alone if callable
- **Diversify by issuer, sector, maturity** — no single bond > 5% of portfolio
- **Credit research matters** — read the covenants and debt structure
- **Liquidity premium** — illiquid bonds deserve extra spread compensation
- **Tax awareness** — municipal bonds only make sense above ~32% tax bracket
- **Benchmark awareness** — know what index you are measured against

---

## Related Skills

- **derivatives-expert**: Interest rate swaps and bond futures
- **macro-economics-expert**: Rate cycle and yield curve drivers
- **risk-management-expert**: Duration and credit risk hedging
- **portfolio-management-expert**: Fixed income allocation
- **quantitative-finance-expert**: Bond pricing models
