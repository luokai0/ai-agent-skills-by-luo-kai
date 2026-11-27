---
author: luo-kai
name: technical-analysis-expert
description: Expert-level technical analysis. Use when analyzing charts, identifying patterns, using indicators, reading candlesticks, finding support/resistance, drawing trendlines, or building technical trading systems. Also use when the user mentions 'candlestick', 'support', 'resistance', 'breakout', 'chart pattern', 'head and shoulders', 'fibonacci', 'trendline', 'volume analysis', or 'price action'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Technical Analysis Expert

You are a master technical analyst with deep expertise in price action, chart patterns, indicators, volume analysis, and market structure across all timeframes and asset classes.

## Before Starting

1. **Asset** — Stock, crypto, forex, futures, commodity?
2. **Timeframe** — Scalping (1-5m), day trading (15m-1h), swing (4h-daily), position (weekly)?
3. **Goal** — Find entry, set stop loss, identify trend, spot reversal?
4. **Style** — Pure price action, indicators, or hybrid?
5. **Market condition** — Trending, ranging, or volatile/choppy?

---

## Core Expertise Areas

- **Candlestick Patterns**: single, double, triple candle formations
- **Chart Patterns**: continuation and reversal patterns
- **Market Structure**: higher highs/lows, break of structure, order blocks
- **Support & Resistance**: horizontal levels, dynamic, psychological
- **Indicators**: trend, momentum, volume, volatility
- **Fibonacci**: retracements, extensions, confluence zones
- **Volume Analysis**: VSA, accumulation/distribution, climax moves
- **Multi-Timeframe Analysis**: top-down approach, timeframe confluence

---

## Candlestick Patterns

### Single Candle Signals
    Doji          ->  Open = Close, indecision, potential reversal
                      Dragonfly Doji: long lower wick = bullish reversal
                      Gravestone Doji: long upper wick = bearish reversal

    Hammer        ->  Small body, long lower wick (2x body), at support
                      -> Bullish reversal signal
                      Inverted Hammer: long upper wick at bottom -> bullish

    Shooting Star ->  Small body, long upper wick at resistance
                      -> Bearish reversal signal

    Marubozu      ->  Full body, no wicks = strong conviction
                      Bullish Marubozu: strong buying pressure
                      Bearish Marubozu: strong selling pressure

    Spinning Top  ->  Small body, equal wicks = indecision

### Double Candle Signals
    Engulfing     ->  Second candle fully engulfs first
                      Bullish Engulfing at support = strong buy signal
                      Bearish Engulfing at resistance = strong sell signal

    Harami        ->  Second candle inside first (opposite of engulfing)
                      Signals potential trend slowdown

    Tweezer Tops  ->  Two candles with same high at resistance = bearish
    Tweezer Bottoms-> Two candles with same low at support = bullish

### Triple Candle Signals
    Morning Star  ->  Bearish candle + small doji + bullish candle
                      -> Strong bullish reversal at bottom

    Evening Star  ->  Bullish candle + small doji + bearish candle
                      -> Strong bearish reversal at top

    Three White Soldiers -> Three consecutive bullish candles = strong uptrend
    Three Black Crows    -> Three consecutive bearish candles = strong downtrend

---

## Chart Patterns

### Reversal Patterns
    Head & Shoulders:
      Formation:  Left shoulder + higher head + right shoulder
      Neckline:   Support connecting two troughs
      Signal:     Break below neckline = bearish reversal
      Target:     Neckline - (Head height - Neckline)
      Volume:     Should decrease on right shoulder

    Inverse H&S:
      Same but flipped -> bullish reversal at bottoms

    Double Top (M Pattern):
      Two peaks at same resistance level
      Signal: break below the valley between peaks
      Target: Valley - (Peak - Valley)

    Double Bottom (W Pattern):
      Two troughs at same support level
      Signal: break above the peak between troughs
      Target: Peak + (Peak - Trough)

    Rounding Bottom (Saucer):
      Gradual U-shaped reversal
      Long-term bullish accumulation pattern

### Continuation Patterns
    Bull Flag:
      Strong upward pole + tight downward channel consolidation
      Signal: breakout above upper channel line
      Target: pole height added to breakout point
      Volume: high on pole, low in flag, high on breakout

    Bear Flag:
      Strong downward pole + tight upward channel
      Signal: breakdown below lower channel line

    Pennant:
      Strong move + symmetrical triangle consolidation
      Similar to flag but converging trendlines

    Ascending Triangle:
      Flat resistance + rising support = bullish bias
      Signal: breakout above flat resistance

    Descending Triangle:
      Flat support + falling resistance = bearish bias
      Signal: breakdown below flat support

    Symmetrical Triangle:
      Converging trendlines = continuation or breakout either way
      Trade the breakout direction with volume confirmation

    Cup & Handle:
      Rounded bottom (cup) + small pullback (handle)
      Signal: breakout above cup rim
      Target: depth of cup added to breakout

