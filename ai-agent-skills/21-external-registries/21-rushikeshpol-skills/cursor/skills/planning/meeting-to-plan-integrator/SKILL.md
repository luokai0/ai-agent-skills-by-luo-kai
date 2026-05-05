---
name: meeting-to-plan-integrator
description: "Takes decisions from a meeting (sprint demo, retro, stakeholder call, team sync) and applies them to the release plan and related artifacts. The 'decisions become actions' bridge. Use when asked to: apply meeting decisions, update the plan from meeting notes, integrate feedback, or cascade changes from a meeting."
---

# Meeting-to-Plan Integrator — Entry Orchestrator

## NON-NEGOTIABLE (read first)
1. Save every artifact to file before presenting in chat. Chat is ephemeral.
2. Never fabricate decisions. Every change must trace to a specific decision from the meeting. Unknown = `[TBD]`.
3. Never skip checkpoints. Every CHECKPOINT requires user confirmation before proceeding.
4. Graded provenance: every edit to a target document carries source attribution: `(Source: [meeting-name], [date])`. Decisions are authoritative claims. Impact analysis is synthesized analysis. Cascade predictions are inference and must be confirmed before applying.
5. One stage at a time. Complete and save before starting the next.
6. Never apply changes the user hasn't confirmed. The change manifest is the contract.

---

## Purpose

Take decisions from a meeting and apply them to the release plan and related artifacts. This is the "decisions become actions" bridge.

**What you'll produce:**
- Updated target documents with source-attributed edits
- **Change-Manifest-[date].md** — record of what changed, why, and where

**When to invoke:**
- After a sprint demo where stakeholders gave feedback
- After a retrospective with action items
- After a stakeholder call with scope or timeline changes
- After any meeting that produced decisions affecting the plan

---

## Workflow Chain

```
[You are here]
SKILL.md (Intake)
     ↓ reads
workflows/01-intake.md           → loads meeting decisions, identifies targets
     ↓ reads
workflows/02-extract-changes.md  → classifies decisions, builds change manifest
     ↓ reads
workflows/03-apply-changes.md    → applies confirmed changes to documents
     ↓ reads
workflows/04-cascade.md          → checks for downstream effects
```

Each workflow file is read in turn. Do NOT skip ahead.

---

## Step 1: Read Shared Context

**MANDATORY READ** the following files before proceeding:

Read the file:

    ../shared/delivery-model.md

Read the file:

    ../shared/execution-rules.md

---

## Step 2: Start Intake

Read the file:

    workflows/01-intake.md

Follow that file's instructions completely. When complete, return here and proceed to Step 3.

---

## Step 3: Extract Changes

Read the file:

    workflows/02-extract-changes.md

Follow that file's instructions completely. When complete, return here and proceed to Step 4.

---

## Step 4: Apply Changes

Read the file:

    workflows/03-apply-changes.md

Follow that file's instructions completely. When complete, return here and proceed to Step 5.

---

## Step 5: Cascade Check

Read the file:

    workflows/04-cascade.md

Follow that file's instructions completely. Skill is done.

---

## Related Skills

| Situation | Skill |
|-----------|-------|
| Generate meeting notes from a transcript (input to this skill) | `transcript-to-meeting-notes` |
| Create or update the release plan | `release-sprint-planner` |
| Plan a sprint kickoff | `sprint-planning-session` |
| Track sprint progress | `sprint-progress-tracker` |
| Generate sprint review | `sprint-review-generator` |
