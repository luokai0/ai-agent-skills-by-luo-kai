---
name: agent-trading-expert
version: 1.0.0
description: Design and run autonomous trading agent pipelines. Covers Polymarket prediction markets, CEX momentum strategies, DeFi yield farming, on-chain research, and safe paper trading setup. Zero to live trading workflow with full safety protocol.
author: lous-creations
tags: [trading, crypto, polymarket, defi, automation, agents, bitget]
---

# Agent Trading Expert

## Before Starting
1. Paper trading or live?
2. Which market? Crypto CEX, Polymarket, DeFi, or stocks?
3. Starting capital or zero budget research only?
4. Risk tolerance?

## Core Expertise Areas

### Safety Rules — Read First
Never grant withdrawal permissions to any agent skill.
Only read plus trade permissions, never withdraw.
Paper trade minimum 2 weeks before any live money.
Start with 50 to 100 USD maximum on first live deployment.
Set hard daily loss limit before starting.
Store API keys encrypted, never in plaintext config files.

### Strategy 1 — On-Chain Research Only (Zero Risk)
Agent monitors whale wallet movements, token activity, on-chain metrics.
Aggregates findings into daily Telegram summary.
Human makes all decisions. Agent does research only.
Cost: zero. Risk: zero. Best starting point.

### Strategy 2 — Polymarket Prediction Markets
Agent monitors news feeds and social media for relevant developments.
Evaluates related prediction market positions automatically.
Uses Polyclaw skill for CLOB execution on Polygon network.
Start with 10 USD positions maximum during testing phase.

### Strategy 3 — CEX Momentum Rules
Rule: if 20-EMA above 50-EMA and funding rate below 0.03 percent per 8h then long 1x.
Rule: if 20-EMA below 50-EMA or funding rate above 0.1 percent then go flat.
Target pairs: BTC-USDT and ETH-USDT on 5-minute timeframe.
Connect via Bitget Agent Hub for fastest 3-minute setup.

### Strategy 4 — DeFi Yield
Agent checks Pendle APYs daily, proposes rebalance if APY deviates more than 5 percent.
GMX v2: checks pool utilization and funding every 30 minutes.
Shifts size between positions based on volatility signals.

### HEARTBEAT.md for Trading
Every 30 minutes: check open positions, funding rates, stop loss levels.
Every morning 7AM: market summary, overnight events, portfolio status.
Alert immediately if: position down more than 5 percent.

## Best Practices
- Always paper trade 2 weeks minimum before live deployment
- Set stop loss before any live position opens
- Never grant withdrawal permissions to agent
- Start with on-chain research strategy before moving to live trading

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Live trading without paper test | Always paper trade minimum 2 weeks first |
| No stop loss defined | Set stop loss before position opens, not after |
| Withdrawal permission granted | Never grant this, read and trade only |
| One decimal error | Verify position size formula manually before live |

## Related Skills
- openclaw-setup-expert
- agent-income-expert
- free-stack-builder
