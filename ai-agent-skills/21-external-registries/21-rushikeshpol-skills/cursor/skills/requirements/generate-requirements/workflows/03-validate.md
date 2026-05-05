# Workflow 3: Validate Requirements

**Called from:** `workflows/02-generate.md` after user confirms
**Final step — no further workflows**
**Reads:** All documents in `[output-folder]/Generated/Internal/`
**Output:** `[output-folder]/Generated/Report/Validation-Report-[Feature-Name].md`

> `[output-folder]` is the path provided by the user during SKILL.md intake. It is NOT a hardcoded path.

## Pipeline Mode: Skip

When this skill is called from `/requirements-pipeline` (Stage 7), skip this workflow entirely.
The pipeline runs `/validate-requirements` at Stage 9 with a comprehensive 15-check validation
that supersedes this workflow's lighter checks. Running both wastes context budget.

Instead, return to the pipeline orchestrator with:
"Workflow 3 (internal validation) skipped -- pipeline will run /validate-requirements at Stage 9."

## NON-NEGOTIABLE (read first)
1. Read the full document before scoring. Never validate from a partial read.
2. Detect fabricated data in every section. Unsourced = flag.
3. Save validation report to file before presenting. Chat is ephemeral.
4. Count and categorize ALL [TBD] markers with stakeholder routing.
5. Wait for user response. Never auto-proceed or suggest next steps without user intent.

## Critical Rules

| Do | Don't |
|-------|---------|
| Validate ALL applicable contexts (mark N/A if not applicable) | Skip context validation |
| Check for fabricated data in every section | Accept unsourced data as valid |
| Count and categorize ALL [TBD] markers | Ignore TBDs |
| Verify internal document consistency | Assume sections within the document align |
| Save report before presenting | Display only in chat |
| Wait for user response | Auto-proceed or suggest story creation without user intent |

---

## 🎯 Purpose

Score all generated requirement documents against structured criteria.
Determine readiness for story creation. Identify and route remaining gaps.

---

## 📖 Step 1: Identify Documents to Validate

Read the Feature Requirements document:
- `[output-folder]/Generated/Internal/Feature-Requirements-[Feature-Name].md` — MANDATORY

Read the document completely before scoring.

---

## 🧩 Step 2: Validate 6-Context Completeness

**Score each context: ✅ Complete (5/5 criteria) | ⚠️ Partial (3-4/5) | ❌ Incomplete (0-2/5)**

### Context 1: Business Context
| Criterion | Check | Score |
|-----------|-------|-------|
| Problem statement clear | ✅/❌ | |
| Business value quantified or qualified | ✅/❌ | |
| Success metrics defined | ✅/❌ | |
| Constraints documented | ✅/❌ | |
| Stakeholders identified | ✅/❌ | |

### Context 2: Product Context
| Criterion | Check | Score |
|-----------|-------|-------|
| In-scope features listed | ✅/❌ | |
| Out-of-scope explicitly stated | ✅/❌ | |
| User needs documented | ✅/❌ | |
| Success criteria defined | ✅/❌ | |
| Dependencies listed | ✅/❌ | |

### Context 3: Persona Context *(N/A for Quick Mode)*
| Criterion | Check | Score |
|-----------|-------|-------|
| Named personas (not generic "user") | ✅/❌/N/A | |
| Goals per persona | ✅/❌/N/A | |
| Pain points per persona | ✅/❌/N/A | |
| Usage context (device, frequency) | ✅/❌/N/A | |
| Representative quote | ✅/❌/N/A | |

### Context 4: UX Context *(N/A for backend-only features)*
| Criterion | Check | Score |
|-----------|-------|-------|
| Design asset references present | ✅/❌/N/A | |
| User flows documented (numbered steps) | ✅/❌/N/A | |
| All visual states covered (empty/loading/error/success) | ✅/❌/N/A | |
| Key interactions defined | ✅/❌/N/A | |
| Responsive behavior noted | ✅/❌/N/A | |

### Context 5: Technical Context
| Criterion | Check | Score |
|-----------|-------|-------|
| System architecture present | ✅/❌ | |
| Technology stack identified | ✅/❌ | |
| APIs/endpoints listed (or TBD with reason) | ✅/❌ | |
| Data model / key entities defined | ✅/❌ | |
| Performance requirements specified | ✅/❌ | |

