# Workflow 1: Prepare Story Context

**Called from:** `SKILL.md` after intake
**Next step:** `workflows/02-decompose.md` after user approves preparation
**Saves to:** `[output-folder]/.meta/Story-Prepare-[Feature].md` + `[output-folder]/.meta/.pipeline-state.json` + `[output-folder]/.meta/story-registry.md`

---

## 📍 You Are Here
**Skill:** generate-user-stories
**Stage:** 1 of 4 — Prepare
**Input:** Epic, requirements doc, or verbal description
**Your only job:** Read inputs, validate sufficiency, determine starting point, initialize tracking files
**DO NOT:** Decompose into stories — that's Stage 2.
**DO NOT:** Create any story files — that's Stage 3.
**DO NOT:** Skip input validation by jumping to decomposition.
**Audience:** You are preparing context for story creation. The stories will be read by developers and QA engineers who pick them up cold.

---

## 📖 Step 1: Read Available Inputs

Read all inputs identified during SKILL.md intake. Determine what you have:

| Input Type | What to extract | Starting stage |
|------------|----------------|---------------|
| **Decomposition file** (from prior run) | Story concepts, coverage map, requirements mapping | Skip to Stage 3 (create) |
| **Epic document** | Business goals, scope, out-of-scope, personas, constraints, designs | Proceed to Stage 2 (decompose) |
| **Requirements doc** | Functional requirements, business rules, personas, technical context | Proceed to Stage 2 (decompose) |
| **Verbal description** (Quick mode) | Feature concept, rough scope, known personas | Proceed to Stage 2 (lighter decompose) |

**If decomposition file exists and is complete:** Skip to Step 5 (initialize files), then route to `03-create-story.md`.

---

## 🔍 Step 2: Validate Input Sufficiency

**For Standard mode — minimum required:**
- Feature name ✅
- At least one of: epic, requirements doc, or decomposition file ✅
- At least 2 functional requirements or scope items identifiable ✅

**For Quick mode — minimum required:**
- Feature name ✅
- Verbal description with at least one user goal ✅

**If insufficient:** Suggest running `/generate-requirements` or `/generate-epic` first. Do not proceed with less than minimum.

---

## 📏 Step 3: Input Size Check

| Input | Rule if oversized |
|-------|-----------------|
| Requirements doc > 3,000 words | Focus on functional requirements sections. Say: "Large doc — focusing on FRs." |
| Epic > 1,000 words | Focus on scope and outcomes sections. |
| Multiple input docs | Ask: "Multiple docs found. Which feature should these stories cover?" |

---

## 🔬 Step 4: Extract Key Context

From available inputs, extract and record:

1. **Feature name and scope** — what's being built
2. **Personas** — specific roles (not generic "user"). Source each: `(Source: Requirements, §X)` or `(Source: project-context.md)`
3. **Platforms** — FE (web), FE (mobile), BE, API. Which platforms does this feature touch?
4. **Functional requirements** — numbered list of what the system must do. Each with source reference.
5. **Business rules** — constraints, validations, limits. Each sourced.
6. **Design references** — Figma links (if processed through `design-to-context`)
7. **Dependencies** — other systems, APIs, teams
8. **Out-of-scope** — what is explicitly excluded

**Quick mode:** Extract what's available. Mark gaps as `[TBD — verbal input only, no source doc]`.

---

## 💾 Step 5: Initialize Tracking Files

**Initialize `story-registry.md`** (empty):
```markdown
# Story Registry: [Feature Name]
## Conventions
[To be established after first story is approved]
## Stories
| # | Title | Platform | User Statement | Status |
|---|-------|----------|---------------|--------|
```
Save to: `[output-folder]/.meta/story-registry.md`

**Initialize `.pipeline-state.json`:**
```json
{
  "skill": "generate-user-stories",
  "feature": "[name]",
  "mode": "[Standard/Quick/Decompose-only]",
  "stage": "01-prepare",
  "stages_completed": ["01-prepare"],
  "stories_written": [],
  "stories_pending": [],
  "last_checkpoint": "approved"
}
```
Save to: `[output-folder]/.meta/.pipeline-state.json`

---

## 💾 Step 6: Save Preparation File

Save ALL extracted context to `[output-folder]/.meta/Story-Prepare-[Feature].md`. This file contains: feature metadata, mode, personas, platforms, FRs, business rules, design refs, dependencies, out-of-scope. **Stage 2 reads this file — not chat context.**

---

## 💬 Step 7: Chat Output (minimal — everything else stays in file)

Only show in chat:
```
Preparation saved: [file path]
Mode: [Standard/Quick] | Personas: [count] | FRs: [count] | Platforms: [list]
Next: Decompose into story concepts using WAHZURT. Approve?
```

**STOP and WAIT for user response.**

---

## 🔄 After User Approves

Update pipeline state, then **read:** `workflows/02-decompose.md`

---

## ✅ Completion Gate
- [ ] All inputs read and context extracted
- [ ] Input sufficiency validated for selected mode
- [ ] story-registry.md initialized and saved
- [ ] .pipeline-state.json initialized and saved
- [ ] User has explicitly approved
If any item is unchecked → do NOT proceed.
