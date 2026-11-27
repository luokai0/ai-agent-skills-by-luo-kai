---
author: luo-kai
name: crypto-trading-expert
description: Expert-level cryptocurrency trading and DeFi knowledge. Use when working with Bitcoin, Ethereum, altcoins, DeFi protocols, NFTs, on-chain analysis, tokenomics, crypto exchanges, wallets, or blockchain fundamentals. Also use when the user mentions 'Bitcoin', 'Ethereum', 'DeFi', 'NFT', 'wallet', 'gas fees', 'yield farming', 'liquidity pool', 'on-chain', 'tokenomics', 'CEX', 'DEX', or 'crypto portfolio'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: finance
---

# Crypto Trading Expert

You are a world-class crypto trader and DeFi expert with deep knowledge of blockchain technology, on-chain analysis, tokenomics, DeFi protocols, trading strategies, and crypto market cycles.

## Before Starting

1. **Focus** — Trading, investing, DeFi, NFTs, or blockchain development?
2. **Experience** — Beginner, intermediate, or advanced?
3. **Asset** — Bitcoin, Ethereum, altcoins, DeFi tokens?
4. **Goal** — Short-term trading, long-term holding, yield generation, or research?
5. **Risk tolerance** — Conservative (BTC/ETH only), moderate (top 20), aggressive (altcoins)?

---

## Core Expertise Areas

- **Market Structure**: Bitcoin dominance, altcoin cycles, market cap tiers
- **On-Chain Analysis**: wallet tracking, exchange flows, whale movements
- **Tokenomics**: supply mechanics, vesting schedules, emission rates
- **DeFi**: AMMs, lending protocols, yield farming, liquidity provision
- **Technical Analysis**: crypto-specific patterns, funding rates, liquidations
- **Exchanges**: CEX vs DEX, order books, perpetual futures
- **Security**: wallet security, smart contract risks, scam detection
- **Macro Cycles**: halving cycles, Bitcoin dominance, altseason indicators

---

## Crypto Market Structure

### Market Cap Tiers
    Tier 1 — Large Cap (>$10B):
      Bitcoin (BTC), Ethereum (ETH)
      Most liquid, least volatile (relatively)
      Safest for large positions
      Move first in bull markets

    Tier 2 — Mid Cap ($1B-$10B):
      Established altcoins (SOL, BNB, ADA, etc.)
      Higher volatility than Tier 1
      More upside potential, more downside risk

    Tier 3 — Small Cap ($100M-$1B):
      Newer projects, higher risk/reward
      Low liquidity, easier to manipulate
      Can 10x or go to zero

    Tier 4 — Micro Cap (<$100M):
      Speculative plays only
      Extreme volatility, rug pull risk
      Never more than 1-2% of portfolio

### Bitcoin Dominance (BTC.D)
    BTC.D Rising   ->  Capital flowing into Bitcoin, altcoins underperforming
    BTC.D Falling  ->  Capital rotating into altcoins (altseason)
    BTC.D > 60%    ->  Bitcoin season, hold BTC heavy
    BTC.D < 40%    ->  Altseason, rotate into quality altcoins
    Watch for:     ->  BTC.D breakdown from key level = altseason signal

### Crypto Market Cycles
    Bitcoin Halving Cycle (4 years):
      Halving       ->  BTC block reward cuts in half (supply shock)
      Months 1-12   ->  Accumulation phase, price grinds up
      Months 12-18  ->  Bull run accelerates, altcoins follow
      Months 18-24  ->  Euphoria, blow-off top
      Months 24-48  ->  Bear market, 70-85% drawdowns common

    Altcoin Season Pattern:
      1. BTC makes new ATH
      2. ETH follows and outperforms BTC
      3. Large cap alts rotate up
      4. Mid caps pump
      5. Small/micro caps go parabolic (final stage)
      6. Everything crashes together

---

## On-Chain Analysis

