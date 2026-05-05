---
name: share-skill
description: Safely prepare and guide skills for contribution to the Zo Skills Registry. Reviews code for secrets, validates SKILL.md format, checks for suspicious patterns, and provides clear next steps for community or external skill submissions.
compatibility: Created for Zo Computer
metadata:
  author: rc2.zo.computer
---
# Share Skill to Registry

This skill helps you safely contribute a skill to the Zo Skills Registry (zocomputer/skills).

## Usage

```bash
# Review a skill for safe sharing
bun /home/workspace/Skills/share-skill/scripts/validate.ts <skill-path>

# Example:
bun /home/workspace/Skills/share-skill/scripts/validate.ts /home/workspace/Skills/my-skill
```

## What This Checks

### Safety Scan (BLOCKING if found)
- Hardcoded secrets (API keys, tokens, passwords)
- Suspicious code patterns (`eval`, `exec`, shell injection risks)
- Obfuscated or minified code
- Private files (`.env`, local caches, personal data)

### Structure Validation
- SKILL.md with required frontmatter (`name`, `description`, `compatibility`)
- Valid skill name (lowercase, hyphens, matches folder name)
- Scripts are documented and executable
- Required folders follow conventions

## Contribution Workflows

### Your Original Skill

1. Fork [zocomputer/skills](https://github.com/zocomputer/skills)
2. Copy your skill folder to `Community/<your-skill>/`
3. Run the validator: `bun validate` (from the repo root)
4. Open a PR with this template:

```markdown
## Skill Submission: <skill-name>

**Author:** @<your-github-username>
**Category:** <automation|integration|utility|media|other>

### What it does
<2-3 sentence description>

### Requirements
- <any external services needed>
- <any API keys required>

### Usage Example
```bash
bun /home/workspace/Skills/<skill-name>/scripts/<script>.ts <args>
```
```

### Someone Else's Skill (External)

1. Fork [zocomputer/skills](https://github.com/zocomputer/skills)
2. Add entry to `external.yml`:

```yaml
- name: <skill-name>
  source: <git-url-or-path>
  author: <original-author>
  license: <license-type>
```

3. Run: `bun run sync-external`
4. Open PR with attribution notes

## Important Notes

- **Never** include secrets in skill code—read from environment variables
- **Never** submit PRs on your behalf automatically
- Skills must be self-contained and documented
- Community skills go in `Community/`; external skills use `external.yml`