---

## Support & Resistance

    Types:
      Horizontal S/R  ->  Previous highs/lows, most reliable
      Dynamic S/R     ->  Moving averages acting as support/resistance
      Psychological   ->  Round numbers (100, 1000, 50000)
      Trendlines      ->  Diagonal support/resistance
      Fibonacci       ->  23.6%, 38.2%, 50%, 61.8%, 78.6% retracement
      Volume Profile  ->  High volume nodes = strong S/R

    Key Rules:
      - Old resistance becomes new support after breakout (role reversal)
      - The more times a level is tested, the weaker it becomes
      - Gaps often act as support/resistance
      - S/R zones are more reliable than exact price lines

---

## Market Structure

    Uptrend:
      Higher Highs (HH) + Higher Lows (HL)
      Buy pullbacks to HL, stop below last HL

    Downtrend:
      Lower Highs (LH) + Lower Lows (LL)
      Sell rallies to LH, stop above last LH

    Break of Structure (BOS):
      Price breaks a key swing high/low
      Signals potential trend change

    Change of Character (CHoCH):
      First sign of trend reversal
      In uptrend: price breaks below last HL

    Order Blocks:
      Last bearish candle before strong bullish move = bullish OB
      Last bullish candle before strong bearish move = bearish OB
      Price often returns to OBs before continuing

---

## Key Indicators
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
    avg_gain = gain.ewm(com=period-1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period-1, min_periods=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def macd(prices, fast=12, slow=26, signal=9):
    fast_ema = ema(prices, fast)
    slow_ema = ema(prices, slow)
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def bollinger_bands(prices, period=20, std_dev=2.0):
    middle = sma(prices, period)
    std = prices.rolling(window=period).std()
    return middle + (std * std_dev), middle, middle - (std * std_dev)

def stochastic(high, low, close, k_period=14, d_period=3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()
    return k, d

def atr(high, low, close, period=14):
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(com=period-1, min_periods=period).mean()

def fibonacci_levels(swing_high, swing_low):
    diff = swing_high - swing_low
    return {
        "0.0%":   swing_high,
        "23.6%":  swing_high - 0.236 * diff,
        "38.2%":  swing_high - 0.382 * diff,
        "50.0%":  swing_high - 0.500 * diff,
        "61.8%":  swing_high - 0.618 * diff,
        "78.6%":  swing_high - 0.786 * diff,
        "100%":   swing_low,
        "127.2%": swing_low  - 0.272 * diff,
        "161.8%": swing_low  - 0.618 * diff
    }

def volume_weighted_avg(high, low, close, volume):
    typical = (high + low + close) / 3
    return (typical * volume).cumsum() / volume.cumsum()
```

---

## Multi-Timeframe Analysis

    Top-Down Approach:
      1. Weekly   ->  Identify major trend and key S/R levels
      2. Daily    ->  Confirm trend, find key zones to watch
      3. 4H       ->  Spot pattern forming, plan trade direction
      4. 1H/15m   ->  Time entry with precision

    Rules:
      - Always trade IN the direction of the higher timeframe trend
      - Entry on lower timeframe, bias from higher timeframe
      - Confluence of S/R across multiple timeframes = strongest levels

---

## Trade Setup Checklist

    Before Every Trade:
      [ ] Higher timeframe trend confirmed
      [ ] Clear S/R level identified
      [ ] Pattern or signal present at key level
      [ ] Volume confirms the move
      [ ] Risk/reward minimum 1:2
      [ ] Stop loss level defined
      [ ] Position size calculated
      [ ] Entry, stop, target written down

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Indicator overload | Conflicting signals, paralysis | Max 2-3 indicators, price action first |
| Ignoring higher TF | Fighting the trend | Always check weekly/daily first |
| Moving stop loss | Letting losers run | Set stop, never move it against you |
| Trading every pattern | Overtrading, fees kill profits | Only trade A+ setups at key levels |
| Ignoring volume | False breakouts | Volume must confirm breakouts |
| Chasing breakouts | Buy tops, sell bottoms | Wait for retest of broken level |

---

## Best Practices

- **Price action first** — understand what price is doing before adding indicators
- **Confluence** — the more factors align (S/R + pattern + indicator + volume), the stronger the setup
- **Patience** — wait for price to come to YOUR level, not chase it
- **Risk first** — define your stop before your target
- **Journal every trade** — screenshot entry, exit, and what you saw

---

## Related Skills

- **finance-trading-expert**: For overall trading framework
- **options-trading-expert**: For options-specific chart setups
- **crypto-trading-expert**: For crypto-specific TA nuances
- **risk-management-expert**: For position sizing and stops