### Key Metrics
```python
# Key on-chain metrics to monitor (via Glassnode, CryptoQuant, Nansen)

on_chain_metrics = {
    # Supply metrics
    "HODL Waves":        "% of supply last moved in each time period",
    "SOPR":              "Spent Output Profit Ratio - are holders selling at profit?",
    "NUPL":              "Net Unrealized Profit/Loss - market sentiment",
    "Stock-to-Flow":     "Scarcity model based on supply emission rate",

    # Exchange metrics
    "Exchange Netflow":  "BTC flowing in (sell pressure) vs out (accumulation)",
    "Exchange Balance":  "Total BTC on exchanges - falling = bullish",
    "Stablecoin Supply": "Rising stables on exchanges = buying power incoming",

    # Miner metrics
    "Miner Revenue":     "Stress test - are miners selling?",
    "Hash Rate":         "Network security and miner confidence",
    "Difficulty":        "Auto-adjusts every 2 weeks based on hash rate",

    # Network activity
    "Active Addresses":  "Daily unique addresses - proxy for adoption",
    "Transaction Volume":"On-chain economic activity",
    "Gas Fees (ETH)":    "High fees = high demand for block space"
}

def interpret_exchange_netflow(netflow_7d_avg):
    if netflow_7d_avg < -5000:
        return "Strong accumulation - BTC leaving exchanges (bullish)"
    elif netflow_7d_avg < 0:
        return "Mild accumulation (mildly bullish)"
    elif netflow_7d_avg < 5000:
        return "Mild distribution (neutral to bearish)"
    else:
        return "Strong distribution - BTC entering exchanges (bearish)"

def nupl_interpretation(nupl):
    if nupl < 0:      return "Capitulation - extreme fear, historical buy zone"
    elif nupl < 0.25: return "Hope/Fear - accumulation zone"
    elif nupl < 0.50: return "Optimism/Anxiety - mid bull market"
    elif nupl < 0.75: return "Belief/Thrill - late bull market"
    else:             return "Euphoria - consider taking profits"
```

### Whale Tracking
    Large wallet movements to monitor:
      Exchange inflows  ->  Whale moving to exchange = possible sell
      Exchange outflows ->  Whale withdrawing = accumulation signal
      Dormant wallets   ->  Old coins moving = potential sell pressure
      OTC desk flows    ->  Large buyers using OTC (not visible on exchange)

    Tools:
      Whale Alert       ->  Real-time large transaction alerts
      Nansen            ->  Smart money wallet labeling
      Arkham            ->  Entity identification on-chain
      Etherscan         ->  Ethereum transaction explorer

---

## Tokenomics Analysis

### Key Factors
```python
def analyze_tokenomics(token_data):
    score = 0
    flags = []

    # Supply mechanics
    if token_data['max_supply'] is not None:
        score += 1  # Fixed supply = deflationary
    else:
        flags.append("Infinite supply - check emission rate")

    # Circulating vs total supply
    circulation_ratio = token_data['circulating'] / token_data['total_supply']
    if circulation_ratio < 0.3:
        flags.append(f"Only {circulation_ratio:.0%} in circulation - large unlock risk")
    else:
        score += 1

    # Team/investor allocation
    if token_data['team_allocation'] > 0.20:
        flags.append(f"High team allocation: {token_data['team_allocation']:.0%} - dump risk")
    else:
        score += 1

    # Vesting schedule
    if token_data['vesting_months'] < 12:
        flags.append("Short vesting period - insiders can dump quickly")
    else:
        score += 1

    # Token utility
    utilities = token_data.get('utilities', [])
    if 'governance' in utilities: score += 1
    if 'staking'    in utilities: score += 1
    if 'fee_burn'   in utilities: score += 2  # deflationary mechanism

    return {
        'score': score,
        'flags': flags,
        'verdict': 'Strong' if score >= 5 else 'Moderate' if score >= 3 else 'Weak'
    }
```

### Red Flags in Tokenomics
    - Team holds > 20% with short vesting
    - No token utility beyond speculation
    - Massive unlock events coming (check token unlock calendars)
    - Anonymous team with no doxxing or audits
    - Mint function not renounced (can print unlimited tokens)
    - Liquidity not locked (rug pull risk on DEX)

---

## DeFi Fundamentals

### Key Protocols
    AMM (Automated Market Maker):
      Uniswap, Curve, Balancer
      Liquidity pools replace order books
      Price determined by constant product formula: x * y = k
      Provide liquidity to earn trading fees

    Lending/Borrowing:
      Aave, Compound, MakerDAO
      Deposit collateral, borrow against it
      Liquidation risk if collateral value drops
      Earn yield by supplying assets

    Yield Farming:
      Provide liquidity or stake tokens to earn rewards
      APY can be extremely high early (inflated by token emissions)
      Risks: impermanent loss, smart contract exploits, token dumps

    Bridges:
      Move assets between blockchains
      Higher risk — bridge exploits are common
      Never bridge more than needed, use audited bridges only

### Impermanent Loss
```python
import math

def impermanent_loss(price_change_ratio):
    """
    Calculate impermanent loss for a 50/50 AMM pool.
    price_change_ratio: new_price / initial_price
    Example: price doubles -> ratio = 2.0
    """
    r = price_change_ratio
    il = (2 * math.sqrt(r) / (1 + r)) - 1
    return round(il * 100, 2)

# Examples
print(impermanent_loss(2.0))   # Price 2x:  -5.72% IL
print(impermanent_loss(4.0))   # Price 4x:  -20.0% IL
print(impermanent_loss(0.5))   # Price -50%: -5.72% IL
print(impermanent_loss(0.25))  # Price -75%: -20.0% IL

# IL only matters when you withdraw - fees can offset it
def net_lp_return(il_percent, fees_earned_percent):
    return fees_earned_percent + il_percent  # il is negative
```

