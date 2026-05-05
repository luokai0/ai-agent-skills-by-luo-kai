---
name: validate-user-stories
description: "Audits existing user stories against 12 validation categories (9 per-story + 2 cross-story + 1 practitioner readability) and fixes failures. Builds a fresh registry from actual story files — never trusts existing registries. Works on any story set regardless of how stories were created. Use when asked to: validate stories, check stories, review stories, audit stories, fix stories, or improve story quality."
---

# Validate User Stories — Entry Orchestrator

## ⚠️ Execution Discipline
You are now operating under this skill's instructions exclusively.
BEFORE generating ANY output, verify:
1. Have I read the workflow file for this step?
2. Have I completed ALL prior stages per the state file?
3. Has the user explicitly approved the last checkpoint?
If ANY answer is NO → stop. Read the correct workflow file.
NEVER generate validation reports without following the workflow files.

## 🎯 Purpose

Audit existing stories against 12 validation categories and fix failures.
Always builds a fresh registry from actual files — never trusts existing registries.
Works on any story set regardless of how stories were created.

**What you'll get:**
- `[output-folder]/validation-registry-[feature].md` — fresh ground truth from actual files
- `[output-folder]/Validation-Report-[Feature].md` — full audit report

**Core principle:** A false pass means broken work enters the sprint. A false fail wastes rework and trust. Both are failures.

---

## 🔄 Workflow Chain

```
[You are here]
SKILL.md (Intake)
     ↓ reads
workflows/01-validate.md     → builds fresh registry, runs 12 categories, generates report
     ↓ reads (if fixes needed)
workflows/02-fix.md          → fixes failures in Ring order, re-validates
```

---

## 📥 Step 1: Three-Tier Scoping Gate

### Tier 1: User-Provided Files (always included)
Story files or feature folder referenced by user. No confirmation needed.

### Tier 2: Same-Folder Scan (user selects)
Glob parent folder(s). Look for: other stories in same feature folder, requirements doc, epic.
Present grouped. User selects. Unselected never read.

### Tier 3: Workspace-Wide Search (opt-in only)
After Tier 2, offer broader search. If declined, proceed with Tier 1+2 only.

---

## 📂 Step 1.5: Load Project Context

**IF `project-context.md` found:** Read and extract personas, stack, conventions.
**IF not found:** Proceed without it.

---

## 📋 Step 2: Gather Context

```
For validation, I need:
1. Which stories? (single file / feature folder / all)
2. Requirements doc or epic? (for source verification — optional but improves quality)
3. Output folder for the validation report
```

---

## 🔀 Step 3: Mode Detection

| Mode | Signal | Route |
|------|--------|-------|
| **VALIDATE** | "validate", "check", "review", "audit" | `workflows/01-validate.md` |
| **FIX** | "fix", "improve", "update", "recover" | `workflows/01-validate.md` → `workflows/02-fix.md` |

---

## ⚡ Step 3.5: Pre-Flight Checks

| Check | Action if missing |
|-------|-------------------|
| At least 1 story file found | Required — ask |
| Feature name captured | Required — infer from folder or ask |
| Output folder confirmed | Required — ask |
| Requirements doc available? | Optional — source verification will be limited without it |

---

## 🚀 Step 4: Start Validation

```
Ready to validate.

Stories found: [count] files in [folder]
Requirements doc: ✅ Found / ❌ Not found (source verification limited)
Output folder: [path]

Starting validation...
```

Then **read:** `workflows/01-validate.md`

---

## 🚨 Critical Rules

1. **Always build fresh registry** — never trust existing `.meta/story-registry.md`. Read actual files.
2. **Ring 1 first** — if Ring 1 fails, skip Ring 2-3. Don't waste effort on format when structure is broken.
3. **Evidence for every finding** — no finding without citing specific story, AC, and evidence.
4. **Impact statements** — every finding says "This means..." (what happens if not fixed).
5. **Creation-validation alignment** — if stories were created by `generate-user-stories`, Categories 1-9 should PASS. Any failure = creation skill bug. Flag it.
6. **Fix first, present second** — never present output the tool knows has quality issues.

---

## 📎 Related Skills

| After validation... | Skill to suggest |
|--------------------|-----------------|
| Walk through findings interactively | `/review-findings` |
| Fix stories and audit for staleness | `02-fix.md` → `/document-audit` |
| Modify a specific story | `/generate-user-stories` (modify mode) |

---

**INTAKE COMPLETE → Read `workflows/01-validate.md` to begin**
