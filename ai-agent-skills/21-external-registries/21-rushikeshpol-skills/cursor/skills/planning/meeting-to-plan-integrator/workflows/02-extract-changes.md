# Workflow 02: Extract Changes

**Called from:** `SKILL.md` Step 3
**Next step:** `workflows/03-apply-changes.md`
**Saves to:** `[release-root]/.meta/Change-Manifest-[date].md`

---

## Purpose

Identify, classify, and structure every decision that affects the plan.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 01 complete | |
| Meeting notes loaded | |
| Target documents identified | |

---

## Step 1: Classify Each Decision

For each decision from the meeting notes:

| Field | Value |
|-------|-------|
| **Decision** | What was decided |
| **Type** | scope-change / timeline-change / priority-change / team-change / risk-update / new-dependency / technical-decision |
| **Source** | Who made this decision, in which meeting |
| **Affects** | Which documents need updating |
| **Specific change** | What text changes in which section |

---

## Step 2: Build Change Manifest

| # | Decision | Type | Source | Affects | Specific Change |
|---|----------|------|--------|---------|----------------|

---

## Step 3: Run Guardrails

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| **Scope change without impact** | Scope changed but no sprint adjustment proposed | Flag: "This scope change may affect sprint [N]. Assess impact." |
| **Timeline compression** | Deadline moved closer with same scope | Flag: "Timeline compressed. Must resolve scope-time-resource tradeoff." |
| **Contradictory changes** | Two decisions conflict (e.g., add scope + reduce timeline) | Block: "Decisions [X] and [Y] conflict. Clarify priority." |

---

## Step 4: Save Change Manifest

Save to: `[release-root]/.meta/Change-Manifest-[date].md`

---

## Completion Gate

- [ ] Every decision classified by type
- [ ] Impact assessed per decision
- [ ] Specific edits drafted
- [ ] Guardrails evaluated
- [ ] Change manifest saved

**CHECKPOINT (Hard stop — T2 Gate):** "Change manifest with [N] changes classified by type. Confirm which to apply."

**STOP and WAIT for user confirmation.** User may confirm all, some, or none.

**When complete, return to `SKILL.md` and proceed to Step 4.**
