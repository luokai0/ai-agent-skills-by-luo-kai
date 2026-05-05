---
name: generate-requirements
description: "Generates Feature Requirements documentation from any combination of inputs -- PRDs, design files/Figma URLs, meeting transcripts, or verbal descriptions. Focuses exclusively on requirements; API contracts and system flows are generated separately after requirements are finalized. Runs in Quick mode (3 contexts, ~15 min) for MVPs/small features or Comprehensive mode (6 contexts, ~30 min) for production/complex features. Use when asked to: generate requirements, write a feature spec, create a PRD, or document a feature."
---

# Generate Requirements — Entry Orchestrator

## NON-NEGOTIABLE (read first)
1. Never fabricate data, business rules, or field names. Mark unknowns as [TBD].
2. Save every output file before presenting in chat. Chat is ephemeral.
3. Wait for user approval at every checkpoint. Never auto-proceed.
4. Requirements describe WHAT, never HOW (solution) or WHAT IT LOOKS LIKE (design).
5. Source traceability on every claim. Unsourced = flag as [TBD].

## Critical Rules

1. **Never skip steps** — The three workflows must run in order
2. **Always save files** — Every output is saved to the workspace, not just shown in chat
3. **Mark TBDs honestly** — Never invent business rules, performance targets, or field names
4. **Wait at checkpoints** — After each workflow, STOP and wait for user approval before continuing
5. **One skill at a time** — Complete each workflow file fully before reading the next
6. **Respect existing patterns** — If Swagger is provided, follow its naming and error conventions

---

## 🎯 Purpose

This skill generates production-ready Agile requirements documentation from messy inputs.
It orchestrates three sequential workflows, each saved as a file, so context survives across long sessions.

**What you'll get:**
- `[output-folder]/Context-Summary-[Feature].md` — internal analysis artifact
- `[output-folder]/Generated/Internal/Feature-Requirements-[Feature].md` — always generated
- `[output-folder]/Generated/Report/Validation-Report-[Feature].md` — quality gate report

`[output-folder]` is provided by the user during intake (Step 2). There is no default — always ask.

> **Note:** This skill focuses on Feature Requirements only. API Contracts and System Flows are generated separately after requirements are finalized, using `/rest-api-contract-generator` and a dedicated system flow skill respectively.

**Core principle: Truth over completeness.** Mark unknowns as [TBD]. Never fabricate data.

---

## 🔗 When Called from `/requirements-pipeline` (Stage 7)

When this skill is invoked from the `/requirements-pipeline`, **skip Steps 1-3 entirely** (workspace scan, project context loading, intake questions, pre-flight checks). The pipeline has already completed all of this.

The pipeline provides:
- **Feature name** -- from Stage 1
- **Mode** -- always Comprehensive
- **All inputs** -- processed and verified in Stages 1-6 (including scenario matrix, assumptions, user flows)
- **Output folder** -- asked by the pipeline at Stage 7 if not already known
- **Project context** -- loaded by the pipeline at Stage 1.1 if `project-context.md` exists
- **Current state** -- from pipeline Stage 1.5

Go directly to **Step 4** (Start Synthesis Workflow) with all values pre-loaded, then read `workflows/01-synthesize.md`.

---

## 🔄 Workflow Chain

This skill chains three workflows in sequence:

```
[You are here]
SKILL.md (Intake)
     ↓ reads
workflows/01-synthesize.md     → saves Context-Summary-[Feature].md
     ↓ reads
workflows/02-generate.md       → saves requirement doc(s)
     ↓ reads
workflows/03-validate.md       → saves Validation-Report-[Feature].md
```

Each workflow file is read in turn. Do NOT skip ahead.

---

## 📥 Step 1: Scan Workspace for Available Inputs

Before asking the user anything, scan the workspace folder for relevant files:

```bash
ls [workspace]
ls [workspace]/requirements/   # check for existing project context and prior sessions
```

