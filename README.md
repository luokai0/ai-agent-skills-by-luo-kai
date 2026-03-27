# 🧠 AI Agent Skills Repository

**by Luo Kai (Lous Creations)** — The world's largest open collection of AI agent skill files

[![Skills](https://img.shields.io/badge/Skills-4146%2B-blue?style=for-the-badge&logo=github)](https://github.com/luokai0/ai-agent-skills-by-luo-kai)
[![Author](https://img.shields.io/badge/Author-Luo%20Kai-purple?style=for-the-badge)](https://github.com/luokai0)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **Every skill in this repo has real, working code — no link-only stubs.**

---

## ⚡ One-Click Download

**Download all skills as a ZIP:**

```bash
# Clone the entire repo
git clone https://github.com/luokai0/ai-agent-skills-by-luo-kai.git

# Or download just the skills folder
curl -L https://github.com/luokai0/ai-agent-skills-by-luo-kai/archive/main.zip -o skills.zip
unzip skills.zip
```

**Use in Claude Code:**
```bash
export SKILL_DIR="$HOME/ai-agent-skills-by-luo-kai/ai-agent-skills"
```

---

## 📊 Repository Stats

| Metric | Value |
|--------|-------|
| Total Skills | **4146+** |
| Categories | **20** |
| All have real code | **Yes** |
| Author | **Luo Kai (luokai0)** |
| License | **MIT** |

---

## 🗂️ Category Structure

```
ai-agent-skills/
├── 01-programming-languages/     # Python, JS/TS, Rust, Go, Java, Swift, Kotlin...
├── 02-frontend-development/      # React, Next.js, SvelteKit, Vue, CSS, a11y...
├── 03-backend-development/       # APIs, microservices, GraphQL...
├── 04-databases-and-storage/     # PostgreSQL, MongoDB, Redis, Supabase...
├── 05-devops-and-cloud/          # AWS, K8s, Docker, Terraform, CI/CD...
├── 06-security-and-auth/         # Auth, OAuth, JWT, AppSec, pen testing...
├── 07-testing-and-quality/       # Unit, E2E, TDD, Playwright, Vitest...
├── 08-architecture-and-patterns/ # Clean arch, SOLID, design patterns...
├── 09-data-and-ai/               # ML, LLMs, RAG, HuggingFace, fal.ai...
├── 10-mobile-development/        # iOS Swift, Android Kotlin, React Native, Flutter...
├── 11-specialized-coding/        # Git, blockchain, game dev, document processing...
├── 12-finance-and-trading/       # Quant, trading systems, financial analysis...
├── 13-physics-and-mathematics/   # Simulation, numerical methods...
├── 14-chemistry-and-biology/     # Bioinformatics, molecular modeling...
├── 15-earth-and-space-sciences/  # Geospatial, climate modeling...
├── 16-engineering/               # Mechanical, electrical, civil...
├── 17-emerging-tech/             # Web3, AR/VR, quantum, robotics...
├── 18-ai-agents-and-automation/  # Agent frameworks, MCP, orchestration...
├── 19-business-and-entrepreneurship/ # Marketing, sales, product, finance...
└── 20-health-and-wellness/       # Medical, fitness, nutrition...
```

---

## 🚀 How to Use

### With Claude Code
```bash
# Add a skill to your project
cp ai-agent-skills/01-programming-languages/01-python/python-expert/SKILL.md .claude/skills/
```

### Install All Skills
```bash
python3 install_all_skills.py
```

### Auto-install New Skills (run in Codespaces)
```bash
git pull
export GITHUB_TOKEN=your_token
python3 install_all_skills.py
```

---

## 📦 Sources

Skills curated and enhanced from:
- **Anthropic Official** — anthropics/skills
- **Composio Awesome** — ComposioHQ/awesome-claude-skills (800+ integrations)
- **Community repos** — 55+ GitHub repositories
- **Original by Luo Kai** — Custom-built skills with full code examples

---

## 🤝 Contributing

All contributions welcome! Format:

```yaml
---
author: your-github-handle
name: your-skill-name
version: 1.0.0
description: One clear sentence describing what this skill does.
license: MIT
---

# Skill Title

[Content with real code examples]
```

---

*Built with ❤️ by [Luo Kai](https://github.com/luokai0) — Lous Creations*
