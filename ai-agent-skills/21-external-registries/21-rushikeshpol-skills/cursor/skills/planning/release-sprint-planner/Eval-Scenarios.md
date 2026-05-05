# Release Sprint Planner — Evaluation Scenarios

Bootstrap evaluation scenarios per Architecture §8.5 Lean Testing.

---

## Scenario 1: Happy Path — Full Inputs

**Input:** Release name + PRD + scope doc + team roster + timeline + meeting notes with constraints. Tier 3 quality.
**Expected behavior:**
- Context assessment rates most dimensions Strong or Moderate
- Release Definition sections pre-filled from inputs, minimal user prompting
- Sprint plan assigns Must-have items respecting dependencies and capacity
- All guardrails pass or trigger appropriate warnings
- 3 artifacts produced: Release-Definition.md, Release-Plan.md, Scope.md
**Verify:**
- Every feature appears in exactly one sprint
- Timeline math is correct
- Success criteria are measurable
- Capacity model aligns with team roster

---

## Scenario 2: Minimal Input — Tier 1

**Input:** Release name + verbal description only. No feature list, no timeline, no team.
**Expected behavior:**
- Quality gate shows Tier 1
- Context assessment rates most dimensions Weak or Missing
- Skill asks targeted questions for release-level gaps
- Release Definition has `[TBD]` markers for unknown sections
- Sprint plan deferred until scope and team are known
**Verify:**
- Skill does not fabricate features, dates, or team members
- `[TBD]` markers present where data is missing
- Questions are release-level, not sprint-level

---

## Scenario 3: Scope Exceeds Capacity

**Input:** 20 Must-have features, team of 2, timeline of 3 feature sprints.
**Expected behavior:**
- `scope-time-resources mismatch` guardrail triggers during Release Definition
- Skill flags: "Must-have scope exceeds available capacity"
- Forces scope/timeline/resource conversation before proceeding
- Does not silently overload sprints
**Verify:**
- Guardrail triggers BEFORE sprint assignment
- User is presented with options: reduce scope, extend timeline, add team
- If user doesn't resolve, plan has visible shortfall markers

---

## Scenario 4: Complex Dependencies

**Input:** 10 features with chain dependencies (A → B → C → D), external API dependency with unknown delivery date.
**Expected behavior:**
- Dependency mapping identifies critical path
- Sprint assignment respects dependency order
- External dependency flagged as risk with `[TBD]` timeline
- Features blocked by external dependency scheduled with buffer
**Verify:**
- No feature scheduled before its dependency
- Critical path identified and highlighted
- External dependency has fallback plan

---

## Scenario 5: UPDATE Mode — Scope Change

**Input:** Existing Release-Plan.md + Release-Definition.md. User says "2 features descoped, timeline moved up 2 weeks."
**Expected behavior:**
- Enters UPDATE mode, loads existing documents
- Loads constraint registry
- Identifies affected sprints
- Applies changes to both Release-Plan.md and Release-Definition.md
- Re-runs guardrails on affected sprints
- Highlights what moved and why
**Verify:**
- Descoped features removed from plan and moved to scope-out
- Timeline adjustment recalculates sprint dates
- Affected sprints rebalanced
- Both documents updated consistently