Look for:
- `project-context.md` — **project-level context file** (pre-populates most questions if present)
- `**/Context-Summary-*.md` — prior session summaries (useful for resume)
- `*.md`, `*.pdf`, `*.docx` — likely PRDs or specs
- `*.yaml`, `*.json`, `*.yml` — likely Swagger/OpenAPI specs
- `*.png`, `*.jpg`, `*.figma` — likely design files
- `*transcript*`, `*notes*`, `*meeting*` — likely transcripts

Report what you found:
```
📂 Found in workspace:
- project-context.md: ✅ Found — project memory loaded / ❌ Not found
- [other files found]
```

---

## 🗂️ Step 1.5: Load Project Context (IF project-context.md exists)

**IF `project-context.md` is found in the workspace root:**

1. Read the file completely
2. Extract and cache internally:
   - Tech stack (frontend, backend, DB)
   - API conventions (auth, naming, error shape, pagination)
   - Defined personas (names, roles, pain points)
   - System components and integrations
   - Compliance baseline
   - Browser/device support
   - Project-wide out-of-scope items
   - Glossary

3. Announce what was loaded:
```
✅ Project context loaded from project-context.md
   I already know:
   - Stack: [Frontend] + [Backend] + [DB]
   - Auth: [method]
   - Personas: [Persona 1 name], [Persona 2 name]
   - Integrations: [count] pre-defined

   I only need feature-specific information.
```

**This context is automatically applied to Workflow 1 (Synthesis) and pre-populates:**
- Technical Context (stack, conventions, integrations)
- Persona Context (uses existing personas; new ones flagged for update)
- Compliance Context (uses baseline; overrides noted per feature)

**IF `project-context.md` is NOT found:**

Proceed to Step 2 as normal. After the session completes, offer:
```
💡 This is the first time I've run on this project. Want me to create a
   project-context.md file from what I learned? This will save time on
   future features.
```

---

## 📋 Step 2: Gather Required Context

**IF project-context.md was loaded**, ask only what's missing:

```
I have your project context. For this feature, I need:

1. **Feature name** — What is this feature called?

2. **Feature-specific inputs** — Do you have any of these for this feature?
   - [ ] PRD or feature description
   - [ ] Design files (Figma URL or images)
   - [ ] Swagger changes / new endpoints
   - [ ] Meeting transcript or notes
   - [ ] Just your description in this chat

3. **New or existing feature?**
   - A) New feature (greenfield)
   - B) Modifying an existing feature

4. **Scope?**
   - A) Quick Mode — lightweight analysis, 3 contexts (Business, Product, UX). Best for MVPs, small changes, internal tools.
   - B) Comprehensive Mode — full analysis, 6 contexts (adds Persona, Technical, Compliance). Best for production features, complex integrations, compliance-sensitive work.
   - C) Suggest based on inputs

5. **Output folder** — Where should generated documents be saved?
   Provide the path to the folder (e.g., `Product Artifacts/Feature Requirements/MyFeature`).
   The skill will create `Generated/Internal/` and `Generated/Report/` subdirectories inside it.
```

**IF project-context.md was NOT loaded**, ask the full set:

```
To generate requirements, I need a few details:

1. **Feature name** — What is this feature called?

2. **Inputs available** — Which of these do you have?
   - [ ] PRD or feature description document
   - [ ] Design files (Figma URL or images)
   - [ ] Swagger/OpenAPI specification
   - [ ] Meeting transcript or notes
   - [ ] Just your description in this chat

3. **New or existing feature?**
   - A) New feature (greenfield)
   - B) Modifying an existing feature

4. **Scope?**
   - A) Quick Mode — lightweight analysis, 3 contexts (Business, Product, UX). Best for MVPs, small changes, internal tools. (~15 min)
   - B) Comprehensive Mode — full analysis, 6 contexts (adds Persona, Technical, Compliance). Best for production features, complex integrations, compliance-sensitive work. (~30 min)
   - C) Not sure — I'll suggest based on your inputs

5. **Output folder** — Where should generated documents be saved?
   Provide the path to the folder (e.g., `Product Artifacts/Feature Requirements/MyFeature`).
   The skill will create `Generated/Internal/` and `Generated/Report/` subdirectories inside it.
```

