# 🤝 Contributing to Awesome AI Skills

Thank you for contributing! This repository follows the [Agent Skills Standard](https://agentskills.io/specification) and welcomes skills for **ALL AI tools**.

---

## 📋 Requirements

### ✅ Acceptance Criteria

| # | Rule | Required |
|---|---|---|
| 1 | Must follow [Agent Skills Standard](https://agentskills.io/specification) (SKILL.md format) | ✅ Yes |
| 2 | Skill must be a **folder** in `skills/` with `SKILL.md` inside | ✅ Yes |
| 3 | `name` field must match folder name (lowercase, hyphens, 1-64 chars) | ✅ Yes |
| 4 | `description` must explain WHAT it does and WHEN to use it | ✅ Yes |
| 5 | Must specify `compatibility` (which AI tools it works with) | ✅ Yes |
| 6 | Must include `metadata.tools` listing compatible tools | ✅ Yes |
| 7 | Not a duplicate of existing skill | ✅ Yes |

### ❌ Auto-Reject Rules

- ❌ No `SKILL.md` file in folder
- ❌ Missing YAML frontmatter
- ❌ Tool-specific without stating compatibility
- ❌ Multiple skills in one PR
- ❌ Spam or promotional content

---

## 🚀 How to Add Your Skill

### Step 1: Fork & create skill folder
```bash
mkdir skills/your-skill-name
```

### Step 2: Write SKILL.md using [template](./template/SKILL.md)
```markdown
---
name: your-skill-name
description: What it does and when to use it
license: CC0-1.0
compatibility: Works with Cursor, Windsurf, Copilot, Claude Code
metadata:
  author: your-github-username
  version: "1.0"
  category: coding
  tools: cursor, windsurf, copilot, claude-code
---

# Your Skill Name
[Instructions]
```

### Step 3: Submit PR with title `Add: [your-skill-name]`

---

## 🏷️ Categories

| Category | Examples |
|---|---|
| `coding` | Clean code, testing, debugging |
| `web-development` | React, Next.js, CSS, APIs |
| `writing` | SEO, copywriting, documentation |
| `business` | Strategy, analytics, planning |
| `design` | UI/UX, branding |
| `devops` | Docker, CI/CD, cloud |
| `security` | Auditing, vulnerability scanning |
| `productivity` | Email, automation |

---

## 📜 Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

Thank you for contributing! 🎉
