---
name: sprint-review-generator
description: "Creates a sprint review document for the sprint demo. Stakeholder-facing artifact answering: What did we build? Did we hit our goal? What did we learn? What's next? Serves two audiences: stakeholders (top sections, jargon-free) and team/PM (full detail). Use when asked to: create a sprint review, prepare the sprint demo doc, write the sprint review, or summarize what we shipped."
---

# Sprint Review Generator — Entry Orchestrator

## NON-NEGOTIABLE (read first)
1. Save every artifact to file before presenting in chat. Chat is ephemeral.
2. Never fabricate delivery data, goal assessments, or metrics. Unknown = `[TBD]`. Inferred = `[INFERRED]`.
3. Never skip checkpoints. Every CHECKPOINT requires user confirmation before proceeding.
4. Graded provenance: goal status and metric claims are authoritative and require source attribution. Review narrative sections (summary, challenges, lessons) are synthesized analysis — inline source tags would make the doc unreadable. Use a Sources section at the bottom instead. Process scaffolding is exempt.
5. One stage at a time. Complete and save before starting the next.
6. Re-read upstream documents at the start of every workflow. Never rely on cached context.
7. Honest tone: if the goal wasn't met, say so clearly and say why. No spin.

---

## Purpose

Create a sprint review document for the sprint demo. This is the stakeholder-facing artifact.

**What you'll produce:**
- **Sprint-[N]-Review.md** — dual-audience document (stakeholder summary + team detail)

**State file:** `[sprint-root]/.meta/skill-state-sprint-review-generator.json`

**When to invoke:** End of sprint, before the sprint demo meeting.

**Audience design:**
1. **Stakeholders / executives** — read the top 3 sections only (Summary, Goal Assessment, What We Delivered). Must be jargon-free, demo-focused, 5-minute read.
2. **Team / PM** — read the full document including challenges, lessons, metrics, and next sprint preview.

---

## Workflow Chain

```
[You are here]
SKILL.md (Intake)
     ↓ reads
workflows/01-intake.md   → gathers sprint data
     ↓ reads
workflows/02-analyze.md  → builds the narrative
     ↓ reads
workflows/03-generate.md → produces Sprint Review doc
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

## Step 3: Analyze

Read the file:

    workflows/02-analyze.md

Follow that file's instructions completely. When complete, return here and proceed to Step 4.

---

## Step 4: Generate Review

Read the file:

    workflows/03-generate.md

Follow that file's instructions completely. Skill is done.

---

## Related Skills

| Situation | Skill |
|-----------|-------|
| Generate the sprint planning doc (input) | `sprint-planning-session` |
| Generate the progress report (input) | `sprint-progress-tracker` |
| Apply review feedback to the plan | `meeting-to-plan-integrator` |
