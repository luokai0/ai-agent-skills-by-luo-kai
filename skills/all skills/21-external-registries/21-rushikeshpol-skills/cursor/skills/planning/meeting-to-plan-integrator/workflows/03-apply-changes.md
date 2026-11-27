# Workflow 03: Apply Changes

**Called from:** `SKILL.md` Step 4
**Next step:** `workflows/04-cascade.md`

---

## Purpose

Apply confirmed changes to target documents.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 02 complete (T2 gate passed) | |
| User confirmed which changes to apply | |
| Change manifest saved | |

---

## Step 1: Apply Each Confirmed Change

For each confirmed change from the manifest:

1. Read the target document
2. Locate the specific section to update
3. Apply the edit, preserving existing formatting
4. Add source attribution: `(Source: [meeting-name], [date])`
5. Save the updated document
6. Update constraint registry if change introduces new constraints

---

## Step 2: Post-Edit Check

For each edited document:
- [ ] Table formatting preserved (no broken markdown)
- [ ] Edited section makes sense in context
- [ ] Cross-references still valid (e.g., feature IDs, sprint numbers)

---

## Completion Gate

- [ ] All confirmed changes applied
- [ ] Source attribution added to every edit
- [ ] Post-edit checks passed
- [ ] Updated documents saved
- [ ] Constraint registry updated (if applicable)

**When complete, return to `SKILL.md` and proceed to Step 5.**
