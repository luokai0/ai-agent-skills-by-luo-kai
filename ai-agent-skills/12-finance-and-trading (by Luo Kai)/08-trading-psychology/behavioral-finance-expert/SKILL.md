---
author: luo-kai
name: behavioral-finance-expert
description: Expert-level behavioral finance and market psychology. Use when analyzing investor biases, market sentiment, crowd psychology, irrational market behavior, cognitive errors in investing, or the psychological drivers of bubbles and crashes. Also use when the user mentions 'cognitive bias', 'loss aversion', 'overconfidence', 'herd behavior', 'anchoring', 'market sentiment', 'fear and greed', 'bubble', 'panic selling', 'disposition effect', or 'mental accounting'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Behavioral Finance Expert

You are a world-class behavioral finance expert with deep knowledge of cognitive biases, market psychology, investor behavior, sentiment analysis, bubble dynamics, and how to exploit or defend against behavioral patterns in financial markets.

## Before Starting

1. **Focus** — Investor biases, market sentiment, bubble analysis, or decision making?
2. **Application** — Personal investing, trading edge, research, or risk management?
3. **Asset class** — Stocks, crypto, real estate, or broad markets?
4. **Goal** — Identify bias, exploit inefficiency, or improve decisions?
5. **Level** — Individual investor psychology or aggregate market behavior?

---

## Core Expertise Areas

- **Cognitive Biases**: systematic errors in thinking and judgment
- **Emotional Biases**: fear, greed, overconfidence, loss aversion
- **Market Anomalies**: momentum, value premium, calendar effects
- **Bubble Dynamics**: formation, stages, crash anatomy
- **Sentiment Analysis**: fear/greed index, put/call ratio, surveys
- **Prospect Theory**: how humans actually evaluate gains and losses
- **Heuristics**: mental shortcuts that cause systematic errors
- **Debiasing**: frameworks to make better financial decisions

---

## Core Cognitive Biases
```python
def cognitive_biases_catalog():
    return {
        'Anchoring': {
            'description': 'Over-rely on first piece of information received',
            'market_example': 'Stock was $100, now $60 — feels cheap even if $40 is fair value',
            'trading_impact': 'Set stop losses and targets relative to purchase price not fair value',
            'fix': 'Always ask: what would fair value be if I had no prior price?'
        },
        'Confirmation Bias': {
            'description': 'Seek information that confirms existing beliefs',
            'market_example': 'Only read bullish analysis on stocks you own',
            'trading_impact': 'Hold losing positions too long, miss contrary evidence',
            'fix': 'Actively seek out the strongest bear case for every position'
        },
        'Overconfidence': {
            'description': 'Overestimate own ability and precision of knowledge',
            'market_example': 'Believe you can time the market, trade too frequently',
            'trading_impact': 'Excessive trading, under-diversification, too-small stops',
            'fix': 'Track your predictions vs outcomes — calibrate with data'
        },
        'Availability Heuristic': {
            'description': 'Judge probability by how easily examples come to mind',
            'market_example': 'After 2008, investors avoid all banks forever',
            'trading_impact': 'Over-weight recent dramatic events, under-weight base rates',
            'fix': 'Use historical base rates, not vivid recent memories'
        },
        'Representativeness': {
            'description': 'Judge by similarity to stereotypes, ignore base rates',
            'market_example': 'Great company = great stock (ignores valuation)',
            'trading_impact': 'Overpay for quality, underpay for ugly but cheap',
            'fix': 'Separate business quality from stock valuation always'
        },
        'Hindsight Bias': {
            'description': 'After event, believe you knew it would happen',
            'market_example': 'Of course 2008 was going to crash — it was obvious',
            'trading_impact': 'Overconfidence in predicting future crashes',
            'fix': 'Keep a decision journal — record reasoning before outcomes'
        },
        'Mental Accounting': {
            'description': 'Treat money differently based on its source or purpose',
            'market_example': 'Trade gambling winnings recklessly vs salary carefully',
            'trading_impact': 'House money effect — take excessive risk with profits',
            'fix': 'A dollar is a dollar regardless of where it came from'
        },
        'Framing Effect': {
            'description': 'Decision changes based on how choices are presented',
            'market_example': '"90% survival rate" vs "10% mortality rate" — same thing',
            'trading_impact': 'React differently to same data depending on framing',
            'fix': 'Reframe every decision from multiple angles before deciding'
        },
        'Recency Bias': {
            'description': 'Over-weight recent events, under-weight long-term history',
            'market_example': 'After 10yr bull market, cannot imagine bear market',
            'trading_impact': 'Chase recent performance, abandon mean-reverting strategies',
            'fix': 'Study long-term market history across multiple cycles'
        },
        'Status Quo Bias': {
            'description': 'Prefer current state, resist change',
            'market_example': 'Hold inherited stock forever regardless of quality',
            'trading_impact': 'Fail to rebalance, hold bad positions out of inertia',
            'fix': 'Regular portfolio review: would you buy this today at this price?'
        }
    }
```

