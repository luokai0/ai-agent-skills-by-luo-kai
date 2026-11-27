---
author: luo-kai
name: trading-psychology-expert
description: Expert-level trading psychology and mental performance. Use when working with trading discipline, emotional control, consistency, building trading habits, overcoming fear and greed, developing a trading mindset, journaling, performance review, or peak performance routines. Also use when the user mentions 'trading discipline', 'emotional trading', 'revenge trading', 'fear of missing out', 'trading journal', 'consistency', 'overtrading', 'trading routine', 'mindset', 'mental game', 'confidence', or 'trading performance'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Trading Psychology Expert

You are a world-class trading psychologist and performance coach with deep expertise in trader mindset, emotional discipline, habit formation, peak performance routines, overcoming psychological barriers, and building the mental framework for long-term trading success.

## Before Starting

1. **Problem** — Emotional trading, inconsistency, fear, overtrading, or confidence?
2. **Experience** — Beginner, intermediate, or experienced trader?
3. **Style** — Day trader, swing trader, or investor?
4. **Pattern** — What recurring psychological pattern is causing problems?
5. **Goal** — Consistency, discipline, confidence, or peak performance?

---

## Core Expertise Areas

- **Emotional Control**: fear, greed, anger, euphoria management
- **Discipline**: rule-following, system adherence, impulse control
- **Consistency**: building habits, routines, process orientation
- **Confidence**: healthy vs overconfidence, building conviction
- **Journaling**: trade review, pattern recognition, self-awareness
- **Peak Performance**: flow state, pre-market routine, energy management
- **Loss Recovery**: drawdown psychology, bounce-back framework
- **Mindset**: growth mindset, probabilistic thinking, detachment

---

## The Psychology of Trading Losses
```python
def loss_psychology_framework():
    return {
        'Normal Loss Response Sequence': [
            '1. Denial — this will come back, market is wrong',
            '2. Anger — stupid trade, bad luck, market makers hunting my stop',
            '3. Bargaining — if it gets back to breakeven I will exit',
            '4. Depression — I am not cut out for this, I always lose',
            '5. Acceptance — loss happened, learn from it, move on'
        ],
        'Healthy Response': [
            'Accept that losses are part of trading — even 60% win rate means 40% losses',
            'Separate outcome from decision quality — good process can have bad outcomes',
            'Review the trade objectively: did I follow my rules?',
            'Extract the lesson without self-judgment',
            'Reset mental state before next trade'
        ],
        'Unhealthy Responses': {
            'Revenge Trading': {
                'pattern':    'Take impulsive trades to win back losses immediately',
                'result':     'Compounds losses, breaks all risk rules',
                'trigger':    'Ego needs to be right, cannot accept loss',
                'fix':        'Hard rule: no trading for 1 hour after a losing trade'
            },
            'Fear Paralysis': {
                'pattern':    'Stop taking valid setups after a loss',
                'result':     'Miss winning trades, system never gets a chance',
                'trigger':    'Loss aversion overrides systematic thinking',
                'fix':        'Reduce position size by 50% after losing day, rebuild confidence'
            },
            'Doubling Down': {
                'pattern':    'Add to losing position hoping it comes back',
                'result':     'Small loss becomes catastrophic',
                'trigger':    'Endowment effect — already own it, hate to lose',
                'fix':        'Pre-set maximum position size — cannot add beyond it'
            }
        }
    }

def loss_recovery_protocol(consecutive_losses, daily_pnl_pct):
    """
    Structured protocol for recovering from losses.
    """
    if consecutive_losses >= 3 or daily_pnl_pct <= -0.02:
        level = 'STOP'
        actions = [
            'Stop trading immediately for today',
            'Step away from screens for minimum 30 minutes',
            'Do not check P&L repeatedly',
            'Physical activity — walk, gym, anything active',
            'Review journal when fully calm — not while emotional',
            'Sleep on it — never make rule changes on a losing day',
            'Return tomorrow with reduced size (50% of normal)'
        ]
    elif consecutive_losses == 2 or daily_pnl_pct <= -0.01:
        level = 'CAUTION'
        actions = [
            'Reduce position size to 50% of normal',
            'Only take A+ setups — higher confirmation threshold',
            'Take a 15-minute break before next trade',
            'Review last two trades objectively',
            'Maximum 2 more trades for the day'
        ]
    else:
        level = 'NORMAL'
        actions = [
            'Single loss is normal — part of the game',
            'Brief review: did I follow rules? Yes = move on',
            'Reset mindset: next trade is independent',
            'Continue normal trading plan'
        ]

    return {
        'consecutive_losses': consecutive_losses,
        'daily_pnl':          f"{daily_pnl_pct*100:.2f}%",
        'protocol_level':     level,
        'actions':            actions
    }
```

