---
author: luo-kai
name: derivatives-expert
description: Expert-level derivatives knowledge. Use when working with futures, forwards, swaps, structured products, interest rate derivatives, credit derivatives, commodity derivatives, or exotic options. Also use when the user mentions 'futures contract', 'forward', 'swap', 'CDS', 'interest rate swap', 'basis', 'contango', 'backwardation', 'notional value', 'mark to market', 'margin call', or 'structured product'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Derivatives Expert

You are a world-class derivatives specialist with deep expertise in futures, forwards, swaps, structured products, credit derivatives, interest rate derivatives, and exotic options across all asset classes.

## Before Starting

1. **Instrument** — Futures, forwards, swaps, structured product, or exotic?
2. **Asset class** — Equity, rates, credit, FX, commodity, or crypto?
3. **Goal** — Hedging, speculation, arbitrage, or income?
4. **Counterparty** — Exchange-traded or OTC?
5. **Risk concern** — Market risk, credit risk, liquidity, or basis risk?

---

## Core Expertise Areas

- **Futures**: pricing, basis, rolling, margin, delivery
- **Forwards**: FX forwards, commodity forwards, customization
- **Swaps**: interest rate, currency, equity, credit default
- **Structured Products**: principal protection, yield enhancement, leverage
- **Credit Derivatives**: CDS, CDO, CLO, credit linked notes
- **Exotic Options**: barriers, digitals, Asians, lookbacks
- **Pricing Models**: Black-Scholes extensions, Monte Carlo, trees
- **Risk Management**: delta, gamma, vega hedging, DV01

---

## Futures

### Futures Fundamentals
```python
import numpy as np

def futures_fair_value(spot, risk_free, dividend_yield,
                        storage_cost, convenience_yield, T):
    """
    Cost of carry model for futures fair value.
    F = S * e^((r + storage - convenience - dividend) * T)
    T: time to expiry in years
    """
    carry = risk_free + storage_cost - convenience_yield - dividend_yield
    fair_value = spot * np.exp(carry * T)
    return round(fair_value, 4)

def basis(spot, futures_price):
    """
    Basis = Spot - Futures
    Positive basis = backwardation (spot > futures)
    Negative basis = contango (spot < futures)
    """
    basis_value = spot - futures_price
    structure = 'Backwardation' if basis_value > 0 else 'Contango'
    return {
        'basis':     round(basis_value, 4),
        'structure': structure,
        'note':      'Backwardation: supply tight or high convenience yield. '
                     'Contango: storage costs dominate, ample supply.'
    }

def roll_yield(front_month, next_month):
    """
    Roll yield from rolling futures position.
    Positive roll yield in backwardation (favorable for long).
    Negative roll yield in contango (drag for long).
    """
    roll = (front_month - next_month) / next_month
    return {
        'roll_yield_pct': round(roll * 100, 4),
        'impact':         'Positive for longs' if roll > 0 else 'Negative for longs (contango drag)'
    }

def futures_pnl(entry, exit_price, contract_size, num_contracts):
    """Calculate futures P&L."""
    pnl_per_contract = (exit_price - entry) * contract_size
    total_pnl = pnl_per_contract * num_contracts
    return {
        'pnl_per_contract': round(pnl_per_contract, 2),
        'total_pnl':        round(total_pnl, 2)
    }

def margin_requirements(notional, initial_margin_pct=0.05,
                         maintenance_margin_pct=0.03):
    """
    Futures margin calculation.
    Initial margin: deposit to open position
    Maintenance margin: minimum to keep position open
    Margin call triggered when equity falls below maintenance
    """
    initial    = notional * initial_margin_pct
    maintenance = notional * maintenance_margin_pct
    return {
        'notional':           round(notional, 2),
        'initial_margin':     round(initial, 2),
        'maintenance_margin': round(maintenance, 2),
        'leverage':           round(1 / initial_margin_pct, 1),
        'margin_call_loss':   round(initial - maintenance, 2)
    }
```

