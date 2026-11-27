---
name: release-sprint-planner
description: "Defines a release — its goal, scope, timeline, team, and constraints — then produces a formal Release Definition and multi-sprint plan. Assesses context across six dimensions, collaboratively builds each section, sizes features, maps dependencies, assigns work to sprints, and iterates until the plan is balanced and agreed. Use when asked to: create a release plan, plan the release, define the release, break this down into sprints, update the plan, rebalance sprints, or adjust scope/timeline."
---

# Release Sprint Planner — Entry Orchestrator

## NON-NEGOTIABLE (read first)
1. Save every artifact to file before presenting in chat. Chat is ephemeral.
2. Never fabricate dates, numbers, statuses, or capacity. Unknown = `[TBD]`. Inferred = `[INFERRED]`.
3. Never skip checkpoints. Every CHECKPOINT requires user confirmation before proceeding.
4. Graded provenance: authoritative claims (dates, capacity numbers, statuses, decisions, constraints) require a source tag. Synthesized analysis uses `(Synthesized from: ...)`. Process scaffolding (section framing, transitions) is exempt. Missing source on an authoritative claim = flag as `(Source: Implicit)` for resolution.
5. One stage at a time. Complete and save before starting the next.
6. Re-read upstream documents at the start of every workflow. Never rely on cached context.
7. Release Definition is the anchor. All downstream documents trace to it. Never contradict it without updating it first.

---

## Purpose

Work with the user to define a release — its goal, scope, timeline, team, and constraints — then produce a formal Release Definition document. From there, break the scope into a multi-sprint plan. Iterate until the plan is clear, balanced, and agreed.

**What you'll produce:**
1. **Release-Definition.md** — the anchor document: what we're building, why, for whom, by when, with what team, and what's at risk.
2. **Release-Plan.md** — the execution document: sprint-by-sprint breakdown showing how the team will deliver the release definition.
3. **Scope.md** — phase-by-phase scope document.

**State file:** `[release-root]/.meta/skill-state-release-sprint-planner.json` — tracks current task, gates passed, and artifacts for resume capability.

**When to invoke:**
- Start of a new release
- Major scope change requiring re-planning (>30% of remaining work affected)
- Team change (dev added/removed) requiring rebalancing
- Timeline change (deadline moved)

---

## Modes

| Mode | Signal | Route |
|------|--------|-------|
| **CREATE** | "create a release plan", "plan the release", "define the release", "break this down into sprints" | Full pipeline: 01 through 07 |
| **UPDATE** | "update the plan", "scope changed", "timeline moved" + existing plan file referenced | Skip to 06-iterate with existing plan and release definition loaded |

---

## Workflow Chain

```
[You are here]
SKILL.md (Intake + Mode Detection)
     ↓ reads
workflows/01-intake.md            → normalizes inputs, creates inventory
     ↓ reads
workflows/02-context-assessment.md → assesses 6 dimensions, fills gaps
     ↓ reads
workflows/03-release-definition.md → builds Release-Definition.md collaboratively
     ↓ reads
workflows/04-analyze-scope.md      → sizes features, maps dependencies
     ↓ reads
workflows/05-draft-plan.md         → assigns work to sprints, produces Release-Plan.md
     ↓ reads
workflows/06-iterate.md            → incorporates feedback (may loop)
     ↓ reads
workflows/07-finalize.md           → locks plan, produces Scope.md, consistency check
```

Each workflow file is read in turn. Do NOT skip ahead.

---

## Step 1: Mode Detection

Determine the mode:
- If the user references an existing Release-Plan.md or Release-Definition.md and wants to modify it → **UPDATE mode**. Skip to Step 6.
- Otherwise → **CREATE mode**. Continue to Step 2.

---

## Step 2: Determine Release Context

Ask the user:
1. **Release root folder** — Where should the release artifacts live? (e.g., `Product Artifacts/Delivery Plan/Releases/[Release-Name]/`)
2. **Release name** — What is this release called?

If the folder doesn't exist, create it along with the `.meta/` subfolder.

Scan for existing context:
- `project-context.md` in the workspace root
- Any documents the user mentions (PRDs, scope docs, meeting notes, etc.)

---

## Step 3: Read Shared Context

**MANDATORY READ** the following files before proceeding:

Read the file:

    ../shared/delivery-model.md

Read the file:

    ../shared/execution-rules.md

Read the file:

    ../shared/constraint-registry-template.md

---

## Step 4: Start Intake (CREATE mode)

Read the file:

    workflows/01-intake.md

Follow that file's instructions completely. When complete, return here and proceed to Step 5.

---

## Step 5: Context Assessment

Read the file:

    workflows/02-context-assessment.md

Follow that file's instructions completely. When complete, return here and proceed to Step 6.

---

## Step 6: Build Release Definition

For **CREATE mode:**

Read the file:

    workflows/03-release-definition.md

For **UPDATE mode:** Skip to Step 9.

When complete, return here and proceed to Step 7.

---

## Step 7: Analyze Scope

Read the file:

    workflows/04-analyze-scope.md

When complete, return here and proceed to Step 8.

---

## Step 8: Draft Sprint Plan

Read the file:

    workflows/05-draft-plan.md

When complete, return here and proceed to Step 9.

---

## Step 9: Iterate

Read the file:

    workflows/06-iterate.md

This workflow may loop multiple times. When the user approves, proceed to Step 10.

---

## Step 10: Finalize

Read the file:

    workflows/07-finalize.md

When complete, the skill is done.

---

## Related Skills

| Situation | Skill |
|-----------|-------|
| Plan individual sprint kickoff | `sprint-planning-session` |
| Mid-sprint progress check | `sprint-progress-tracker` |
| End-of-sprint review document | `sprint-review-generator` |
| Apply meeting feedback to the plan | `meeting-to-plan-integrator` |