---

## Emotional Biases
```python
def emotional_biases_catalog():
    return {
        'Loss Aversion': {
            'description':    'Losses feel ~2x more painful than equal gains feel good',
            'prospect_theory': 'Kahneman & Tversky: utility of loss > utility of gain',
            'market_example': 'Hold losers too long hoping to break even',
            'trading_impact': [
                'Disposition effect: sell winners too early, hold losers too long',
                'Risk aversion in gains domain, risk seeking in loss domain',
                'Refuse to cut losses — let small loss become catastrophic'
            ],
            'fix': 'Pre-commit to exit rules before entering — remove emotion from exit'
        },
        'Fear of Missing Out (FOMO)': {
            'description':    'Fear of not participating in rising markets',
            'market_example': 'Buy Bitcoin at all-time high because everyone is talking about it',
            'trading_impact': 'Chase parabolic moves, buy tops, panic into positions',
            'fix': 'Define entry criteria in advance — only enter on YOUR signal'
        },
        'Panic Selling': {
            'description':    'Irrational selling during market drops',
            'market_example': 'Sell everything in March 2020 crash at exact bottom',
            'trading_impact': 'Lock in losses at worst time, miss recovery',
            'fix': 'Pre-write your investment thesis and read it during drawdowns'
        },
        'Regret Aversion': {
            'description':    'Avoid actions that might cause regret',
            'market_example': 'Do not buy after missing initial move — fear of FOMO regret',
            'trading_impact': 'Paralysis, missed opportunities, holding cash too long',
            'fix': 'Focus on process quality not outcome — good process can have bad outcomes'
        },
        'Endowment Effect': {
            'description':    'Value things more once you own them',
            'market_example': 'Demand more to sell a stock than you would pay to buy it',
            'trading_impact': 'Hold positions longer than rational, resist trimming winners',
            'fix': 'Ask: if I did not own this, would I buy it today at this price?'
        },
        'Herding': {
            'description':    'Follow crowd behavior regardless of own analysis',
            'market_example': 'Buy meme stocks because everyone else is',
            'trading_impact': 'Amplify bubbles and crashes, poor entry/exit timing',
            'fix': 'Have a written investment thesis independent of what others say'
        },
        'Overoptimism': {
            'description':    'Systematically overestimate positive outcomes',
            'market_example': 'Assume your stock picks will outperform — most do not',
            'trading_impact': 'Under-estimate risk, over-concentrate, under-hedge',
            'fix': 'Apply base rates: most active traders underperform index funds'
        }
    }
```

---

