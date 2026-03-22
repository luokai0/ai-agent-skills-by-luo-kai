---
name: gumloop-automation
version: 1.0.0
description: Design and build Gumloop automation pipelines for passive income. Covers daily content pipelines, Google Drive integration, trigger setup, AI writing nodes, scheduling at 8AM, connecting to Gumroad for product sales, and monitoring pipeline health.
author: lous-creations
tags: [gumloop, automation, pipeline, content, gumroad, income, google-drive]
---

# Gumloop Automation

## Before Starting
1. What should the pipeline produce? Content, research, data, or notifications?
2. What triggers it? Schedule, webhook, or manual?
3. Where does output go? Google Drive, Gumroad, email, or Telegram?

## Core Expertise Areas

### Core Pipeline Pattern
Trigger at 8AM daily -> Research node finds trending topic -> AI Write node writes guide -> Save to Google Drive -> Notify via Telegram.
This is the proven pattern that runs autonomously without human input.

### Node Types
Trigger: schedule with cron, webhook from external service, or manual run.
Input: web search, RSS feed, Google Sheets, API call.
Process: AI write, summarize, transform, filter, classify.
Output: Google Drive save, email send, Telegram message, Gumroad upload.

### Daily Content Pipeline Setup
Step 1: Add Schedule trigger, set to 0 8 * * * for 8AM daily.
Step 2: Add Web Search node, prompt: find top trending AI topic today.
Step 3: Add AI Write node, prompt: write 800 word beginner guide on the topic.
Step 4: Add Google Drive Save node, folder: Daily Guides.
Step 5: Add Telegram node, message: New guide saved with title.

### Gumroad Connection
Manual step: download PDF from Drive, upload to Gumroad product page.
Automated via Gumroad API: POST to /products endpoint with PDF attachment.
Set price to 0 for free lead magnet or 5 to 10 USD for paid product.
Free products build email list, paid products generate direct revenue.

### Pipeline Monitoring
Always add error notification node so failures alert you on Telegram.
Check pipeline logs weekly to catch silent failures.
Test pipeline manually before enabling schedule.
Store all API keys in Gumloop secrets, never in node config directly.

## Best Practices
- Test pipeline manually before enabling schedule
- Add error alert node to every pipeline
- Keep AI prompts specific for consistent output quality
- Monitor Google Drive storage to prevent pipeline failures

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Pipeline fails silently | Always add error alert node |
| AI output inconsistent | Make prompts more specific with examples |
| Google Drive fills up | Add cleanup node to delete files older than 30 days |
| No monitoring | Add Telegram notification to every pipeline output |

## Related Skills
- agent-income-expert
- openclaw-setup-expert
- clawhub-publisher
