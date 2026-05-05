# Stage 2: Interpretation Checkpoint (MANDATORY STOP)

**Before doing any analysis or editing, summarize what you understood from ALL inputs.**

Present to the user, separating STATED facts from INFERRED conclusions:

```
Here's what I extracted from all inputs:

**Problem / Feature:**
[1-2 sentence summary of what this feature is about]

**Current State:**
[What exists today — from Step 1.5. If unknown, state: "CURRENT STATE UNKNOWN — not yet provided"]

**STATED facts (directly from sources):**
- [Fact 1] (Source: SRC-N, section/decision)
- [Fact 2] (Source: SRC-N, section/decision)

**INFERRED conclusions (derived or gap-filled — need your confirmation):**
- [Inference 1] — reasoning: [why this was inferred] (Based on: SRC-N)
- [Inference 2] — reasoning: [why this was inferred] (Based on: SRC-N)

**Actors identified:**
- [Actor 1: role and relevance] (Source: SRC-N)
- [Actor 2: role and relevance] (Source: SRC-N)

**Constraints / rules identified:**
- [Constraint 1] (Source: SRC-N, section/decision)
- [Constraint 2] (Source: SRC-N, section/decision)

**Open / unclear items:**
- [Item 1 — what's unclear and why it matters]

**Decisions already made (from transcripts/meetings):**
- [Decision 1] (Source: SRC-N, Decision N)

Does this match your understanding? Anything missing or incorrect?
Please review the INFERRED items — confirm, correct, or reject each one.
```

Every fact, constraint, and decision must carry its source ID.

**Inference Register rules:**
- Any item not directly quoted or clearly present in a source is INFERRED and must be listed in the INFERRED section, not the STATED section.
- The user must confirm, correct, or reject each INFERRED item before proceeding.
- Confirmed inferences become STATED facts (with `Source: User-confirmed`).
- Rejected inferences are removed.
- Unresolved inferences become `[TBD]` — they must NOT be written as confident fact in later stages.

## Save Stage 2 artifact

**Save to:** `[output]/stage_output/Stage2-Interpretation.md`

Include: all sections above (Problem/Feature, Current State, STATED facts, INFERRED items, Actors, Constraints, Open items, Decisions). End with an `## ACTION REQUIRED` section listing what the user needs to confirm/reject.

**In chat, present only:** A brief summary (file path, count of STATED facts, count of INFERRED items needing review, count of open items) and ask the user to review the file.

**STOP and WAIT for user confirmation.** Do not proceed to Stage 3 until the user confirms or corrects.
