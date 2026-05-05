# Workflow 1: Validate User Stories (12 Categories)

**Called from:** `SKILL.md` after intake
**Next step:** `workflows/02-fix.md` if failures found, or complete if all pass
**Saves:** `[output-folder]/validation-registry-[feature].md` + `[output-folder]/Validation-Report-[Feature].md`

---

## 📍 You Are Here
**Skill:** validate-user-stories
**Stage:** 1 of 2 — Validate
**Input:** Story files in feature folder + optional requirements doc
**Your only job:** Build fresh registry, run 12 validation categories, generate report
**DO NOT:** Evaluate Ring 2-3 if Ring 1 failed — short-circuit.
**DO NOT:** Assign a severity without citing the specific evidence that supports it.
**DO NOT:** Declare "pass" without checking. Every pass needs evidence too.
**Audience:** You are auditing stories that will go to a sprint team. Accuracy matters more than speed.

---

## 📖 Step 0: Build Fresh Validation Registry (ALWAYS)

**Never skip. Never trust existing `.meta/story-registry.md`.**

Read EVERY story file in the feature folder. Per story, extract:
- Title, platform, user statement, AC titles, key fields/endpoints, implicit boundary

Save to: `[output-folder]/validation-registry-[feature].md`
Verify: story count matches files in folder. Every file has an entry.

---

## 🔍 Step 1: Per-Story Validation (Categories 1-9)

**Ring 1 — Accuracy (structurally broken if fails). If ANY Ring 1 fails → skip Ring 2-3.**

| Cat | Check | Evidence to cite |
|-----|-------|-----------------|
| 1 | **No Fabrication** — every field, rule, value from source or marked [TBD] | Specific field/value + whether source contains it |
| 2 | **No Over-Generalization** — AC scope matches source exactly | Specific widened actor/condition vs what source says |
| 3 | **Source Traceability** — every AC cites requirement | Which ACs lack `(Req §X)` citations |
| 4 | **User Statement Quality** — specific persona, clear goal, clear value, INVEST | What's wrong with persona/goal/value |
| 5 | **No Implementation Details** — WHAT not HOW, Dev Notes empty | Specific code/component/framework reference found |
| 6 | **No Weak Language** — no should/may/could, no vague quantifiers | Specific banned word + location |

**Ring 2 — Usability (hard to use if fails). Only evaluate if Ring 1 passed.**

| Cat | Check | Evidence to cite |
|-----|-------|-----------------|
| 7 | **AC Scope** — count ≤ 6, each distinct, Given/When/Then, correct terminology | AC count + which ACs overlap |
| 8 | **Visual Evidence** (FE only) — images in ACs, Figma links with /m=dev | Which ACs lack visual evidence |

**Ring 3 — Format (style violation). Only evaluate if Ring 1+2 passed.**

| Cat | Check | Evidence to cite |
|-----|-------|-----------------|
| 9 | **Story Structure** — title format, sections present, 60-90 lines (warn 91-120, review 121+) | Missing sections, line count |

**Creation-validation alignment:** If story was created by `generate-user-stories`, Categories 1-9 should PASS (creation gates identical). Any failure = flag: "Creation gate failure detected."

---

## 🔗 Step 2: Cross-Story Validation (Categories 10-11)

Work from validation registry. Spot-check 2-3 files where flags arise.

| Cat | Check |
|-----|-------|
| 10 | **Story Set Architecture** — circular deps? orphaned stories? distinct responsibilities? coverage vs decomposition? |
| 11 | **Cross-Story Coherence** — AC duplication? field name consistency? FE/BE alignment? boundary conflicts? terminology drift? |

---

## 👁️ Step 3: Practitioner Readability (Category 12 — Ring 1 weight)

Spot-check 2-3 highest-risk stories (complex ACs, many dependencies, FE/BE spanning).

**Developer cold read:** Read story once. Can you state what to build without re-reading?
Check: perspective drift, dependency inversion, hidden exceptions, internal contradictions.

**QA cold read:** Read story once. Can you state how to verify each AC is done?
Check: observable outcomes, testable conditions, no ambiguous language.

A story that fails either cold read is **structurally broken** regardless of other checks.

---

## 📊 Step 4: Generate Report

Use `templates/validation-report.md`. Combine all results.

**Per story:** ✅ PASS / ⚠️ PASS WITH WARNINGS / ❌ FAIL
**Overall:** All PASS → ✅ | Ring 1 all PASS + Ring 2-3 warnings → ⚠️ | Any Ring 1 FAIL → ❌

Save to: `[output-folder]/Validation-Report-[Feature].md`

Update `[output-folder]/.meta/.pipeline-state.json` (if exists): stage "01-validate", stages_completed.

Present summary: overall result, per-story verdicts, critical issues count, warnings count, requirements coverage matrix.

**STOP and WAIT.**

Offer: "Run `/review-findings` to walk through findings interactively?"

---

## ✅ Completion Gate
- [ ] Fresh validation registry built from actual files
- [ ] Categories 1-9 run per story (with Ring short-circuit)
- [ ] Categories 10-11 run on registry
- [ ] Category 12 spot-checked on 2-3 highest-risk stories
- [ ] Report saved with evidence for every finding
- [ ] User has reviewed report
If any item is unchecked → do NOT proceed.
