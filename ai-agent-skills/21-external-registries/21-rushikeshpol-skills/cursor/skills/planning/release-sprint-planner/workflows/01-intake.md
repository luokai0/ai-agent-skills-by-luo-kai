# Workflow 01: Intake

**Called from:** `SKILL.md` Step 4
**Next step:** `workflows/02-context-assessment.md`
**Saves to:** `[release-root]/.meta/Input-Inventory.md`

---

## Purpose

Gather raw inputs from any format and normalize them into a structured inventory so the context assessment can work from real data.

---

## Step 1: Gather Inputs

Prompt the user for each (accept any format):
- **Release name** (required)
- **Any existing artifacts:** scope docs, PRDs, meeting notes, feature lists, transcripts, design files, verbal descriptions
- **Known constraints or deadlines** mentioned upfront

For each input provided, read it and note what it contains.

---

## Step 2: Normalize

- Convert all feature/scope inputs into an internal feature table:

| # | Feature / Item | Source | Notes |
|---|---------------|--------|-------|

- Load `project-context.md` if available in the workspace root (pre-populates tech stack, personas, integrations, constraints)
- Identify information gaps: what do we have vs what do we still need?

---

## Step 3: Quality Gate — Tier Check

| Tier | Requirements | Status |
|------|-------------|--------|
| **Tier 1** (minimum viable) | Release name + at least a verbal description of what's being built | ✅ / ❌ |
| **Tier 2** (recommended) | Tier 1 + feature list + timeline + team size | ✅ / ❌ |
| **Tier 3** (comprehensive) | Tier 2 + requirements docs + meeting notes + constraints documented | ✅ / ❌ |

If Tier 1 is not met, STOP: "I need at minimum a release name and a description of what's being built."

---

## Step 4: Save Inventory

Save the normalized input inventory to: `[release-root]/.meta/Input-Inventory.md`

---

## Step 5: Update State File

Save the state file at `[release-root]/.meta/skill-state-release-sprint-planner.json`:

```json
{
  "skill": "release-sprint-planner",
  "release": "[release-name]",
  "current_task": "T0",
  "task_status_map": {
    "T0": "completed", "T1": "pending", "T2": "pending",
    "T3": "pending", "T4": "pending", "T5": "pending",
    "T6": "pending", "T7": "pending", "T8": "pending"
  },
  "gates_passed": {
    "context_assessment_confirmed": false,
    "release_definition_confirmed": false,
    "draft_plan_confirmed": false
  },
  "artifacts": {
    "input_inventory": "[release-root]/.meta/Input-Inventory.md",
    "context_assessment": null,
    "release_definition": null,
    "release_plan": null,
    "scope": null
  },
  "last_updated_utc": "[timestamp]"
}
```

---

## Completion Gate

- [ ] All user-provided inputs read and catalogued
- [ ] Features normalized into internal table
- [ ] project-context.md loaded (if available)
- [ ] Quality tier assessed
- [ ] Input inventory saved to file
- [ ] State file created

**CHECKPOINT (Notification):** "Here is what I have to work with: [inventory summary]. Tier [X] achieved. Let me assess what context I have before we start defining the release."

**When complete, return to `SKILL.md` and proceed to Step 5.**
