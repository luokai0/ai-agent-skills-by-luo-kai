---
author: luo-kai
name: risk-management-expert
description: Expert-level financial risk management. Use when working with position sizing, portfolio risk, drawdown control, VaR, stress testing, hedging, correlation risk, tail risk, or building risk frameworks. Also use when the user mentions 'position sizing', 'stop loss', 'drawdown', 'risk-reward', 'Kelly criterion', 'portfolio heat', 'correlation', 'tail risk', 'hedge', 'risk-adjusted return', or 'maximum loss'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Risk Management Expert

You are a world-class risk manager with deep expertise in position sizing, portfolio risk, drawdown control, hedging strategies, tail risk, and building robust risk frameworks for traders and investors.

## Before Starting

1. **Portfolio type** — Single strategy, multi-strategy, or long-term investment?
2. **Asset class** — Stocks, forex, crypto, options, futures?
3. **Risk concern** — Position sizing, drawdown, correlation, tail risk, or hedging?
4. **Account size** — Retail, professional, or institutional?
5. **Goal** — Preserve capital, maximize risk-adjusted return, or limit drawdown?

---

## Core Expertise Areas

- **Position Sizing**: fixed fractional, Kelly criterion, volatility-based
- **Portfolio Risk**: correlation, concentration, beta exposure
- **Drawdown Control**: max drawdown rules, circuit breakers, recovery
- **VaR & CVaR**: historical, parametric, Monte Carlo methods
- **Hedging**: delta hedging, portfolio hedging, tail risk hedging
- **Stress Testing**: scenario analysis, historical crisis simulation
- **Risk-Adjusted Returns**: Sharpe, Sortino, Calmar, MAR ratios
- **Psychological Risk**: overtrading, revenge trading, emotional discipline

---

## Position Sizing Models
```python
import numpy as np
import pandas as pd

def fixed_fractional(account_balance, risk_percent, entry, stop_loss):
    """
    Risk fixed % of account per trade.
    Most common professional position sizing method.
    """
    risk_amount    = account_balance * risk_percent
    risk_per_unit  = abs(entry - stop_loss)
    position_size  = risk_amount / risk_per_unit

    return {
        'position_size':  round(position_size, 4),
        'risk_amount':    round(risk_amount, 2),
        'risk_percent':   f"{risk_percent*100:.1f}%",
        'risk_per_unit':  round(risk_per_unit, 4),
        'reward_2r':      round(entry + (entry - stop_loss) * 2, 4),
        'reward_3r':      round(entry + (entry - stop_loss) * 3, 4),
    }

def kelly_criterion(win_rate, avg_win, avg_loss, fraction=0.5):
    """
    Kelly Criterion for optimal position sizing.
    Use half-Kelly (fraction=0.5) in practice to reduce variance.
    Returns fraction of capital to risk.
    """
    b = avg_win / avg_loss
    p = win_rate
    q = 1 - win_rate
    kelly = (b * p - q) / b
    adjusted = max(0, kelly * fraction)

    return {
        'full_kelly':     round(kelly * 100, 2),
        'half_kelly':     round(adjusted * 100, 2),
        'edge':           round((b * p - q) * 100, 2),
        'recommendation': f"Risk {adjusted*100:.1f}% per trade"
    }

def volatility_based_sizing(account_balance, target_daily_vol,
                             asset_daily_vol, price):
    """
    Size position so it contributes target daily vol to portfolio.
    Professional volatility targeting approach.
    """
    position_value = (account_balance * target_daily_vol) / asset_daily_vol
    shares = position_value / price

    return {
        'position_value': round(position_value, 2),
        'shares':         round(shares, 4),
        'pct_of_account': round(position_value / account_balance * 100, 2),
        'daily_vol_contribution': f"{target_daily_vol*100:.2f}%"
    }

def atr_position_size(account_balance, risk_percent, atr, atr_multiplier=2):
    """
    ATR-based position sizing.
    Stop = atr_multiplier * ATR from entry.
    """
    risk_amount   = account_balance * risk_percent
    stop_distance = atr * atr_multiplier
    position_size = risk_amount / stop_distance

    return {
        'position_size':  round(position_size, 4),
        'stop_distance':  round(stop_distance, 4),
        'risk_amount':    round(risk_amount, 2)
    }

def portfolio_heat(positions, account_balance):
    """
    Total risk exposure across all open positions.
    Portfolio heat = sum of all individual position risks.
    Should not exceed 6-10% of account.
    """
    total_risk = sum(
        abs(p['entry'] - p['stop']) * p['size']
        for p in positions
    )
    heat_pct = total_risk / account_balance * 100

    return {
        'total_risk':    round(total_risk, 2),
        'portfolio_heat': round(heat_pct, 2),
        'status':        'Safe' if heat_pct < 6 else
                         'Elevated' if heat_pct < 10 else 'Danger'
    }
```

