# Workflow 5: Modify Existing Story

**Called from:** `SKILL.md` when MODIFY mode detected
**Next step:** Complete after changes applied and approved.
**Reads:** Existing story file + `[output-folder]/.meta/story-registry.md` (if exists)

---

## 📍 You Are Here
**Skill:** generate-user-stories
**Stage:** MODIFY mode (standalone — not part of the create pipeline)
**Input:** Existing story file + user's change request
**Your only job:** Understand the change, assess impact, apply targeted edits, update registry
**DO NOT:** Regenerate the entire story when only one AC needs changing.
**DO NOT:** Skip the breaking change assessment.
**DO NOT:** Change anything the user didn't ask to change — prior approvals are sacred.
**Audience:** The modified story must still pass the two cold-read tests for developer and QA.

---

## 📖 Step 0: Verify Existing Reality (mandatory)

1. Read the existing story file completely
2. Create internal baseline: current user statement, ACs, dependencies, key fields/endpoints
3. If Swagger/API spec is referenced: read it to understand current API behavior
4. Document: "EXISTING BEHAVIOR as of [date]"

---

## 🔍 Step 1: Understand the Change Request

Classify the request:

| Type | Signal | Example |
|------|--------|---------|
| **Targeted AC change** | "change AC 3", "update the date range" | Change one specific AC |
| **Add new requirements** | "add error handling", "also cover mobile" | New ACs from updated requirements |
| **Quality improvement** | "make it clearer", "fix the user statement" | Better writing, not new scope |
| **Story split** | "this is too big", "break this into two" | Scope reduction |
| **Requirement update** | "the requirement changed", "new Swagger" | Upstream change |

Present classification: "I understand you want to [type]. Here's my plan:"
**STOP and WAIT for confirmation.**

---

## ⚖️ Step 2: Assess Impact (4-way classification)

Classify every proposed change:

| Classification | Definition | Action |
|---------------|-----------|--------|
| **EXISTING (MODIFY)** | Changes to existing ACs | Check: does this affect other stories' boundaries? |
| **NEW (ADDITIVE)** | New ACs added | Check: AC count still ≤ 6? If not → split. |
| **BREAKING** | Invalidates other stories' assumptions | **STOP.** Flag affected stories. Ask user. |
| **NON-BREAKING** | Backward-compatible | Proceed with targeted edit. |

**If BREAKING changes found:** "This change affects [Story X] because [reason]. Proceed?"
**STOP and WAIT if BREAKING.**

---

## ✏️ Step 3: Apply the Change (Ring order)

**Targeted AC change:** Use Edit tool on the saved file. Change ONLY the specific AC.
**Add new requirements:** Add new ACs. If > 6 total → suggest split (don't compress).
**Quality improvement:** Apply specific fix. Re-run relevant gates.
**Story split:** Decompose into 2+ stories. Save new files, archive original, update registry.
**Requirement update:** Identify affected ACs. Apply targeted edits.

After ALL changes, re-run gates in Ring order:
- Ring 1: No fabrication, no over-generalization, source traceability, user statement, no code, no weak language
- Ring 2: AC scope ≤ 6, terminology, visual evidence (FE)
- Ring 3: Structure, line count

---

## 📝 Step 4: Update Change History + Registry

Add entry to story's Change History:
```
| [date] | [N+1] | [what changed] | [why — user request or requirement change] |
```

If `[output-folder]/.meta/story-registry.md` exists: update the entry for this story.
If breaking changes affected other stories: update those entries too.

---

## 💬 Step 5: Present Changes

```
Changes applied to: [story file path]

Changed:
- [what was modified]

NOT changed:
- [everything else — confirming prior approvals are intact]

[If breaking: "Also affected: [story X] — [what changed there]"]

Quality gates: ✅ All passed after edit
```

**STOP and WAIT for user response.**

---

## ✅ Completion Gate
- [ ] Existing story read and baselined before changes
- [ ] Change request classified and confirmed by user
- [ ] Breaking change assessment completed
- [ ] Targeted edits applied (not full regeneration unless structural)
- [ ] Quality gates re-run in Ring order
- [ ] Change History updated
- [ ] Registry updated (if exists)
- [ ] User has explicitly approved changes
If any item is unchecked → do NOT mark as complete.
