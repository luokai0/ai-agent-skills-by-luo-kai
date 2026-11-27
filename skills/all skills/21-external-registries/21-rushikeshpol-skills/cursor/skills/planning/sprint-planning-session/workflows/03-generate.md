# Workflow 03: Generate

**Called from:** `SKILL.md` Step 6
**Next step:** `workflows/04-refine.md` (optional)
**Saves to:** `[sprint-root]/Sprint-[N]-Planning.md`

---

## Purpose

Produce the Sprint Planning Session document using the organized groups and validated inputs.

---

## Preflight Checks

All must be YES before proceeding:

| Check | Status |
|-------|--------|
| Workflow 02 complete (T2 gate passed) | |
| User confirmed organized groups | |
| Guardrail alerts addressed | |
| Template loaded | |

If any check fails → return to `workflows/02-organize.md`.

---

## Step 1: Load Template

Read the file:

    templates/sprint-planning.md

Use this template as the structure for the output document. Every section is required. If a section truly doesn't apply, use "N/A — [reason]" rather than leaving it empty.

---

## Step 2: Generate Document

Fill the template using:
- Sprint metadata (number, dates, goal) from intake
- Organized groups from Workflow 02
- Team capacity from intake
- Carryover items from intake (if any)
- Dependencies and blockers from ticket data
- Risks identified during guardrail evaluation

**Writing rules:**
- Sprint goal must be user-facing: "Officers can log in and clock in" not "Implement login API"
- "Done" checklist items must be specific and testable, not vague
- Each "Done" item must map to at least one committed ticket
- Dates in Mon DD format (e.g., "Apr 29")
- No developer jargon in the sprint goal or "Done" section

---

## Step 3: Self-Check Before Saving

Run the self-check. All P1 items must pass or the document is regenerated.

**P1 — Hard gate (regenerate if fails):**
- [ ] Every ticket in the normalized list appears in the output
- [ ] Sprint goal is user-facing (not developer-facing)
- [ ] No required section is empty (use "N/A — [reason]" if nothing applies)
- [ ] Every "Done" checklist item maps to at least one ticket
- [ ] Source attribution present on authoritative claims (dates, numbers, statuses, decisions)

**P2 — Edit gate (fix before saving):**
- [ ] Every risk has a mitigation or owner
- [ ] Carryover items from prior sprint acknowledged
- [ ] Guardrail results addressed
- [ ] No unresolved `(Source: Implicit)` on authoritative claims

**P3 — Note and proceed:**
- [ ] Date formatting consistent (Mon DD)
- [ ] Template structure fully followed
- [ ] Terminology consistent with prior documents in the chain

---

## Step 4: Save Document

Save to: `[sprint-root]/Sprint-[N]-Planning.md`

---

## Step 5: Update State File

Update the state file: set `current_task` to `"T4"`, mark `T3` as `"completed"`, `T4` as `"in_progress"`, and record the planning doc artifact path.

---

## Completion Gate

- [ ] Template fully populated
- [ ] Self-check P1 all passed
- [ ] Self-check P2 items fixed
- [ ] Document saved to file
- [ ] State file updated

**CHECKPOINT (Review gate — T4 Verify):** "Planning session doc saved to [path]. Review and confirm, or request changes."

If the user requests changes → proceed to `workflows/04-refine.md`.
Otherwise, the skill is complete.

**When complete, return to `SKILL.md` and proceed to Step 7.**