---

## Drawdown Management
```python
def drawdown_analysis(equity_curve):
    """Comprehensive drawdown analysis."""
    peak      = equity_curve.cummax()
    drawdown  = (equity_curve - peak) / peak

    # Find all drawdown periods
    is_dd     = drawdown < 0
    dd_start  = is_dd & ~is_dd.shift(1).fillna(False)
    dd_end    = ~is_dd & is_dd.shift(1).fillna(False)

    max_dd    = drawdown.min()
    max_dd_dt = drawdown.idxmin()

    # Recovery factor
    total_return   = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    recovery_factor = total_return / abs(max_dd)

    # Time underwater
    pct_underwater = is_dd.mean() * 100

    return {
        'max_drawdown':      f"{max_dd*100:.2f}%",
        'max_dd_date':       str(max_dd_dt),
        'current_drawdown':  f"{drawdown.iloc[-1]*100:.2f}%",
        'recovery_factor':   round(recovery_factor, 2),
        'pct_time_underwater': round(pct_underwater, 1),
        'total_return':      f"{total_return*100:.2f}%"
    }

def drawdown_circuit_breakers(daily_pnl, account_balance):
    """
    Automated circuit breaker rules.
    Reduce or stop trading when drawdown thresholds hit.
    """
    cumulative_pnl = daily_pnl.cumsum()
    peak           = cumulative_pnl.cummax()
    drawdown_pct   = (cumulative_pnl - peak) / account_balance * 100

    current_dd = drawdown_pct.iloc[-1]

    if current_dd <= -10:
        action = "STOP TRADING — 10% drawdown breaker hit. Review strategy."
        size_mult = 0.0
    elif current_dd <= -6:
        action = "REDUCE SIZE 50% — 6% drawdown warning level."
        size_mult = 0.5
    elif current_dd <= -3:
        action = "REDUCE SIZE 25% — 3% drawdown caution level."
        size_mult = 0.75
    else:
        action = "Normal trading — within acceptable drawdown."
        size_mult = 1.0

    return {
        'current_drawdown': round(current_dd, 2),
        'action':           action,
        'size_multiplier':  size_mult
    }

def recovery_analysis(max_drawdown, annual_return):
    """Estimate recovery time from drawdown."""
    if annual_return <= 0:
        return "Cannot recover with negative returns"

    daily_return  = annual_return / 252
    days_to_recover = abs(max_drawdown) / daily_return

    return {
        'drawdown':          f"{max_drawdown*100:.1f}%",
        'annual_return':     f"{annual_return*100:.1f}%",
        'days_to_recover':   round(days_to_recover),
        'months_to_recover': round(days_to_recover / 21, 1),
        'new_return_needed': round((1/(1+max_drawdown) - 1) * 100, 2)
    }
```

---

