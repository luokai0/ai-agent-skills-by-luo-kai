---
name: generate-epic
description: "Creates structured epic documents from requirements documentation or verbal descriptions. Extracts business goals, success criteria, scope boundaries, and dependencies. Produces a single Epic-[Feature].md file ready for story decomposition. Use when asked to: create an epic, write an epic, generate an epic, or document a feature as an epic."
---

# Generate Epic — Entry Orchestrator

## ⚠️ Execution Discipline
You are now operating under this skill's instructions exclusively.
BEFORE generating ANY output, verify:
1. Have I read the workflow file for this step?
2. Have I completed ALL prior stages per the state file?
3. Has the user explicitly approved the last checkpoint?
If ANY answer is NO → stop. Read the correct workflow file.
NEVER generate epics without following the workflow files.

## 🎯 Purpose

Create a structured epic document from a validated requirements doc (or verbal description as fallback).
This skill orchestrates two sequential workflows, each saved as a file.

**What you'll get:**
- `[output-folder]/Epic-[Feature-Name].md` — the epic document (root folder, clean)
- `[output-folder]/.meta/` — intermediate artifacts (Epic-Prepare, .pipeline-state.json)

**Core principle: Truth over completeness.** Mark unknowns as `[TBD — requires: {need}] (Route to: {role})`. Never fabricate data.

**Audience frame:** You are writing for a PO and team lead who need to understand the feature's business value, scope, and decomposability.

---

## 🔗 When Called from `/story-pipeline` (Stage 1)

When invoked from the story-pipeline, **skip Steps 1-3** (scoping gate, project context, intake). The pipeline has already completed these.

The pipeline provides:
- **Feature name** — from pipeline intake
- **All inputs** — scoped and verified
- **Output folder** — from pipeline
- **Project context** — loaded by pipeline if exists

Go directly to **Step 4** with all values pre-loaded, then read `workflows/01-prepare.md`.

---

## 🔄 Workflow Chain

```
[You are here]
SKILL.md (Intake)
     ↓ reads
workflows/01-prepare.md     → extracts context, identifies gaps, presents summary
     ↓ reads
workflows/02-generate-epic.md  → saves Epic-[Feature-Name].md
```

Each workflow file is read in turn. Do NOT skip ahead.

---

## 📥 Step 1: Three-Tier Scoping Gate

**Never scan the full workspace by default.** Inputs are gathered progressively with user confirmation.

### Tier 1: User-Provided Files (always included)
Collect everything the user explicitly provided:
- Files or folders referenced in their message
- URLs pasted in chat (Figma, FigJam, etc.)
- Verbal descriptions typed directly

These are primary inputs — no confirmation needed, no scanning needed.

### Tier 2: Same-Folder Scan (user selects)
Glob ONLY the parent folder(s) of user-provided files. Present discovered files grouped by type:
```
I found these additional files in the same folder(s):

Requirements / Specs:
- [filename] (modified: [date])

Epics / Planning:
- [filename] (modified: [date])

Which of these should be included? Unselected files will be ignored.
```

User explicitly selects. Unselected files are never read.

### Tier 3: Workspace-Wide Search (opt-in only)
After Tier 2 confirmation, offer:
```
Would you like me to search the rest of the workspace for related files?
I'll use targeted keyword search — not a full scan.
```

If accepted: extract key terms from Tier 1+2, grep + glob across workspace, present matches for user selection.
If declined: proceed with Tier 1 + Tier 2 selections only.

### Final Input Set
```
Final input set:
- [N] files from Tier 1 (user-provided)
- [M] files from Tier 2 (same-folder, user-selected)
- [P] files from Tier 3 (workspace search, user-selected) [if applicable]
Total: [N+M+P] inputs
```

No additional files will be read unless the user explicitly provides them later.

---

## 📂 Step 1.5: Load Project Context

**Check for `project-context.md` in the workspace root.**

**IF found:** Read completely and extract: personas, stack, integrations, constraints, glossary.
```
Project context loaded from project-context.md:
- Stack: [summary]
- Personas: [list]
- Constraints: [count] known
This context will be applied during epic generation.
```

**IF not found:** Proceed without it. After completion, offer to create via `/project-context`.

---

## 📋 Step 2: Gather Required Context

**IF project-context.md was loaded**, ask only what's missing:
```
I have your project context. For this epic, I need:
1. Feature name — What is this feature called?
2. Requirements doc — Do you have a Feature-Requirements-[Feature].md?
3. New or existing feature? (greenfield / enhancement)
4. Output folder — Where should the epic be saved?
```

**IF no requirements doc exists:** Suggest running `/generate-requirements` or `/requirements-pipeline` first. Accept brief verbal description as fallback with reduced quality warning:
```
No requirements doc found. I can create an epic from your description,
but quality will be limited. For production epics, run /generate-requirements first.
```

---

## ⚡ Step 3: Pre-Flight Checks

| Check | Source | Action if missing |
|-------|--------|-------------------|
| Feature name captured | User input | Required — ask |
| At least 1 input source | User input or scan | Required — verbal qualifies |
| Greenfield vs enhancement | User input | Required — ask |
| Output folder confirmed | User input | Required — ask |
| Project context loaded? | project-context.md | Optional — proceed without |
| Design files provided? | Workspace or user | If Figma URL: verify processed through `design-to-context`. Unprocessed URL cannot be cited as source. |

### Processing Verification Gate (if design files provided)
```
Processing verification:
- [input] → [skill] → [output file] → ✅ / ❌
```
Rules:
- Every design URL routed to `design-to-context` MUST have saved output before proceeding
- URL alone is NOT a processed output
- ❌ = run the skill immediately before proceeding

---

## 🚀 Step 4: Start Preparation Workflow

```
Ready to start.

Feature: [name]
Type: [Greenfield / Enhancement]
Inputs: [list]
Project context: ✅ Loaded / ❌ Not found
Output folder: [path]

Starting Workflow 1: Preparation...
```

Then **read the file:** `workflows/01-prepare.md`

Follow that file's instructions completely from start to finish.

---

## 🚨 Critical Rules

1. **Never skip workflows** — The two workflows must run in order
2. **Always save files** — Every output is saved to workspace, not just shown in chat
3. **Mark TBDs honestly** — `[TBD — requires: {need}] (Route to: {role})`. Never fabricate.
4. **Wait at checkpoints** — After each workflow, STOP and wait for user approval
5. **One skill at a time** — Complete each workflow file fully before reading the next
6. **Source accuracy > completeness** — An incomplete epic that is honest beats a complete epic with invented data

---

## 📎 Related Skills

| Situation | Skill to suggest |
|-----------|-----------------|
| No requirements doc exists | `/generate-requirements` or `/requirements-pipeline` — run first |
| Epic is approved, ready for stories | `/generate-user-stories` — run after |
| User has Figma URL or design screenshots | `/design-to-context` — process before using as source |
| Full pipeline from requirements to stories | `/story-pipeline` — orchestrates everything |

---

**INTAKE COMPLETE → Read `workflows/01-prepare.md` to begin**