### Context 6: Compliance Context *(N/A for Quick Mode)*
| Criterion | Check | Score |
|-----------|-------|-------|
| Regulatory requirements stated (or N/A) | ✅/❌/N/A | |
| Security requirements defined | ✅/❌ | |
| Accessibility noted (or N/A) | ✅/❌/N/A | |
| Browser/device support specified | ✅/❌/N/A | |
| Backward compatibility addressed | ✅/❌/N/A | |

---

## 🔬 Step 3: Source Data Integrity Check

**Critical: Detect any fabricated, unsourced, or misattributed data.**

### 3a: Source Presence Check

| Data Element | Check | Verdict |
|--------------|-------|---------|
| Business rules | Sourced from document? | ✅ Sourced / ❌ Inferred without source |
| Performance targets | Sourced or [TBD]? | ✅ Sourced / ❌ Made up |
| API field names | From Swagger/code? | ✅ Sourced / ❌ Invented |
| Personas | From research/docs? | ✅ Sourced / ❌ Generic |
| User flows | From designs? | ✅ Sourced / ❌ Assumed |
| Technical details | From architecture/code? | ✅ Sourced / ❌ Guessed |

### 3b: Source Accuracy Verification

For each `(Source: SRC-N)` citation in the document, verify the source actually contains the claimed information:

| Check | What to look for | Verdict |
|-------|------------------|---------|
| **Citation accuracy** | Does SRC-N actually say what the doc claims it says? | ✅ Accurate / ⚠️ Partially accurate / ❌ Inaccurate |
| **Over-generalization** | Does the source say "X in context A" but the doc says "X everywhere"? | ✅ Scoped correctly / ❌ Over-generalized |
| **Implicit sources** | Are `(Source: Implicit)` tags genuinely logical derivations, or gap-fills? | ✅ Valid derivation / ❌ Should be [TBD] |

### 3c: Requirement Purity Check

| Check | What to look for | Verdict |
|-------|------------------|---------|
| **Solutions in FRs** | Does any FR prescribe HOW (implementation mechanism) instead of WHAT (capability)? | ✅ Pure requirement / ❌ Contains solution |
| **Design in FRs** | Does any FR prescribe UI layout, navigation pattern, or visual structure? | ✅ Pure requirement / ❌ Contains design decision |
| **Current state claims** | Are claims about "currently" or existing product verified against a confirmed source? | ✅ Verified / ❌ Assumed |

**Count [TBD] markers:**
- Total TBDs: [N]
- 🔴 Critical (blocks story creation): [N] — list each with stakeholder routing
- 🟡 Important (reduces quality): [N]
- 🟢 Optional: [N]

**Thresholds:**
- 5+ Critical TBDs → ❌ FAIL source integrity
- 10+ Total TBDs → ⚠️ WARNING (incomplete)
- Any fabricated data (sourced as "invented") → ❌ FAIL source integrity
- Any inaccurate source citation → ❌ FAIL source integrity
- Any solution or design decision written as a requirement → ⚠️ WARNING (purity)

---

## 🔀 Step 4: Cross-Section Deduplication Check

Scan the document's Constraints, Known Limitations, Assumptions, Dependencies, and Open Questions sections for items that appear in more than one location.

**Classification reference (each item gets exactly one home):**

| Classification | Definition |
|---|---|
| **Hard Constraint** | Non-negotiable system rule (regulatory, legal, timeline) |
| **Dependency** | Deliverable another team must provide before we can build |
| **Assumption** | Something we believe but haven't confirmed; carries risk if wrong |
| **Known Limitation** | Confirmed gap we are shipping with (accepted trade-off) |
| **Open Question** | Stakeholder decision needed before proceeding |

**Check for these specific overlaps:**

| Check | Sections to compare | Verdict |
|-------|---------------------|---------|
| Same fact in Constraints AND Dependencies | Section 2/7 vs Section 13 | ❌ Duplicate if constraint is just restating the dependency |
| Same uncertainty in Assumptions AND Open Questions | Section 13 vs Section 15 | ❌ The OQ should own it |
| Known Limitation restates a Dependency with an owner | Section 11 vs Section 13 | ❌ The Dependency should own it |
| Same rule in two Constraint locations | Section 2 vs Section 7 | ❌ Keep the more specific version |
| Confirmed assumption still in Assumptions table | Section 13 | ❌ Should be deleted or moved to Known Limitations |
| Cross-references stale after renumbering | All sections | ❌ Update references |

