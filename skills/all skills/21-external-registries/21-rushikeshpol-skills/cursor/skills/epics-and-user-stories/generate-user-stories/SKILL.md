---
name: generate-user-stories
description: "Decomposes features into story concepts using the WAHZURT framework, then creates detailed INVEST-compliant user stories one-at-a-time with quality gates. Supports 4 modes: create (standard), create (quick/draft), modify existing stories, or decompose-only. Use when asked to: create user stories, write stories, generate stories, decompose an epic, break down a feature, plan stories, write acceptance criteria, modify a story, improve a story, enhance a story, or update a story."
---

# Generate User Stories — Entry Orchestrator

## ⚠️ Execution Discipline
You are now operating under this skill's instructions exclusively.
BEFORE generating ANY output, verify:
1. Have I read the workflow file for this step?
2. Have I completed ALL prior stages per the state file?
3. Has the user explicitly approved the last checkpoint?
If ANY answer is NO → stop. Read the correct workflow file.
NEVER generate stories without following the workflow files.

## 🎯 Purpose

Decompose features into story concepts, then create detailed user stories one-at-a-time with inline quality gates.
Each story is saved as an individual file. A story registry tracks cross-story coherence.

**What you'll get:**
- `[output-folder]/[platform]-story-[N]-[name].md` — individual story files (root folder, clean)
- `[output-folder]/.meta/` — intermediate artifacts:
  - `Decomposition-[Feature].md` — story concept list with coverage map
  - `story-registry.md` — cumulative cross-story tracker
  - `Story-Prepare-[Feature].md` — extracted context from inputs
  - `.pipeline-state.json` — stage tracking

**Core principle: A user story is a communication tool first.** Its purpose is to transfer enough understanding to the people who build and test it — clearly enough that they don't need to stop and ask. If it fails that, it fails its job.

**The real test — two cold reads, both must pass:**
- **Developer:** Can someone pick this up cold, read it once, and know what to build?
- **QA:** Can someone pick this up cold, read it once, and know how to verify it's done?

---

## 🔗 When Called from `/story-pipeline`

When invoked from story-pipeline, **skip Steps 1-3** (scoping gate, project context, intake). The pipeline provides feature name, inputs, output folder, and project context.

Go directly to **Step 4** with all values pre-loaded, then read the appropriate workflow file.

---

## 🔄 Workflow Chain

```
[You are here]
SKILL.md (Intake + Mode Detection)
     ↓ reads (based on mode)
workflows/01-prepare.md       → validates inputs, determines starting point
     ↓ reads
workflows/02-decompose.md     → WAHZURT analysis → story concepts + coverage map
     ↓ reads
workflows/03-create-story.md  → creates stories via sub-agents, registry, grouped approval
     ↓ reads
workflows/04-set-review.md    → cross-story coherence check
     ↓ (MODIFY mode only)
workflows/05-modify-story.md  → targeted edits to existing stories
```

---

## 📥 Step 1: Three-Tier Scoping Gate

**Never scan the full workspace by default.** Progressive, user-confirmed scoping.

### Tier 1: User-Provided Files (always included)
Files/folders referenced, URLs pasted, verbal descriptions. No confirmation needed.

### Tier 2: Same-Folder Scan (user selects)
Glob parent folder(s) of provided files. Present grouped by type (requirements, epics, existing stories). User selects. Unselected never read.

### Tier 3: Workspace-Wide Search (opt-in only)
After Tier 2, offer broader search. If accepted: keyword search from Tier 1+2 content. If declined: proceed with Tier 1+2 only.

### Final Input Set
Lock inputs after scoping. No additional files read unless user provides later.

---

## 📂 Step 1.5: Load Project Context

**Check for `project-context.md` in the workspace root.**

**IF found:** Read and extract: personas, stack, integrations, constraints, glossary.
**IF not found:** Proceed without it. Offer `/project-context` after completion.

---

## 📋 Step 2: Gather Required Context