### Key Futures Contracts
```python
def futures_universe():
    return {
        'Equity Index': {
            'ES':  'S&P 500 E-mini ($50 x index)',
            'NQ':  'Nasdaq 100 E-mini ($20 x index)',
            'YM':  'Dow Jones E-mini ($5 x index)',
            'RTY': 'Russell 2000 E-mini ($50 x index)',
            'MES': 'Micro S&P 500 ($5 x index)'
        },
        'Fixed Income': {
            'ZB':  '30-year Treasury Bond ($1000 x price)',
            'ZN':  '10-year Treasury Note ($1000 x price)',
            'ZF':  '5-year Treasury Note ($1000 x price)',
            'ZT':  '2-year Treasury Note ($2000 x price)',
            'GE':  'Eurodollar (interest rate futures)'
        },
        'Energy': {
            'CL':  'WTI Crude Oil (1000 barrels)',
            'NG':  'Natural Gas (10,000 MMBtu)',
            'RB':  'RBOB Gasoline (42,000 gallons)',
            'HO':  'Heating Oil (42,000 gallons)'
        },
        'Metals': {
            'GC':  'Gold (100 troy oz)',
            'SI':  'Silver (5000 troy oz)',
            'HG':  'Copper (25,000 lbs)',
            'PL':  'Platinum (50 troy oz)'
        },
        'Agricultural': {
            'ZC':  'Corn (5000 bushels)',
            'ZW':  'Wheat (5000 bushels)',
            'ZS':  'Soybeans (5000 bushels)',
            'KC':  'Coffee (37,500 lbs)',
            'CT':  'Cotton (50,000 lbs)'
        },
        'FX': {
            '6E':  'Euro FX (125,000 EUR)',
            '6J':  'Japanese Yen (12,500,000 JPY)',
            '6B':  'British Pound (62,500 GBP)',
            '6A':  'Australian Dollar (100,000 AUD)'
        }
    }
```

---

## Forwards
```python
def fx_forward_rate(spot, domestic_rate, foreign_rate, T):
    """
    Interest Rate Parity: F = S * (1 + r_d)^T / (1 + r_f)^T
    Higher interest rate currency trades at forward discount.
    """
    forward = spot * ((1 + domestic_rate) ** T) / ((1 + foreign_rate) ** T)
    forward_points = (forward - spot) * 10000  # in pips for FX

    return {
        'spot':           spot,
        'forward_rate':   round(forward, 6),
        'forward_points': round(forward_points, 2),
        'premium_discount': 'Premium' if forward > spot else 'Discount'
    }

def commodity_forward(spot, storage_rate, insurance_rate,
                       financing_rate, convenience_yield, T):
    """Forward price for physical commodities."""
    carrying_cost = financing_rate + storage_rate + insurance_rate
    forward = spot * np.exp((carrying_cost - convenience_yield) * T)
    return round(forward, 4)

def ndf_settlement(notional, fixing_rate, contract_rate, currency_pair):
    """
    Non-Deliverable Forward settlement.
    Used for restricted currencies (INR, BRL, CNY).
    Settled in USD, no physical delivery.
    """
    pnl = notional * (fixing_rate - contract_rate) / fixing_rate
    return {
        'notional':       notional,
        'contract_rate':  contract_rate,
        'fixing_rate':    fixing_rate,
        'settlement_usd': round(pnl, 2),
        'direction':      'Receive' if pnl > 0 else 'Pay'
    }
```

---

## Swaps

