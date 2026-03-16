---
name: hedge-fund-strategies-expert
description: Expert-level hedge fund strategies and alternative investments. Use when working with long/short equity, global macro, event driven, relative value, managed futures, arbitrage, activist investing, or fund structure. Also use when the user mentions 'long/short', 'global macro', 'event driven', 'merger arbitrage', 'convertible arb', 'managed futures', 'CTA', 'activist investor', 'short selling', 'alpha generation', 'fund of funds', or 'hedge fund structure'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Hedge Fund Strategies Expert

You are a world-class hedge fund analyst and portfolio manager with deep expertise in all major hedge fund strategies including long/short equity, global macro, event driven, relative value, managed futures, and quantitative strategies.

## Before Starting

1. **Strategy** — Long/short, global macro, event driven, relative value, or quant?
2. **Asset class** — Equities, fixed income, FX, commodities, or multi-asset?
3. **Goal** — Alpha generation, risk reduction, uncorrelated returns, or learning?
4. **Timeframe** — Short term (days), medium (weeks-months), or long term (years)?
5. **Capital** — Retail adaption or institutional implementation?

---

## Core Expertise Areas

- **Long/Short Equity**: pair trades, sector rotation, net exposure management
- **Global Macro**: top-down thematic trades across all asset classes
- **Event Driven**: M&A arb, spinoffs, distressed, special situations
- **Relative Value**: fixed income arb, convertible arb, vol arb
- **Managed Futures/CTA**: trend following, systematic multi-asset
- **Quantitative**: statistical arb, factor investing, ML strategies
- **Short Selling**: identifying frauds, overvalued companies, structural shorts
- **Fund Structure**: fees, terms, risk management, prime brokerage

---

## Long/Short Equity
```python
def long_short_framework():
    return {
        'Core Concept': {
            'long':     'Buy undervalued or high-quality companies',
            'short':    'Sell overvalued, deteriorating, or fraudulent companies',
            'net_exp':  'Net exposure = longs - shorts (typically 30-70% net long)',
            'gross_exp':'Gross exposure = longs + shorts (typically 100-200%)',
            'goal':     'Generate alpha on both sides, reduce market beta'
        },
        'Gross vs Net Exposure': {
            '130/30':   'Long 130%, short 30% — net 100%, gross 160%',
            '150/50':   'Long 150%, short 50% — net 100%, gross 200%',
            'Market Neutral': 'Long 100%, short 100% — net 0%, gross 200%',
            'Variable':  'Adjust net exposure based on market conditions'
        },
        'Long Book Criteria': [
            'Undervalued vs intrinsic value (margin of safety)',
            'Improving fundamentals — earnings revisions up',
            'Competitive moat strengthening',
            'Insider buying, share buybacks',
            'Catalyst: earnings beat, product launch, spin-off'
        ],
        'Short Book Criteria': [
            'Overvalued vs fundamentals — multiple expansion bubble',
            'Deteriorating business — declining revenue, margin compression',
            'Accounting irregularities — aggressive revenue recognition',
            'Management credibility issues',
            'Structural disruption — obsolete business model',
            'High short interest already (crowded short risk)',
            'Catalyst: earnings miss, guidance cut, regulatory action'
        ]
    }

def pair_trade_analysis(stock_a, stock_b, lookback=252):
    """
    Statistical pair trade setup.
    Long the relatively cheap, short the relatively expensive.
    """
    import pandas as pd
    import numpy as np
    from statsmodels.tsa.stattools import coint

    prices_a = stock_a['prices']
    prices_b = stock_b['prices']

    # Test for cointegration
    _, pvalue, _ = coint(prices_a, prices_b)

    # Calculate spread
    hedge_ratio = np.cov(prices_a, prices_b)[0,1] / np.var(prices_b)
    spread      = prices_a - hedge_ratio * prices_b
    zscore      = (spread - spread.mean()) / spread.std()
    current_z   = zscore.iloc[-1]

    # Relative valuation metrics
    pe_ratio_a  = stock_a.get('pe_ratio', 0)
    pe_ratio_b  = stock_b.get('pe_ratio', 0)
    pe_spread   = pe_ratio_a - pe_ratio_b

    return {
        'cointegration_pvalue': round(pvalue, 4),
        'cointegrated':         pvalue < 0.05,
        'hedge_ratio':          round(hedge_ratio, 4),
        'current_zscore':       round(current_z, 3),
        'pe_spread':            round(pe_spread, 2),
        'signal': {
            'action':   f'Long {stock_b["name"]}, Short {stock_a["name"]}'
                        if current_z > 2 else
                        f'Long {stock_a["name"]}, Short {stock_b["name"]}'
                        if current_z < -2 else 'No signal',
            'strength': 'Strong' if abs(current_z) > 2.5 else
                        'Moderate' if abs(current_z) > 2.0 else 'Weak'
        }
    }

def net_exposure_management(market_regime, vix_level):
    """Dynamically adjust net exposure based on market conditions."""
    if vix_level > 35:
        net_target   = 0.10   # near market neutral in panic
        gross_target = 0.80
    elif vix_level > 25:
        net_target   = 0.25
        gross_target = 1.20
    elif market_regime == 'bull_trending':
        net_target   = 0.60
        gross_target = 1.60
    elif market_regime == 'late_cycle':
        net_target   = 0.35
        gross_target = 1.40
    else:
        net_target   = 0.50
        gross_target = 1.50

    return {
        'net_exposure':   f"{net_target*100:.0f}%",
        'gross_exposure': f"{gross_target*100:.0f}%",
        'implied_short':  f"{(gross_target - net_target)/2*100:.0f}%"
    }
```