---

## Emotional State Management
```python
def emotional_states_in_trading():
    return {
        'Fear': {
            'symptoms': [
                'Hesitate to pull trigger on valid setups',
                'Exit winners too early',
                'Size too small relative to conviction',
                'Skip trades during volatility',
                'Constant checking of P&L'
            ],
            'root_cause': 'Trading with money you cannot afford to lose, '
                          'or recent losses have shaken confidence',
            'solutions': [
                'Trade smaller until confidence returns',
                'Review past successful trades to rebuild evidence base',
                'Focus on process not P&L — close P&L screen if needed',
                'Paper trade for 1-2 weeks to rebuild pattern recognition',
                'Only risk money you are emotionally detached from'
            ]
        },
        'Greed': {
            'symptoms': [
                'Override exit rules hoping for more profit',
                'Size up beyond risk rules after winners',
                'Take trades outside of defined setup criteria',
                'Add to winning positions recklessly',
                'Stay in trades past target'
            ],
            'root_cause': 'Attachment to outcomes, confusing luck with skill',
            'solutions': [
                'Pre-set profit targets — use limit orders so exits are automatic',
                'Journal the feeling: write down when you feel greedy',
                'Review times you gave back profits — costs are real',
                'Scale out mechanically — take some at T1, rest at T2'
            ]
        },
        'Overconfidence': {
            'symptoms': [
                'Increase size dramatically after winning streak',
                'Skip analysis — feels obvious',
                'Take more trades than system allows',
                'Dismiss risk management as unnecessary'
            ],
            'root_cause': 'Attribution of luck to skill after winning streak',
            'solutions': [
                'Track expectancy over minimum 50 trades — not 5',
                'Hard size rules that cannot be overridden by feel',
                'Review your worst losing trades to stay humble',
                'Winning streaks end — position sizing must not change'
            ]
        },
        'Boredom': {
            'symptoms': [
                'Trade when no setup present',
                'Lower criteria to find action',
                'Overtrade to feel productive',
                'Take opposite side just to have a position'
            ],
            'root_cause': 'Identity attached to trading activity not results',
            'solutions': [
                'Recognize doing nothing IS a trading decision',
                'Track how much boredom trades cost annually',
                'Have a not-trading activity prepared (research, reading)',
                'Quality over quantity — one great trade beats five bad ones'
            ]
        }
    }

def pre_trade_emotional_checklist():
    return [
        'Am I calm? (Not angry, not euphoric, not desperate)',
        'Am I trading my plan or reacting to something that just happened?',
        'Is this setup in my playbook or am I forcing it?',
        'What is my position size — is it within my rules?',
        'Do I know exactly where my stop is before entering?',
        'Am I trading to make back a loss? (If yes — stop)',
        'Am I trading FOMO? (If yes — stop)',
        'If this trade loses, will I be okay financially and emotionally?'
    ]
```

---

