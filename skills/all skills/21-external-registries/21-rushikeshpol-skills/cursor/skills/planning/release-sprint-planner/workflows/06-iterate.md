# Workflow 06: Iterate (Re-Entrant)

**Called from:** `SKILL.md` Step 9
**Next step:** `workflows/07-finalize.md`
**Saves to:** `[release-root]/Release-Plan.md` (updated), `[release-root]/Release-Definition.md` (if affected)

---

## Purpose

Incorporate feedback and improve the plan. This workflow may loop multiple times.

---

## Prerequisite (UPDATE Mode Entry Point)

If entering directly in UPDATE mode (skipping workflows 01-05):
1. Load the existing Release-Definition.md and Release-Plan.md
2. Load the constraint registry from `.meta/constraint-registry.md`
3. Load the shared context files (delivery-model.md, execution-rules.md)

---

## Step 1: Accept Feedback

Accept feedback from:
- User verbal input
- Meeting notes or transcript summaries
- Team feedback (forwarded by user)
- Changed constraints (timeline, team, scope)

---

## Step 2: Apply Changes

For each iteration:
1. Identify what changed
2. Apply changes to Release-Plan.md
3. If changes affect the release definition (scope, timeline, team, risks), update Release-Definition.md too
4. Re-run guardrails on affected sprints (see `workflows/05-draft-plan.md` Step 3)
5. Highlight what moved and why
6. Save updated files

---

## Completion Gate

- [ ] Changes applied to Release-Plan.md
- [ ] Release-Definition.md updated if needed
- [ ] Guardrails re-run on affected sprints
- [ ] Updated files saved

**CHECKPOINT (Review gate — T7 iterate):** "Updated plan saved. Changes: [list]. Review and confirm, or request another iteration."

**Exit condition:** User says "looks good", "approved", or "finalize".

**When user approves, return to `SKILL.md` and proceed to Step 10.**