---

## Global Macro
```python
def global_macro_framework():
    return {
        'Top Down Process': [
            '1. Identify macro regime: growth, inflation, policy cycle',
            '2. Determine which economies are in which phase',
            '3. Find divergences: countries at different cycle points',
            '4. Express views across asset classes: rates, FX, equities',
            '5. Size positions by conviction and risk budget'
        ],
        'Classic Macro Themes': {
            'Rate Divergence': {
                'trade':   'Long currency of hiking CB, short currency of cutting CB',
                'example': 'Long USD/JPY when Fed hiking while BOJ holds zero rates',
                'risk':    'Intervention risk, sudden policy reversal'
            },
            'Inflation Regime': {
                'trade':   'Long commodities + TIPS + energy in reflation',
                'example': '2021-2022: long oil, copper, TIPS against long bonds',
                'risk':    'Demand destruction, policy overtightening'
            },
            'EM vs DM Rotation': {
                'trade':   'Long EM when USD weakening + commodity cycle up',
                'example': 'Long EEM, EM bonds when Fed pivots to cutting',
                'risk':    'Sudden USD reversal, EM political risk'
            },
            'Yield Curve Trades': {
                'trade':   'Steepener when Fed cutting, flattener when hiking',
                'example': 'Long 2yr, short 10yr in late cycle (flattener)',
                'risk':    'Curve can stay inverted longer than expected'
            },
            'Safe Haven': {
                'trade':   'Long gold + long JPY + long US Treasuries in risk-off',
                'example': 'Classic flight-to-quality in recession/crisis',
                'risk':    'Safe haven correlation breaks in liquidity crisis'
            }
        }
    }

def macro_trade_construction(theme, conviction_level,
                               risk_budget_pct=0.02):
    """
    Structure a macro trade with multiple legs.
    """
    trade_structures = {
        'Fed Pivot (Dovish)': {
            'core':      'Long 10yr Treasuries (TLT)',
            'extension': 'Long gold (GLD)',
            'equity':    'Long growth/tech (QQQ)',
            'fx':        'Short USD (DXY puts or UUP puts)',
            'em':        'Long EM (EEM)',
            'sizing':    f"Core: {risk_budget_pct*100:.1f}% risk each leg"
        },
        'Stagflation': {
            'core':      'Long gold + Long commodities (DJP)',
            'extension': 'Long energy stocks (XLE)',
            'rates':     'Short long duration bonds (TBT)',
            'equity':    'Short growth, long value/energy',
            'fx':        'Long commodity currencies (AUD, CAD)'
        },
        'Global Recession': {
            'core':      'Long US Treasuries + Long JPY',
            'extension': 'Long VIX (UVXY) or put spreads on SPY',
            'credit':    'Short HY credit (HYG puts)',
            'em':        'Short EM (EEM puts or short EWZ)',
            'commodity': 'Short copper, oil'
        }
    }
    return trade_structures.get(theme, {})
```

---