**Count duplicates found:**
- Total cross-section duplicates: [N]
- 🔴 Critical (blocks clarity): [N]
- 🟡 Warning (redundant but not contradictory): [N]

**Thresholds:**
- 3+ cross-section duplicates → ⚠️ WARNING (deduplication incomplete)
- Any contradictory duplicate (same topic, different rules) → ❌ FAIL

---

## 📊 Step 5: Compute Overall Score

### Scoring Formula

**Context Completeness Score:**
- Count criteria across all applicable contexts
- Score = (✅ passes) / (total applicable criteria) × 100
- Quick Mode: score against 3 contexts (15 criteria max)
- Comprehensive Mode: score against 6 contexts (30 criteria max)

**Threshold:**
| Score | Status |
|-------|--------|
| 90–100% | ✅ PASS |
| 70–89% | ⚠️ PASS WITH WARNINGS |
| < 70% | ❌ FAIL |

**Overall readiness:** ALL four checks (Completeness, Source Integrity, Deduplication, Alignment) must PASS for overall PASS.

---

## 📋 Step 6: Generate Validation Report

**Template:**

```markdown
# Requirements Validation Report: [Feature Name]

**Date:** [Date]
**Document validated:**
- Feature Requirements: ✅/❌

---

## RESULT: ✅ PASS / ⚠️ PASS WITH WARNINGS / ❌ FAIL

**Summary:**
- Completeness: [X]% ([N] contexts complete)
- Source integrity: [N] fabricated items / [N] critical TBDs
- Deduplication: [N] cross-section duplicates found
- Internal consistency: [N] issues
- Readiness: ✅ Ready / ⚠️ Proceed with caution / ❌ Not ready

---

## Context Completeness

| Context | Status | Score | Issues |
|---------|--------|-------|--------|
| Business | ✅/⚠️/❌ | [N]/5 | [issues if any] |
| Product | ✅/⚠️/❌ | [N]/5 | |
| Persona | ✅/⚠️/❌/N/A | [N]/5 | |
| UX | ✅/⚠️/❌/N/A | [N]/5 | |
| Technical | ✅/⚠️/❌ | [N]/5 | |
| Compliance | ✅/⚠️/❌/N/A | [N]/5 | |

---

## Source Integrity

**Fabricated data:** [count] items
- [List with file location]

**[TBD] Markers:** [total]
- 🔴 Critical [N]: [list with stakeholder routing]
  - [TBD description] → Route to: [PM / Architect / Designer / Legal]
- 🟡 Important [N]: [list]
- 🟢 Optional [N]: [list]

**Source attribution:** ✅ Adequate / ⚠️ Some missing / ❌ Poor

---

## Critical Issues (Must Fix Before Story Creation)
1. [Issue — location in document — how to fix]
2. [Issue — location — fix]

## Warnings (Should Fix)
1. [Warning]
2. [Warning]

---

## Readiness Assessment

**Can proceed to story creation?**
- ✅ YES — Requirements complete and validated
- ⚠️ YES WITH CAUTION — Minor gaps; flag to dev team
- ❌ NO — Critical issues must be resolved first

**Missing information needed:**
- [TBD item] → Contact: [stakeholder]

---

## Recommended Next Steps
1. [Action 1]
2. [Action 2]

---

**Validation completed:** [timestamp]
```

**Save file:** `[output-folder]/Generated/Report/Validation-Report-[Feature-Name].md`

---

## 💬 Step 7: Present Report and Close

Present validation report to user:

```markdown
✅ Validation complete.

**Result: [PASS / PASS WITH WARNINGS / FAIL]**

[Key findings in 2-3 sentences]

📄 Report saved: [output-folder]/Generated/Report/Validation-Report-[Feature-Name].md

---

**All files in your output folder ([output-folder]):**
- Context-Summary-[Feature].md
- Generated/Internal/Feature-Requirements-[Feature].md
- Generated/Report/Validation-Report-[Feature].md

---

**What's next?**
- To fix issues: provide the missing information and I'll update the documents
- To create user stories: use the Story Creation workflow with these requirements as input
- To re-validate: make changes and ask me to "re-validate requirements"
```

---

---

Workflow 3 complete. Return to `SKILL.md` post-pipeline steps.
