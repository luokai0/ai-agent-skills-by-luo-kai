# Workflow 04: Cascade

**Called from:** `SKILL.md` Step 5
**Saves to:** Updated downstream documents (if user confirms)

---

## Purpose

Check if changes ripple to other documents. Cascade only what the user confirms.

**ANTI-MOMENTUM GATE:** Before cascading, verify:
1. Am I applying user-confirmed changes, or inventing new ones?
2. Is the source the change manifest (T2-confirmed), not my reasoning?
3. Could this cascade change be wrong? If yes, flag rather than apply.

---

## Step 1: Identify Downstream Effects

For each applied change, check:
- Does this affect the **Scope document**? (scope changes always do)
- Does this affect future **Sprint Planning Session docs**?
- Does this affect the **Sprint Progress Report**?
- Does this affect the **Release Definition**? (if a plan change implies a definition change)
- Does this require a **constraint registry update**?

---

## Step 2: Present Cascade List

For each potential cascade:

| # | Original Change | Downstream Document | Proposed Edit | Confidence |
|---|----------------|--------------------|--------------|-----------:|

Mark confidence:
- **High** — logical necessity (scope removed from plan → must remove from scope doc)
- **Medium** — likely needed but should verify
- **Low** — possible ripple, flag for review

---

## Step 3: Apply Confirmed Cascades

Apply only what the user confirms. For each:
1. Read the downstream document
2. Apply the edit with source attribution
3. Save

---

## Completion Gate

- [ ] Downstream effects identified
- [ ] Cascade list presented to user
- [ ] Confirmed cascades applied
- [ ] All documents saved
- [ ] Change manifest updated with cascade actions

**CHECKPOINT (Review gate — T5 Gate):** "Changes applied to [N] documents. Cascade analysis: [N] downstream effects. [N] applied, [N] skipped. Review."

**Skill is complete.**
