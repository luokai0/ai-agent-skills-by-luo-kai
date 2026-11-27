---
author: luo-kai
name: finance-trading-expert
description: Expert-level finance and trading knowledge. Use when working with stock analysis, technical indicators, portfolio management, risk management, options, derivatives, crypto, forex, valuation models, or trading strategies. Also use when the user mentions 'moving average', 'RSI', 'P/E ratio', 'options', 'hedge', 'volatility', 'DCF', 'arbitrage', 'candlestick', 'order book', or 'alpha'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Finance & Trading Expert

You are an expert in financial markets, trading strategies, and investment analysis with deep knowledge of technical analysis, fundamental analysis, risk management, derivatives, and quantitative finance.

## Before Starting

1. **Asset class** — Stocks, forex, crypto, options, futures, bonds?
2. **Strategy type** — Day trading, swing trading, long-term investing, hedging?
3. **Analysis style** — Technical, fundamental, quantitative, macro?
4. **Risk tolerance** — Conservative, moderate, aggressive?
5. **Goal** — Alpha generation, risk reduction, income, capital preservation?

---

## Core Expertise Areas

- **Technical Analysis**: candlestick patterns, chart patterns, indicators, volume
- **Fundamental Analysis**: DCF, comparable companies, earnings, balance sheet
- **Risk Management**: position sizing, stop-loss, VaR, drawdown, Kelly criterion
- **Derivatives**: options Greeks, pricing models, hedging strategies
- **Quantitative Finance**: factor models, backtesting, statistical arbitrage
- **Portfolio Theory**: MPT, Sharpe ratio, correlation, diversification
- **Market Microstructure**: order types, bid-ask spread, liquidity, slippage
- **Crypto & DeFi**: on-chain analysis, tokenomics, yield farming, CEX vs DEX

---

## Key Concepts & Formulas

### Market Mental Model

    Price Action Hierarchy:
      Macro / Fundamentals  ->  Sets the long-term trend (months-years)
      Sector Rotation       ->  Which industries are in/out of favor
      Technical Structure   ->  Support, resistance, trend lines (days-weeks)
      Momentum / Sentiment  ->  Short-term moves, reversals (hours-days)
      Order Flow            ->  Intraday price discovery (minutes)

    Asset Classes by Risk/Return:
      Cash / T-Bills        ->  Low risk, low return (~5% in high-rate env)
      Government Bonds      ->  Low-medium risk, fixed income
      Corporate Bonds       ->  Medium risk, higher yield than gov
      Large Cap Stocks      ->  Medium risk, ~7-10% historical annual return
      Small Cap / Growth    ->  Higher risk, higher potential return
      Options / Derivatives ->  Variable - can amplify gains or losses
      Crypto                ->  High volatility, 24/7 market

### Technical Analysis - Key Indicators
```python
import pandas as pd
import numpy as np

def sma(prices, period):
    return prices.rolling(window=period).mean()

def ema(prices, period):
    return prices.ewm(span=period, adjust=False).mean()

def rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(prices):
    ema12 = ema(prices, 12)
    ema26 = ema(prices, 26)
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def bollinger_bands(prices, period=20, std_dev=2.0):
    middle = sma(prices, period)
    std = prices.rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return upper, middle, lower

def atr(high, low, close, period=14):
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(com=period - 1, min_periods=period).mean()

def vwap(high, low, close, volume):
    typical_price = (high + low + close) / 3
    return (typical_price * volume).cumsum() / volume.cumsum()
```

### Fundamental Analysis - Valuation
```python
def dcf_valuation(free_cash_flows, terminal_growth_rate, wacc, net_debt, shares_outstanding):
    pv_fcfs = sum(
        fcf / (1 + wacc) ** (i + 1)
        for i, fcf in enumerate(free_cash_flows)
    )
    terminal_value = (free_cash_flows[-1] * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
    pv_terminal = terminal_value / (1 + wacc) ** len(free_cash_flows)
    enterprise_value = pv_fcfs + pv_terminal
    equity_value = enterprise_value - net_debt
    return equity_value / shares_outstanding

def valuation_ratios(price, eps, book_value, revenue_per_share, ebitda_per_share, fcf_per_share):
    return {
        "P/E":       price / eps,
        "P/B":       price / book_value,
        "P/S":       price / revenue_per_share,
        "EV/EBITDA": price / ebitda_per_share,
        "P/FCF":     price / fcf_per_share
    }

def capm(risk_free_rate, beta, market_return):
    return risk_free_rate + beta * (market_return - risk_free_rate)
```

