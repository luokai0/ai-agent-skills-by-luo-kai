---
name: sprint-progress-tracker
description: "Creates a snapshot of where the sprint stands — planned vs actual. Surfaces risks early. Feeds data into the sprint review and next sprint planning. Use when asked to: check sprint progress, mid-sprint check, close out the sprint, what's the sprint status, or generate a progress report."
---

# Sprint Progress Tracker — Entry Orchestrator

## NON-NEGOTIABLE (read first)
1. Save every artifact to file before presenting in chat. Chat is ephemeral.
2. Never fabricate statuses, completion data, or metrics. Unknown = `[TBD]`. Inferred = `[INFERRED]`.
3. Never skip checkpoints. Every CHECKPOINT requires user confirmation before proceeding.
4. Graded provenance: ticket statuses, metrics, and goal assessments are authoritative claims and require source attribution. Health narrative is synthesized analysis. Process scaffolding is exempt. Missing source on an authoritative claim = flag as `(Source: Implicit)`.
5. One stage at a time. Complete and save before starting the next.
6. Re-read upstream documents at the start of every workflow. Never rely on cached context.

---

## Purpose

Create a snapshot of where the sprint stands — planned vs actual. Surface risks early. Feed data into the sprint review and next sprint planning.

**What you'll produce:**
- **Sprint-[N]-Progress.md** (close-out mode) or **Sprint-[N]-Progress-Midpoint.md** (mid-sprint mode)

**State file:** `[sprint-root]/.meta/skill-state-sprint-progress-tracker.json`

**When to invoke:**
- **Mid-sprint check** (Day 5-6): Are we on track? What's at risk?
- **End-of-sprint close-out** (Day 10): What was delivered? What carries over?

---

## Modes

| Mode | Trigger | Output depth |
|------|---------|-------------|
| **Mid-sprint** | User invokes between Day 3 and Day 7 | Focus on goal risk, blockers, and at-risk items. Lighter output (~50 lines). |
| **Close-out** | User invokes after Day 8 or says "sprint is done" | Full comparison: planned vs delivered. Carryover list. Feeds sprint review. (~100-150 lines). |

---

## Workflow Chain

```
[You are here]
SKILL.md (Intake + Mode Detection)
     ↓ reads
workflows/01-intake.md   → loads planned work, normalizes current status
     ↓ reads
workflows/02-analyze.md  → assesses sprint health, runs guardrails
     ↓ reads
workflows/03-generate.md → produces Sprint Progress Report
```

Each workflow file is read in turn. Do NOT skip ahead.

---

## Step 1: Determine Mode

Infer from sprint dates or ask:
- If we're between Day 3 and Day 7 → **Mid-sprint mode**
- If we're after Day 8 or user says "sprint is done" → **Close-out mode**

---

## Step 2: Read Shared Context

**MANDATORY READ** the following files before proceeding:

Read the file:

    ../shared/delivery-model.md

Read the file:

    ../shared/execution-rules.md

---

## Step 3: Start Intake

Read the file:

    workflows/01-intake.md

Follow that file's instructions completely. When complete, return here and proceed to Step 4.

---

## Step 4: Analyze

Read the file:

    workflows/02-analyze.md

Follow that file's instructions completely. When complete, return here and proceed to Step 5.

---

## Step 5: Generate Report

Read the file:

    workflows/03-generate.md

Follow that file's instructions completely. Skill is done.

---

## Related Skills

| Situation | Skill |
|-----------|-------|
| Generate the sprint planning doc (input to this skill) | `sprint-planning-session` |
| Generate the sprint review (uses this skill's close-out output) | `sprint-review-generator` |
| Apply meeting decisions to the plan | `meeting-to-plan-integrator` |
