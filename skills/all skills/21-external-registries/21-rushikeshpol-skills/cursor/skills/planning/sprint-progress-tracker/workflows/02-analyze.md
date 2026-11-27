# Workflow 02: Analyze

**Called from:** `SKILL.md` Step 4
**Next step:** `workflows/03-generate.md`

---

## Purpose

Assess sprint health and identify risks. This analysis feeds the progress report.

**ANTI-MOMENTUM GATE:** Am I assessing health or just restating the status table? If the analysis adds no insight beyond what the status table already shows, stop and think harder.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 01 complete | |
| Status mapping saved | |
| Mode determined (mid-sprint / close-out) | |

---

## Step 1: Calculate Metrics

| Metric | Formula |
|--------|---------|
| **Completion rate** | Done / total committed (exclude stretch, added) |
| **Sprint goal assessment** | Are the goal-critical items on track? |
| **At-risk items** | In-progress but unlikely to finish (based on remaining time) |
| **Scope changes** | Items added or dropped since planning |

---

## Step 2: Close-Out Mode Additional Analysis

For close-out mode only:
- **Carryover list:** items not done that should carry to next sprint
- **Velocity data:** story points or ticket count completed (if available)
- **Recommendations for next sprint:** specific, actionable insights based on what happened

---

## Step 3: Run Guardrails

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| **Goal at risk** | Goal-critical items are Blocked or Not Started past mid-sprint | Flag: "Sprint goal at risk. [item] is [status]. Recommend: [action]." |
| **Scope creep** | More than 20% of committed items are "Added" | Warn: "[N] items added since planning. Sprint scope has grown [X]%." |
| **Persistent blocker** | Same blocker appears in both mid-sprint and close-out | Escalate: "Blocker '[X]' persisted entire sprint. Needs PM escalation." |
| **Silent ticket** | Ticket has no status update (Not Started after Day 5) | Flag: "[ticket] has no status update. Check with owner." |
| **Carryover accumulation** | Close-out shows >30% carryover from committed items | Warn: "High carryover rate ([X]%). Consider capacity/scope adjustment." |

---

## Step 4: Build Health Narrative

Write 1-2 sentences that summarize the sprint's health honestly. This is synthesized analysis, not an authoritative claim.

Examples:
- "Sprint is on track. Clock-in geo is complete. Non-geo is 70% done with 4 days remaining — tight but achievable."
- "Sprint is at risk. 2 of 5 committed items are blocked, including a goal-critical feature."

---

## Completion Gate

- [ ] Metrics calculated
- [ ] Close-out analysis done (if close-out mode)
- [ ] Guardrails evaluated
- [ ] Health narrative drafted
- [ ] State file updated (T1 completed)

**CHECKPOINT (Hard stop — T2 Gate):** "Here's the status mapping + health assessment. Confirm or correct before I generate the report."

**STOP and WAIT for user confirmation.**

**When complete, return to `SKILL.md` and proceed to Step 5.**