## Prospect Theory
```python
def prospect_theory_framework():
    """
    Kahneman & Tversky's Prospect Theory (1979)
    How humans actually evaluate outcomes vs expected utility theory
    """
    return {
        'Key Findings': {
            'Reference Dependence': 'Evaluate outcomes relative to reference point (purchase price)',
            'Loss Aversion':        'Lambda ≈ 2.25 — losses weighted ~2x more than gains',
            'Diminishing Sensitivity': 'Each extra gain/loss matters less (concave for gains, convex for losses)',
            'Probability Weighting': 'Overweight small probabilities, underweight large ones'
        },
        'Implications': {
            'Disposition Effect':   'Sell winners (concave gains) hold losers (convex losses)',
            'Insurance Demand':     'Overpay for insurance (overweight small loss probability)',
            'Lottery Demand':       'Overpay for lotto tickets (overweight tiny win probability)',
            'Break-Even Effect':    'Take more risk when close to breaking even on loss'
        },
        'Trading Applications': {
            'Set absolute stops': 'Remove loss domain decision-making entirely',
            'Scale out winners':  'Matches natural preference — take some gains early',
            'Avoid P&L watching': 'Real-time P&L triggers loss aversion responses',
            'Use position limits': 'Pre-commit to max position size prevents doubling down'
        }
    }

def value_function(outcome, lambda_loss=2.25, alpha=0.88):
    """
    Kahneman-Tversky value function.
    Concave for gains, convex for losses, steeper for losses.
    """
    if outcome >= 0:
        return outcome ** alpha
    else:
        return -lambda_loss * (abs(outcome) ** alpha)
```

---

## Market Sentiment Analysis
```python
def sentiment_indicators():
    return {
        'Fear & Greed Index (CNN)': {
            'range':        '0 (extreme fear) to 100 (extreme greed)',
            'components':   ['VIX', 'Put/Call ratio', 'Junk bond demand',
                            'Market momentum', 'Safe haven demand',
                            'Stock price breadth', 'Stock price strength'],
            'contrarian':   'Buy near 0-15, consider selling near 85-100',
            'limitation':   'Better for timing entry than exit'
        },
        'Put/Call Ratio': {
            'formula':      'Put volume / Call volume',
            'bearish':      '> 1.0 — more puts than calls = fear',
            'bullish':      '< 0.7 — more calls than puts = complacency',
            'contrarian':   'Extreme readings signal potential reversal',
            'equity_pcr':   '> 0.80 = fear, < 0.60 = greed (equity only)'
        },
        'VIX (Fear Gauge)': {
            'description':  'Implied volatility of S&P 500 options',
            'low':          '< 15 = complacency, potential for spike',
            'normal':       '15-25 = normal market conditions',
            'elevated':     '25-35 = fear, hedging demand rising',
            'extreme':      '> 40 = panic, historical buy signal',
            'vix_spikes':   'Mean-revert — spikes above 40 are buying opportunities'
        },
        'AAII Sentiment Survey': {
            'description':  'Weekly survey of individual investor sentiment',
            'contrarian':   'When >55% bullish = historically poor returns ahead',
            'buy_signal':   'When >50% bearish = historically good entry',
            'limitation':   'Noisy week-to-week, better as 4-week moving average'
        },
        'Short Interest': {
            'high_short':   'High short interest = potential short squeeze fuel',
            'days_to_cover':'Short interest / average daily volume',
            'squeeze_risk': 'Days to cover > 5 = significant squeeze potential',
            'signal':       'Declining short interest in rally = confirmation'
        },
        'Insider Buying': {
            'signal':       'Cluster of insider buys = management confidence',
            'strongest':    'Multiple insiders buying same stock same period',
            'less_useful':  'Insider selling — many reasons to sell, one to buy'
        },
        'Fund Flows': {
            'outflows':     'Investors pulling money from equity funds = fear',
            'inflows':      'Record inflows = late-cycle euphoria signal',
            'contrarian':   'Maximum outflows near market bottoms historically'
        }
    }

def sentiment_score_model(indicators):
    """
    Composite sentiment score from multiple indicators.
    Returns score 0-100 (0=extreme fear, 100=extreme greed)
    """
    score = 0
    weights = {
        'fear_greed_index': 0.25,
        'put_call_ratio':   0.20,
        'vix_score':        0.20,
        'aaii_bull_pct':    0.15,
        'fund_flows':       0.10,
        'insider_buying':   0.10
    }

    # Normalize each indicator to 0-100
    normalized = {
        'fear_greed_index': indicators.get('fear_greed_index', 50),
        'put_call_ratio':   max(0, min(100, (1.5 - indicators.get('put_call_ratio', 1.0)) / 1.5 * 100)),
        'vix_score':        max(0, min(100, (50 - indicators.get('vix', 20)) / 50 * 100)),
        'aaii_bull_pct':    indicators.get('aaii_bull_pct', 40),
        'fund_flows':       indicators.get('fund_flows_score', 50),
        'insider_buying':   indicators.get('insider_buying_score', 50)
    }

    composite = sum(
        normalized[k] * weights[k]
        for k in weights
    )

    return {
        'composite_score': round(composite, 1),
        'regime':          'Extreme Fear'  if composite < 20 else
                           'Fear'          if composite < 40 else
                           'Neutral'       if composite < 60 else
                           'Greed'         if composite < 80 else
                           'Extreme Greed',
        'contrarian_signal': 'BUY signal'  if composite < 20 else
                             'SELL signal' if composite > 80 else
                             'Neutral'
    }
```

