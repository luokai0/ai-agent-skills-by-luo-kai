# Workflow 01: Intake

**Called from:** `SKILL.md` Step 4
**Next step:** `workflows/02-organize.md`
**Saves to:** `[sprint-root]/stage_output/Normalized-Tickets.md`

---

## Purpose

Gather and normalize all inputs for this sprint. Accept tickets in any format and convert them to a standard internal table.

---

## Step 1: Normalize Ticket List

Convert the raw ticket input (any format — ADO export, Jira paste, CSV, markdown table, verbal list) into a normalized table:

| Ticket ID | Title | Category | Owner | Priority | Notes |
|-----------|-------|----------|-------|----------|-------|

**Category values:** `user-story`, `dev-task`, `bug`, `carryover`, `stretch`

Rules:
- If the input has no IDs, assign sequential IDs: `T-001`, `T-002`, etc.
- If the input has no categories, infer from context (features → user-story, setup → dev-task, etc.) and mark as `[INFERRED]`
- If the input has no owners, leave blank — the guardrail will flag this later
- If the input has no priorities, infer from sprint goal alignment and mark as `[INFERRED]`

---

## Step 2: Detect Carryover

If a prior Sprint Review or Sprint Progress Report was found during SKILL.md Step 1:

1. Read the prior document
2. Find items marked as incomplete, partial, or carried over
3. Present to the user:

```
Carryover candidates from Sprint [N-1]:
- [Ticket ID] [Title] — was [status] at sprint end
- [Ticket ID] [Title] — was [status] at sprint end

Should these be included as carryover in Sprint [N]?
```

If no prior documents available, skip this step.

---

## Step 3: Quality Gate — Tier Check

Assess the input quality tier:

| Tier | Requirements | Status |
|------|-------------|--------|
| **Tier 1** (minimum viable) | Sprint number + dates + goal + at least 1 ticket | ✅ / ❌ |
| **Tier 2** (recommended) | Tier 1 + categorized tickets + team capacity confirmed | ✅ / ❌ |
| **Tier 3** (comprehensive) | Tier 2 + Release Plan linked + prior sprint review linked + full ticket details (descriptions, ACs, estimates) | ✅ / ❌ |

If Tier 1 is not met, STOP: "I need at minimum a sprint number, dates, goal, and at least one ticket to proceed."

If Tier 1 is met but Tier 2 is not, note gaps and proceed: "Proceeding at Tier 1. Missing: [list]. The output will have `[TBD]` markers for missing information."

---

## Step 4: Save Normalized Tickets

Save the normalized ticket table to: `[sprint-root]/stage_output/Normalized-Tickets.md`

---

## Step 5: Update State File

Save or update the state file at `[release-root]/.meta/skill-state-sprint-planning-session.json`:

```json
{
  "skill": "sprint-planning-session",
  "sprint": "[N]",
  "current_task": "T0",
  "task_status_map": {
    "T0": "completed", "T1": "pending",
    "T2": "pending", "T3": "pending", "T4": "pending"
  },
  "artifacts": {
    "normalized_tickets": "[sprint-root]/stage_output/Normalized-Tickets.md",
    "organized_groups": null,
    "planning_doc": null
  },
  "last_updated_utc": "[timestamp]"
}
```

If the release root is not available (standalone mode), skip state file creation.

---

## Completion Gate

- [ ] All raw ticket input normalized into standard table format
- [ ] Carryover detection completed (or skipped if no prior docs)
- [ ] Quality tier assessed
- [ ] Normalized tickets saved to file
- [ ] Constraint registry loaded (if available)
- [ ] State file updated (if release root available)

**CHECKPOINT (Notification):** "Here are [N] tickets normalized into [categories breakdown]. Tier [X] achieved. Proceeding to organize."

If any item is unchecked → do NOT proceed.

**When complete, return to `SKILL.md` and proceed to Step 5.**