## Trading Journal System
```python
def trading_journal_template():
    return {
        'Pre-Trade Entry': {
            'date_time':          'YYYY-MM-DD HH:MM',
            'ticker':             'Symbol',
            'direction':          'Long / Short',
            'setup_type':         'Which pattern from my playbook?',
            'timeframe':          'Entry timeframe',
            'entry_price':        'Actual entry',
            'stop_loss':          'Pre-defined stop (never moved against)',
            'target_1':           'First profit target',
            'target_2':           'Second profit target',
            'position_size':      'Shares/contracts',
            'risk_amount':        '$ amount at risk',
            'risk_pct_account':   '% of account at risk',
            'thesis':             'Why does this trade work?',
            'invalidation':       'What would make this wrong?',
            'emotional_state':    '1-10 (1=fearful, 5=neutral, 10=euphoric)',
            'confidence':         '1-10 (conviction in setup)'
        },
        'Post-Trade Entry': {
            'exit_price':         'Actual exit',
            'exit_reason':        'Stop hit / Target hit / Manual exit / Why manual?',
            'pnl_dollars':        'Profit/loss in dollars',
            'pnl_r':              'P&L in R multiples (1R = initial risk)',
            'followed_rules':     'Yes / No',
            'if_no_why':          'Which rule was broken and why?',
            'execution_quality':  '1-10',
            'what_went_well':     'Specific positives',
            'what_to_improve':    'Specific improvement area',
            'emotional_exit':     'Emotional state at exit',
            'lesson':             'One specific lesson from this trade',
            'screenshot':         'Chart screenshot at entry and exit'
        },
        'Weekly Review': {
            'trades_taken':       'Total number',
            'win_rate':           'Winners / Total',
            'avg_winner_r':       'Average winning trade in R',
            'avg_loser_r':        'Average losing trade in R',
            'expectancy':         '(WR x avg_win) - (LR x avg_loss)',
            'rules_followed_pct': '% of trades where all rules followed',
            'biggest_mistake':    'Most costly psychological error',
            'pattern_noticed':    'Recurring behavior (good or bad)',
            'adjustment':         'One specific change for next week'
        }
    }

def r_multiple_analysis(trades):
    """
    Analyze trading performance in R multiples.
    R = initial risk per trade (stops loss amount)
    """
    import pandas as pd
    import numpy as np

    df          = pd.DataFrame(trades)
    winners     = df[df['r_multiple'] > 0]
    losers      = df[df['r_multiple'] <= 0]

    win_rate    = len(winners) / len(df)
    avg_win     = winners['r_multiple'].mean()
    avg_loss    = abs(losers['r_multiple'].mean())
    expectancy  = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
    profit_factor = winners['r_multiple'].sum() / abs(losers['r_multiple'].sum())

    return {
        'total_trades':     len(df),
        'win_rate':         round(win_rate * 100, 1),
        'avg_winner_r':     round(avg_win, 2),
        'avg_loser_r':      round(avg_loss, 2),
        'expectancy_r':     round(expectancy, 3),
        'profit_factor':    round(profit_factor, 2),
        'total_r':          round(df['r_multiple'].sum(), 2),
        'assessment': {
            'expectancy':   'Positive edge' if expectancy > 0 else 'Negative edge',
            'profit_factor':'Good' if profit_factor > 1.5 else
                            'Acceptable' if profit_factor > 1.0 else
                            'Below breakeven'
        },
        'rule_adherence':   round(df['followed_rules'].mean() * 100, 1)
                            if 'followed_rules' in df.columns else 'Not tracked'
    }
```

---

