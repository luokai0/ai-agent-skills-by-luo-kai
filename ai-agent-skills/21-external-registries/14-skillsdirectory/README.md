<p align="center">
  <img src="https://img.shields.io/badge/Agent_Skills-Standard-8B5CF6?style=for-the-badge" alt="Agent Skills" />
  <img src="https://img.shields.io/badge/Format-SKILL.md-00B4D8?style=for-the-badge" alt="SKILL.md" />
  <img src="https://img.shields.io/badge/Tools-Cursor_|_Windsurf_|_Copilot_|_Claude-blueviolet?style=for-the-badge" alt="Tools" />
  <img src="https://img.shields.io/badge/PRs-Welcome-orange?style=for-the-badge" alt="PRs Welcome" />
  <img src="https://img.shields.io/badge/License-CC0%201.0-lightgrey?style=for-the-badge" alt="License" />
</p>

<h1 align="center">🧠 Awesome AI Skills</h1>

<p align="center">
  <strong>A community-curated collection of Agent Skills for ALL AI coding assistants</strong>
  <br />
  <em>Cursor • Windsurf • GitHub Copilot • Claude Code • VS Code AI • Any Agent</em>
  <br />
  <em>Following the <a href="https://agentskills.io/specification">Agent Skills Standard</a> (SKILL.md format)</em>
</p>

<p align="center">
  <a href="https://aiagentbase.app/skills">🌐 Browse & Deploy on AiAgentBase</a> •
  <a href="#-how-to-contribute">🤝 Contribute</a> •
  <a href="#-skill-catalog">📂 Catalog</a> •
  <a href="https://agentskills.io">📋 Spec</a>
</p>

---

