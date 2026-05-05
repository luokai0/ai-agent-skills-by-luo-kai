# Workflow 02: Analyze

**Called from:** `SKILL.md` Step 3
**Next step:** `workflows/03-generate.md`

---

## Purpose

Build the narrative for the review. This must be an honest assessment, not a status restatement.

**ANTI-MOMENTUM GATE:** Am I building an honest narrative or restating status data? The review should tell a story — what happened, what we learned, what changes.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 01 complete | |
| All required inputs loaded | |

---

## Step 1: Assess Goal

- Goal met? Partially met? Not met?
- Be explicit and honest. Use data from the progress report.

---

## Step 2: Group Delivered Work

- Group by feature area (what's demo-able)
- Use user-facing language, not ticket IDs
- Note which items are demo-ready vs completed-but-not-demoed

---

## Step 3: Group Incomplete Work

- Group with honest reasons (not defensive)
- Each incomplete item must have a "why" and a "next step"

---

## Step 4: Extract Insights

- **Challenges:** what blocked us, what was harder than expected
- **Decisions:** what did we decide during the sprint that wasn't planned at the start
- **Lessons (inferred):** based on carryover, blockers, scope changes — what should we do differently
  - Lessons inference uses data patterns; mark as `[INFERRED]` if not explicitly stated by user

---

## Step 5: Draft Next Sprint Preview

From the Release Plan:
- Next sprint goal
- Key features planned
- Known risks surfaced this sprint that affect next

---

## Step 6: Run Guardrails

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| **Goal assessment missing** | No explicit met/not-met statement | Block: must state goal outcome |
| **Incomplete without reason** | Item listed as not delivered with no explanation | Flag: add "why" for every incomplete item |
| **Spin narrative** | Tone implies success when data shows otherwise | Flag: rewrite to match data honestly |
| **Missing next-sprint preview** | No forward-looking section | Warn: stakeholders want to know what's next |

---

## Completion Gate

- [ ] Goal assessment drafted (explicit met/partial/not met)
- [ ] Delivered work grouped by feature area
- [ ] Incomplete work listed with reasons
- [ ] Insights extracted (challenges, decisions, lessons)
- [ ] Next sprint preview drafted
- [ ] Guardrails evaluated
- [ ] State file updated (T1 completed)

**CHECKPOINT (Hard stop — T2 Gate):** "Narrative outline + goal assessment: [met/partially met/not met] because [reason]. Confirm before I generate the document."

**STOP and WAIT for user confirmation.**

**When complete, return to `SKILL.md` and proceed to Step 4.**