## Portfolio Risk Metrics
```python
def portfolio_risk_report(weights, returns, risk_free=0.05):
    """Complete portfolio risk metrics."""
    weights  = np.array(weights)
    cov      = returns.cov() * 252
    cor      = returns.corr()

    # Portfolio stats
    port_ret = np.sum(returns.mean() * weights) * 252
    port_vol = np.sqrt(weights @ cov @ weights)
    sharpe   = (port_ret - risk_free) / port_vol

    # Marginal & component risk contribution
    marginal_risk  = cov @ weights / port_vol
    component_risk = weights * marginal_risk
    risk_contrib   = component_risk / port_vol

    # Concentration
    herfindahl = np.sum(weights ** 2)  # 1/n for equal weight
    effective_n = 1 / herfindahl

    return {
        'annual_return':     round(port_ret * 100, 2),
        'annual_vol':        round(port_vol * 100, 2),
        'sharpe_ratio':      round(sharpe, 3),
        'effective_n':       round(effective_n, 1),
        'concentration_hhi': round(herfindahl, 4),
        'risk_contributions': dict(zip(
            returns.columns,
            [round(r*100, 2) for r in risk_contrib]
        ))
    }

def correlation_risk(returns, threshold=0.7):
    """Identify high correlation pairs — hidden concentration risk."""
    cor = returns.corr()
    high_cor_pairs = []

    tickers = returns.columns
    for i in range(len(tickers)):
        for j in range(i+1, len(tickers)):
            c = cor.iloc[i, j]
            if abs(c) > threshold:
                high_cor_pairs.append({
                    'pair':        (tickers[i], tickers[j]),
                    'correlation': round(c, 3),
                    'risk':        'High' if abs(c) > 0.85 else 'Elevated'
                })

    return sorted(high_cor_pairs, key=lambda x: abs(x['correlation']), reverse=True)

def beta_adjusted_exposure(positions, benchmark_returns):
    """Calculate beta-adjusted portfolio exposure."""
    total_beta_exposure = 0
    report = []

    for pos in positions:
        asset_returns = pos['returns']
        beta = asset_returns.cov(benchmark_returns) / benchmark_returns.var()
        beta_exposure = beta * pos['weight']
        total_beta_exposure += beta_exposure
        report.append({
            'asset':         pos['name'],
            'weight':        round(pos['weight'] * 100, 2),
            'beta':          round(beta, 3),
            'beta_exposure': round(beta_exposure * 100, 2)
        })

    return {
        'positions':           report,
        'total_beta_exposure': round(total_beta_exposure * 100, 2),
        'market_equivalent':   f"{total_beta_exposure*100:.1f}% long market"
    }
```

---

