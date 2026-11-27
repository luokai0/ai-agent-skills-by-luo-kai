# User Story Validation Report: [Feature Name]

**Date:** [YYYY-MM-DD]
**Stories validated:** [count]
**Source docs:** [list of requirements/epic docs used for source verification]

---

## RESULT: ✅ PASS / ⚠️ PASS WITH WARNINGS / ❌ FAIL

**Thresholds:** All categories PASS → ✅ | Ring 1 all PASS + Ring 2-3 warnings → ⚠️ | Any Ring 1 FAIL → ❌

---

## Per-Story Results

| Story | Ring 1 (1-6) | Ring 2 (7-8) | Ring 3 (9) | Verdict |
|-------|-------------|-------------|-----------|---------|
| [story title] | ✅/❌ [details] | ✅/⚠️ [details] | ✅/⚠️ [details] | PASS/WARN/FAIL |

---

## Cross-Story Results (Categories 10-11)

### Category 10: Story Set Architecture
- Circular dependencies: [findings with evidence]
- Orphaned stories: [findings]
- Distinct responsibilities: [findings]
- Coverage vs decomposition: [findings]

### Category 11: Cross-Story Coherence
- AC duplication: [findings with specific story + AC references]
- Field name consistency: [findings]
- FE/BE alignment: [findings]
- Boundary conflicts: [findings]
- Terminology drift: [findings]

---

## Practitioner Readability (Category 12)

**Stories spot-checked:** [list]

| Story | Developer Cold Read | QA Cold Read | Issues |
|-------|-------------------|-------------|--------|
| [title] | ✅/❌ | ✅/❌ | [specific issues if any] |

---

## Critical Issues (Must Fix)

| # | Story | Category | Finding | Evidence | Impact | Fix Action |
|---|-------|----------|---------|----------|--------|------------|
| 1 | [story] | [cat #] | [what's wrong] | [specific AC/line] | [This means...] | [what to do] |

---

## Warnings (Should Fix)

| # | Story | Category | Finding | Evidence | Impact |
|---|-------|----------|---------|----------|--------|
| 1 | [story] | [cat #] | [what's wrong] | [specific AC/line] | [This means...] |

---

## Requirements Coverage

| Requirement | Story(ies) Covering It | Status |
|-------------|----------------------|--------|
| [FR-1 or §X] | [story title(s)] | ✅ Covered |
| [FR-5 or §Y] | [none] | ❌ GAP — no story covers this |

---

## Readiness Assessment

**Can proceed to sprint?** YES / YES WITH CAUTION / NO

- **YES:** All categories pass. Stories are sprint-ready.
- **YES WITH CAUTION:** Ring 1 passes. Ring 2-3 warnings exist but don't block delivery.
- **NO:** Ring 1 failures exist. Stories are structurally broken. Fix before sprint.
