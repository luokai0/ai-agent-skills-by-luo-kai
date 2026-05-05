# Workflow 1: Prepare Epic Context

**Called from:** `SKILL.md` after intake
**Next step:** `workflows/02-generate-epic.md` after user approves preparation summary
**Saves to:** `[output-folder]/.meta/Epic-Prepare-[Feature].md` + `[output-folder]/.meta/.pipeline-state.json`

---

## 📍 You Are Here
**Skill:** generate-epic
**Stage:** 1 of 2 — Prepare
**Input:** Requirements doc (or verbal description)
**Your only job:** Read inputs, extract epic-relevant facts, identify gaps, present summary
**DO NOT:** Generate the epic document — that's Stage 2.
**DO NOT:** Skip Current State Discovery by assuming greenfield.
**DO NOT:** Infer business outcomes — extract only what source states.
**Audience:** You are writing for a PO and team lead who need to understand the feature's business value, scope, and decomposability.

---

## 📏 Step 1: Input Size Check

| Input | Rule if oversized |
|-------|-----------------|
| Requirements doc > 3,000 words | Focus on: business goals, success criteria, scope boundaries, constraints. Say: "Large requirements doc — extracting epic-relevant sections." |
| Multiple requirements docs provided | Ask: "Multiple docs found. Which feature should this epic cover?" |

---

## 🔍 Step 2: Current State Discovery (mandatory)

Ask the user (if not already answered in SKILL.md intake):
- "Is this a new feature (greenfield) or an enhancement to something that already exists?"
- If enhancement: "What exists today? Describe or provide: existing screens, current capabilities, known limitations."

**If enhancement:** Require current state baseline. Process any Figma links through `design-to-context`.
**If unknown:** Flag: `[CURRENT STATE UNKNOWN — do not assume what exists today]`. Carry this flag into epic generation.
**If greenfield:** Proceed — no current state needed.

---

## 📖 Step 3: Read and Extract

Read requirements doc (primary input) and project context (if loaded).

Extract these elements with source attribution using `(Source: Requirements, §X)` or `(Source: project-context.md)`:

**Epic Priority 1 — Business Outcome:**
- Business goals (measurable where possible)
- Success criteria / KPIs
- Why this feature exists (business value)

**Epic Priority 2 — Decomposability:**
- Major capability areas (can these become independent stories?)
- Any circular dependencies that would prevent decomposition

**Epic Priority 3 — Scope Boundaries:**
- In-scope capabilities
- Out-of-scope items (explicitly stated)
- Constraints (timeline, budget, regulatory, technical)

**Also extract:**
- Personas involved (specific roles, not generic "user")
- Platforms (web, mobile, API)
- Risks and dependencies
- Design references (Figma links, if processed)

---

## 🔬 Step 4: Inference Register

Separate STATED facts (explicitly in source) from INFERRED conclusions (derived from scope/context). Present both lists with source references. Ask user to confirm or reject each inference.

- Confirmed inferences → marked `(Source: Inferred from §X, confirmed by user)`
- Rejected inferences → dropped entirely
- User must confirm before inferences become source material for the epic

---

## 🚩 Step 5: Gap Identification

For each extracted element, classify:
- ✅ **Known** — clearly stated in source
- ⚠️ **Inferred** — logically deduced (lower confidence)
- ❌ **TBD** — missing; must be gathered

Categorize TBDs by severity using epic priority stack:

| Gap Area | Priority | Severity if missing |
|----------|----------|-------------------|
| Business outcome / success criteria | Priority 1 | 🔴 RED |
| Decomposability (monolithic, circular deps) | Priority 2 | 🔴 RED |
| Scope boundaries (in/out of scope) | Priority 3 | 🟡 YELLOW |
| Format elements (milestones, change history) | Priority 4 | 🟢 GREEN |

**Blocking threshold:**
- **3+ RED gaps → STOP.** Request input: "I need [specific items] before I can create a useful epic."
- **1-2 RED gaps → Mark `[TBD — requires: {need}] (Route to: {role})`**, proceed with warning
- **YELLOW/GREEN only → Proceed normally**

---

## 💾 Step 6: Save Preparation File

Save ALL extracted context, inferences, and gap analysis to `[output-folder]/.meta/Epic-Prepare-[Feature].md`. This file contains: feature metadata, current state, all Priority 1-3 extractions with source citations, inference register, gap analysis. **Stage 2 reads this file — not chat context.**

---

## 💬 Step 7: Chat Output (minimal — everything else stays in file)

Only show in chat:
1. **Inferences needing confirmation** (numbered list, one line each)
2. **Blocking gaps** (if 3+ RED): "❌ Cannot proceed — [N] critical gaps: [list]"
3. **Summary** (always): file path, coverage per priority (✅/⚠️/❌), gap counts, "Ready to generate epic?"

**STOP and WAIT for user response.**

---

## 🔄 After User Approves

1. Update inference statuses in `[output-folder]/.meta/Epic-Prepare-[Feature].md` (confirmed/rejected)
2. Save pipeline state to `[output-folder]/.meta/.pipeline-state.json`: skill, feature, stage "01-prepare", stages_completed, last_checkpoint "approved"
3. **Read the file:** `workflows/02-generate-epic.md`

---

## ✅ Completion Gate
- [ ] All inputs read and extracted
- [ ] Current state determined (greenfield / enhancement / unknown)
- [ ] Preparation file saved to `[output-folder]/.meta/Epic-Prepare-[Feature].md`
- [ ] Inference register presented and user confirmed
- [ ] Gaps identified and categorized
- [ ] Pipeline state file saved
- [ ] User has explicitly approved
If any item is unchecked → do NOT proceed.