## VaR & Stress Testing
```python
def historical_var_cvar(returns, confidence=0.95, portfolio_value=100000):
    """Historical simulation VaR and CVaR."""
    sorted_returns = returns.sort_values()
    var_return     = sorted_returns.quantile(1 - confidence)
    cvar_return    = sorted_returns[sorted_returns <= var_return].mean()

    return {
        'VaR':          round(abs(var_return) * portfolio_value, 2),
        'VaR_pct':      round(abs(var_return) * 100, 3),
        'CVaR':         round(abs(cvar_return) * portfolio_value, 2),
        'CVaR_pct':     round(abs(cvar_return) * 100, 3),
        'interpretation': f"95% confident daily loss will not exceed "
                          f"${abs(var_return)*portfolio_value:.0f}"
    }

def stress_test_scenarios(portfolio_returns, portfolio_value):
    """
    Simulate portfolio P&L under historical crisis scenarios.
    Approximate single-day shocks for each event.
    """
    scenarios = {
        'COVID Crash Mar 2020':    -0.12,
        'GFC Lehman Day 2008':     -0.09,
        'Black Monday 1987':       -0.22,
        'Flash Crash 2010':        -0.09,
        'Russia/LTCM 1998':        -0.07,
        'Dot-com Peak Day 2000':   -0.06,
        'Brexit Vote 2016':        -0.05,
        '2022 Rate Hike Shock':    -0.04,
    }

    results = {}
    port_vol = portfolio_returns.std() * np.sqrt(252)

    for event, market_shock in scenarios.items():
        # Scale shock by portfolio beta (assume beta=1 for simplicity)
        port_shock   = market_shock * 1.0
        dollar_loss  = port_shock * portfolio_value
        results[event] = {
            'shock':       f"{market_shock*100:.1f}%",
            'port_impact': f"{port_shock*100:.1f}%",
            'dollar_loss': f"${abs(dollar_loss):,.0f}"
        }

    return results

def tail_risk_metrics(returns):
    """Tail risk and distribution shape metrics."""
    from scipy import stats

    skew    = returns.skew()
    kurt    = returns.kurtosis()
    var_95  = -returns.quantile(0.05)
    var_99  = -returns.quantile(0.01)
    cvar_95 = -returns[returns < -var_95].mean()

    # Tail ratio: right tail / left tail
    right_tail = returns.quantile(0.95)
    left_tail  = abs(returns.quantile(0.05))
    tail_ratio = right_tail / left_tail

    return {
        'skewness':        round(skew, 4),
        'excess_kurtosis': round(kurt, 4),
        'fat_tails':       kurt > 3,
        'tail_ratio':      round(tail_ratio, 3),
        'var_95':          round(var_95 * 100, 3),
        'var_99':          round(var_99 * 100, 3),
        'cvar_95':         round(cvar_95 * 100, 3),
        'risk_profile':    'Negative skew + fat tails = crash risk'
                           if skew < -0.5 and kurt > 3 else 'Normal'
    }
```

---

## Hedging Strategies
```python
def portfolio_hedge_ratio(portfolio_returns, hedge_returns):
    """
    Calculate optimal hedge ratio using OLS regression.
    Hedge ratio = beta of portfolio to hedge instrument.
    """
    import statsmodels.api as sm
    X = sm.add_constant(hedge_returns)
    model = sm.OLS(portfolio_returns, X).fit()
    hedge_ratio = model.params[1]
    r_squared   = model.rsquared

    return {
        'hedge_ratio':  round(hedge_ratio, 4),
        'r_squared':    round(r_squared, 4),
        'effectiveness': f"{r_squared*100:.1f}% of variance hedged",
        'interpretation': f"Short {abs(hedge_ratio):.2f} units of hedge per 1 unit of portfolio"
    }

def options_hedge_cost(portfolio_value, put_premium_pct,
                       strike_pct=0.95, contracts_needed=None):
    """
    Calculate cost of buying protective puts as portfolio insurance.
    """
    protection_level = portfolio_value * strike_pct
    annual_cost      = portfolio_value * put_premium_pct
    daily_cost       = annual_cost / 252

    return {
        'portfolio_value':   portfolio_value,
        'protection_level':  protection_level,
        'max_loss':          portfolio_value - protection_level,
        'max_loss_pct':      f"{(1-strike_pct)*100:.1f}%",
        'annual_cost':       round(annual_cost, 2),
        'annual_cost_pct':   f"{put_premium_pct*100:.2f}%",
        'daily_cost':        round(daily_cost, 2)
    }
```

---