### Interest Rate Swaps
```python
def irs_valuation(fixed_rate, float_rates, notional,
                   discount_factors, payment_dates):
    """
    Interest Rate Swap valuation.
    Fixed leg: pay fixed rate on notional
    Float leg: receive floating rate (SOFR/LIBOR)
    Value = PV(float leg) - PV(fixed leg)
    """
    # PV of fixed leg
    pv_fixed = sum(
        fixed_rate * notional * dt * df
        for dt, df in zip(payment_dates, discount_factors)
    )

    # PV of floating leg (approximation using forward rates)
    pv_float = sum(
        fr * notional * dt * df
        for fr, dt, df in zip(float_rates, payment_dates, discount_factors)
    )

    value_to_fixed_payer = pv_float - pv_fixed
    dv01 = pv_fixed * 0.0001 / fixed_rate  # approx dollar value of 1bp

    return {
        'pv_fixed':              round(pv_fixed, 2),
        'pv_float':              round(pv_float, 2),
        'value_fixed_payer':     round(value_to_fixed_payer, 2),
        'value_fixed_receiver':  round(-value_to_fixed_payer, 2),
        'dv01':                  round(dv01, 2)
    }

def swap_types():
    return {
        'Vanilla IRS': {
            'description': 'Fixed vs floating interest rate exchange',
            'use':         'Hedge floating rate debt, express rate view',
            'example':     'Company pays fixed 4%, receives SOFR + spread'
        },
        'Basis Swap': {
            'description': 'Float vs float, different reference rates',
            'use':         'Hedge basis risk between rate benchmarks',
            'example':     'SOFR vs Fed Funds basis swap'
        },
        'Cross Currency Swap': {
            'description': 'Exchange principal + interest in two currencies',
            'use':         'Hedge FX exposure on foreign currency debt',
            'example':     'USD fixed vs EUR fixed + exchange principals'
        },
        'Equity Swap': {
            'description': 'Equity return vs fixed or floating rate',
            'use':         'Gain equity exposure without owning shares',
            'example':     'Total return S&P 500 vs SOFR + spread'
        },
        'Commodity Swap': {
            'description': 'Fixed commodity price vs floating spot',
            'use':         'Hedge commodity price exposure',
            'example':     'Oil producer locks in $80/bbl fixed price'
        },
        'Total Return Swap': {
            'description': 'Total return of asset vs financing rate',
            'use':         'Leveraged exposure, short selling, regulatory arbitrage',
            'example':     'Archegos used TRS for concentrated leveraged positions'
        }
    }
```

### Credit Default Swaps
```python
def cds_basics():
    return {
        'definition': 'Insurance contract against bond default',
        'buyer':      'Pays premium (spread), receives par if default',
        'seller':     'Receives premium, pays par minus recovery if default',
        'spread':     'Annual premium in basis points on notional',
        'uses': {
            'hedge':      'Bond holder buys CDS protection',
            'speculate':  'Buy CDS without owning bond (naked CDS)',
            'arbitrage':  'Cash bond vs CDS basis trades'
        }
    }

def cds_implied_default_probability(spread_bps, recovery_rate=0.40,
                                     maturity=5):
    """
    Approximate default probability from CDS spread.
    P(default) ≈ spread / (1 - recovery_rate)
    """
    spread = spread_bps / 10000
    annual_default_prob = spread / (1 - recovery_rate)
    cumulative_default  = 1 - (1 - annual_default_prob) ** maturity

    return {
        'spread_bps':              spread_bps,
        'annual_default_prob':     round(annual_default_prob * 100, 3),
        'cumulative_default_5yr':  round(cumulative_default * 100, 2),
        'implied_rating':          'IG' if spread_bps < 150 else
                                   'HY' if spread_bps < 500 else 'Distressed'
    }

def cds_pnl(notional, entry_spread, exit_spread, dv01_per_bp):
    """P&L from CDS position (protection buyer perspective)."""
    spread_change = exit_spread - entry_spread
    pnl = -spread_change * dv01_per_bp  # buyer profits when spread widens
    return {
        'spread_change_bps': spread_change,
        'pnl':               round(pnl, 2),
        'direction':         'Profit' if pnl > 0 else 'Loss'
    }
```

---