## Peak Performance Routine
```python
def daily_trading_routine():
    return {
        'Pre-Market (60-90 min before open)': [
            'Physical: 20+ min exercise or walk — activates prefrontal cortex',
            'No news or social media first 30 min after waking',
            'Review trading plan from prior night',
            'Mark key levels on charts: S/R, VWAP, prior day H/L/close',
            'Check economic calendar — know all high impact events',
            'Review overnight gaps and pre-market movers',
            'Write 3 specific setups you are watching today',
            'Set alerts — do not watch screen, let alerts come to you',
            'Mental state check: rate yourself 1-10 on readiness',
            'If below 6/10 — reduce size or do not trade today'
        ],
        'During Market Hours': [
            'Execute plan — do not deviate without documented reason',
            'After each trade: brief 2-min review before next trade',
            'No social media or financial news while in trades',
            'Honor stops immediately — no negotiation',
            'If daily loss limit hit: close platform, walk away',
            'If daily profit target hit: consider stopping or reducing size',
            'Hydrate, brief movement break every 90 minutes'
        ],
        'Post-Market (within 2 hours of close)': [
            'Journal every trade while memory is fresh',
            'Screenshot charts with annotations',
            'Rate emotional state during trading 1-10',
            'Identify the one best trade and one worst decision',
            'Mark levels for tomorrow',
            'Review what setups are setting up for next session',
            'Physical decompression: walk, gym, anything non-screen'
        ],
        'Weekly Review (Sunday)': [
            'Compile weekly stats: win rate, R multiple, expectancy',
            'Review all trade screenshots',
            'Identify #1 psychological pattern (positive or negative)',
            'Set ONE specific behavioral goal for next week',
            'Review economic calendar for the week',
            'Assess current market regime and adjust approach if needed'
        ]
    }

def flow_state_conditions():
    """
    Conditions that create flow state (peak performance) in trading.
    """
    return {
        'Physical': [
            'Well rested — 7-8 hours sleep minimum',
            'Fed but not overfull — heavy meals reduce alertness',
            'Hydrated — even mild dehydration impairs decision making',
            'Exercised — dopamine, norepinephrine elevated',
            'No alcohol or substances from prior night'
        ],
        'Mental': [
            'Clear plan — know exactly what you are looking for',
            'Detached from outcome — process focused not P&L focused',
            'Moderate challenge — not too easy (boredom) not too hard (anxiety)',
            'Distraction-free environment — phone away, notifications off',
            'Calm confidence — have done the preparation work'
        ],
        'Environmental': [
            'Dedicated workspace — not couch, not kitchen table',
            'Organized screens — charts clean, no clutter',
            'Same routine every day — reduces decision fatigue',
            'Remove financial stress — do not trade rent money'
        ],
        'Blockers to Flow': [
            'Checking P&L constantly — shifts focus to outcome',
            'Social media during session',
            'Multiple opinions from Twitter/YouTube while trading',
            'Trading while tired, sick, or emotionally upset',
            'Financial pressure from account size or life situation'
        ]
    }
```

---

## Habit Formation for Traders
```python
def trading_habits_framework():
    return {
        'Keystone Habits (highest leverage)': [
            'Daily journaling — builds self-awareness faster than anything',
            'Pre-market routine — consistency reduces decision fatigue',
            'Following the stop — honoring stops builds discipline muscle',
            'Weekly review — creates feedback loop for improvement'
        ],
        'Building New Habits': {
            'Cue':      'Identify trigger for desired behavior',
            'Routine':  'The specific behavior you want',
            'Reward':   'Immediate positive reinforcement',
            'Example': {
                'Cue':     'After entering a trade',
                'Routine': 'Immediately set stop loss order',
                'Reward':  'Check mark in journal — small win feeling'
            }
        },
        'Breaking Bad Habits': {
            'Identify trigger': 'When exactly does revenge trading happen?',
            'Create friction':  'Make bad behavior harder (log off platform)',
            'Replace':          'Substitute harmful action with neutral one',
            'Track relapses':   'Count without judgment — awareness is enough'
        },
        '21-Day Habit Experiment': [
            'Choose ONE behavior to change',
            'Define it precisely: not vague "trade better"',
            'Track it daily with simple yes/no',
            'Do not add a second habit until first is automatic',
            'After 21 days: review data, decide to continue or modify'
        ]
    }

def identity_based_trading():
    """
    Identity shift: from "trying to trade well" to "I am a disciplined trader"
    Based on James Clear's Atomic Habits framework.
    """
    return {
        'Outcome Identity': 'I want to make money trading (weak — outcome dependent)',
        'Process Identity': 'I am a trader who follows rules consistently (strong)',
        'Identity Votes': [
            'Every time you follow your stop: "This is what disciplined traders do"',
            'Every journal entry: "This is what professional traders do"',
            'Every time you pass on a bad setup: "This is what selective traders do"'
        ],
        'Identity Statements': [
            'I am a trader who never moves stops against my position',
            'I am a trader who journals every trade',
            'I am a trader who only takes setups from my playbook',
            'I am a trader who protects capital above all else'
        ],
        'Key Insight': 'Behavior change that conflicts with identity never lasts. '
                       'Change identity first, behavior follows naturally.'
    }
```

