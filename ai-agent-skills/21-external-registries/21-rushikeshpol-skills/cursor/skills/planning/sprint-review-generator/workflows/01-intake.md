# Workflow 01: Intake

**Called from:** `SKILL.md` Step 2
**Next step:** `workflows/02-analyze.md`

---

## Purpose

Gather all sprint data for the review.

---

## Step 1: Gather Inputs

- **Sprint Planning Session doc** (required — the baseline)
- **Sprint Progress Report — close-out mode** (required, or raw status data)
- **Constraint registry:** load `.meta/constraint-registry.md` if available
- **Sprint goal** (infer from planning doc)
- **Demo items:** what can we show? (user describes or provides screenshots)
- **Challenges encountered during the sprint** (verbal OK)
- **Key decisions made during the sprint** (verbal OK)
- **Lessons learned** (verbal OK — skill will also infer from data)
- **Metrics:** velocity, burndown, defect count (optional)

---

## Step 2: Quality Gate — Tier Check

| Tier | Requirements | Status |
|------|-------------|--------|
| **Tier 1** (minimum viable) | Planning doc + progress report (or raw status) + sprint goal | ✅ / ❌ |
| **Tier 2** (recommended) | Tier 1 + challenges described + demo items listed | ✅ / ❌ |
| **Tier 3** (comprehensive) | Tier 2 + metrics + lessons learned + key decisions documented | ✅ / ❌ |

If Tier 1 is not met, STOP: "I need at minimum the Sprint Planning Session doc, a progress report (or status data), and the sprint goal."

---

## Step 3: Update State File

Save the state file at `[sprint-root]/.meta/skill-state-sprint-review-generator.json`:

```json
{
  "skill": "sprint-review-generator",
  "sprint": "[sprint-number]",
  "current_task": "T0",
  "task_status_map": {
    "T0": "completed", "T1": "pending", "T2": "pending"
  },
  "artifacts": {
    "review": null
  },
  "last_updated_utc": "[timestamp]"
}
```

---

## Completion Gate

- [ ] All required inputs loaded
- [ ] Quality tier assessed
- [ ] State file created

**CHECKPOINT (Notification):** "I have data for Sprint [N] review. Tier [X] achieved. Missing: [list]. Proceed?"

**When complete, return to `SKILL.md` and proceed to Step 3.**
