# AI Agent Skills

A collection of agent skills for **Cursor** and **Claude Code** that automate product management, requirements engineering, and team workflows. Skills are markdown files that the AI agent reads at runtime to execute structured, multi-step tasks.

---

## What Are Agent Skills?

Agent skills are instruction files (`SKILL.md`) stored in a skills folder the agent scans at startup. When you invoke a skill — either explicitly by name or implicitly by describing a task — the agent reads the skill file and follows its step-by-step instructions. Skills can call other skills, save files to your workspace, ask you questions, and produce publication-ready documents.

---

## Repository Structure

```
ai-skills/
├── cursor/
│   └── skills/              21 skills — 12 production + 9 WIP across 3 category plugins + 3 standalone
│       ├── planning/         Planning plugin — 5 delivery lifecycle skills  ⚠️ WIP
│       │   ├── release-sprint-planner/
│       │   ├── sprint-planning-session/
│       │   ├── sprint-progress-tracker/
│       │   ├── sprint-review-generator/
│       │   ├── meeting-to-plan-integrator/
│       │   └── shared/       Shared domain knowledge referenced by all planning skills
│       ├── requirements/     Requirements plugin — 9 discovery and analysis skills
│       │   ├── requirements-pipeline/
│       │   │   └── stages/   Stage instruction files (e.g., 01-intake.md)
│       │   ├── generate-requirements/
│       │   │   ├── workflows/ Workflow instruction files
│       │   │   └── archive/  Archived templates (moved to dedicated skills)
│       │   ├── validate-requirements/
│       │   │   └── checks/   Semantic and structural check definitions
│       │   └── ...
│       ├── epics-and-user-stories/  Epics & Stories plugin — 4 story lifecycle skills  ⚠️ WIP
│       │   ├── generate-epic/
│       │   ├── generate-user-stories/
│       │   ├── validate-user-stories/
│       │   └── generate-uat/
│       ├── design-to-context/
│       ├── figjam-diagram-generator/
│       └── transcript-to-meeting-notes/
├── skill-eval/              Skill evaluation utilities
└── docs/
    ├── workflow-guide.md    How skills relate to each other + pipeline diagram
    ├── skill-catalog.md     Per-skill reference: inputs, outputs, mode, related skills
    └── invocation-guide.md  How to install and invoke each skill
```

Skills marked **⚠️ WIP** are still being refined and may change. The 12 skills in `requirements/` and the 3 standalone skills are production-ready. All skills use the same `SKILL.md` format and work with both Cursor and Claude Code.

---

## Installation

### Cursor

Skills live in `~/.cursor/skills/`. The recommended approach is to symlink each skill so that a `git pull` automatically picks up changes without re-linking.

```bash
# Clone the repo (if you haven't already)
git clone https://github.com/rushikeshpol02/ai-skills.git ~/ai-skills

# Create the skills folder if it doesn't exist
mkdir -p ~/.cursor/skills

# Symlink each skill (handles flat and nested category structure)
find ~/ai-skills/cursor/skills -mindepth 2 -maxdepth 3 -name "SKILL.md" | while read f; do
  skill=$(dirname "$f")
  ln -s "$skill" ~/.cursor/skills/$(basename "$skill")
done
```

Restart Cursor. Skills are loaded at agent startup — no other configuration required.

**Keeping skills up to date:**

```bash
cd ~/ai-skills && git pull
# Symlinks pick up changes automatically — no re-linking needed
```

---

### Claude Code

Skills live in `~/.claude/skills/`. Same symlink approach:

```bash
# Create the skills folder if it doesn't exist
mkdir -p ~/.claude/skills

# Symlink each skill (handles flat and nested category structure)
find ~/ai-skills/cursor/skills -mindepth 2 -maxdepth 3 -name "SKILL.md" | while read f; do
  skill=$(dirname "$f")
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done
```

Skills are discovered automatically by Claude Code at startup.

---

### Install for Both at Once

```bash
git clone https://github.com/rushikeshpol02/ai-skills.git ~/ai-skills
mkdir -p ~/.cursor/skills ~/.claude/skills

find ~/ai-skills/cursor/skills -mindepth 2 -maxdepth 3 -name "SKILL.md" | while read f; do
  skill=$(dirname "$f")
  name=$(basename "$skill")
  ln -s "$skill" ~/.cursor/skills/"$name"
  ln -s "$skill" ~/.claude/skills/"$name"
done
```

---

## Skills at a Glance

### Epics & User Stories Skills ⚠️ Work in Progress

> These skills are still being refined. Core functionality works but prompts, templates, and workflows are subject to change.

| Skill | One-liner | Mode |
|-------|-----------|------|
| [generate-epic](cursor/skills/epics-and-user-stories/generate-epic/SKILL.md) | Create a structured epic document from requirements or a verbal description; produces Epic-[Feature].md ready for story decomposition | Standalone |
| [generate-user-stories](cursor/skills/epics-and-user-stories/generate-user-stories/SKILL.md) | Decompose features using WAHZURT framework and generate INVEST-compliant user stories one-at-a-time with quality gates; supports create, quick/draft, modify, and decompose-only modes | Standalone |
| [validate-user-stories](cursor/skills/epics-and-user-stories/validate-user-stories/SKILL.md) | Audit existing user stories against 12 validation categories (9 per-story + 2 cross-story + 1 readability) and fix failures; always builds a fresh registry from actual files | Standalone |
| [generate-uat](cursor/skills/epics-and-user-stories/generate-uat/SKILL.md) | Generate a client-ready UAT test plan from GitHub issue files or a ticket list; extracts ACs, deduplicates cross-platform scenarios, and produces a requirement-pure test document | Standalone |