---

## Bubble Dynamics
```python
def bubble_stages():
    """
    Minsky-Kindleberger bubble model — 5 stages.
    """
    return {
        'Stage 1 — Displacement': {
            'description': 'New technology, policy, or paradigm creates opportunity',
            'examples':    'Internet (1990s), zero rates (2010s), DeFi (2020)',
            'sentiment':   'Early adopters excited, mainstream skeptical',
            'valuation':   'Reasonable — story has merit',
            'action':      'Smart money accumulating quietly'
        },
        'Stage 2 — Boom': {
            'description': 'Prices rise, media attention grows, credit expands',
            'examples':    'Nasdaq 1997-1998, housing 2004-2006, crypto 2020',
            'sentiment':   'Optimistic, FOMO beginning',
            'valuation':   'Stretched but justifiable with assumptions',
            'action':      'Institutional money entering, early retail interest'
        },
        'Stage 3 — Euphoria': {
            'description': '"This time is different" — old valuation metrics abandoned',
            'examples':    'Pets.com IPO, NFTs at $69M, ARKK at $156',
            'sentiment':   'Extreme greed, everyone is a genius',
            'valuation':   'Detached from fundamentals, narrative-driven',
            'warning_signs': [
                'Taxi drivers giving stock tips',
                'Record IPOs and SPACs',
                'Leverage at all-time highs',
                'Short sellers capitulating',
                '"Paradigm shift" language everywhere'
            ]
        },
        'Stage 4 — Distress': {
            'description': 'Insiders begin selling, credit tightens, cracks appear',
            'examples':    'March 2000, August 2007, November 2021 crypto peak',
            'sentiment':   'Denial — buying the dip mentality',
            'valuation':   'Still elevated, dead cat bounces',
            'action':      'Smart money exiting, retail doubling down'
        },
        'Stage 5 — Revulsion': {
            'description': 'Panic selling, forced liquidations, complete despair',
            'examples':    'Nasdaq -78% 2000-2002, housing 2008-2009, crypto -80%+',
            'sentiment':   'Extreme fear, "never investing again"',
            'valuation':   'Often overcorrects — becomes genuinely cheap',
            'action':      'Smart money accumulating again at distressed prices'
        }
    }

def bubble_checklist(asset_data):
    """Score current bubble risk for an asset."""
    score  = 0
    flags  = []

    checks = [
        ('price_above_200ma_pct' , 50,  2, 'Price >50% above 200-day MA'),
        ('pe_ratio'              , 50,  2, 'P/E ratio above 50x'),
        ('retail_participation'  , 0.7, 2, 'Retail >70% of trading volume'),
        ('leverage_ratio'        , 3,   2, 'Margin debt at record highs'),
        ('media_mentions_spike'  , True,1, 'Mainstream media saturation'),
        ('record_issuance'       , True,2, 'Record IPOs/token launches'),
        ('short_interest_low'    , 0.02,1, 'Short interest below 2%'),
        ('ipo_first_day_returns' , 0.5, 1, 'Average IPO first day gain >50%'),
    ]

    for key, threshold, weight, description in checks:
        val = asset_data.get(key)
        if val is None:
            continue
        triggered = val > threshold if isinstance(threshold, (int,float)) else val == threshold
        if triggered:
            score += weight
            flags.append(description)

    return {
        'bubble_score': score,
        'max_score':    13,
        'risk_level':   'Extreme' if score >= 8 else
                        'High'    if score >= 5 else
                        'Moderate'if score >= 3 else 'Low',
        'flags':        flags
    }
```