---

## Probabilistic Thinking
```python
def probabilistic_mindset():
    return {
        'Core Principle': 'Trading is a probability game — '
                          'you cannot control individual outcomes, '
                          'only process and expectancy over many trades',
        'Wrong Thinking': [
            'This trade WILL work — high conviction means high probability',
            'I KNOW where this is going',
            'The market SHOULD do this',
            'This loss means my system is broken'
        ],
        'Right Thinking': [
            'Based on my edge, this has a 55-65% probability of working',
            'Even my best setups lose 35-45% of the time',
            'This individual trade outcome is nearly random',
            'My edge only shows over 50-100+ trades, not one trade',
            'A loss tells me nothing about the next trade'
        ],
        'Practical Application': [
            'Think in terms of batches: "Over next 20 trades, my system expects X"',
            'Never judge a strategy on less than 50 trades',
            'Accept that 10 consecutive losses is statistically possible even with 60% win rate',
            'Focus on: did I take the right setup? Not: did it win?'
        ]
    }

def losing_streak_probability(win_rate, streak_length):
    """
    Probability of a losing streak occurring — it will happen.
    Knowing this mathematically helps remove emotional shock.
    """
    import math

    prob_of_streak  = (1 - win_rate) ** streak_length
    expected_trades = 1 / prob_of_streak

    return {
        'win_rate':             f"{win_rate*100:.0f}%",
        'streak_length':        streak_length,
        'probability_single':   round(prob_of_streak * 100, 3),
        'expected_every_n_trades': round(expected_trades, 0),
        'in_1000_trades':       round(1000 / expected_trades, 1),
        'message':              f'A {streak_length}-loss streak happens approximately '
                                f'every {expected_trades:.0f} trades — plan for it'
    }
```

---

## Common Psychological Patterns
```python
def trading_psychology_patterns():
    return {
        'The Breakeven Trap': {
            'pattern':    'Hold losing trade hoping to get back to breakeven',
            'psychology': 'Loss aversion — losses feel 2x more painful than gains',
            'cost':       'Small losses become large losses',
            'fix':        'Pre-commit: if stop hit, I exit. No negotiation.'
        },
        'Winner Cutting': {
            'pattern':    'Exit winning trades far too early',
            'psychology': 'Bird in hand — fear of watching profit disappear',
            'cost':       'Win rate looks good but R:R is terrible',
            'fix':        'Scale out: take 50% at T1, trail stop on rest'
        },
        'FOMO Chasing': {
            'pattern':    'Enter after move already made — buy tops',
            'psychology': 'Fear of missing out on further move',
            'cost':       'Poor entry = worse R:R, more likely to be stopped out',
            'fix':        'Write down: if I missed it, I missed it. Next setup.'
        },
        'System Hopping': {
            'pattern':    'Change strategy after a few losses',
            'psychology': 'Recency bias + impatience + need to be right',
            'cost':       'Never give any system enough trades to show its edge',
            'fix':        'Commit to a system for minimum 50 trades before evaluating'
        },
        'Size Creep': {
            'pattern':    'Gradually increase size until one trade destroys account',
            'psychology': 'Overconfidence after winning streak',
            'cost':       'Wipes out months of gains in one trade',
            'fix':        'Fixed % rule — size NEVER changes based on recent P&L'
        },
        'Analysis Paralysis': {
            'pattern':    'So many indicators and time frames — cannot decide',
            'psychology': 'Fear of being wrong, perfectionism',
            'cost':       'Miss trades, constant second-guessing',
            'fix':        'Maximum 2 indicators + price action. Simplicity wins.'
        }
    }
```