### Planning Skills ⚠️ Work in Progress

> These skills are still being refined. Core functionality works but prompts, templates, and workflows are subject to change.

| Skill | One-liner | Mode |
|-------|-----------|------|
| [release-sprint-planner](cursor/skills/planning/release-sprint-planner/SKILL.md) | Define a release goal, scope, and timeline; produce a formal Release Definition and multi-sprint plan | Standalone |
| [sprint-planning-session](cursor/skills/planning/sprint-planning-session/SKILL.md) | Turn a ticket list into a structured sprint planning document with goal, grouped work, and done criteria | Standalone |
| [sprint-progress-tracker](cursor/skills/planning/sprint-progress-tracker/SKILL.md) | Generate a mid-sprint or close-out progress snapshot showing planned vs actual and surfacing risks | Standalone |
| [sprint-review-generator](cursor/skills/planning/sprint-review-generator/SKILL.md) | Produce a stakeholder-facing sprint review document covering what was built, goal outcome, and next steps | Standalone |
| [meeting-to-plan-integrator](cursor/skills/planning/meeting-to-plan-integrator/SKILL.md) | Apply decisions from a sprint demo, retro, or stakeholder call back to the release plan and artifacts | Standalone |

### Requirements Pipeline Skills

| Skill | One-liner | Mode |
|-------|-----------|------|
| [requirements-pipeline](cursor/skills/requirements/requirements-pipeline/SKILL.md) | 9-stage discovery and analysis pipeline from messy inputs to production-ready docs; supports multi-feature decomposition | Pipeline Orchestrator |
| [generate-requirements](cursor/skills/requirements/generate-requirements/SKILL.md) | Generate Feature Requirements from well-defined inputs; API contracts generated separately using `rest-api-contract-generator` | Pipeline Stage / Standalone |
| [design-to-context](cursor/skills/design-to-context/SKILL.md) | Convert Figma URLs or design images into User Flow Docs, Design Descriptions, or Context Summaries | Pipeline Stage / Standalone |
| [transcript-to-meeting-notes](cursor/skills/transcript-to-meeting-notes/SKILL.md) | Turn meeting transcripts (.vtt, .md, .docx, .txt) into structured discovery summaries | Pipeline Stage / Standalone |
| [identify-assumptions](cursor/skills/requirements/identify-assumptions/SKILL.md) | Surface and structure risky assumptions using PM / Designer / Engineer perspectives | Pipeline Stage / Standalone |
| [validate-requirements](cursor/skills/requirements/validate-requirements/SKILL.md) | Combined semantic + structural review with 15 checks; supports incremental mode for re-validation | Pipeline Stage / Standalone |
| [document-audit](cursor/skills/requirements/document-audit/SKILL.md) | Scan any non-requirements document for stale markers, contradictions, and broken cross-references | Pipeline Stage / Standalone |

### Post-Pipeline Skills

| Skill | One-liner | Mode |
|-------|-----------|------|
| [review-findings](cursor/skills/requirements/review-findings/SKILL.md) | Walk through audit or validation report findings interactively and collect decisions | Post-Pipeline |
| [update-documents](cursor/skills/requirements/update-documents/SKILL.md) | Propagate a change (fact, scope, terminology) across multiple related documents with subagent execution | Post-Pipeline |
| [client-ready-requirements](cursor/skills/requirements/client-ready-requirements/SKILL.md) | Transform an internal requirements doc into a client-safe version for all stakeholder types | Post-Pipeline |
| [figjam-diagram-generator](cursor/skills/figjam-diagram-generator/SKILL.md) | Generate Mermaid.js diagrams in FigJam from requirements, user flows, or verbal input via Figma MCP | Post-Pipeline |
| [securitas-client-ready-requirements](cursor/skills/requirements/securitas-client-ready-requirements/SKILL.md) | Transform internal requirements into streamlined Securitas client-ready format | Post-Pipeline / Client-Specific |

---

## Documentation

- **[Workflow Guide](docs/workflow-guide.md)** — How the pipeline skills fit together, when to use the full pipeline vs a single skill, and mermaid diagrams of every relationship.
- **[Skill Catalog](docs/skill-catalog.md)** — Deep-dive reference for every skill: inputs, outputs, files produced, and related skills.
- **[Invocation Guide](docs/invocation-guide.md)** — How to trigger skills by name, by context, and how to chain the full pipeline in one conversation.

---

## Contributing

Skills are organized into category plugins:

- **`cursor/skills/epics-and-user-stories/`** — story lifecycle skills (epics, user stories, UAT)
- **`cursor/skills/planning/`** — delivery lifecycle skills (sprint planning, release planning, reviews)
- **`cursor/skills/requirements/`** — requirements and analysis skills (pipeline, validation, transformation)
- **`cursor/skills/`** (root) — standalone cross-cutting skills (`design-to-context`, `figjam-diagram-generator`, `transcript-to-meeting-notes`)

To add a new skill:
1. Place it in the appropriate category folder: `cursor/skills/<category>/<skill-name>/`
2. Add a `SKILL.md` — the agent reads this file at runtime
3. Update [docs/skill-catalog.md](docs/skill-catalog.md) with the new entry

Skills in this repo are production-ready. Work-in-progress or personal skills should live outside this repo (e.g., `~/personal-skills/wip/`) and be symlinked separately — this keeps the repo clean and ensures only stable skills are published.
