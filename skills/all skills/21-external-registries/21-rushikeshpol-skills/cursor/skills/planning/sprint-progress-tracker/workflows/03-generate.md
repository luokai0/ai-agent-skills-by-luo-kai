# Workflow 03: Generate

**Called from:** `SKILL.md` Step 5
**Saves to:** `[sprint-root]/Sprint-[N]-Progress.md` or `Sprint-[N]-Progress-Midpoint.md`

---

## Purpose

Produce the Sprint Progress Report. Mode determines which sections appear.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 02 complete (T2 gate passed) | |
| Health assessment confirmed by user | |

---

## Step 1: Generate Report

Load the template:

    templates/sprint-progress.md

Fill the template with analysis results. Mode determines included sections:

**Both modes include:**
- Sprint Health (metrics + narrative)
- Ticket Status table
- At-Risk Items / Incomplete Items
- Scope Changes Since Planning
- Guardrail Alerts (if any)

**Close-out mode additionally includes:**
- Carryover Candidates
- Recommendations for Next Sprint

---

## Step 2: Self-Check

**P1 — Hard gate (regenerate if fails):**
- [ ] Goal status explicitly stated (On Track / At Risk / Not Met)
- [ ] Every planned ticket appears in status table
- [ ] Source attribution on status data (who provided the status)

**P2 — Edit gate (fix before saving):**
- [ ] Scope changes listed with reasons
- [ ] Every blocker has owner or escalation
- [ ] Guardrail results addressed

**P3 — Note and proceed:**
- [ ] Date formatting consistent (Mon DD)
- [ ] Health narrative is honest (no spin)

---

## Step 3: Save Report

Save to:
- Mid-sprint: `[sprint-root]/Sprint-[N]-Progress-Midpoint.md`
- Close-out: `[sprint-root]/Sprint-[N]-Progress.md`

Update state file: mark all tasks completed.

---

## Completion Gate

- [ ] Report generated with all applicable sections
- [ ] Self-check passed
- [ ] Report saved to file
- [ ] State file updated

**CHECKPOINT (Review gate):** "Progress report saved to [path]. Review and confirm, or request changes."

**Skill is complete.**