---

## Self-Assessment Tools
```python
def weekly_psychology_scorecard():
    return {
        'Rate 1-10 this week': {
            'Rule Following':      '10 = followed every rule perfectly',
            'Emotional Control':   '10 = traded without emotion all week',
            'Discipline':          '10 = took only playbook setups',
            'Risk Management':     '10 = never broke position size rules',
            'Journal Consistency': '10 = journaled every trade',
            'Pre-Market Prep':     '10 = full routine every day'
        },
        'Honest Questions': [
            'How many trades this week were NOT in my playbook?',
            'How many times did I move a stop against my position?',
            'Did I revenge trade at any point? When?',
            'What was my emotional state on my worst trade?',
            'What is the ONE thing I need to fix most next week?'
        ],
        'Score Interpretation': {
            '55-60': 'Elite consistency — maintain and refine',
            '45-54': 'Good — identify top 1-2 areas to improve',
            '35-44': 'Developing — focus on one rule at a time',
            'Below 35': 'Consider paper trading or reduced size until basics solid'
        }
    }

def trading_readiness_assessment():
    """
    Daily check before trading — go/no-go decision.
    """
    questions = {
        'Sleep':            'Did you get 7+ hours of sleep?',
        'Exercise':         'Have you done at least 20 min physical activity?',
        'Emotional State':  'Are you calm and neutral (not angry, anxious, or euphoric)?',
        'Plan':             'Do you have a written plan for today?',
        'Financial Stress': 'Are you trading money you can emotionally afford to lose?',
        'Distraction':      'Are you free from major personal stressors today?',
        'Recent Losses':    'Are you NOT trying to make back recent losses?'
    }

    return {
        'questions':        questions,
        'scoring':          'Yes = 1 point, No = 0 points',
        'thresholds': {
            '7/7': 'Green light — trade full size',
            '5-6/7': 'Yellow light — trade at 50-75% size',
            'Below 5': 'Red light — do not trade today, protect capital'
        },
        'key_insight': 'Protecting yourself on bad days is as important as '
                       'capitalizing on good days'
    }
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Journaling without reviewing | Data collected but no learning | Weekly review is mandatory |
| Vague journal entries | Cannot extract patterns | Be specific: exact emotional state, exact rule broken |
| All focus on strategy | Psychology ignored | 80% of edge comes from execution, not system |
| Perfectionism | Beat yourself up over every loss | Losses are data, not failures |
| Comparing to others | Envy leads to size-up and FOMO | Your only competition is last week's you |
| No off switch | Trading identity consumes everything | Scheduled off time is performance enhancer |
| Ignoring physical health | Tired brain makes poor decisions | Sleep and exercise are trading tools |

---

## Best Practices

- **Journal every trade** — self-awareness is the foundation of improvement
- **Process over outcome** — did you follow the rules? That is success
- **Reduce size when off** — fighting mental state is expensive
- **Take breaks** — trading fatigue is real and costly
- **Weekly review non-negotiable** — the feedback loop drives growth
- **One change at a time** — fix one psychological pattern per month
- **Physical health first** — sleep and exercise are your highest-leverage tools

---

## Related Skills

- **behavioral-finance-expert**: Academic psychology behind market behavior
- **risk-management-expert**: Rules that protect from emotional decisions
- **finance-trading-expert**: Overall trading framework
- **technical-analysis-expert**: Pattern recognition reduces uncertainty
- **financial-planning-expert**: Separating trading from financial security
