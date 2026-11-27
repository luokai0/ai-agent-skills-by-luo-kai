---
name: review-findings
description: "Interactively walks users through findings from any audit or validation report (validate-requirements, document-audit, or future skills). Reads the report file, detects its format, presents findings via AskQuestion for user decisions, and produces a resolution summary. Use after any skill that generates a findings report, or standalone against any structured findings markdown file."
---

# Review Findings — Interactive Resolution Skill

## Purpose

Walks users through findings from audit/validation reports, collects decisions via structured questions, and produces a resolution summary. Works with any skill that generates a findings report — the report file is the interface.

**Key principle:** This skill does not re-run checks or read source documents. It reads ONE small report file (~100-200 lines) and presents its findings interactively. The heavy analysis was already done by the producing skill.

## When to Use

- After `validate-requirements` generates a validation report (includes both semantic and structural findings for requirements docs)
- After `document-audit` generates an audit report (for non-requirements docs)
- After any future skill that produces a structured findings file
- When the user wants to systematically work through findings rather than handle them ad-hoc
- When collecting decisions for later batch application via `update-documents`

## Inputs

1. **Report file path** — the findings report to review (REQUIRED)
2. That's it. Everything else is in the report.

---

## Phase 1: Setup

### 1.1 Read the report file

Read the full report file using the Read tool.

### 1.2 Detect format

Determine which skill produced the report by checking the heading:

| Heading | Format | Producer |
|---|---|---|
| `# Requirements Review` | validate-requirements | `validate-requirements` skill (combined semantic + structural) |
| `# Requirements Accuracy Review` | validate-requirements-legacy | `validate-requirements` skill (pre-merge format — treat same as above) |
| `# Document Audit Report` | document-audit | `document-audit` skill |
| Other | generic | Unknown — use fallback parsing |

### 1.3 Parse findings by category

**validate-requirements format — 4 categories:**

| Category | Severity | Table Columns |
|---|---|---|
| Critical | MUST FIX | #, Type, Location, Check, Finding, Source Says, Doc Claims, Recommendation |
| Should Fix | SHOULD FIX | #, Type, Location, Check, Finding, Recommendation |
| Verify | VERIFY | #, Type, Location, Check, Finding, Question for User |
| Gaps | GAP | #, Type, Location, Check, Finding, Suggested Addition |

The Type column (Semantic / Structural) distinguishes which dimension each finding comes from. Use it when presenting findings to help the user understand the nature of the issue.

Also parse the "Clean" section to know which checks passed. The summary table is split into two sub-tables: "Semantic Checks" (Checks 1–11) and "Structural Checks" (Checks S1–S4).

**document-audit format — 3 categories:**

| Category | Severity | Structure |
|---|---|---|
| Must Fix (HIGH) | MUST FIX | Text blocks: type (STALE/CONTRADICTION/BROKEN REF), marker, evidence, recommendation, confidence |
| Review Required (MEDIUM) | VERIFY | Same structure |
| Informational (LOW) | INFO | Same structure |

**Generic fallback:**
- Look for markdown headers containing severity keywords (Critical, High, Medium, Low, Must Fix, Should Fix, etc.)
- Parse any tables or structured text blocks under each header
- Present raw content if parsing fails

### 1.4 Count findings

Build a summary: total findings, count per category.

---

## Phase 2: Entry Gate (MANDATORY)

**Never start the interactive flow without asking first.**

Present the summary to the user:

```
Found [N] findings in [report filename]:
- [N] Critical / Must Fix
- [N] Should Fix
- [N] Verify / Review Required
- [N] Gaps / Informational
```

Then use AskQuestion to ask how to proceed:

```
AskQuestion:
  id: "review-mode"
  prompt: "How would you like to review the findings?"
  options:
    - id: "all"
      label: "Walk through all findings interactively"
    - id: "critical-only"
      label: "Walk through Critical / Must Fix only"
    - id: "verify-only"
      label: "Walk through Verify / Review Required only"
    - id: "bulk-approve"
      label: "Approve all recommendations — just apply them"
    - id: "skip"
      label: "Skip — I'll handle them manually"
```

**If "skip":** End the skill. No further action.

**If "bulk-approve":** Skip to Phase 4 — mark all findings as "Approved as recommended" and produce the resolution summary.

**If a specific category:** Only walk through that category in Phase 3, skip others.

**If "all":** Walk through every category in Phase 3.

---

## Phase 3: Interactive Review

Walk through findings in severity order: Critical/Must Fix first, Gaps/Informational last.

### 3.1 Critical / Must Fix Findings

Present each finding INDIVIDUALLY (too important to batch).

For each finding, use AskQuestion:

```
AskQuestion:
  id: "critical-[N]"
  prompt: "[Finding description]\n\nLocation: [section/line]\nRecommendation: [recommendation]"
  options:
    - id: "approve"
      label: "Approve fix as recommended"
    - id: "alternative"
      label: "I have a different fix (will provide details)"
    - id: "skip"
      label: "Skip — leave as-is"
```

