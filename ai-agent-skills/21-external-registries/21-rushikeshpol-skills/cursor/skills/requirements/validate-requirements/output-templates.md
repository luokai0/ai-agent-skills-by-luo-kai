# Phase 3: Output Templates

**Called from:** `SKILL.md` (Phase 3: Generate Output)
**Produces:** Chat summary (displayed to user) + Full report file (saved to disk)

---

## Output 1: Chat Summary (displayed to user)

```
## Requirements Review — [Feature Name]

**Document:** [filename]
**Sources checked:** [N]
**Findings:** [N] total ([N] Critical, [N] Should Fix, [N] Verify, [N] Gaps)
[If incremental mode, include the following block — omit entirely in full mode:]
**Mode:** Incremental (prior report: [filename], [date])
**Changes detected:** [N] sections modified, [N] FRs changed, [N] sources unchanged
**Checks re-run:** [list of check numbers]
**Checks carried forward:** [list of check numbers] (no relevant changes detected)
**Prior findings resolved:** [N] (fixed since last report)
**Prior findings carried forward:** [N]
**New findings:** [N]

### Semantic Checks (content accuracy)

| Check | Findings | Status | Mode |
|-------|----------|--------|------|
| 1. Source Accuracy | [N] | PASS / FAIL | Re-run / Carried forward |
| 2. Inference Detection | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 3. Requirement Purity | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 4. Over-Generalization | [N] | PASS / FAIL | Re-run / Carried forward |
| 5. Scope Boundary | [N] | PASS / FAIL / SKIPPED | Re-run / Carried forward |
| 6. Testability | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 7. Ambiguity | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 8. Assumption-Req Dependency | [N] | PASS / FAIL | Re-run / Carried forward |
| 9. Negative Path Coverage | [N] | PASS / FAIL | Re-run / Carried forward |
| 10. Actor Capability | [N] | PASS / FAIL | Re-run / Carried forward |
| 11. Intra-Document Consistency | [N] | PASS / FAIL | Always re-run |

### Structural Checks (document integrity)

| Check | Findings | Status | Mode |
|-------|----------|--------|------|
| S1. Staleness | [N] | PASS / FAIL | Always re-run |
| S2. Contradictions | [N] | PASS / FAIL | Always re-run |
| S3. Cross-References | [N] | PASS / FAIL | Always re-run |
| S4. Completeness | [N] | PASS / FAIL | Always re-run |

[In full mode, omit the Mode column from both tables.]

### Top Issues
1. [Most critical finding — brief description]
2. [Second most critical finding]
3. [Third most critical finding]

**Full report saved to:** [filepath]

### Recommended Next Steps

1. **Review findings interactively** — use `review-findings` skill with this report to walk through each finding, collect your decisions, and produce a resolution summary.
2. **Or resolve manually** — work through findings by category:
   a. Resolve Verify items first (quick yes/no confirmations)
   b. Batch-approve Should Fix items
   c. Fill Gaps (add to doc or convert to Open Questions)
   d. Fix Critical items immediately
3. **Apply fixes** — use `update-documents` with the resolution summary to apply all approved changes in one pass.

Would you like to use `review-findings` to walk through these interactively?
```

---

## Output 2: Full Report File

Save as `Validation-Report-[Feature].md` in the same directory as the requirements document.

After the file is saved, if the local traceability pilot is enabled for `validate-requirements`, record the `report-saved` checkpoint before publishing the chat summary. After the chat summary is published, record `summary-published`. These trace records are hidden/operator-facing only and must not be shown in the normal chat output unless explicitly requested.

**Determine output path (in order of precedence):**

1. **Parent skill provided a path** (e.g., called from `/requirements-pipeline` with an established `[output]` folder): save inside that folder as `stage_output/Stage9-Validation-Report.md`.
2. **No parent path — check for existing reports folder:** Look in the same directory as the document for a folder named `report`, `Report`, `reports`, or `Reports` (case-insensitive). If found, use it.
3. **No reports folder found:** Create a `reports/` folder in the same directory as the document (`mkdir -p`), then save there.

