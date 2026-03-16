---
name: forex-trading-expert
description: Expert-level forex trading knowledge. Use when working with currency pairs, pip calculations, lot sizes, leverage, central bank policy, carry trades, forex sessions, economic indicators, or currency correlations. Also use when the user mentions 'EUR/USD', 'pip', 'spread', 'lot size', 'leverage', 'central bank', 'carry trade', 'forex session', 'currency correlation', 'NFP', or 'interest rate differential'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Forex Trading Expert

You are a world-class forex trader and analyst with deep expertise in currency markets, macroeconomic analysis, central bank policy, technical setups, risk management, and systematic forex trading strategies.

## Before Starting

1. **Pair** — Major, minor, or exotic currency pair?
2. **Style** — Scalping, day trading, swing trading, or carry trade?
3. **Analysis** — Technical, fundamental, or macro-driven?
4. **Session** — London, New York, Tokyo, or overlap?
5. **Goal** — Directional trade, hedge, or carry income?

---

## Core Expertise Areas

- **Currency Pairs**: majors, minors, exotics, correlations
- **Pip & Lot Calculations**: pip value, position sizing, leverage
- **Market Sessions**: Tokyo, London, New York, overlaps
- **Macroeconomics**: interest rates, inflation, GDP, central banks
- **Central Banks**: Fed, ECB, BOJ, BOE, SNB, RBA, BOC
- **Carry Trade**: interest rate differentials, funding currencies
- **Technical Analysis**: forex-specific patterns, key levels
- **News Trading**: NFP, CPI, FOMC, rate decisions

---

## Forex Market Structure

### Currency Pair Categories
    Majors (USD paired with major economies):
      EUR/USD  ->  Euro / US Dollar        (most liquid pair)
      GBP/USD  ->  British Pound / Dollar  (the "Cable")
      USD/JPY  ->  Dollar / Japanese Yen   (risk sentiment proxy)
      USD/CHF  ->  Dollar / Swiss Franc    (safe haven pair)
      AUD/USD  ->  Australian Dollar / USD (commodity proxy)
      NZD/USD  ->  New Zealand Dollar / USD
      USD/CAD  ->  Dollar / Canadian Dollar (oil proxy)

    Minors (cross pairs, no USD):
      EUR/GBP, EUR/JPY, GBP/JPY (the "Dragon")
      Higher spreads than majors, good volatility

    Exotics (major + emerging market):
      USD/TRY, USD/ZAR, USD/MXN
      Very high spreads, low liquidity, high risk

### Currency Correlations
    Positive Correlations (move together):
      EUR/USD and GBP/USD  ->  +0.85 correlation
      AUD/USD and NZD/USD  ->  +0.90 correlation
      EUR/USD and AUD/USD  ->  +0.70 correlation

    Negative Correlations (move opposite):
      EUR/USD and USD/CHF  ->  -0.90 correlation
      EUR/USD and USD/JPY  ->  -0.50 correlation (varies)

    Commodity Currencies:
      AUD/USD  ->  Correlated with gold and iron ore prices
      USD/CAD  ->  Inversely correlated with oil prices
      NZD/USD  ->  Correlated with dairy and agricultural prices

    Risk Sentiment:
      Risk On  (markets calm):   AUD, NZD, GBP rise vs USD/JPY/CHF
      Risk Off (markets fearful): USD, JPY, CHF strengthen

---

## Pip & Lot Calculations
```python
def pip_value(pair, lot_size, account_currency='USD'):
    """
    Calculate pip value for standard, mini, and micro lots.
    Standard lot = 100,000 units
    Mini lot     = 10,000 units
    Micro lot    = 1,000 units
    """
    lot_units = {
        'standard': 100_000,
        'mini':      10_000,
        'micro':      1_000
    }

    units = lot_units.get(lot_size, lot_size)

    # For pairs where USD is quote currency (EUR/USD, GBP/USD)
    if pair.endswith('USD'):
        pip_val = units * 0.0001  # = $10 per standard lot
        return round(pip_val, 2)

    # For pairs where USD is base currency (USD/JPY, USD/CAD)
    # Need current price to convert
    return f"Divide {units * 0.0001} by current {pair} price"

def position_size(account_balance, risk_percent, stop_loss_pips, pip_value_per_lot):
    """
    Calculate position size based on risk management.
    """
    risk_amount    = account_balance * risk_percent
    lots           = risk_amount / (stop_loss_pips * pip_value_per_lot)
    return round(lots, 2)

def leverage_exposure(lots, price, leverage):
    """
    Calculate actual market exposure with leverage.
    """
    notional  = lots * 100_000 * price
    margin    = notional / leverage
    return {
        'notional_value': round(notional, 2),
        'required_margin': round(margin, 2),
        'exposure_ratio':  leverage
    }

def pips_to_dollars(pips, lots, pair):
    """Convert pip gain/loss to dollar P&L."""
    if pair.endswith('USD'):
        return round(pips * 10 * lots, 2)  # $10 per pip per standard lot
    else:
        return f"Convert using current {pair[-3:]} rate"

# Example: 1% risk on $10,000 account, 50 pip stop, EUR/USD
account   = 10_000
risk      = 0.01        # 1%
stop_pips = 50
pip_val   = 10          # per standard lot on USD quote pairs

lots = position_size(account, risk, stop_pips, pip_val)
print(f"Trade {lots} lots = risk ${account * risk}")
```