## Structured Products
```python
def structured_product_types():
    return {
        'Principal Protected Note (PPN)': {
            'structure':   '100% bonds + call options',
            'risk':        'No downside (principal protected)',
            'upside':      'Participation in index gains (capped)',
            'cost':        'Opportunity cost vs direct investment',
            'best_for':    'Risk-averse investors wanting market exposure'
        },
        'Autocallable': {
            'structure':   'High coupon paid if index stays above barrier',
            'risk':        'Full downside if index breaches barrier at maturity',
            'upside':      'Enhanced yield (8-15% annual coupon typical)',
            'trigger':     'Auto-called early if index above call level',
            'best_for':    'Yield seekers in sideways/mildly bullish markets'
        },
        'Reverse Convertible': {
            'structure':   'High coupon + short put on underlying',
            'risk':        'Receive shares (not cash) if stock falls below barrier',
            'upside':      'High fixed coupon regardless of stock movement',
            'best_for':    'Investors comfortable owning the underlying at discount'
        },
        'Leveraged Note': {
            'structure':   '2x or 3x exposure to index return',
            'risk':        'Amplified losses, volatility decay over time',
            'best_for':    'Short-term tactical views only',
            'warning':     'Daily rebalancing causes decay in volatile markets'
        },
        'CLO (Collateralized Loan Obligation)': {
            'structure':   'Pool of leveraged loans tranched by seniority',
            'tranches':    'AAA (senior), AA, A, BBB, BB, Equity (first loss)',
            'risk':        'Credit risk, liquidity risk, correlation risk',
            'yield':       'Equity tranche: 15-20%+, AAA: SOFR + 130-170bps'
        }
    }

def capital_protected_note_decomposition(face_value, bond_rate,
                                          T, call_option_price,
                                          participation_rate=1.0):
    """
    Decompose a principal protected note into components.
    Face value = Zero coupon bond + Call options
    """
    # Zero coupon bond cost (PV of face value)
    zcb_cost    = face_value / (1 + bond_rate) ** T
    option_budget = face_value - zcb_cost

    # Number of calls purchasable
    calls_purchasable = option_budget / call_option_price
    effective_participation = calls_purchasable / (face_value / 100)

    return {
        'face_value':              face_value,
        'zcb_cost':                round(zcb_cost, 2),
        'option_budget':           round(option_budget, 2),
        'effective_participation': round(effective_participation * 100, 1),
        'note':                    'Higher rates = more option budget = higher participation'
    }
```

---

## Exotic Options
```python
def exotic_options_guide():
    return {
        'Barrier Options': {
            'Knock-In':   'Option activates only if price hits barrier',
            'Knock-Out':  'Option cancels if price hits barrier',
            'Down-and-In Call': 'Activates when price falls to barrier (cheap)',
            'Up-and-Out Call':  'Cancels when price rises to barrier (cheaper than vanilla)',
            'Use':        'Cheaper than vanilla, precise hedging'
        },
        'Asian Options': {
            'description': 'Payoff based on AVERAGE price over period',
            'less_volatile': 'Average is smoother than spot at expiry',
            'cheaper':     'Lower vol = lower premium than vanilla',
            'use':         'Commodity hedging (avg production price)'
        },
        'Digital/Binary Options': {
            'Cash-or-Nothing': 'Pay fixed $X if ITM at expiry, else $0',
            'Asset-or-Nothing':'Deliver asset if ITM, else nothing',
            'use':         'Event-driven trades, precise payout structures',
            'risk':        'Huge delta near expiry at strike (discontinuous)'
        },
        'Lookback Options': {
            'description': 'Payoff based on MAX or MIN price over period',
            'Fixed':       'Strike set at expiry based on optimal historical price',
            'Floating':    'Allows buying at lowest / selling at highest price',
            'cost':        'Most expensive exotic — perfect hindsight',
            'use':         'Rare — mostly academic benchmark'
        },
        'Compound Options': {
            'description': 'Option on an option',
            'types':       'Call on call, put on put, call on put, put on call',
            'use':         'Hedge contingent exposures (M&A deal options)'
        },
        'Variance Swap': {
            'description': 'Swap realized variance vs fixed strike variance',
            'long':        'Profit when realized vol > implied vol at inception',
            'use':         'Pure volatility exposure without delta hedging',
            'vega':        'Linear in variance, convex in vol'
        }
    }
```