### Risk Management
```python
def kelly_criterion(win_rate, avg_win, avg_loss):
    b = avg_win / avg_loss
    p = win_rate
    q = 1 - win_rate
    kelly = (b * p - q) / b
    return max(0, kelly * 0.5)

def historical_var(returns, confidence=0.95):
    return -returns.quantile(1 - confidence)

def sharpe_ratio(returns, risk_free_rate=0.05):
    daily_rf = risk_free_rate / 252
    excess = returns - daily_rf
    return (excess.mean() / excess.std()) * np.sqrt(252)

def max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()

def stop_loss_levels(entry_price, atr_value, risk_percent=0.02, portfolio_size=10000):
    atr_stop = entry_price - (2 * atr_value)
    fixed_risk = portfolio_size * risk_percent
    position_size = fixed_risk / (entry_price - atr_stop)
    return {
        "stop_loss_price": round(atr_stop, 4),
        "position_size":   round(position_size, 2),
        "risk_amount":     round(fixed_risk, 2),
        "risk_reward_2x":  round(entry_price + (entry_price - atr_stop) * 2, 4)
    }
```

### Backtesting
```python
def backtest(prices, signal_fn, commission=0.001):
    df = prices.copy()
    df['signal'] = signal_fn(df)
    df['position'] = df['signal'].shift(1)
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['position'] * df['returns']
    df['trade'] = df['position'].diff().abs()
    df['strategy_returns'] -= df['trade'] * commission
    equity = (1 + df['strategy_returns']).cumprod()
    return {
        'total_return': round((equity.iloc[-1] - 1) * 100, 2),
        'sharpe_ratio': round(sharpe_ratio(df['strategy_returns']), 3),
        'max_drawdown': round(max_drawdown(equity) * 100, 2),
        'win_rate':     round((df['strategy_returns'] > 0).mean() * 100, 2),
        'num_trades':   int(df['trade'].sum()),
        'equity_curve': equity
    }

def golden_cross_signal(df):
    sma50  = sma(df['close'], 50)
    sma200 = sma(df['close'], 200)
    signal = pd.Series(0, index=df.index)
    signal[sma50 > sma200] = 1
    signal[sma50 < sma200] = -1
    return signal
```

---

## Options - Greeks & Strategies

    The Greeks:
      Delta  ->  Price sensitivity to $1 move in underlying (call: 0-1, put: -1-0)
      Gamma  ->  Rate of change of delta, highest ATM near expiry
      Theta  ->  Time decay per day (negative for long options)
      Vega   ->  Sensitivity to 1% change in implied volatility
      Rho    ->  Sensitivity to interest rate changes

    Common Strategies:
      Covered Call     ->  Long stock + short call (income)
      Cash-Secured Put ->  Short put with cash reserved (acquire stock cheaper)
      Bull Call Spread ->  Long call + short higher call (reduce cost)
      Iron Condor      ->  Short strangle + long wings (profit from low vol)
      Straddle         ->  Long call + put same strike (profit from big move)
      Protective Put   ->  Long stock + long put (downside insurance)

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Overfitting backtest | Works on history only | Walk-forward + out-of-sample testing |
| Ignoring slippage | Backtest profits vanish live | Add realistic commission model |
| No stop loss | One trade wipes gains | Always define max loss before entry |
| Averaging down losers | Doubles exposure to failure | Cut losses early, add to winners |
| Over-leveraging | Small move = account blown | Risk max 1-2% per trade |
| Ignoring correlation | False diversification | Check asset correlation matrix |

---

## Best Practices

- Define **risk before entry** — know your stop and position size first
- Keep a **trading journal** — log every trade with reasoning and outcome
- Use **paper trading** to validate new strategies before real capital
- Never risk more than **1-2% of total capital** on a single trade
- Stay **emotionally neutral** — follow the system, not feelings
- Review and **adapt quarterly** — markets change, strategies must evolve

---

## Related Skills

- **python-expert**: For implementing quant strategies
- **data-engineering**: For building financial data pipelines
- **ml-expert**: For ML-based alpha factor research
- **statistics-expert**: For time series analysis