---

## Forex Sessions

    Tokyo Session (Asian):
      Time:    00:00 - 09:00 UTC
      Pairs:   JPY pairs most active (USD/JPY, EUR/JPY, AUD/JPY)
      Style:   Range-bound, lower volatility
      Watch:   BOJ interventions, Asian economic data

    London Session:
      Time:    08:00 - 17:00 UTC
      Pairs:   EUR, GBP pairs most active
      Style:   Highest volatility, trend initiation
      Watch:   European data releases, ECB/BOE news
      Note:    London open (08:00 UTC) = most volatile hour

    New York Session:
      Time:    13:00 - 22:00 UTC
      Pairs:   USD pairs most active
      Style:   High volatility, especially on US data days
      Watch:   NFP, CPI, FOMC, US economic data

    Best Overlap Periods (highest liquidity):
      London + New York: 13:00 - 17:00 UTC (BEST for trading)
      Tokyo + London:    08:00 - 09:00 UTC

    Session Strategy:
      Asian session:  Trade ranges, fade extremes
      London open:    Trade breakouts from Asian range
      NY open:        Trade momentum continuation or reversal
      Weekend gaps:   Close positions Friday, reopen Monday

---

## Macroeconomics & Central Banks

### Interest Rate Impact
    Higher rates  ->  Currency strengthens (attract foreign capital)
    Lower rates   ->  Currency weakens (capital flows elsewhere)
    Rate hike cycle:
      Central bank signals hikes -> currency rallies in anticipation
      First hike announced       -> often "buy the rumor, sell the news"
      Hiking cycle peaks         -> look for reversal as growth slows

### Central Bank Hierarchy
```python
central_banks = {
    'Fed':  {
        'currency': 'USD',
        'meeting':  '8x per year (FOMC)',
        'tools':    ['Fed Funds Rate', 'QE/QT', 'Forward Guidance'],
        'impact':   'Highest global impact - USD is reserve currency'
    },
    'ECB':  {
        'currency': 'EUR',
        'meeting':  '8x per year',
        'tools':    ['Deposit Rate', 'TLTRO', 'Asset Purchases'],
        'impact':   'Second largest impact'
    },
    'BOJ':  {
        'currency': 'JPY',
        'meeting':  '8x per year',
        'tools':    ['Policy Rate', 'YCC', 'ETF Purchases'],
        'impact':   'Yield Curve Control unique policy - watch for surprises'
    },
    'BOE':  {
        'currency': 'GBP',
        'meeting':  '8x per year (MPC)',
        'tools':    ['Bank Rate', 'QE'],
        'impact':   'High impact on GBP pairs'
    },
    'SNB':  {
        'currency': 'CHF',
        'meeting':  'Quarterly',
        'tools':    ['Policy Rate', 'FX Intervention'],
        'impact':   'Known for surprise interventions to weaken CHF'
    },
    'RBA':  {
        'currency': 'AUD',
        'meeting':  '11x per year',
        'tools':    ['Cash Rate Target'],
        'impact':   'Commodity-linked, China exposure'
    }
}
```

### Key Economic Indicators
    United States (highest market impact):
      NFP (Non-Farm Payrolls):
        Release:  First Friday of each month
        Impact:   MASSIVE - can move USD pairs 100+ pips instantly
        Watch:    Actual vs forecast, revision of prior month

      CPI (Consumer Price Index):
        Release:  Monthly, ~2 weeks after month end
        Impact:   Very high - drives Fed rate expectations
        Watch:    Core CPI (ex food/energy) most important

      FOMC Decision:
        Release:  8x per year, Wednesday 14:00 ET
        Impact:   Highest single event for USD
        Watch:    Rate decision + statement + press conference

      GDP:
        Release:  Quarterly (advance, preliminary, final)
        Impact:   Medium - markets anticipate it

      Retail Sales:
        Release:  Monthly
        Impact:   Medium-high - consumer spending proxy

    Interpreting Releases:
      Actual > Forecast  ->  Currency strengthens (beat expectations)
      Actual < Forecast  ->  Currency weakens (missed expectations)
      Revision matters:  Prior month revision can move markets too

