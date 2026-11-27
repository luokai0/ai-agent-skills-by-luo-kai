# Workflow 4: Set Review — Cross-Story Coherence Check

**Called from:** `workflows/03-create-story.md` after all stories created and approved
**Next step:** Complete. Suggest `/validate-user-stories` for full 12-category audit.
**Reads:** `[output-folder]/.meta/story-registry.md` + `[output-folder]/.meta/Decomposition-[Feature].md` + source requirements doc

---

## 📍 You Are Here
**Skill:** generate-user-stories
**Stage:** 4 of 4 — Set Review
**Input:** Completed story registry + decomposition + requirements doc
**Your only job:** Verify cross-story coherence and requirements coverage using the registry
**DO NOT:** Declare coherence without checking each item in the checklist. Cite specific evidence for each pass.
**DO NOT:** Rubber-stamp with "everything looks good."
**DO NOT:** Re-validate individual story quality — that's `validate-user-stories`.
**Audience:** You are checking that the story SET works as a cohesive unit for a sprint team.

---

## 📖 Step 1: Read Inputs

1. Read `story-registry.md` (compact, complete)
2. Read `Decomposition-[Feature].md` for coverage comparison
3. Read source requirements doc (or epic) for reverse traceability
4. Spot-check 2-3 story files for registry accuracy (does the registry entry match the actual file?)

---

## 🔍 Step 2: Run Coherence Checks

For each check, cite specific evidence (story names, AC numbers, field names). Never just "pass."

### Check 1: Coverage Gaps
Compare decomposition concepts vs written stories.
- Every concept in decomposition has a corresponding story file?
- Any concept dropped during creation? Flag it.

### Check 2: AC Duplication
Scan registry for same behavior appearing in multiple stories.
- Same field name or endpoint claimed by two stories?
- Same user action described in two different stories?

### Check 3: Boundary Conflicts
Check Boundary column in registry.
- Two stories claiming same behavior or data ownership?
- Gaps where no story owns a behavior that should exist?

### Check 4: Dependency Ordering
Check Dependencies table in registry.
- Circular dependencies? (A depends on B, B depends on A)
- Orphaned stories? (story depends on something that doesn't exist)

### Check 5: Terminology Consistency
Scan registry + spot-check files.
- Same concept called different names in different stories?
- Conventions section followed by all stories?

### Check 6: Platform Coherence
FE stories expect data that BE stories provide?
- FE story references a field → does a BE story produce it?
- BE story returns data → does an FE story consume it?

### Check 7: Requirements-to-Stories Reverse Traceability
Every functional requirement in source doc has at least one story covering it.

```
| Requirement | Story(ies) | Status |
|-------------|-----------|--------|
| [FR-1 or §X] | [story title(s)] | ✅ Covered |
| [FR-5 or §Y] | [none] | ❌ GAP — no story covers this |
```

---

## 💬 Step 3: Present Coherence Report (inline — not a file)

```
Set Review: [Feature Name]

Stories reviewed: [count]
Checks run: 7

Results:
1. Coverage: [pass/issues found]
2. AC Duplication: [pass/issues found]
3. Boundary Conflicts: [pass/issues found]
4. Dependencies: [pass/issues found]
5. Terminology: [pass/issues found]
6. Platform Coherence: [pass/issues found]
7. Requirements Coverage: [N]/[total] covered, [gaps] gaps

[If issues found: list each with specific stories affected and recommended fix]

Recommendation:
- [All clear / Fix issues before validation / Add missing stories]

Next: Run /validate-user-stories for a full 12-category audit.
```

**STOP and WAIT for user response.**

---

## 🔄 After User Acknowledges

Update `[output-folder]/.meta/.pipeline-state.json`: stage "04-set-review", stages_completed.

If DECOMPOSE-only or pipeline: mark skill as complete.
Suggest: "Run `/validate-user-stories` for full validation with practitioner readability checks."

---

## ✅ Completion Gate
- [ ] All 7 coherence checks run with specific evidence cited
- [ ] Requirements-to-stories traceability matrix built
- [ ] Issues (if any) presented with affected stories and recommended fixes
- [ ] Pipeline state updated
- [ ] User has acknowledged
If any item is unchecked → do NOT mark as complete.
