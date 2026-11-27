---
name: clawhub-publisher
version: 1.0.0
description: Package and publish skills to the ClawHub marketplace for passive income. Covers SKILL.md format requirements, metadata standards, testing, the publish command, versioning, pricing, and strategies to maximize installs and revenue.
author: luo-kai
tags: [clawhub, publishing, skills, marketplace, income, passive]
---

# ClawHub Publisher

## Before Starting
1. Is SKILL.md complete with valid YAML frontmatter?
2. Has the skill been tested locally?
3. Is the skill name unique on ClawHub?

## Core Expertise Areas

### SKILL.md Required Format
The frontmatter must include all required fields:


### Publish Command
npx clawhub publish — reads SKILL.md, validates frontmatter, uploads to registry.
Subsequent publishes with same name create a new version automatically.
npx clawhub unpublish skill-name — removes skill from marketplace.

### Maximize Installs
Use exact words people search for in your description.
Add 5 or more relevant tags covering all use cases.
Keep description under 200 words but highly specific.
Include trigger phrases section so agents auto-select your skill.
Post about it on Reddit r/openclaw and Twitter with openclaw hashtag.
Top sellers earn 1000 USD or more per month from a single vertical skill.

### Versioning Strategy
Bump patch version 1.0.1 for bug fixes and small improvements.
Bump minor version 1.1.0 for new sections or added capabilities.
Bump major version 2.0.0 for complete rewrites.
Always update version in frontmatter before publishing.

### Income Model
Free skills build installs and reputation, paid skills earn directly.
ClawHub takes 30 percent, you keep 70 percent on paid skills.
Vertical skills earn more than generic ones.
Your SKILL.md files from this repo are already in the right format.
Publish all 287 skills to ClawHub with one command per skill.

## Best Practices
- Check clawhub.com for duplicate names before publishing
- Test skill locally before publishing to avoid bad reviews
- Respond to user issues quickly to maintain high rating
- Update skills regularly to keep them relevant and visible

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Missing required frontmatter fields | Validate YAML before running publish |
| Vague description losing search visibility | Be specific about triggers and use cases |
| No trigger phrases | Add explicit trigger phrases section |
| Publishing broken skill | Always test locally first |

## Related Skills
- mcp-builder-expert
- agent-income-expert
- openclaw-setup-expert