## Risk-Adjusted Performance
```python
def risk_adjusted_metrics(returns, benchmark=None, risk_free=0.05):
    rf_daily  = risk_free / 252
    excess    = returns - rf_daily
    ann_ret   = returns.mean() * 252
    ann_vol   = returns.std() * np.sqrt(252)

    # Sharpe
    sharpe    = excess.mean() / excess.std() * np.sqrt(252)

    # Sortino (downside deviation only)
    downside  = returns[returns < rf_daily].std() * np.sqrt(252)
    sortino   = (ann_ret - risk_free) / downside

    # Calmar (return / max drawdown)
    equity    = (1 + returns).cumprod()
    max_dd    = ((equity - equity.cummax()) / equity.cummax()).min()
    calmar    = ann_ret / abs(max_dd)

    # Omega ratio
    threshold = rf_daily
    gains     = returns[returns > threshold] - threshold
    losses    = threshold - returns[returns <= threshold]
    omega     = gains.sum() / losses.sum()

    metrics = {
        'Sharpe Ratio':  round(sharpe, 3),
        'Sortino Ratio': round(sortino, 3),
        'Calmar Ratio':  round(calmar, 3),
        'Omega Ratio':   round(omega, 3),
        'Annual Return': f"{ann_ret*100:.2f}%",
        'Annual Vol':    f"{ann_vol*100:.2f}%",
        'Max Drawdown':  f"{max_dd*100:.2f}%",
    }

    if benchmark is not None:
        beta  = returns.cov(benchmark) / benchmark.var()
        alpha = ann_ret - (risk_free + beta*(benchmark.mean()*252 - risk_free))
        metrics['Beta']          = round(beta, 3)
        metrics['Alpha']         = f"{alpha*100:.2f}%"
        metrics['Info Ratio']    = round(
            (returns - benchmark).mean() /
            (returns - benchmark).std() * np.sqrt(252), 3
        )

    return metrics
```

---

## Risk Rules Framework

### The 10 Golden Rules of Risk Management
    1. NEVER risk more than 1-2% of account on a single trade
    2. NEVER let portfolio heat exceed 6-10% total open risk
    3. ALWAYS define stop loss BEFORE entering any trade
    4. NEVER move stop loss against your position
    5. REDUCE SIZE after 3% drawdown, STOP after 10%
    6. NEVER average into losing positions
    7. ALWAYS check correlation before adding new positions
    8. SIZE DOWN in high volatility environments (VIX > 25)
    9. NEVER risk money you cannot afford to lose 100% of
    10. REVIEW risk metrics weekly — not just P&L

### Daily Risk Checklist
    Before Trading:
      [ ] Check portfolio heat (total open risk %)
      [ ] Review current drawdown level
      [ ] Check VIX / market volatility regime
      [ ] Confirm no high-impact news in session
      [ ] Verify position sizing for planned trades

    After Trading:
      [ ] Log all trades with entry, exit, size, reason
      [ ] Update running P&L and drawdown
      [ ] Check if any circuit breakers triggered
      [ ] Review any mistakes or emotional decisions

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No position sizing rules | One trade wipes account | Fixed fractional 1-2% always |
| Moving stop to breakeven too fast | Gets stopped out before move | Use ATR-based trailing stop |
| Ignoring correlation | Double exposure unknowingly | Check correlation matrix weekly |
| Sizing up after wins | Overconfidence leads to big loss | Keep size consistent regardless of streak |
| No circuit breakers | Small drawdown becomes catastrophic | Hard rules at 3%, 6%, 10% |
| Revenge trading | Emotional decisions after loss | Walk away after 2 losses in a day |
| Ignoring regime change | Strategy works in bull, fails in bear | Monitor vol regime, adjust sizing |

---

## Best Practices

- **Asymmetric risk** — target 2:1 or 3:1 reward-to-risk minimum
- **Consistency** — same sizing rules every trade, no exceptions
- **Journal everything** — track P&L, mistakes, emotional state
- **Size down in uncertainty** — when in doubt, smaller position
- **Preserve capital first** — you cannot trade without capital
- **Expect drawdowns** — every strategy has them, plan for them
- **Separate strategy risk** — different rules for different strategies

---

## Related Skills

- **finance-trading-expert**: Overall trading framework
- **quantitative-finance-expert**: Statistical risk models
- **portfolio-management-expert**: Portfolio-level risk allocation
- **options-trading-expert**: Options-based hedging strategies
- **macro-economics-expert**: Macro regime risk awareness
