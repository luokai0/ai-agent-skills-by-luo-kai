---
name: deep-intel
version: 1.0.0
description: Context-aware exhaustive research. Reads USER.md and MEMORY.md first, decomposes topic into 8+ research angles, fetches full pages, cross-references findings, delivers strategic brief filtered through your goals and constraints.
author: luo-kai
tags: [research, intelligence, agents, strategy, automation]
requires: [web_search, web_fetch, memory]
---

# Deep Intel Skill

## What This Skill Does

Runs a complete multi-layer research mission on any topic and delivers a
strategic intelligence brief tailored to YOUR situation. Not a generic
research tool. Reads USER.md and MEMORY.md first so every finding is
filtered through your goals, constraints, and context before delivery.

## Before Starting

Ask the user:
1. What is the topic to research?
2. What is the goal? (understand, find opportunity, build, compete, invest)
3. Any specific angle to prioritize?

## Research Process

### Phase 0 — Load User Context
Read MEMORY.md and USER.md before any search.
Extract goals, constraints, location, stack, budget, active projects.
Filter every finding through this context throughout.

### Phase 1 — Topic Decomposition
Identify ALL research angles automatically:
- Core ecosystem: names, websites, repos, people
- Technical architecture and how it was built
- Community projects and user-made tools
- Strategies and use cases with real numbers only
- Hidden features and undocumented capabilities
- Security risks and known failures
- Real people with similar constraints and what they achieved
- All free tools and APIs relevant to this topic
- Every competing platform or alternative
- Market gaps nobody has filled yet

### Phase 2 — Parallel Search Execution
Run a separate search for EACH angle identified above.
Rules:
- Minimum 8 searches per topic
- Use web_fetch on top 2-3 results per search — full page not snippet
- Cross-reference findings across angles
- Flag contradictions between sources
- Prioritize primary sources over aggregators
- Include current date in queries for fast-moving topics

### Phase 3 — Context Filtering
Before writing the report, filter ALL findings through user context:
- Remove anything not relevant to their goals
- Flag anything conflicting with their constraints
- Elevate findings that directly address their situation
- Note anything requiring resources the user does not have

### Phase 4 — Intelligence Brief Structure
Deliver in this exact order:
1. ECOSYSTEM MAP — all players, names, repos, websites
2. HOW IT WORKS — technical architecture, co-founder level depth
3. WHAT PEOPLE ARE DOING — real strategies with real numbers
4. WHAT PEOPLE ARE MISSING — underused tools and hidden features
5. PEOPLE LIKE YOU — cases matching user constraints exactly
6. FREE TOOLS AVAILABLE — complete zero-cost stack for this topic
7. RISKS AND FAILURES — what went wrong for others
8. MARKET GAPS — what nobody has built yet
9. YOUR STRATEGIC OPPORTUNITY — 3 specific actions for THIS user

## Best Practices

- Always read USER.md and MEMORY.md FIRST before any search
- Fetch full pages not just search snippets
- Run minimum 8-12 separate searches per topic
- Cross-reference findings across multiple sources
- Section 9 YOUR STRATEGIC OPPORTUNITY is mandatory — never skip it
- Use real numbers only: stars, users, dollars, dates — no vague claims
- Flag when a finding contradicts another finding
- Note which findings require resources the user does not have

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Stopping after 2-3 searches | Run minimum 8 separate angle searches |
| Using snippets only | Always web_fetch full pages for top results |
| Generic output ignoring user context | Read USER.md first, filter everything |
| Missing the opportunity section | Section 9 is mandatory, never skip |
| Aggregator sources only | Always find and fetch primary sources |
| No cross-referencing | Explicitly compare findings across angles |

## Trigger Phrases

- Deep research [topic]
- Full intel on [topic]
- Research everything about [topic] for my situation
- Go deep on [topic]
- Understand [topic] from every angle
- Complete investigation of [topic]

## Related Skills

- openclaw-setup-expert — set up the agent that runs this skill
- agent-income-expert — monetize findings from deep-intel research
- free-stack-builder — build the zero-cost infrastructure to run it
- dev-memory — persistent developer context across sessions
