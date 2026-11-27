---
name: openclaw-setup-expert
version: 1.0.0
description: Complete OpenClaw agent setup from zero. Installs on Windows WSL2 or Linux, configures SOUL.md, HEARTBEAT.md, MEMORY.md, AGENTS.md, connects Telegram interface, sets up free model routing with Gemini Flash and Groq. Zero cost stack.
author: luo-kai
tags: [openclaw, agents, setup, automation, telegram, free-stack]
---

# OpenClaw Setup Expert

## Before Starting
1. Which OS? Windows WSL2, Linux, or Mac?
2. Which messaging channel? Telegram recommended for zero cost.
3. Which AI model? Gemini Flash free tier recommended for heartbeats.
4. What is the agent purpose?

## Core Expertise Areas

### Installation
Windows WSL2: install WSL2 first, then run OpenClaw inside Linux environment.
Linux direct: npm install -g openclaw then openclaw setup.
Oracle Cloud free VPS: 4 vCPU 4GB RAM always free, best for 24/7 uptime.
Verify install: openclaw --version confirms successful installation.

### The 5 Core Files
SOUL.md: who the agent IS, personality, tone, hard limits, keep under 500 lines.
AGENTS.md: what the agent DOES and how, step-by-step workflows per task type.
HEARTBEAT.md: autonomous wake-up schedule and tasks, cron format.
MEMORY.md: long-term persistent facts, preferences, ongoing project state.
USER.md: profile of the human owner, goals, constraints, preferences.

### SOUL.md Template
Start with identity: You are [NAME], a [purpose] assistant for [user description].
Define tone: direct, friendly, patient. Never condescending.
Set hard limits: Never [action 1]. Always [action 2].
Keep under 500 lines. Longer SOUL.md dilutes instruction following.

### HEARTBEAT.md Template
Format: cron expression plus task description plus alert condition.
Every 30 minutes: check priority items, reply HEARTBEAT_OK if nothing urgent.
Every morning 7AM: daily briefing, calendar, top priorities.
Alert immediately if: critical threshold crossed.

### Free Model Routing
Heartbeats: gemini-2.5-flash-lite, 1000 req/day free, use for routine checks.
Reasoning: groq-llama-70b, 30 RPM free, very fast for agent thinking.
Complex tasks: claude-sonnet only when needed, paid, use sparingly.
Cost target: under 5 USD/month with this routing strategy.

### Telegram Setup
Create bot via @BotFather on Telegram, get token.
Add token to openclaw config file.
Whitelist your Telegram user ID to block unauthorized access.
Test with: hello in Telegram, agent should respond.

## Key Patterns



## Best Practices
- Always set auth token before exposing gateway to network
- Set hard API spending limit of 10 USD/day maximum
- Keep SOUL.md under 500 lines
- Test HEARTBEAT.md manually before enabling cron schedule
- Run in Docker for security isolation on shared servers

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Gateway exposed without auth | Always set auth token before network exposure |
| API costs exploding | Use Gemini Flash for heartbeats, not Claude |
| Agent forgets context | Write important facts to MEMORY.md explicitly |
| SOUL.md too long | Keep under 500 lines, longer dilutes focus |
| Heartbeat spam | Set HEARTBEAT_OK protocol for no-action responses |

## Related Skills
- soul-architect
- free-stack-builder
- agent-income-expert
