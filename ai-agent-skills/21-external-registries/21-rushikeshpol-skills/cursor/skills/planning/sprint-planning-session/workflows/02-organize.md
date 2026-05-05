# Workflow 02: Organize

**Called from:** `SKILL.md` Step 5
**Next step:** `workflows/03-generate.md`
**Saves to:** `[sprint-root]/stage_output/Organized-Groups.md`

---

## Purpose

Group tickets into logical work areas and validate the sprint plan against the goal. Run guardrails to catch problems before the planning document is generated.

---

## Preflight Checks

All must be YES before proceeding:

| Check | Status |
|-------|--------|
| Workflow 01 complete | |
| Normalized ticket table saved | |
| Sprint goal stated | |
| Capacity stated (or `[TBD]`) | |

If any check fails → return to `workflows/01-intake.md`.

---

## Step 1: Group Tickets

Apply grouping logic in priority order:

1. **If Release Plan has workstreams:** group by workstream (e.g., "Identity", "Clock-In", "Schedule")
2. **If tickets have a common domain tag:** group by domain
3. **Otherwise:** group by natural functional area (infrastructure, UI, backend, testing, etc.)

Each group gets:
- A descriptive name (e.g., "Identity — Login & Session")
- A 1-sentence context line explaining why this group matters this sprint
- The ticket table for that group

Separate **committed work** from **stretch goals**. Stretch items go in their own section.

---

## Step 2: Validate Against Goal

Check each validation:

| Validation | Question | Result |
|-----------|----------|--------|
| **Goal-work match** | Does the committed work achieve the sprint goal? | ✅ / ⚠️ / ❌ |
| **Capacity check** | Does capacity support the committed work? | ✅ / ⚠️ / ❌ |
| **Blocker check** | Are there blocked items in committed work? | ✅ / ⚠️ |
| **Owner check** | Are there unassigned tickets? | ✅ / ⚠️ |

---

## Step 3: Run Guardrails

Evaluate each guardrail. Only report those that trigger.

| Guardrail | Trigger | Detection | Action |
|-----------|---------|-----------|--------|
| **Goal-work mismatch** | Committed tickets don't achieve the sprint goal | Tickets categorized but none map to the stated goal | Warn: either the goal is wrong or the tickets are wrong |
| **Capacity breach** | More tickets than team can reasonably deliver | Ticket count or story points exceed capacity model | Warn: identify stretch vs committed, or reduce scope |
| **Missing owners** | Tickets have no assigned owner | Owner column blank for >50% of tickets | Warn: list unassigned tickets, suggest assignment |
| **Carryover not acknowledged** | Items from prior sprint not included | Prior Sprint Progress Report shows incomplete items not in this sprint's ticket list | Warn: list missing carryover items, ask if intentional |
| **Blocked item in committed work** | A committed item has a known blocker | Dependency or blocker field filled, no mitigation stated | Flag: move to stretch or add mitigation plan |

---

## Step 4: Save Organized Groups

Save the organized groups and guardrail results to: `[sprint-root]/stage_output/Organized-Groups.md`

---

## Step 5: Update State File

Update the state file: set `current_task` to `"T2"`, mark `T1` as `"completed"`, `T2` as `"in_progress"`, and record the organized groups artifact path.

---

## Completion Gate

- [ ] All tickets grouped into logical work areas
- [ ] Committed work separated from stretch goals
- [ ] All validations evaluated
- [ ] Guardrails run and results recorded
- [ ] Organized groups saved to file
- [ ] State file updated

**CHECKPOINT (Hard stop — T2 Gate):** "Here are the work groups. [N] guardrail warnings. Confirm before I generate the planning doc."

**STOP and WAIT for user confirmation.** Do not proceed until the user confirms the groups and addresses any guardrail warnings.

**When complete, return to `SKILL.md` and proceed to Step 6.**