## Event Driven
```python
def event_driven_strategies():
    return {
        'Merger Arbitrage': {
            'concept':   'Buy target after deal announced, short acquirer (optional)',
            'spread':    'Deal price - current price = gross spread',
            'annualized':'Gross spread / deal price * (365 / days to close)',
            'risks':     ['Deal break', 'Regulatory block', 'Financing falls through'],
            'edge':      'Capture spread while managing deal break risk',
            'sizing':    'Size by deal break probability and portfolio concentration'
        },
        'Spin-offs': {
            'concept':   'Parent spins off subsidiary as independent company',
            'edge':      'Spinco often sold by index funds (wrong index), undervalued',
            'timing':    'Buy spinco in first 6-12 months after separation',
            'research':  'Read Form 10 filing carefully — management incentives key',
            'examples':  'PayPal from eBay, Zoetis from Pfizer'
        },
        'Distressed Debt': {
            'concept':   'Buy debt of companies in or near bankruptcy',
            'strategies':['Loan-to-own: buy debt, convert to equity in reorg',
                          'Pure credit: buy cheap debt, sell at recovery',
                          'Post-reorg equity: buy newly issued equity cheaply'],
            'skills':    'Bankruptcy law, capital structure, liquidation analysis',
            'risk':      'Illiquid, long timelines, binary outcomes'
        },
        'Activist Investing': {
            'concept':   'Buy large stake, push for strategic change',
            'catalysts': ['Board seat', 'CEO change', 'Buybacks', 'Sale of company',
                         'Spin-off', 'Cost cuts'],
            'followers': 'Track activist filings (13D) and ride their coattails',
            'risk':      'Management resistance, campaign fails, stock falls'
        },
        'Special Situations': {
            'concept':   'Corporate actions creating mispricings',
            'types':     ['Rights offerings', 'Dutch tender offers',
                         'Share class conversions', 'Stub trades',
                         'Post-bankruptcy equities', 'Rights issues']
        }
    }

def merger_arb_analysis(target_price, deal_price, current_price,
                          days_to_close, deal_break_probability=0.05,
                          break_price=None):
    """
    Merger arbitrage spread analysis and expected value.
    """
    if break_price is None:
        break_price = current_price * 0.75  # assume 25% fall on break

    gross_spread    = deal_price - current_price
    spread_pct      = gross_spread / current_price
    annualized_ret  = spread_pct * (365 / days_to_close)

    # Expected value analysis
    prob_close      = 1 - deal_break_probability
    ev_close        = prob_close * (deal_price - current_price)
    ev_break        = deal_break_probability * (break_price - current_price)
    expected_value  = ev_close + ev_break
    ev_annualized   = (expected_value / current_price) * (365/days_to_close)

    return {
        'current_price':      current_price,
        'deal_price':         deal_price,
        'gross_spread':       round(gross_spread, 2),
        'spread_pct':         round(spread_pct * 100, 3),
        'annualized_return':  round(annualized_ret * 100, 2),
        'break_probability':  f"{deal_break_probability*100:.1f}%",
        'expected_value':     round(expected_value, 2),
        'ev_annualized':      round(ev_annualized * 100, 2),
        'verdict':            'Attractive' if ev_annualized > 0.08 else
                              'Marginal'   if ev_annualized > 0.04 else
                              'Unattractive'
    }
```

---

## Managed Futures / CTA
```python
def trend_following_system(prices, fast_period=50, slow_period=200,
                             atr_period=20, risk_per_trade=0.01):
    """
    Classic CTA trend following system.
    Signal: price above/below moving average crossover.
    Sizing: volatility-adjusted (ATR-based).
    """
    import pandas as pd
    import numpy as np

    df          = pd.DataFrame({'close': prices})
    df['fast']  = df['close'].ewm(span=fast_period).mean()
    df['slow']  = df['close'].ewm(span=slow_period).mean()
    df['signal']= np.where(df['fast'] > df['slow'], 1, -1)

    # ATR for position sizing
    df['tr']    = df['close'].diff().abs()
    df['atr']   = df['tr'].ewm(span=atr_period).mean()

    # Position size: risk_per_trade / (atr * contract_value)
    df['position_size'] = risk_per_trade / df['atr']

    # Strategy returns
    df['returns']       = df['close'].pct_change()
    df['strat_returns'] = df['signal'].shift(1) * df['returns']

    return df

def cta_strategy_types():
    return {
        'Trend Following': {
            'description': 'Buy what is going up, sell what is going down',
            'timeframes':  'Medium to long term (weeks to months)',
            'instruments': 'Futures across equities, rates, FX, commodities',
            'edge':        'Behavioral — anchoring, under-reaction to trends',
            'drawdown':    'Suffers in choppy, range-bound markets',
            'correlation': 'Negative correlation to equities in crises (crisis alpha)'
        },
        'Mean Reversion': {
            'description': 'Fade extreme moves — buy oversold, sell overbought',
            'timeframes':  'Short term (hours to days)',
            'edge':        'Overreaction to news, liquidity provision',
            'risk':        'Trending markets cause sustained losses'
        },
        'Carry': {
            'description': 'Long high-carry assets, short low-carry assets',
            'instruments': 'FX carry, bond carry, commodity carry',
            'edge':        'Risk premium for holding illiquid or risky assets',
            'risk':        'Sudden risk-off — carry unwind is fast and brutal'
        },
        'Systematic Macro': {
            'description': 'Rules-based global macro signals',
            'signals':     ['Macro momentum', 'Value', 'Carry', 'Sentiment'],
            'edge':        'Disciplined execution without emotional override'
        }
    }
```

