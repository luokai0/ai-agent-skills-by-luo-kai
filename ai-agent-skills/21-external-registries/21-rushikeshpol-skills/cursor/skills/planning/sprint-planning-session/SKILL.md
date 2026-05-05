---
name: sprint-planning-session
description: "Takes a sprint's planned work (from a release plan, ticket board, or verbal list) and produces a structured Sprint Planning Session document. Normalizes any ticket format, groups work into logical areas, validates against the sprint goal, runs guardrails, and generates a document that gives the team clarity on what they're building, why, and what 'done' looks like. Use when asked to: create a sprint planning doc, plan a sprint, organize sprint tickets, write a sprint kickoff document, or prepare for sprint planning."
---

# Sprint Planning Session — Entry Orchestrator

## NON-NEGOTIABLE (read first)
1. Save every artifact to file before presenting in chat. Chat is ephemeral.
2. Never fabricate dates, numbers, statuses, or capacity. Unknown = `[TBD]`. Inferred = `[INFERRED]`.
3. Never skip checkpoints. Every CHECKPOINT requires user confirmation before proceeding.
4. Graded provenance: authoritative claims (dates, capacity numbers, statuses, decisions, constraints) require a source tag. Synthesized analysis uses `(Synthesized from: ...)`. Process scaffolding (section framing, transitions) is exempt. Missing source on an authoritative claim = flag as `(Source: Implicit)` for resolution.
5. One stage at a time. Complete and save before starting the next.
6. Re-read upstream documents at the start of every workflow. Never rely on cached context.
7. Every ticket in the input must appear in the output. None silently dropped.

---

## Purpose

Take the sprint's planned work (from the release plan + ticket list) and produce a document that gives the team clarity on what they're building, why, and what "done" looks like.

**What you'll produce:**
- `[sprint-root]/Sprint-[N]-Planning.md` — the sprint planning session document

**State file:** `[release-root]/.meta/skill-state-sprint-planning-session.json` — tracks current task and artifacts for resume capability. Updated after each workflow step.

**When to invoke:** Before every sprint kickoff. The PM has tickets in their board (ADO, Jira, or a list) and needs to turn them into a structured planning document.

---

## Workflow Chain

```
[You are here]
SKILL.md (Intake)
     ↓ reads
workflows/01-intake.md        → normalizes tickets, detects carryover
     ↓ reads
workflows/02-organize.md      → groups tickets, runs guardrails
     ↓ reads
workflows/03-generate.md      → produces Sprint-N-Planning.md
     ↓ reads (optional)
workflows/04-refine.md        → applies user feedback
```

Each workflow file is read in turn. Do NOT skip ahead.

---

## Step 1: Determine Release Context

Ask the user:
1. **Release root folder** — Where are the release artifacts? (e.g., `Product Artifacts/Delivery Plan/Releases/Redesign_Aug2026/`)
2. **Sprint number** — Which sprint is this?

If the user provides both, scan the release root for:
- `Release-Plan.md` — for sprint goal and planned scope
- `Sprint-[N-1]/Sprint-[N-1]-Review.md` or `Sprint-[N-1]-Progress.md` — for carryover detection
- `.meta/constraint-registry.md` — for active constraints

Report what you found:
```
Found in release root:
- Release-Plan.md: ✅ Found / ❌ Not found
- Prior sprint review: ✅ Found / ❌ Not found
- Constraint registry: ✅ Found / ❌ Not found
```

If no release root is provided, that's fine — the skill works standalone with just a ticket list.

---

## Step 2: Gather Sprint Inputs

Ask the user for:
- **Sprint dates** (start and end) — or infer from Release Plan if linked
- **Sprint goal** — or extract from Release Plan if linked
- **Ticket list** — accept ANY format: paste from ADO/Jira, CSV, markdown table, verbal list, screenshot
- **Team capacity** — who is available, any PTO or reduced capacity

---

## Step 3: Read Shared Context

**MANDATORY READ** the following files before proceeding:

Read the file:

    ../shared/delivery-model.md

Extract the sprint anatomy and commitment model. Understand where this sprint sits in the release lifecycle.

Read the file:

    ../shared/execution-rules.md

Load the shared NON-NEGOTIABLE rules, quality criteria, self-check structure, and provenance model.

If a constraint registry was found in Step 1, read it and note active constraints that affect this sprint.

---

## Step 4: Start Intake Workflow

Read the file:

    workflows/01-intake.md

Follow that file's instructions completely from start to finish. When complete, return here and proceed to Step 5.

---

## Step 5: Organize and Validate

Read the file:

    workflows/02-organize.md

Follow that file's instructions completely. When complete, return here and proceed to Step 6.

---

## Step 6: Generate Planning Document

Read the file:

    workflows/03-generate.md

Follow that file's instructions completely. When complete, return here and proceed to Step 7.

---

## Step 7: Refine (if needed)

If the user requests changes after reviewing the generated document:

Read the file:

    workflows/04-refine.md

Otherwise, the skill is complete.

---

## Related Skills

| Situation | Skill |
|-----------|-------|
| Need to create or update the release plan first | `release-sprint-planner` |
| Mid-sprint progress check | `sprint-progress-tracker` |
| End-of-sprint review document | `sprint-review-generator` |
| Apply meeting feedback to the plan | `meeting-to-plan-integrator` |