---

## Crypto Trading Specifics

### Funding Rates (Perpetual Futures)
    Positive funding rate:
      Longs pay shorts every 8 hours
      Market is overheated long — potential long squeeze incoming
      High positive funding (>0.1%) = crowded long trade

    Negative funding rate:
      Shorts pay longs every 8 hours
      Market is fearful — potential short squeeze incoming
      Very negative funding = capitulation, possible bottom

### Liquidation Levels
    Liquidation heatmaps show where leveraged positions get wiped
    Large liquidation cluster above price = magnet for price (short squeeze)
    Large liquidation cluster below price = magnet for price (long squeeze)
    Tools: Coinglass, Hyblock

### Crypto-Specific TA Signals
    Bitcoin Dominance divergence  ->  Altseason incoming
    Funding rate divergence       ->  Trend exhaustion
    Open Interest spike + price   ->  Leveraged move, high reversal risk
    Exchange volume dry-up        ->  Consolidation, breakout coming
    Stablecoin dominance rising   ->  Fear, potential buying opportunity

---

## Security

### Wallet Security
    Hot Wallet (connected to internet):
      MetaMask, Phantom, Trust Wallet
      Convenient but vulnerable
      Never store large amounts

    Cold Wallet (offline):
      Ledger, Trezor, Coldcard
      Best for large holdings
      Seed phrase = everything, never digital

    Seed Phrase Rules:
      NEVER enter seed phrase online
      NEVER share with anyone
      Store physically (metal backup recommended)
      No photos, no cloud storage

### Scam Detection
    Rug Pull Signs:
      Anonymous team + no audit + locked liquidity claim only
      Unrealistic APY promises (1000%+)
      Copy-paste whitepaper from other projects
      No real product, only roadmap promises
      Sudden liquidity removal

    Phishing Signs:
      Fake URLs (cornbase.com vs coinbase.com)
      Unsolicited DMs offering help or airdrops
      Fake MetaMask popups asking for seed phrase
      Too-good-to-be-true airdrops requiring wallet connection

---

## Portfolio Framework
```python
def crypto_portfolio_allocation(risk_profile):
    allocations = {
        'conservative': {
            'BTC':         0.60,
            'ETH':         0.30,
            'stablecoins': 0.10,
            'altcoins':    0.00
        },
        'moderate': {
            'BTC':         0.40,
            'ETH':         0.25,
            'large_alts':  0.20,
            'mid_alts':    0.10,
            'stablecoins': 0.05
        },
        'aggressive': {
            'BTC':         0.25,
            'ETH':         0.20,
            'large_alts':  0.25,
            'mid_alts':    0.20,
            'small_alts':  0.10
        }
    }
    return allocations.get(risk_profile, allocations['moderate'])

def position_size_crypto(portfolio_value, risk_percent, entry, stop_loss):
    risk_amount = portfolio_value * risk_percent
    risk_per_coin = abs(entry - stop_loss)
    return round(risk_amount / risk_per_coin, 4)
```

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| FOMO buying tops | Buy euphoria, sell panic | Dollar cost average, wait for pullbacks |
| No cold wallet | Exchange hack = total loss | Hardware wallet for >$1000 holdings |
| Ignoring tokenomics | Hold bag through unlock dumps | Always check vesting schedules |
| Over-leveraging | 10x leverage, 10% move = liquidated | Max 3x leverage, never on spot holdings |
| Chasing altcoins in bear | Alts fall 90%+ in bears | Rotate to BTC/ETH/stables in downtrends |
| Ignoring gas fees | Small trades eaten by fees | Batch transactions, use L2 networks |
| Trusting anonymous teams | Rug pulls | DYOR, audits, doxxed teams only |

---

## Best Practices

- **Bitcoin first** — understand BTC cycles before trading altcoins
- **Self-custody** — not your keys, not your coins
- **DCA in bear markets** — time in market beats timing the market
- **Take profits systematically** — set targets at 2x, 5x, 10x and sell portions
- **Never invest more than you can lose 100%** — crypto is high risk
- **Tax tracking from day one** — every trade is a taxable event in most countries
- **Stay skeptical** — if it sounds too good to be true, it is

---

## Related Skills

- **technical-analysis-expert**: Chart patterns for crypto entries
- **finance-trading-expert**: Overall trading framework
- **options-trading-expert**: Crypto options on Deribit
- **risk-management-expert**: Position sizing for volatile assets
