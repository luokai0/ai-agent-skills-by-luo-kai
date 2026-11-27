# Sprint Review Generator — Evaluation Scenarios

Bootstrap evaluation scenarios per Architecture §8.5 Lean Testing.

---

## Scenario 1: Happy Path — Goal Met

**Input:** Sprint Planning doc + close-out progress report showing 9/10 items done. Goal met. User provides challenges and demo list.
**Expected behavior:**
- Goal assessment: Met
- Stakeholder sections are jargon-free, demo-focused
- Team sections include challenges and lessons
- Sources section at bottom
**Verify:**
- No ticket IDs in stakeholder sections
- Every planning doc item accounted for
- Tone is positive but factual (not hyperbolic)

---

## Scenario 2: Goal Partially Met — Honest Tone

**Input:** Sprint Planning doc + close-out report showing 5/10 items done. 2 goal-critical items incomplete.
**Expected behavior:**
- Goal assessment: Partially Met with clear explanation
- "What Didn't Land" section lists 5 items with reasons
- Tone reflects reality (does not spin partial delivery as success)
- Carryover items recommended for next sprint
**Verify:**
- `Spin narrative` guardrail does not trigger (because tone is already honest)
- If summary says "successful sprint" despite 50% completion, P2 self-check fails

---

## Scenario 3: Minimal Input — Tier 1

**Input:** Sprint Planning doc + verbal status ("we finished the login and profile, everything else is still going").
**Expected behavior:**
- Quality gate shows Tier 1
- Review produced with available data
- Lessons section is thin (noted as limited)
- Metrics section marked `[TBD]` or omitted
**Verify:**
- Skill does not fabricate challenges or lessons
- Items without explicit status are noted as "status not confirmed"

---

## Scenario 4: Lessons Inference

**Input:** Sprint Planning doc + close-out report. 3 items carried over, all from same workstream. Same blocker persisted all sprint.
**Expected behavior:**
- Skill infers lesson: "Workstream [X] had persistent blocker impacting 3 items. Consider: dedicate time to resolve blockers before sprint start."
- Inference marked as `[INFERRED]`
- User can confirm, modify, or reject
**Verify:**
- Lesson is specific and actionable (not "communicate better")
- Marked as `[INFERRED]` since user didn't state it
- Evidence column cites the data pattern

---

## Scenario 5: Stakeholder-Ready Check

**Input:** Full Tier 3 inputs with metrics and decisions.
**Expected behavior:**
- Top 3 sections (Summary, Goal Assessment, What We Delivered) pass the "5-minute stakeholder read" test
- No technical jargon, no ticket IDs, no internal process references
- Team sections have full detail
**Verify:**
- P3 self-check: stakeholder sections free of jargon
- Appendix contains full ticket detail
- Sources section lists all input documents
