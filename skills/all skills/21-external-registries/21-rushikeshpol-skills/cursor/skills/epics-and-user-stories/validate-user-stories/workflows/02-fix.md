# Workflow 2: Fix Failed Stories

**Called from:** `workflows/01-validate.md` after user reviews validation report
**Next step:** Complete. Offer `/document-audit` for staleness check.
**Reads:** `[output-folder]/Validation-Report-[Feature].md` (or Resolution file from `/review-findings`)

---

## 📍 You Are Here
**Skill:** validate-user-stories
**Stage:** 2 of 2 — Fix
**Input:** Validation report with findings (or Resolution file with approved findings only)
**Your only job:** Fix failed stories in Ring order, re-validate fixed stories
**DO NOT:** Fix Ring 2-3 issues while Ring 1 failures remain.
**DO NOT:** Apply fixes to one story in a cross-story issue without fixing the other.
**DO NOT:** Regenerate entire stories when targeted edits suffice.
**Audience:** Fixed stories must still pass the two cold-read tests.

---

## 📖 Step 1: Read Findings

Read the validation report (or Resolution file if `/review-findings` was run — only fix APPROVED findings).

Sort findings by Ring:
1. **Ring 1 failures** — fix these FIRST (No Fabrication, No Over-Generalization, Source Traceability, User Statement, No Implementation Details, No Weak Language)
2. **Ring 2 failures** — fix AFTER Ring 1 passes (AC Scope, Visual Evidence)
3. **Ring 3 failures** — fix LAST (Story Structure)
4. **Cross-story issues** (Categories 10-11) — fix BOTH affected stories

---

## ✏️ Step 2: Apply Fixes (Ring order)

### Ring 1 Fixes (mandatory before Ring 2-3)

| Finding | Fix approach |
|---------|-------------|
| Fabricated data | Replace with `[TBD — requires: X] (Route to: Y)` or correct from source |
| Over-generalization | Narrow to match source scope exactly |
| Missing source citation | Add `(Req §X)` if source exists, or flag `[SOURCE UNVERIFIED]` |
| Bad user statement | Rewrite with specific persona + clear goal + clear value |
| Implementation details | Remove code/component refs. Rewrite as WHAT user experiences. Empty Dev Notes. |
| Weak language | Replace should→must, remove vague quantifiers, add specifics or [TBD] |

**Method:** Use Edit tool for targeted changes. Read the specific story file, apply the fix to the specific AC or section.

### Ring 2 Fixes (only after Ring 1 passes)

| Finding | Fix approach |
|---------|-------------|
| > 6 ACs | Story too big. Surface split recommendation to user (don't compress). |
| Missing visual evidence (FE) | Add Figma link or flag `[TBD — requires: design mockup] (Route to: UX Designer)` |

### Ring 3 Fixes (only after Ring 1+2 pass)

| Finding | Fix approach |
|---------|-------------|
| Missing sections | Add from template |
| Wrong title format | Fix to `[Platform] -- [Feature] -- [Context]` |
| Over line count | Review for prose that should be links, ACs that could consolidate |

### Cross-Story Fixes (Categories 10-11)
Fix BOTH stories in a boundary conflict or duplication issue. Never fix just one side.

---

## 🔄 Step 3: Re-Validate Fixed Stories

After fixes applied:
1. Re-run affected validation categories on each fixed story (start from Ring 1)
2. Update validation registry entries for fixed stories
3. Record fix results

---

## 💬 Step 4: Present Results

```
Fixes Applied: [Feature Name]

Fixed:
- [Story X]: [what was fixed] — now ✅ PASS
- [Story Y]: [what was fixed] — now ✅ PASS

Remaining issues (if any):
- [Issue] — requires user input: [what's needed]

Updated files:
- [list of modified story files]

Overall: ✅ PASS / ⚠️ PASS WITH WARNINGS / ❌ Still has issues
```

**STOP and WAIT.**

Offer: "Run `/document-audit` on the fixed stories to catch staleness or broken cross-references introduced by edits?"

---

## ✅ Completion Gate
- [ ] Fixes applied in Ring order (Ring 1 first, then Ring 2, then Ring 3)
- [ ] Cross-story issues fixed on BOTH sides
- [ ] Fixed stories re-validated
- [ ] Validation registry updated
- [ ] Pipeline state updated (if `[output-folder]/.meta/.pipeline-state.json` exists)
- [ ] User has reviewed results
If any item is unchecked → do NOT mark as complete.