---

## Market Anomalies & Behavioral Edges
```python
def market_anomalies():
    return {
        'Momentum (WML)': {
            'finding':     'Winners keep winning, losers keep losing (3-12 months)',
            'explanation': 'Underreaction to news, herding, slow diffusion of info',
            'edge':        'Long top decile, short bottom decile returns',
            'decay':       'Reverses at 12+ months (long-term mean reversion)',
            'risk':        'Momentum crashes in sharp reversals (2009, 2020)'
        },
        'Value Premium': {
            'finding':     'Cheap stocks (high B/M, low P/E) outperform long term',
            'explanation': 'Overreaction to bad news, recency bias, extrapolation',
            'edge':        'Long cheap stocks, short expensive stocks',
            'patience':    'Can underperform for years (1990s growth mania)'
        },
        'Post-Earnings Drift': {
            'finding':     'Stocks continue drifting in direction of earnings surprise',
            'explanation': 'Investors underreact to earnings news initially',
            'edge':        'Buy stocks with large positive surprises day of report',
            'decay':       'Drift persists 1-3 months after announcement'
        },
        'Small Cap Premium': {
            'finding':     'Small caps outperform large caps long term',
            'explanation': 'Neglect, illiquidity premium, higher growth potential',
            'caveat':      'Has weakened since Fama-French published it (1992)'
        },
        'January Effect': {
            'finding':     'Small caps outperform in January',
            'explanation': 'Tax-loss selling in December, buying back in January',
            'caveat':      'Largely arbitraged away in recent decades'
        },
        'Earnings Announcement Premium': {
            'finding':     'Stocks earn excess returns around earnings announcements',
            'explanation': 'Risk premium for uncertainty resolution',
            'edge':        'Long straddle before earnings for vol expansion'
        },
        'IPO Underperformance': {
            'finding':     'IPOs underperform market by 3-5yr after listing',
            'explanation': 'Overoptimism, insider information advantage, timing',
            'edge':        'Avoid buying IPOs in secondary market at high prices'
        }
    }
```

---

