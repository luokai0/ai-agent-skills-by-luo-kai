# Stage 4: Scenario Matrix — Combinations, Edge Cases, Boundary Conditions

**Called from:** `SKILL.md` (Pipeline Orchestrator)
**Next step:** Return to `SKILL.md` for Stage 5: Assumptions Identification
**Saves to:** `[output]/stage_output/Stage4-Scenarios-Matrix.md`

---

## 4.1 Build scenario matrix

Cross-reference variables to identify all meaningful combinations:

| Scenario ID | [Variable 1] | [Variable 2] | [Variable N] | Expected Behavior | Priority | Notes |
|---|---|---|---|---|---|---|
| S1 | [value] | [value] | [value] | [What happens] | 🔴 Critical | |

**Rules:**
- Include happy path scenarios first
- Include boundary conditions (minimum, maximum, just-above, just-below thresholds)
- Include error scenarios (invalid inputs, timeouts, missing data)
- Include edge cases (concurrent actions, interrupted flows, partial data)
- Sort scenarios: happy paths first, then by priority (🔴 Critical → 🟡 Important → 🟢 Edge case)

## 4.2 Identify edge cases

Use the gap analysis from Stage 3 (5 lenses) as the primary input for edge cases. The boundary conditions, sequence disruptions, failure modes, and constraint collisions identified there should each produce at least one scenario row.

Additionally, for any variable NOT already covered by Stage 3's lenses:
- What happens at the boundary? (e.g., exactly at a threshold)
- What if this value is missing or null?
- What if two actors do conflicting things simultaneously?
- What if the process is interrupted midway?

## 4.3 Present matrix for review

Show the full scenario matrix and edge case list. Ask:
- Any scenarios missing?
- Any edge cases you've seen in practice?
- Which scenarios are highest priority?

**Save to:** `[output]/stage_output/Stage4-Scenarios-Matrix.md`

---

Stage 4 complete. Return to `SKILL.md` and proceed to Stage 5: Assumptions Identification.
