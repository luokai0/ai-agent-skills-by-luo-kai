# Sprint Progress Tracker — Evaluation Scenarios

Bootstrap evaluation scenarios per Architecture §8.5 Lean Testing.

---

## Scenario 1: Happy Path — Mid-Sprint Check

**Input:** Sprint Planning Session doc + ticket-level statuses for all items. Day 5 of sprint.
**Expected behavior:**
- Mode detected as mid-sprint
- All tickets mapped to normalized status
- Completion rate calculated, goal assessed
- Health narrative written (synthesized, honest)
- Report saved as Sprint-[N]-Progress-Midpoint.md
**Verify:**
- Every ticket from planning doc appears in status table
- Goal status is explicit (On Track / At Risk)
- No close-out-only sections present

---

## Scenario 2: Close-Out with Carryover

**Input:** Sprint Planning Session doc + end-of-sprint statuses. 3 of 10 items not done (1 blocked, 2 in progress).
**Expected behavior:**
- Mode detected as close-out
- Carryover candidates identified with recommended actions
- Carryover accumulation guardrail evaluated (30% threshold)
- Recommendations for next sprint are specific and actionable
- Report saved as Sprint-[N]-Progress.md
**Verify:**
- All 3 incomplete items appear in Carryover Candidates
- Each has a recommended action
- Recommendations section is not generic

---

## Scenario 3: Minimal Input — Verbal Status Only

**Input:** Sprint Planning Session doc + user provides verbal update ("we finished 3 items, 2 are blocked").
**Expected behavior:**
- Quality gate shows Tier 1
- Status mapping inferred from verbal input, marked as `(Source: user verbal)`
- Report produced but with lower confidence
**Verify:**
- Skill does not fabricate per-ticket statuses beyond what user stated
- Unstated tickets show as `[TBD]` or "status unknown"

---

## Scenario 4: Guardrail Stress — Goal At Risk

**Input:** Sprint Planning Session doc with 3 goal-critical items. Status: all 3 are Not Started on Day 6.
**Expected behavior:**
- `Goal at risk` guardrail triggers
- Flag: "Sprint goal at risk. [3 items] are Not Started."
- Health narrative reflects risk honestly
**Verify:**
- Guardrail alert present in report
- Health narrative does not spin ("on track" when it isn't)
- Goal status explicitly says "At Risk"

---

## Scenario 5: Scope Creep Detection

**Input:** Sprint Planning Session doc with 8 committed items. Current status shows 8 original + 4 added items.
**Expected behavior:**
- `Scope creep` guardrail triggers (4/8 = 50% > 20% threshold)
- Scope Changes section lists all 4 added items with reasons
- Warn: "Sprint scope has grown 50%."
**Verify:**
- All 4 added items appear in Scope Changes table
- Each has a reason
- Guardrail warning is visible