---

## Derivatives Risk Management
```python
def derivatives_risk_metrics(position):
    """Key risk metrics for derivatives positions."""
    return {
        'Delta':   'Change in value per $1 move in underlying',
        'Gamma':   'Rate of change of delta — risk of delta hedges',
        'Vega':    'Change in value per 1% change in implied vol',
        'Theta':   'Time decay per day',
        'Rho':     'Change in value per 1% change in interest rates',
        'DV01':    'Dollar value of 1 basis point (for rate products)',
        'CS01':    'Credit spread 01 — value change per 1bp spread move',
        'Notional':'Total face value of contract (not same as risk!)'
    }

def hedge_effectiveness(hedged_returns, unhedged_returns):
    """Measure how well a derivatives hedge is working."""
    import pandas as pd
    variance_reduction = 1 - (hedged_returns.var() / unhedged_returns.var())
    correlation = hedged_returns.corr(unhedged_returns)

    return {
        'variance_reduction': round(variance_reduction * 100, 2),
        'correlation':        round(correlation, 4),
        'hedge_ratio':        round(
            hedged_returns.cov(unhedged_returns) / unhedged_returns.var(), 4
        ),
        'effectiveness':      'Excellent' if variance_reduction > 0.80 else
                              'Good'      if variance_reduction > 0.60 else
                              'Moderate'  if variance_reduction > 0.40 else
                              'Poor'
    }
```

---

## Key Concepts

    Contango vs Backwardation:
      Contango:       Futures > Spot (most common)
                      Storage costs + financing dominate
                      Long futures = negative roll yield (drag)
                      Common in oil, natural gas

      Backwardation:  Futures < Spot
                      High convenience yield or supply shortage
                      Long futures = positive roll yield (tailwind)
                      Common in tight commodity markets

    Mark to Market:
      Futures positions settled daily to market value
      Profits credited, losses debited from margin account
      Prevents credit risk buildup (unlike forwards)

    Basis Risk:
      Risk that hedge does not perfectly offset exposure
      Basis = Spot - Futures (changes over time)
      Cross-hedging: using correlated but non-identical instrument

    Notional vs Exposure:
      $1M notional CDS != $1M at risk
      $1M equity swap notional = full equity market risk
      Always think in terms of actual risk, not notional

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Ignoring basis risk | Hedge does not offset exposure | Match instrument to exposure precisely |
| Contango drag | Long commodity ETFs lose to roll | Use backwardated markets or short-term futures |
| Margin call surprise | Forced liquidation at worst time | Keep 2-3x initial margin as buffer |
| Counterparty risk in OTC | Dealer defaults, swap worthless | Use central clearing, collateral agreements |
| Notional confusion | Overestimate or underestimate risk | Always translate notional to actual risk |
| Early exercise on Americans | Miss optimal exercise timing | Model early exercise properly |
| Model risk in exotics | Model misprices barrier options | Use multiple models, stress test |

---

## Best Practices

- **Understand the payoff diagram** before entering any derivative
- **Know your Greeks** — delta hedge regularly for options books
- **Margin buffer** — always hold 2-3x initial margin minimum
- **Central clearing** for OTC when possible — reduces counterparty risk
- **Stress test** — what happens in 2008, 2020 scenarios?
- **Document hedges** — accounting treatment matters (hedge accounting)
- **Unwind plan** — know how to exit before you enter

---

## Related Skills

- **options-trading-expert**: Vanilla options deep dive
- **fixed-income-expert**: Bond futures and rate derivatives
- **risk-management-expert**: Greeks hedging and portfolio risk
- **quantitative-finance-expert**: Derivatives pricing models
- **macro-economics-expert**: Macro drivers of derivatives markets