**Mode inference (if user selects C):**
- Multiple actors, complex interactions, compliance concerns → Comprehensive
- External system integrations or dependencies → Comprehensive
- Simple UI-only feature, single actor, low risk → Quick
- Production deadline / enterprise context → Comprehensive
- State recommendation: "Based on your inputs, I recommend [Mode] because [reason]. Confirm?"

---

## ⚡ Step 3: Pre-Flight Checks

Before starting synthesis, confirm:

| Check | Source | Action if missing |
|-------|--------|-------------------|
| Feature name captured | User input | Required — ask |
| At least 1 input source | User input or workspace scan | Required — verbal description qualifies |
| Mode determined | Inferred or confirmed | Required — infer or ask |
| Output folder confirmed | User input | Required — ask. No default; user must provide the path. |
| Project context loaded? | project-context.md | If found: pre-populated. If not: proceed without it |
| Design files provided? | Workspace or user | Note: "I'll analyze designs in Workflow 1" |
| Transcript provided? | Workspace or user | Note: "I'll extract decisions from transcript in Workflow 1" |

**Output folder structure:**

The user provides `[output-folder]` during intake. The skill creates subdirectories inside it:
```
[output-folder]/
├── Context-Summary-[Feature].md          ← analysis artifact
├── Generated/
│   ├── Internal/
│   │   └── Feature-Requirements-[Feature].md   ← requirements document
│   └── Report/
│       └── Validation-Report-[Feature].md      ← quality gate
```
Create the `Generated/Internal/` and `Generated/Report/` subdirectories when saving files. The project-context.md stays in the workspace root (not inside the feature folder).

---

## 🚀 Step 4: Start Synthesis Workflow

Once intake is complete, confirm what you have and what's pre-loaded:

```
✅ Ready to start.

Feature: [name]
Mode: [Quick / Comprehensive]
Inputs: [list]
Project context: ✅ Loaded ([N] contexts pre-populated) / ❌ Not found (starting fresh)
Output folder: [output-folder]/
  Internal docs → [output-folder]/Generated/Internal/
  Reports       → [output-folder]/Generated/Report/

Starting Workflow 1: Context Synthesis...
```

Pass the following to Workflow 1:
- Feature name
- Mode (Quick / Comprehensive)
- Input sources list
- Output folder path (user-provided)
- Project context (if loaded) — mark which contexts are pre-populated vs need feature-specific input
- Whether "verify existing" (Step 0.5) should run

Then **read the file:**
```
workflows/01-synthesize.md
```

Follow that file's instructions completely from start to finish.

---

## 📎 Related Skills (Complementary)

These existing skills can assist with specific inputs before running this workflow:

| Situation | Skill to suggest |
|-----------|-----------------|
| User has a meeting recording or .vtt transcript | `transcript-to-meeting-notes` — process first, use output as PRD input |
| User has Figma URL or design screenshots | Design analysis is built into this skill's Workflow 1 |
| Requirements are finalized and need API contracts | `rest-api-contract-generator` — run after requirements are stable |
| Requirements are finalized and need system flow docs | Future: `system-flow-generator` — run after requirements are stable |

---

---

## 🔄 After All Workflows Complete: Update Project Context

When Workflow 3 (Validation) finishes, offer to create or update the project context:

```
To capture what was learned in this session (new personas, systems,
constraints, terminology), run /project-context to create or update
your project-context.md.

This is optional but recommended -- it saves time on future sessions.
```

The `/project-context` skill handles both first-time creation and incremental updates with source confirmation and conflict detection. Do NOT attempt to create or update `project-context.md` inline.

---

**INTAKE COMPLETE → Read `workflows/01-synthesize.md` to begin**
