---
name: startup-strategy-expert
version: 1.0.0
description: Launch and scale startups from zero. Covers idea validation, MVP scoping, market sizing, go-to-market, and fundraising strategy.
author: luo-kai
tags: [startup, entrepreneurship, mvp, fundraising, gtm, validation]
---

# Startup Strategy Expert

## Before Starting
1. Do you have a specific idea or are you exploring?
2. B2B or B2C target market?
3. Bootstrap or venture-backed goal?

## Core Expertise Areas

### Idea Validation
Use the Mom Test — talk to potential customers without pitching.
Ask about their problems, not your solution.
Validate pain severity: would they pay for this today?
Run 10 customer interviews before writing a single line of code.
Red flag: people say "that sounds cool" but won't commit to time or money.

### MVP Scoping
Define the single core value proposition — one job the product does perfectly.
List every feature, then cut 80 percent of them.
Build the smallest version that delivers core value.
Target: launch in 4 to 8 weeks maximum.
Measure one key metric from day one.

### Market Sizing
TAM = Total Addressable Market — everyone who could use this.
SAM = Serviceable Addressable Market — who you can realistically reach.
SOM = Serviceable Obtainable Market — realistic year 1 target.
Investors want a path to 1B+ TAM, even starting small.
Bottom-up sizing beats top-down: count real customers, not percentages.

### Go-To-Market Strategy
Choose one acquisition channel and dominate it before expanding.
Content-led: SEO, blog, build an audience over time.
Community-led: Reddit, Discord, niche forums, genuine participation.
Product-led: free tier, viral loops, self-serve onboarding.
Sales-led: outbound, partnerships, enterprise contracts.

### Fundraising Fundamentals
Pre-seed: angels, friends/family. Check size 25k to 500k.
Seed: institutional angels, seed VCs. Check size 500k to 3M.
Series A: requires traction. ARR 1M to 3M+. Check size 5M to 15M.
Pitch deck order: problem, solution, market, traction, team, ask.
Warm intros convert 10x better than cold outreach.

## Key Patterns

### Lean Canvas
```
Problem: [top 3 problems customers face]
Solution: [top 3 features that address them]
Unique Value Prop: [single clear message why you are different]
Unfair Advantage: [what cannot be easily copied]
Customer Segments: [target customers, early adopters]
Key Metrics: [numbers that matter — activation, retention, revenue]
Channels: [path to customers]
Cost Structure: [fixed and variable costs]
Revenue Streams: [how and how much you make money]
```

### Pitch Deck Structure
```
Slide 1: One-sentence company description
Slide 2: Problem — make them feel the pain
Slide 3: Solution — show do not tell
Slide 4: Why now — market timing
Slide 5: Market size — TAM SAM SOM
Slide 6: Business model — revenue mechanics
Slide 7: Traction — any real numbers, even small
Slide 8: Team — why you will win this
Slide 9: The ask — how much, for what milestones
```

### Default Alive Calculation
```python
def months_of_runway(cash, monthly_burn, monthly_revenue, revenue_growth_rate):
    # Determine if company reaches profitability before cash runs out
    month = 0
    while cash > 0:
        cash -= monthly_burn
        cash += monthly_revenue
        monthly_revenue *= (1 + revenue_growth_rate)
        month += 1
        if monthly_revenue >= monthly_burn:
            return f"Default alive: reaches profitability in month {month}"
    return f"Default dead: cash runs out in month {month}"
```

## Best Practices
- Talk to 10 real potential customers before building anything
- Launch ugly — perfect is the enemy of shipped
- Track one North Star Metric obsessively
- Know your runway at all times — default alive mindset
- Hire slow, fire fast — one bad hire can kill an early startup
- Write down every customer conversation and look for patterns

## Common Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Building in stealth | No feedback, building the wrong thing | Launch publicly early, get real users fast |
| Raising too much too early | Dilution and pressure before product-market fit | Raise minimum needed to hit next milestone |
| Premature scaling | Burning cash before finding what works | Find repeatable growth first then scale |
| Ignoring churn | Acquiring users who immediately leave | Fix retention before pouring fuel on acquisition |
| Consensus-driven product | Mediocre product that pleases no one | Gather input widely, decide narrowly |

## Related Skills
- product-management-expert
- digital-products-expert
- agent-income-expert
- free-stack-builder
