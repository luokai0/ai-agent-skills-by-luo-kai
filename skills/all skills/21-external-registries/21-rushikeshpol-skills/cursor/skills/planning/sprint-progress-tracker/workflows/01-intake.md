# Workflow 01: Intake

**Called from:** `SKILL.md` Step 3
**Next step:** `workflows/02-analyze.md`
**Saves to:** `[sprint-root]/.meta/Status-Mapping.md`

---

## Purpose

Load planned work and current status. Normalize every ticket into a consistent status.

---

## Step 1: Gather Inputs

- **Sprint Planning Session doc** (required — this is the baseline)
- **Current ticket statuses** (any format — verbal, CSV, screenshot, board export)
- **Mode:** mid-sprint or close-out (detected in SKILL.md)
- **Constraint registry:** load `.meta/constraint-registry.md` if available
- **Blockers or risks surfaced since planning** (optional — verbal OK)

---

## Step 2: Normalize Status

Map every ticket from the planning doc to one of:

| Status | Definition |
|--------|-----------|
| **Done** | Meets "done" criteria from planning doc |
| **In Progress** | Started, actively being worked |
| **Blocked** | Started but cannot proceed — must state blocker |
| **Not Started** | No work begun |
| **Dropped** | Removed from sprint scope — must state reason |
| **Added** | Not in original plan — must state reason |

Produce the status mapping table:

| # | Title | Owner | Planned Status | Current Status | Notes |
|---|-------|-------|---------------|---------------|-------|

---

## Step 3: Quality Gate — Tier Check

| Tier | Requirements | Status |
|------|-------------|--------|
| **Tier 1** (minimum viable) | Planning doc + at least a verbal status update | ✅ / ❌ |
| **Tier 2** (recommended) | Tier 1 + ticket-level status for all items | ✅ / ❌ |
| **Tier 3** (comprehensive) | Tier 2 + blocker details + notes on each in-progress item | ✅ / ❌ |

If Tier 1 is not met, STOP: "I need at minimum the Sprint Planning Session doc and a status update."

---

## Step 4: Save Status Mapping

Save to: `[sprint-root]/.meta/Status-Mapping.md`

---

## Step 5: Update State File

Save the state file at `[sprint-root]/.meta/skill-state-sprint-progress-tracker.json`:

```json
{
  "skill": "sprint-progress-tracker",
  "sprint": "[sprint-number]",
  "mode": "[mid-sprint / close-out]",
  "current_task": "T0",
  "task_status_map": {
    "T0": "completed", "T1": "pending", "T2": "pending"
  },
  "artifacts": {
    "status_mapping": "[sprint-root]/.meta/Status-Mapping.md",
    "progress_report": null
  },
  "last_updated_utc": "[timestamp]"
}
```

---

## Completion Gate

- [ ] Sprint Planning Session doc loaded and parsed
- [ ] All tickets mapped to normalized status
- [ ] Quality tier assessed
- [ ] Status mapping saved
- [ ] State file created/updated

**CHECKPOINT (Notification):** "Loaded [N] tickets from planning doc. Status mapped for all items. Proceeding to analysis."

**When complete, return to `SKILL.md` and proceed to Step 4.**
