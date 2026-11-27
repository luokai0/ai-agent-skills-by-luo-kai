# Contributing to RisingWave Agent Skills

Thank you for contributing! Here's how to get started.

[1. Getting Started](#getting-started) | [2. Issues](#issues) | [3. Pull Requests](#pull-requests) | [4. Contributing New Rules](#contributing-new-rules) | [5. Creating a New Skill](#creating-a-new-skill)

## Getting Started

Please read our [Code of Conduct](https://github.com/risingwavelabs/.github/blob/main/CODE_OF_CONDUCT.md) before contributing.

No special tooling required — the repository contains only Markdown files. Clone and edit directly.

```bash
git clone https://github.com/risingwavelabs/agent-skills.git
cd agent-skills
```

## Issues

If you find incorrect information, have a suggestion for a new rule or skill, or want to improve existing content, please open an Issue.

- Search [existing Issues](https://github.com/risingwavelabs/agent-skills/issues) before creating a new one.
- Include a clear description of what is wrong or what should be added.
- Use appropriate labels: `bug`, `enhancement`, `new-rule`, `new-skill`, `documentation`.

## Pull Requests

We actively welcome Pull Requests.

- Link your PR to the related Issue.
- Keep changes focused — one rule or fix per PR.
- For new skills or major restructuring, open a Discussion first.
- Bump the `version` field in the affected `SKILL.md` frontmatter for every change.

## Contributing New Rules

Rules are individual Markdown files in `skills/risingwave-best-practices/rules/`.

1. Copy `_template.md` to `{prefix}-{your-rule-name}.md` (use the correct category prefix — see `_sections.md`)
2. Fill in the frontmatter: `title`, `impact`, `impactDescription`, `tags`
3. Write the explanation (1–2 sentences, why it matters)
4. Provide an **Incorrect** and **Correct** SQL example with comments
5. Add a `Reference:` link to the official [RisingWave docs](https://docs.risingwave.com)
6. Add the rule to the Quick Reference section in `SKILL.md`
7. Bump `version` in `skills/risingwave-best-practices/SKILL.md`

**Impact levels:**

| Level | Meaning |
|-------|---------|
| CRITICAL | Data correctness issue, or 10× or more improvement |
| HIGH | 2–10× improvement, or significant scalability impact |
| MEDIUM | 10–25% improvement, or maintainability benefit |
| LOW | Minor improvements or edge cases |

**Rule quality checklist:**
- [ ] SQL examples are runnable (not pseudocode)
- [ ] Incorrect example shows a real anti-pattern, not just missing syntax
- [ ] Correct example directly fixes the anti-pattern shown
- [ ] Reference links to the relevant docs.risingwave.com page
- [ ] Tags include connector names, SQL keywords, or error messages agents might search for

## Creating a New Skill

Skills follow the [Agent Skills Open Standard](https://agentskills.io/).

### 1. Create the directory structure

```bash
mkdir -p skills/my-skill/references
```

### 2. Create SKILL.md

```yaml
---
name: my-skill
description: Use when [specific triggers and keywords]
license: Apache-2.0
metadata:
  author: RisingWave Labs
  version: "0.1.0"
---

# My Skill

Brief overview.

## Core Principles

Key gotchas and patterns.

## References

- [references/detail.md](references/detail.md)
```

### 3. Add to README.md

Add the skill to the **Available Skills** section in `README.md` with a description and use-when list.

## Questions?

- Open an Issue for bugs or suggestions
- Start a [Discussion](https://github.com/risingwavelabs/agent-skills/discussions) for broader proposals

## License

By contributing, you agree your contributions will be licensed under the Apache 2.0 License.
