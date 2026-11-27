# Meeting-to-Plan Integrator — Evaluation Scenarios

Bootstrap evaluation scenarios per Architecture §8.5 Lean Testing.

---

## Scenario 1: Happy Path — Sprint Demo Feedback

**Input:** Meeting notes from sprint demo with 3 decisions: 1 scope change (feature deprioritized), 1 timeline adjustment (UAT moved earlier), 1 new risk identified. Target: Release-Plan.md + Release-Definition.md.
**Expected behavior:**
- All 3 decisions classified correctly by type
- Change manifest built with specific edits per document
- User confirms all 3
- Both documents updated with source attribution
- Cascade to Scope.md identified (scope change)
**Verify:**
- Each edit has `(Source: Sprint Demo, [date])`
- Scope.md cascade flagged as High confidence
- Change manifest saved to `.meta/`

---

## Scenario 2: Contradictory Decisions

**Input:** Meeting notes with 2 decisions: "Add feature X to Sprint 3" and "Move Sprint 3 deadline forward by 1 week."
**Expected behavior:**
- `Contradictory changes` guardrail triggers
- Block: "Adding scope and compressing timeline conflict. Clarify priority."
- Skill waits for user resolution before building manifest
**Verify:**
- Neither change applied until contradiction resolved
- Guardrail alert is clear and specific

---

## Scenario 3: Verbal Input — Minimal Tier

**Input:** User verbally says "In the retro, we decided to reduce WIP to 2 per dev and drop the chat feature from this release." Target: Release-Plan.md.
**Expected behavior:**
- Quality gate shows Tier 1
- 2 decisions extracted from verbal input
- Change manifest built with attribution: `(Source: user verbal, retro)`
- Edits applied after confirmation
**Verify:**
- Skill does not fabricate additional decisions
- Attribution is honest about source quality

---

## Scenario 4: Transcript-to-Meeting-Notes Input

**Input:** Output from `transcript-to-meeting-notes` skill with 5 structured decisions and source attribution.
**Expected behavior:**
- Processing verification gate runs (correct routing, accurate extraction)
- Quality gate shows Tier 3
- Source chain preserved: transcript → meeting notes → change manifest → edit
**Verify:**
- Each decision in manifest traces back to meeting notes section
- Source attribution chain is complete

---

## Scenario 5: Cascade with Mixed Confidence

**Input:** 1 scope removal decision applied to Release-Plan.md. Cascade analysis finds: (a) Scope.md needs update (High), (b) Sprint Planning doc might be affected (Medium), (c) Sprint Progress Report might reference the feature (Low).
**Expected behavior:**
- All 3 cascade effects presented with confidence levels
- High-confidence cascade recommended for application
- Medium presented without recommendation
- Low flagged for review only
- Only user-confirmed cascades applied
**Verify:**
- No cascade applied without confirmation
- Anti-momentum gate prevents inventing new changes