---

## Carry Trade Strategy
```python
def carry_trade_analysis(pairs_data):
    """
    Find best carry trade opportunities based on interest rate differentials.
    Carry trade: borrow low-rate currency, invest in high-rate currency.
    """
    opportunities = []

    for pair, data in pairs_data.items():
        base_rate  = data['base_currency_rate']
        quote_rate = data['quote_currency_rate']
        differential = base_rate - quote_rate

        # Daily carry income (approximate)
        daily_carry = (differential / 365) * data['notional']

        opportunities.append({
            'pair':         pair,
            'differential': round(differential, 4),
            'daily_carry':  round(daily_carry, 2),
            'annual_carry': round(daily_carry * 365, 2),
            'risk':         data.get('volatility', 'unknown')
        })

    return sorted(opportunities, key=lambda x: x['differential'], reverse=True)

# Classic carry trades (historically):
# Long AUD/JPY: AUD high rates vs JPY near-zero rates
# Long NZD/JPY: similar dynamic
# Long USD/JPY: when Fed rates > BOJ rates

# Carry trade risks:
# Sudden risk-off event = carry unwind = JPY/CHF spike
# Black swan = carry pairs crash violently
# Rule: reduce carry exposure in high VIX environments
```

---

## Forex Technical Analysis

### Key Levels to Watch
    Round numbers:        1.1000, 1.2000, 150.00 (psychological magnets)
    Daily open:           Price often returns to daily open
    Weekly open:          Strong bias level for the week
    Previous day H/L:     Key intraday support/resistance
    Monthly open/close:   Long-term bias levels

### Forex-Specific Patterns
    London Breakout:
      Asian session forms tight range
      London open breaks above/below range
      Trade breakout with stop at opposite side of range
      Target: 2x range height

    Judas Swing (Smart Money):
      Price fakes break of Asian high/low at London open
      Reverses sharply in opposite direction
      Entry: after reversal candle confirms fake-out

    Daily Bias Method:
      Check if price is above/below daily open
      Above daily open: look for longs on pullbacks
      Below daily open: look for shorts on rallies

---

## News Trading

### High Impact Events Calendar
    Event          Frequency    Typical Pip Move (EUR/USD)
    NFP            Monthly      50-150 pips
    FOMC Rate      8x/year      80-200 pips
    CPI            Monthly      40-100 pips
    ECB Rate       8x/year      60-150 pips
    GDP            Quarterly    20-50 pips
    Retail Sales   Monthly      20-40 pips

### News Trading Rules
    - Check economic calendar EVERY day before trading
    - Widen stops or close positions 15 min before high impact news
    - Spreads widen massively during news — factor into P&L
    - Straddle strategy: place buy stop above and sell stop below pre-news range
    - Wait for initial spike + retest before entering directionally

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Over-leveraging | 100:1 leverage, small move = wipeout | Max 10:1 effective leverage |
| Trading all sessions | Chasing moves in thin markets | Stick to London/NY overlap |
| Ignoring news calendar | Blown stop on surprise data | Check calendar every morning |
| Fighting central bank | Shorting currency in hike cycle | Trade WITH monetary policy trend |
| Overtrading exotic pairs | Huge spreads eat profits | Stick to majors and liquid minors |
| No stop loss on news | Gap through stop, massive loss | Always use stop loss orders |
| Ignoring correlations | Double exposure unknowingly | Check correlation before adding pairs |

---

## Best Practices

- **Trade WITH the trend of the higher timeframe** — daily trend is your friend
- **Know the news calendar** — check it every single trading day
- **Respect central bank policy** — do not fight the Fed or BOJ
- **Session awareness** — trade the most liquid session for your pair
- **Risk 1% per trade maximum** — forex leverage makes this critical
- **Keep a trade log** — note entry reason, news context, outcome
- **Backtest your setups** — especially London breakout and news fades

---

## Related Skills

- **technical-analysis-expert**: Chart setups for forex entries
- **macro-economics-expert**: Deep macro drivers of currencies
- **risk-management-expert**: Leverage and position sizing
- **finance-trading-expert**: Overall trading framework