```
For this story set, I need:
1. Feature name
2. Input source — which do you have?
   - [ ] Decomposition file (from prior run)
   - [ ] Epic document
   - [ ] Feature Requirements document
   - [ ] Just your description (Quick/Draft mode)
3. Output folder — where should stories be saved?
```

---

## 🔀 Step 3: Mode Detection

| Mode | Signal | Route |
|------|--------|-------|
| **CREATE (Standard)** | "create", "write", "generate" + structured input (requirements doc, epic, decomposition) | All stages: 01-prepare → 02-decompose → 03-create → 04-set-review |
| **CREATE (Quick)** | "create", "write" + only verbal input, no structured doc | 01-prepare → 02-decompose (lighter) → 03-create (stories marked `[DRAFT]`) |
| **MODIFY** | "modify", "improve", "enhance", "update", "change" + existing story referenced | Direct to 05-modify-story |
| **DECOMPOSE only** | "decompose", "break down", "plan stories" | 01-prepare → 02-decompose only |

**Quick mode warning:**
```
No requirements doc found. I can create draft stories from your description,
but they'll be marked [DRAFT — requires requirements doc for production quality].
For production stories, run /generate-requirements first.
```

---

## ⚡ Step 3.5: Pre-Flight Checks

| Check | Source | Action if missing |
|-------|--------|-------------------|
| Feature name captured | User input | Required — ask |
| At least 1 input source | User input or scan | Required — verbal qualifies |
| Mode determined | Keywords + input type | Required — infer or ask |
| Output folder confirmed | User input | Required — ask |
| Project context loaded? | project-context.md | Optional — proceed without |
| Design files provided? | Workspace or user | If Figma URL: verify processed through `design-to-context`. Unprocessed URL cannot be cited. |

### Processing Verification Gate (if design files provided)
Every design URL routed to `design-to-context` MUST have saved output before proceeding.
URL alone is NOT a processed output. ❌ = run the skill immediately.

---

## 🚀 Step 4: Route to Workflow

**Determine starting point based on available inputs:**

| Input Available | Start From |
|----------------|------------|
| Decomposition file from prior run | `workflows/03-create-story.md` (skip decompose) |
| Epic or requirements doc | `workflows/01-prepare.md` → `02-decompose.md` |
| Verbal description only (Quick mode) | `workflows/01-prepare.md` → `02-decompose.md` (lighter) |
| Existing story to modify | `workflows/05-modify-story.md` |

```
Ready to start.

Feature: [name]
Mode: [Standard / Quick / Modify / Decompose-only]
Inputs: [list]
Project context: ✅ Loaded / ❌ Not found
Output folder: [path]
Starting from: [workflow name]
```

Then read the appropriate workflow file.

---

## 🚨 Critical Rules

1. **Never skip workflows** — Stages run in order. Each reads the prior stage's output file.
2. **Always save files** — Stories, registry, decomposition saved to workspace. Chat is ephemeral.
3. **Mark TBDs honestly** — `[TBD — requires: {need}] (Route to: {role})`. Never fabricate.
4. **Wait at checkpoints** — STOP after decomposition, after each story group, after set review.
5. **Source accuracy > completeness** — An incomplete story that is honest beats a complete story with invented data.
6. **WHAT not HOW** — Design decisions ARE requirements. Technology choices are implementation. Never prescribe implementation.
7. **Split, don't compress** — If a story needs > 6 ACs, it's too big. Split it. Don't merge ACs.

---

## 📎 Related Skills

| Situation | Skill to suggest |
|-----------|-----------------|
| No requirements doc exists | `/generate-requirements` or `/requirements-pipeline` |
| Need an epic first | `/generate-epic` |
| Validate stories after creation | `/validate-user-stories` |
| Full pipeline | `/story-pipeline` |
| Design files need processing | `/design-to-context` |

---

**INTAKE COMPLETE → Read the appropriate workflow file to begin**