## Debiasing Framework
```python
def debiasing_checklist():
    return {
        'Before Entering Trade': [
            'Write down your thesis — what has to be true for this to work?',
            'What is the strongest counter-argument to your view?',
            'What price action would tell you your thesis is wrong?',
            'Are you buying because of FOMO or because of analysis?',
            'What is your position size — is it driven by conviction or hope?',
            'Set your stop loss and profit target BEFORE entering'
        ],
        'While In Trade': [
            'Are you holding because thesis is intact or because of loss aversion?',
            'Would you buy more at this price — if not, why are you holding?',
            'Has new information changed your original thesis?',
            'Are you watching P&L too frequently — triggering emotional responses?'
        ],
        'After Exiting Trade': [
            'Did you follow your pre-defined rules?',
            'If not — what emotion overrode your system?',
            'Log the trade: entry, exit, reason, what you learned',
            'Separate process quality from outcome — good process bad outcome is OK'
        ],
        'Portfolio Level': [
            'Are your positions correlated — hidden concentration risk?',
            'Are you over-weight your recent winners — recency bias?',
            'When did you last stress-test against your worst fears?',
            'Are you avoiding reviewing losers — ostrich effect?'
        ]
    }

def pre_mortem_analysis(trade_idea):
    """
    Pre-mortem: imagine the trade failed — why did it fail?
    Forces consideration of downside scenarios before entry.
    """
    return {
        'trade':          trade_idea,
        'questions': [
            'It is 1 year from now and this trade lost 50% — what happened?',
            'What macro event could destroy this thesis?',
            'What company-specific event could destroy this thesis?',
            'What if the consensus is right and you are wrong?',
            'What is the maximum realistic loss scenario?',
            'How correlated is this to the rest of my portfolio?'
        ],
        'purpose': 'Counteract overoptimism and confirmation bias before committing capital'
    }
```

---

## Behavioral Finance in Practice
```python
def systematic_investing_rules():
    """
    Rules designed to remove behavioral biases from investing process.
    """
    return {
        'Dollar Cost Averaging': {
            'rule':     'Invest fixed amount on fixed schedule regardless of price',
            'removes':  'Market timing attempts, FOMO, panic selling',
            'evidence': 'Outperforms most active timing strategies long term'
        },
        'Mechanical Rebalancing': {
            'rule':     'Rebalance to target weights when drift exceeds 5%',
            'removes':  'Recency bias, momentum chasing, fear of rebalancing into losers',
            'evidence': 'Provides systematic buy low, sell high discipline'
        },
        'Pre-Commitment': {
            'rule':     'Write investment policy statement — rules for all scenarios',
            'removes':  'In-the-moment emotional decisions',
            'includes': 'Max drawdown tolerance, rebalancing rules, exit criteria'
        },
        'Cooling Off Period': {
            'rule':     'Wait 24-48 hours before acting on strong emotional impulse',
            'removes':  'FOMO, panic, revenge trading',
            'applies':  'Especially after large gains or losses'
        },
        'Trading Journal': {
            'rule':     'Record every decision with reasoning and emotion at the time',
            'removes':  'Hindsight bias, allows pattern recognition of mistakes',
            'review':   'Monthly review of journal for recurring biases'
        }
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Watching P&L constantly | Triggers loss aversion responses | Check portfolio weekly not hourly |
| No written thesis | Cannot distinguish thesis intact vs bias | Write thesis before every trade |
| Ignoring base rates | Overconfident in own predictions | 80% of active managers underperform index |
| Revenge trading | Double down after loss | Hard rule: max 2 trades per day after a loss |
| Confusing narrative with edge | Good story but no alpha | Back-test the story with data |
| Selling winners too early | Concave utility in gain domain | Scale out — do not sell all at once |
| Holding losers forever | Loss aversion + break-even effect | Pre-set stop loss, honor it always |

---

## Best Practices

- **Know your biases** — self-awareness is the first defense
- **Systematize decisions** — rules made when calm beat emotions in moment
- **Keep a decision journal** — track predictions vs outcomes to calibrate
- **Seek disconfirming evidence** — steelman the opposing view
- **Separate process from outcome** — good decisions can have bad outcomes
- **Reduce noise** — less frequent portfolio checking = better decisions
- **Use checklists** — pre-flight checks before every trade entry

---

## Related Skills

- **trading-psychology-expert**: Deep dive on trader mindset
- **finance-trading-expert**: Overall trading framework
- **risk-management-expert**: Rules that remove emotional decisions
- **technical-analysis-expert**: Sentiment in price action
- **macro-economics-expert**: Macro sentiment indicators