> 🚀 **Looking for Premium Skills with 1-Click Setup?** Visit [AiAgentBase.app/skills](https://aiagentbase.app/skills) — The Community-Driven AI Skills Marketplace

---

## 📖 What Are Agent Skills?

**Agent Skills** are `.md` files that turn any AI coding assistant into a **specialized expert**. They follow the open [Agent Skills Standard](https://agentskills.io/specification).

```
Without Skill:  Generic AI assistant → Average code
With Skill:     Clean Code Architect → SOLID, tested, maintainable code ✨
```

### Why Skills > Heavy MCP Servers (for knowledge)?

| Feature | MCP Server | SKILL.md |
|---|---|---|
| Token Usage | ~50,000 tokens | ~200 tokens |
| Setup | Complex (Docker, env vars) | Drop into project |
| Speed | Slower (API calls) | Instant (text) |
| Portability | Tool-specific | Works everywhere |

> 💡 **Pro Tip:** Use **Skills for knowledge/rules** + **MCP for actions/tools**. Check our [MCP Servers Hub](https://github.com/skillsdirectory/mcp-servers-hub)!

---

## 📂 Skill Catalog

### 💻 Coding — General

| Skill | Description | Tools |
|---|---|---|
| [clean-code-architect](./skills/clean-code-architect/) | SOLID principles, design patterns & refactoring | All |
| [git-flow-master](./skills/git-flow-master/) | Perfect commits, branches, PRs & merge strategies | All |
| [test-driven-developer](./skills/test-driven-developer/) | TDD cycle, unit/integration/E2E tests & mocking | All |

### 💻 Coding — Language Specific

| Skill | Description | Tools |
|---|---|---|
| [typescript-guru](./skills/typescript-guru/) | Advanced generics, utility types & strict patterns | All |

### 🌐 Web Development

| Skill | Description | Tools |
|---|---|---|
| [react-component-pro](./skills/react-component-pro/) | Reusable, accessible, performant React components | All |
| [api-architect](./skills/api-architect/) | RESTful & GraphQL API design with best practices | All |

### ✍️ Writing & Content

| Skill | Description | Tools |
|---|---|---|
| [seo-content-writer](./skills/seo-content-writer/) | SEO-optimized content with keyword strategy | All |
| [copywriting-expert](./skills/copywriting-expert/) | Persuasive copy using AIDA, PAS frameworks | All |

### 📊 Business & Strategy

| Skill | Description | Tools |
|---|---|---|
| [startup-advisor](./skills/startup-advisor/) | Business strategy, market validation & growth | All |
| [data-analyst](./skills/data-analyst/) | Data exploration, SQL, visualization & insights | All |

---

## 🔧 How to Use These Skills

### In Cursor / Windsurf
```bash
# Clone this repo
git clone https://github.com/skillsdirectory/awesome-ai-skills.git

# Copy skills to your project
cp -r awesome-ai-skills/skills/clean-code-architect .cursor/skills/
# or
cp -r awesome-ai-skills/skills/typescript-guru .windsurf/skills/
```

### In Claude Code
```bash
# Reference directly
cp -r awesome-ai-skills/skills/react-component-pro ./skills/
# Claude will auto-detect SKILL.md files
```

### In Any AI Tool
Just paste the content of `SKILL.md` into your AI tool's system prompt or custom instructions.

---

## 📈 Stats

| Metric | Count |
|---|---|
| Total Skills | 10 |
| Categories | 5 |
| Compatible Tools | Cursor, Windsurf, Copilot, Claude Code, Any AI |
| Format | Agent Skills Standard (SKILL.md) |

---

## 🤝 How to Contribute

We welcome skills for ALL AI tools! Follow the [Agent Skills Standard](https://agentskills.io/specification).

### Quick Steps

1. ⭐ **Star this repo**
2. 🍴 **Fork** this repository
3. 📁 **Create a folder** in `skills/` with your skill name
4. 📝 **Add a `SKILL.md`** file following the [template](./template/SKILL.md)
5. 📤 **Submit a Pull Request**

👉 **Full guidelines:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🔗 Related Projects

| Project | Description |
|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | Official Anthropic skills repository |
| [agentskills.io](https://agentskills.io) | Agent Skills specification |
| [claude-skills](https://github.com/skillsdirectory/claude-skills) | Claude-specific skills |
| [mcp-servers-hub](https://github.com/skillsdirectory/mcp-servers-hub) | MCP servers directory |

---

## 📄 License

[CC0 1.0 Universal](LICENSE) — Free to use, modify, and share.

---

## ⚖️ Disclaimer

> **This is an independent, community-maintained project.**
>
> - This repository is **NOT** affiliated with, endorsed by, sponsored by, or associated with **any** of the companies or products referenced herein, including but not limited to:
>   - **Anthropic** (Claude, Claude Code, Claude API)
>   - **Anysphere** (Cursor)
>   - **Codeium** (Windsurf)
>   - **Microsoft / GitHub** (GitHub Copilot, VS Code)
>   - **OpenAI** (ChatGPT, GPT)
>   - **Google / Alphabet** (Gemini, Google AI)
>   - **Meta** (React, Llama)
>   - Any other company, tool, framework, or service mentioned in this repository
> - All product names, trademarks, and registered trademarks are the property of their respective owners. Use of these names is solely for the purpose of **describing compatibility** and is considered nominative fair use.
> - The **Agent Skills Standard** (agentskills.io) is an open standard. This repository implements that standard independently.
> - All skills in this repository are **original community contributions**. They are not derived from or copies of any proprietary content.
> - This repository and its maintainers make **no warranties** regarding the quality, accuracy, or fitness of any skills listed herein. Use at your own risk.
> - **Individual contributors** are responsible for the content they submit. Maintainers review submissions but do not guarantee their correctness or safety.
> - Listings of third-party tools, servers, or services are for **informational purposes only** and do not constitute an endorsement or guarantee.

---

<p align="center">
  <strong>🌟 Found this useful? Give us a ⭐ Star!</strong>
  <br /><br />
  <a href="https://aiagentbase.app/skills">
    <img src="https://img.shields.io/badge/🚀_Get_Premium_Skills-AiAgentBase.app-FF6B35?style=for-the-badge" alt="AiAgentBase" />
  </a>
</p>