---

## Short Selling
```python
def short_selling_framework():
    return {
        'Categories': {
            'Overvaluation': {
                'thesis':   'Stock priced for perfection — any miss = crash',
                'metrics':  'P/S > 30x on negative FCF, EV/EBITDA > 50x',
                'catalyst': 'Earnings miss, guidance cut, multiple compression',
                'risk':     'Can stay expensive longer than expected (TSLA 2019-2020)'
            },
            'Fundamental Deterioration': {
                'thesis':   'Business is structurally declining',
                'signals':  ['Revenue declining', 'Margin compression',
                            'Customer churn rising', 'Market share loss'],
                'catalyst': 'Quarterly results confirm trend',
                'risk':     'Management turns around business'
            },
            'Accounting Fraud': {
                'thesis':   'Financial statements do not reflect reality',
                'signals':  ['Revenue growing but cash not',
                            'Receivables growing faster than revenue',
                            'Auditor changes', 'CFO departures',
                            'Related party transactions',
                            'Frequent restatements'],
                'catalyst': 'Short seller report, SEC investigation, restatement',
                'risk':     'Timing — fraud can persist for years'
            },
            'Structural Disruption': {
                'thesis':   'Business model being disrupted by technology/competition',
                'examples': 'Blockbuster vs Netflix, Kodak vs digital',
                'catalyst': 'Disruptor gaining market share visibly',
                'risk':     'Disruption takes longer than expected'
            }
        }
    }

def short_squeeze_risk(short_interest_pct, days_to_cover,
                        float_pct, recent_price_move):
    """Assess risk of short squeeze on a position."""
    score = 0
    flags = []

    if short_interest_pct > 0.20:
        score += 3
        flags.append(f"Very high short interest: {short_interest_pct*100:.1f}%")
    elif short_interest_pct > 0.10:
        score += 2

    if days_to_cover > 5:
        score += 3
        flags.append(f"High days to cover: {days_to_cover:.1f}")
    elif days_to_cover > 3:
        score += 1

    if float_pct < 0.20:
        score += 2
        flags.append(f"Low float: {float_pct*100:.1f}%")

    if recent_price_move > 0.20:
        score += 2
        flags.append(f"Already moving up: +{recent_price_move*100:.1f}%")

    return {
        'squeeze_risk_score': score,
        'risk_level':         'Extreme' if score >= 8 else
                              'High'    if score >= 5 else
                              'Moderate'if score >= 3 else 'Low',
        'flags':              flags,
        'recommendation':     'Reduce or exit short' if score >= 6 else
                              'Monitor closely'      if score >= 4 else
                              'Position acceptable'
    }
```

---

## Relative Value
```python
def relative_value_strategies():
    return {
        'Convertible Bond Arbitrage': {
            'concept':   'Long convertible bond, short underlying equity',
            'edge':      'Convertibles often mispriced — buy cheap optionality',
            'delta_hedge':'Short stock to neutralize equity exposure',
            'profit':    'Gamma trading — rebalance delta as stock moves',
            'risk':      'Credit risk on bond, short squeeze on equity'
        },
        'Fixed Income Relative Value': {
            'on_the_run': 'Newest Treasury more liquid, trades rich vs off-the-run',
            'trade':      'Long off-the-run, short on-the-run (cheaper vs expensive)',
            'risk':       'Convergence can take time, liquidity crises widen spread'
        },
        'Volatility Arbitrage': {
            'concept':   'Trade difference between implied and realized volatility',
            'long_vol':  'Buy cheap options, delta hedge — profit from vol expansion',
            'short_vol': 'Sell expensive options, delta hedge — collect premium',
            'vix_arb':   'VIX futures vs S&P realized vol discrepancy'
        },
        'Capital Structure Arbitrage': {
            'concept':   'Trade different securities of same company',
            'example':   'Long bonds vs short equity when CDS/equity mispriced',
            'tools':     'Merton model to find mispricing between debt and equity',
            'risk':      'Correlation between instruments can change suddenly'
        }
    }
```

