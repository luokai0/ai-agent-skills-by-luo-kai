---
name: free-stack-builder
version: 1.0.0
description: Build a complete autonomous AI agent system at absolute zero cost. Full verified stack: Oracle Cloud Always Free VPS for 24/7 uptime, Gemini Flash free tier for AI, Groq for fast reasoning, Telegram as interface, Supabase for database, Netlify for web presence. No credit card required for any component.
author: luo-kai
tags: [free, zero-cost, oracle, gemini, groq, telegram, stack, agents]
---

# Free Stack Builder

## Before Starting
1. What is the agent purpose?
2. Does it need 24/7 uptime or just on-demand?
3. Which messaging interface? Telegram recommended.

## Core Expertise Areas

### The Complete Zero-Cost Stack
| Layer | Service | Free Tier |
|---|---|---|
| Compute | Oracle Cloud Always Free | 4 vCPU 4GB RAM forever |
| AI Heartbeats | Gemini 2.5 Flash-Lite | 1000 req/day free |
| AI Reasoning | Groq Llama 70B | 30 RPM very fast free |
| Interface | Telegram Bot | Completely free |
| Database | Supabase | 500MB free forever |
| Web presence | Netlify | Free hobby tier |
| Skills | GitHub repo | Free public repo |

### Oracle Cloud Setup
Sign up at cloud.oracle.com, choose Always Free tier.
Create Ubuntu instance with 4 OCPU and 4GB RAM.
Open port 18789 for OpenClaw gateway in security rules.
SSH in and install: sudo apt update, install nodejs npm, then npm install -g openclaw.
This VPS runs your agent 24/7 at zero cost permanently.

### Google AI Studio Free Tier
Sign up at ai.google.dev, no credit card required.
Get API key, add to OpenClaw config as default model.
Gemini 2.5 Flash-Lite: 1000 requests/day for heartbeats.
Gemini 2.5 Flash: 250 requests/day for reasoning tasks.
Total daily capacity sufficient for active agent without any cost.

### Groq Free Tier
Sign up at console.groq.com, no credit card required.
Llama 3.3 70B: 30 RPM, fast for agent reasoning tasks.
Use for tasks requiring strong reasoning but not heartbeats.
Routing rule: Gemini for routine, Groq for thinking, avoid paid models.

### Windows Laptop Path
Install WSL2 on Windows, enables Linux environment.
Run OpenClaw inside WSL2, connects to Telegram bot.
Use Oracle Cloud free VPS when you need 24/7 uptime.
Use local laptop for development and testing only.

## Best Practices
- Use Oracle Cloud VPS for 24/7 agents, laptop only for testing
- Route heartbeats to Gemini Flash-Lite to stay within free limits
- Monitor daily API usage to avoid unexpected charges
- Keep all credentials in environment variables never in config files

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Oracle idle reclamation | Upgrade to pay-as-you-go free, keeps Always Free resources |
| Exceeding Gemini free quota | Use Flash-Lite for heartbeats, Flash only for complex tasks |
| Agent offline when laptop sleeps | Use Oracle Cloud VPS for always-on deployment |
| High API costs | Check routing config, ensure heartbeats using free tier |

## Related Skills
- openclaw-setup-expert
- soul-architect
- agent-income-expert
