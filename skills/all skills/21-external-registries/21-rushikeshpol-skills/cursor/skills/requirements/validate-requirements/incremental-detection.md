# Phase 0: Change Detection (Incremental Mode)

**Called from:** `SKILL.md` (Execution Workflow, Phase 0)
**Prerequisite:** `T0 Gather` and `T1 Understand` must already be `completed`.
**Next step:** Return to `SKILL.md` and proceed to Phase 1: Setup.

---

**Checklist update:** Set `T2 Analyze` to `in_progress` before starting Phase 0.

## 0.1 — Parse the prior report

Read the prior validation report. Extract:
- **Validated on** date
- **All findings** (every row from Critical, Should Fix, Verify, and Gaps tables) — capture the finding's location, check number, problematic text, and recommendation
- **Clean checks** (checks that passed with 0 findings)
- **Check summary table** (which checks were PASS / FAIL / SKIPPED)

## 0.2 — Detect document changes

Compare the current requirements document against what the prior report validated:

1. **Change History section** — read the document's Change History table. Any version entries dated after the prior report's `Validated on` date represent changes made since the last validation. Record which sections, FRs, and tables were affected.
2. **Prior finding spot-checks** — for each prior finding, check whether the problematic text (quoted in the finding) still exists at or near the reported location. This detects edits that weren't logged in Change History.
3. **Section-level diff** — walk through the document's major sections (Executive Summary, Business Context, FRs, User Flows, Visual States, Error Handling, Assumptions, Dependencies, Risks, Open Questions) and flag any section whose content differs from what the prior findings reference.

Produce a **change manifest**:

| Change | What changed | Sections affected | FRs affected |
|---|---|---|---|
| [From Change History or spot-check] | [Description] | [Section list] | [FR list or "none"] |

## 0.3 — Detect external changes

Check whether inputs outside the requirements document have changed:

| Input | How to detect | Changed? |
|---|---|---|
| **Source documents** | Compare file modification timestamps against the prior report's `Validated on` date | Yes / No |
| **Sibling requirements docs** | Same timestamp check | Yes / No |
| **Stage4 Scenario Matrix** | Same timestamp check | Yes / No |
| **Stage6 User Flows** | Same timestamp check | Yes / No |

## 0.4 — Build the check execution plan

Using the change manifest (0.2) and external change detection (0.3), classify each check. Every check has an **incremental skip condition** defined in `checks/semantic-checks.md` and `checks/structural-checks.md`. Apply those conditions:

| Decision | Meaning |
|---|---|
| **RE-RUN** | Check's inputs have changed — run it fresh |
| **RE-RUN (scoped)** | Only some inputs changed — run only on the changed FRs/sections, carry forward findings for unchanged ones |
| **CARRY FORWARD** | Check's inputs are provably unchanged — carry forward all prior findings as-is |

**Conservative rule:** If there is any doubt about whether a change affects a check, classify it as RE-RUN. The goal is to skip only checks that are *provably* unaffected.

Record the execution plan for display in the report header.

**Checklist update:** Set `T3 Plan` to `in_progress` at start of 0.4. Keep it active through 0.5 and mark `completed` when execution plan + triage buckets are finalized.

## 0.5 — Triage prior findings

For every finding in the prior report, classify it into one of three buckets:

| Bucket | Condition | Action |
|---|---|---|
| **RESOLVED** | The problematic text no longer exists in the document (the user fixed it) | Mark as resolved — exclude from the new report. Count for the report header. |
| **SURVIVING** | The problematic text still exists unchanged at or near the reported location, and the check is classified as CARRY FORWARD | Carry into the new report with a `(carried from [prior report date])` tag |
| **RE-EVALUATE** | The location exists but the text has changed, OR the check is classified as RE-RUN | Do not carry forward — the check will re-evaluate this location during its fresh run |

---

**Trace checkpoint:** After Phase 0.5 is complete, record `incremental-plan-ready` with concise metadata for checks re-run, checks carried forward, resolved findings, and surviving findings.

Phase 0 complete. Return to `SKILL.md` and proceed to Phase 1: Setup.