---

## Fund Structure & Terms
```python
def hedge_fund_terms():
    return {
        'Fee Structure': {
            '2_and_20':     '2% management fee + 20% performance fee (standard)',
            'high_water':   'Performance fee only on new profits above prior peak',
            'hurdle_rate':  'Minimum return before performance fee kicks in (e.g. 8%)',
            'crystallization': 'When performance fees are locked in (annual typical)',
            'trend':        'Fees compressing — 1.5/17 or 1/15 more common now'
        },
        'Liquidity Terms': {
            'lock_up':      'Period investor cannot redeem (1-2 years typical)',
            'notice_period':'Required notice before redemption (30-90 days)',
            'gates':        'Fund can limit redemptions in stress (10-25% quarterly)',
            'side_pockets': 'Illiquid assets segregated, no redemption until liquidated'
        },
        'Risk Limits': {
            'gross_exposure':'Max total long + short as % of NAV',
            'net_exposure':  'Max net long or short directional bias',
            'single_name':   'Max % of NAV in single position (5-10%)',
            'sector_limit':  'Max sector concentration (20-30%)',
            'var_limit':     'Daily VaR typically 1-3% of NAV'
        },
        'Prime Brokerage': {
            'role':          'Provides leverage, stock lending, clearing',
            'margin':        'Typically 20-50% initial margin for equities',
            'stock_borrow':  'HTB (hard to borrow) stocks cost 5-30%+ annually',
            'rehypothecation':'PB can use your assets as their own collateral'
        }
    }

def performance_fee_calculation(beginning_nav, ending_nav,
                                  high_water_mark, mgmt_fee_pct=0.02,
                                  perf_fee_pct=0.20, hurdle=0.08):
    """Calculate hedge fund fees for a period."""
    gross_return    = (ending_nav - beginning_nav) / beginning_nav
    mgmt_fee        = beginning_nav * mgmt_fee_pct

    # Performance fee only above HWM and hurdle
    new_hwm         = max(high_water_mark, beginning_nav * (1 + hurdle))
    perf_base       = max(0, ending_nav - new_hwm)
    perf_fee        = perf_base * perf_fee_pct

    net_nav         = ending_nav - mgmt_fee - perf_fee
    net_return      = (net_nav - beginning_nav) / beginning_nav

    return {
        'gross_return':     round(gross_return * 100, 2),
        'net_return':       round(net_return * 100, 2),
        'management_fee':   round(mgmt_fee, 0),
        'performance_fee':  round(perf_fee, 0),
        'total_fees':       round(mgmt_fee + perf_fee, 0),
        'fee_drag':         round((gross_return - net_return) * 100, 2),
        'new_hwm':          round(max(high_water_mark, ending_nav - perf_fee), 0)
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Crowded longs/shorts | Everyone exits at same time | Track crowding via 13F filings |
| Short squeeze ignoring | Small short destroyed by squeeze | Always check days to cover |
| Merger deal break | Stock falls 20-30% instantly | Size arb positions by deal risk |
| Factor exposure unhedged | Long/short has hidden beta | Hedge sector and factor exposures |
| Illiquidity mismatch | Investors redeem, cannot sell | Match fund liquidity to portfolio |
| High water mark trap | Never earn performance fees | Reset HWM or reduce management fee |
| Leverage in crisis | Forced liquidation at worst time | Stress test leverage at 2008 levels |

---

## Best Practices

- **Know your edge** — every strategy needs a behavioral or structural reason to work
- **Manage crowding** — most popular trades are most dangerous
- **Hedge your hedges** — long/short does not mean market neutral automatically
- **Think about liquidity** — can you exit in a crisis without moving the market?
- **Crisis alpha** — best strategies provide positive returns in equity crashes
- **Fees matter** — 2 and 20 requires consistent alpha to beat passive investing
- **Risk limits first** — define max loss before building the book

---

## Related Skills

- **quantitative-finance-expert**: Systematic strategy development
- **risk-management-expert**: Portfolio risk and exposure management
- **behavioral-finance-expert**: Behavioral edges in L/S equity
- **derivatives-expert**: Options strategies in event driven
- **macro-economics-expert**: Global macro framework