```markdown
# Requirements Review

**Document:** [filename]
**Validated on:** [date]
**Sources checked:** [N] source documents
**Checks run:** 15 (11 semantic + 4 structural)
[If incremental mode, include the following block — omit entirely in full mode:]
**Mode:** Incremental (prior report: [filename], [date])
**Changes detected:** [N] sections modified, [N] FRs changed, [N] sources unchanged
**Checks re-run:** [list — these checks ran fresh because their inputs changed]
**Checks carried forward:** [list — these checks were skipped because inputs are unchanged since [prior date]]
**Prior findings resolved:** [N] (fixed since last report)
**Prior findings carried forward:** [N]
**New findings:** [N]

### Semantic Checks (content accuracy)

| Check | Findings | Status | Mode |
|-------|----------|--------|------|
| 1. Source Accuracy | [N] | PASS / FAIL | Re-run / Carried forward |
| 2. Inference Detection | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 3. Requirement Purity | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 4. Over-Generalization | [N] | PASS / FAIL | Re-run / Carried forward |
| 5. Scope Boundary | [N] | PASS / FAIL / SKIPPED | Re-run / Carried forward |
| 6. Testability | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 7. Ambiguity | [N] | PASS / FAIL | Re-run / Scoped / Carried forward |
| 8. Assumption-Req Dependency | [N] | PASS / FAIL | Re-run / Carried forward |
| 9. Negative Path Coverage | [N] | PASS / FAIL | Re-run / Carried forward |
| 10. Actor Capability | [N] | PASS / FAIL | Re-run / Carried forward |
| 11. Intra-Document Consistency | [N] | PASS / FAIL | Always re-run |

### Structural Checks (document integrity)

| Check | Findings | Status | Mode |
|-------|----------|--------|------|
| S1. Staleness | [N] | PASS / FAIL | Always re-run |
| S2. Contradictions | [N] | PASS / FAIL | Always re-run |
| S3. Cross-References | [N] | PASS / FAIL | Always re-run |
| S4. Completeness | [N] | PASS / FAIL | Always re-run |

[In full mode, omit the Mode column from both tables.]

---

[If incremental mode, include a Resolved section before the findings:]

## Resolved (fixed since prior report)

[List prior findings whose problematic text no longer exists in the document. These are not counted as current findings.]

| # | Prior Location | Prior Check | Prior Finding | Resolution |
|---|---------------|-------------|---------------|------------|
| 1 | [Section, line from prior report] | [Check #] | [Original finding description] | Text removed or rewritten |

---

## Critical (MUST FIX — factually wrong or misleading)

| # | Type | Location | Check | Finding | Source Says | Doc Claims | Recommendation |
|---|------|----------|-------|---------|-------------|------------|----------------|
| 1 | Semantic | [Section, line] | [Check #] | [Description] | [What source actually says] | [What doc claims] | [Fix] |
| 2 | Structural | [Section, line] | [Check S#] | [Description] | — | — | [Fix] |

## Should Fix (reframe, relocate, or make precise)

| # | Type | Location | Check | Finding | Recommendation |
|---|------|----------|-------|---------|----------------|
| 1 | Semantic | [Section, line] | [Check #] | [Description] | [Fix] |
| 2 | Structural | [Section, line] | [Check S#] | [Description] | [Fix] |

## Verify (needs user confirmation)

| # | Type | Location | Check | Finding | Question for User |
|---|------|----------|-------|---------|-------------------|
| 1 | Semantic | [Section, line] | [Check #] | [Description] | [What to confirm] |
| 2 | Structural | [Section, line] | [Check S#] | [Description] | [What to confirm] |

## Gaps (missing coverage)

| # | Type | Location | Check | Finding | Suggested Addition |
|---|------|----------|-------|---------|-------------------|
| 1 | Semantic | [Section, line] | [Check #] | [Description] | [What to add] |
| 2 | Structural | [Section, line] | [Check S#] | [Description] | [What to add] |

[For carried-forward findings in any severity table, append `(carried from [prior report date])` to the Finding cell so the user can distinguish new discoveries from surviving prior findings.]

## Clean (no issues found)

[List checks that passed with 0 findings and a brief note on what was verified]

---

## Recommended Next Steps

1. **Review findings interactively** — Use the `review-findings` skill with this report file to walk through each finding, collect decisions, and produce a resolution summary.
2. **Or resolve manually** — Work through findings by category: Verify items first, then Should Fix, then Gaps, then Critical.
3. **Apply fixes** — Use `update-documents` with the resolution summary (from `review-findings`) or apply changes directly.
4. **Re-run validation** — After fixes are applied, re-run `validate-requirements` to confirm findings are resolved. Provide this report as the prior report to enable incremental mode.
```