If user selects "alternative": ask a follow-up question in chat for their preferred fix. Record their response as the resolution.

### 3.2 Should Fix Findings

Present in batches of up to 3 findings if there are many (5+). Otherwise present individually.

For each finding (or batch), use AskQuestion:

```
AskQuestion:
  id: "shouldfix-[N]"
  prompt: "[Finding description]\n\nRecommendation: [recommendation]"
  options:
    - id: "approve"
      label: "Approve"
    - id: "skip"
      label: "Skip — leave as-is"
    - id: "modify"
      label: "Modify recommendation"
```

If user selects "modify": ask for their preferred change. Record their response.

### 3.3 Verify / Review Required Findings

Present each finding INDIVIDUALLY (each needs a distinct decision).

For each finding, use AskQuestion:

```
AskQuestion:
  id: "verify-[N]"
  prompt: "[Finding description]\n\nQuestion: [question for user]"
  options:
    - id: "confirm"
      label: "Confirm — this is accurate as written"
    - id: "reject"
      label: "Reject — remove or rewrite"
    - id: "context"
      label: "Needs more context — I'll explain"
```

If "confirm": record as confirmed. The finding's text should get a `(Source: User-confirmed)` tag when fixes are applied.

If "reject": ask what should replace it, or confirm removal.

If "context": ask for the additional context, then re-present the question with the new information.

### 3.4 Gaps / Informational Findings

Present in batches of up to 3 findings if there are many.

For each finding (or batch), use AskQuestion:

```
AskQuestion:
  id: "gap-[N]"
  prompt: "[Finding description]\n\nSuggested addition: [suggestion]"
  options:
    - id: "add-requirement"
      label: "Add to requirements document"
    - id: "add-question"
      label: "Add as Open Question"
    - id: "skip"
      label: "Skip — not needed"
```

---

## Phase 4: Resolution Summary

After all findings are reviewed (or bulk-approved), produce two outputs:

### Output 1: Chat Summary

Display a brief summary in chat:

```
## Resolution Summary — [Report Name]

**Findings reviewed:** [N] of [total]
**Decisions:**
- Approved: [N]
- Confirmed: [N]
- Rejected: [N]
- Skipped: [N]
- Added as Open Question: [N]
- Modified: [N]

**Resolution file saved to:** [filepath]

### Next Step
To apply the approved fixes, use `update-documents` with the resolution file as input.
```

### Output 2: Resolution File

Save as `Resolution-[ReportName].md` in the same directory as the report file.

Format:

```markdown
# Resolution Summary

**Report:** [report filename]
**Reviewed on:** [date]
**Findings reviewed:** [N] of [total]

## Approved Fixes (ready to apply)

| # | Location | Original Finding | Decision | Action |
|---|----------|-----------------|----------|--------|
| 1 | [section/line] | [finding text] | Approved | [recommendation to apply] |

## Confirmed Items (add source tags)

| # | Location | Finding | Action |
|---|----------|---------|--------|
| 1 | [section/line] | [finding text] | Add `(Source: User-confirmed)` tag |

## Rejected Items (remove or rewrite)

| # | Location | Finding | User Direction |
|---|----------|---------|---------------|
| 1 | [section/line] | [finding text] | [what user said to do instead] |

## Added as Open Questions

| # | Finding | Open Question Text |
|---|---------|-------------------|
| 1 | [gap description] | [formatted as an OQ entry] |

## Skipped (no action)

| # | Location | Finding | Reason |
|---|----------|---------|--------|
| 1 | [section/line] | [finding text] | User chose to skip |

## Modified Recommendations

| # | Location | Original Recommendation | User's Alternative |
|---|----------|------------------------|-------------------|
| 1 | [section/line] | [original] | [user's version] |
```

---

## Integration with Other Skills

| Context | How it's called |
|---|---|
| **After `validate-requirements`** | User runs validation → combined report generated (semantic + structural findings) → next steps suggest `review-findings` → user invokes it with the report path |
| **After `document-audit`** | Same pattern for non-requirements docs — audit report generated → user invokes `review-findings` |
| **With `update-documents`** | Resolution file from Phase 4 can be used as input to `update-documents` to apply all approved fixes in one pass |
| **Standalone** | User points it at any findings report file |

---

## Critical Rules

1. **Always ask before starting.** Phase 2 Entry Gate is mandatory. Never jump into the interactive flow without the user's explicit choice.
2. **Critical findings are always individual.** Never batch Critical/Must Fix findings — each one deserves its own question.
3. **Record everything.** Every decision (including "skip") is recorded in the resolution file. Nothing is lost.
4. **Don't fix — collect decisions.** This skill collects user decisions. It does not modify the requirements document or any other file except the resolution summary.
5. **Respect the user's choice.** If they say "skip", stop. If they say "critical only", don't sneak in other categories.
6. **Resolution file is the handoff.** The resolution file is structured so `update-documents` (or a human) can apply fixes without re-reading the original report.
7. **Format-agnostic fallback.** If the report format is unrecognized, present findings as raw text with generic approve/skip options. Never fail because of an unexpected format.
