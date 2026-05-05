# Workflow 07: Finalize

**Called from:** `SKILL.md` Step 10
**Next step:** None — skill completes after this
**Saves to:** `[release-root]/Release-Plan.md` (final), `[release-root]/Scope.md`, `[release-root]/Release-Definition.md` (final)

---

## Purpose

Lock the plan and produce companion documents. Run a final consistency check.

---

## Step 1: Complete Release Plan

Add to Release-Plan.md if not already present:
- Planning rules (from user input or defaults)
- Workstream ownership table (if workstream-based)
- Key technical decisions table (from meeting notes / user input)
- Deferred / out of scope table (sourced from Release Definition scope-out)
- UAT cadence table (sourced from Release Definition UAT strategy)
- Stream completion / buffer analysis
- Backend timeline (if applicable)

---

## Step 2: Produce Scope Document

Create `[release-root]/Scope.md`:
- Phase-by-phase scope document (what's in Phase 1, what's deferred)
- Sourced from Release Definition scope-in and scope-out sections

---

## Step 3: Final Consistency Check

Verify all of the following:

- [ ] Every Must-have feature from Release Definition appears in exactly one sprint
- [ ] No sprint exceeds capacity from Release Definition
- [ ] All dependencies satisfied
- [ ] Sprint goals align with assigned work
- [ ] Sprint goals trace back to release goal
- [ ] UAT dates align with sprint end dates and Release Definition UAT strategy
- [ ] Deferred items list matches Release Definition scope-out
- [ ] Go/no-go criteria from Release Definition are achievable given the plan
- [ ] Success criteria from Release Definition have measurable checkpoints in plan

If any check fails, flag it and fix before saving.

---

## Step 4: Save Final Artifacts

Save:
- `[release-root]/Release-Plan.md` (final)
- `[release-root]/Scope.md` (new)
- `[release-root]/Release-Definition.md` (updated with any final changes from iteration)

Update state file: mark all tasks as completed.

---

## Completion Gate

- [ ] Release Plan finalized with all supplementary sections
- [ ] Scope.md created
- [ ] Release Definition updated if needed
- [ ] Final consistency check passed
- [ ] All files saved
- [ ] State file marked complete

**CHECKPOINT (Notification):** "Release planning complete. Files saved:
- Release-Definition.md (anchor)
- Release-Plan.md (execution)
- Scope.md (phase tracker)

The sprint-planning-session skill can now be used for individual sprint kickoffs."

**Skill is complete.**
