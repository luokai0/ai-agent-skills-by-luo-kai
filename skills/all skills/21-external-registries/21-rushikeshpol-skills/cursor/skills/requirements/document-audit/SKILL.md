---
name: document-audit
description: "Scans any document for stale content, contradictions, unresolved markers, and broken cross-references. Detects [PENDING], [TBD], and [UNKNOWN] markers that are already answered elsewhere in the document or conversation. Flags contradictions between sections, orphaned references, and notes left over from earlier drafts. Use after iterative editing rounds, after incorporating meeting feedback, or as a final quality gate before sharing a document."
---

# Document Audit — Staleness & Consistency Sweep

## Purpose

Performs a systematic audit of any document to catch problems that accumulate during iterative editing — stale placeholders, contradictions between sections, orphaned references, and outdated notes.

**When to use:**
- After incorporating new information (meeting feedback, design updates, stakeholder decisions)
- After multiple rounds of editing in a single session
- As a final quality gate before sharing a document with stakeholders
- When resuming work on a document after a break

**Domain-agnostic.** Works on requirements docs, PRDs, meeting notes, specs — any structured document.

---

## Step 1: Read the full document

Read the entire document end-to-end using the Read tool. Do not skim. Build an internal model of:
- All section headings and their hierarchy
- All cross-references between sections (e.g., "see Section 5.3")
- All placeholder markers: `[PENDING]`, `[PENDING CONFIRMATION]`, `[PENDING LEGAL]`, `[TBD]`, `[TBD —`, `[UNKNOWN]`, `[TO BE CONFIRMED]`, `[OPEN]`
- All assumption references (numbered assumptions, named assumptions)
- All decision markers (confirmed, resolved, rejected, deferred)
- The document's internal timeline (version history, dates, meeting references)

---

## Step 2: Staleness Check

For every placeholder marker found, check:

| Check | What to look for | Action |
|---|---|---|
| **Answered elsewhere in the doc** | A `[PENDING]` marker in one section, but the answer exists in another section (e.g., a decision was recorded later in the doc) | Flag: "This [PENDING] in Section X is answered in Section Y — recommend removing the marker and updating the text." |
| **Answered in conversation context** | If running within a session where the user has provided additional information that resolves a `[TBD]` | Flag: "This [TBD] was resolved during our conversation — recommend updating." |
| **Outdated note from earlier draft** | Notes like "needs Legal input" when Legal has already provided input (evidenced by later sections referencing Legal's response) | Flag: "This note appears outdated — Section Z references Legal's input on this topic." |
| **Stale decision reference** | A section discusses options A/B as open, but another section records the decision | Flag: "Decision has been made (Section Y) but Section X still presents this as open." |

### Output format for each finding:

```
STALE: [Section/line reference]
   Marker: "[exact marker text]"
   Evidence: [Where the answer exists — section, line, or conversation reference]
   Recommendation: [Remove marker / Update text / Merge with existing content]
   Confidence: [HIGH — answer is explicit / MEDIUM — answer is implied / LOW — may need user confirmation]
```

---

## Step 3: Contradiction Check

Scan for statements in one section that conflict with statements in another section:

| Check | What to look for |
|---|---|
| **Scope contradictions** | Something listed in "In Scope" that is also listed in "Out of Scope" or deferred |
| **Decision contradictions** | A section saying a decision is pending while another section records the decision as made |
| **Number/threshold contradictions** | Different values for the same threshold in different sections (e.g., "3.5 hours" in one place, "4 hours" in another) |
| **Status contradictions** | An assumption marked "Confirmed" in the assumptions table but still marked `[PENDING CONFIRMATION]` in the body text |
| **Terminology inconsistency** | The same concept referred to by different names in different sections (e.g., "exception" vs. "claim" vs. "penalty request") |

### Output format:

```
CONTRADICTION: [Brief description]
   Location A: [Section — exact text]
   Location B: [Section — exact text]
   Recommendation: [Which one is correct based on context, or flag for user decision]
```

---

## Step 4: Cross-Reference Check

Verify all internal references resolve correctly:

| Check | What to look for |
|---|---|
| **Section references** | "See Section 5.3" — does Section 5.3 exist? Was it renumbered? |
| **Assumption references** | "Assumption 11" in the body — does assumption 11 exist in the assumptions table? Does it say what the body claims? |
| **Dependency references** | "Dependency 4" — does it exist in the dependencies table? |
| **Document references** | References to other documents — are the filenames/paths still correct? |

### Output format:

```
BROKEN REF: [Section — exact reference text]
   Issue: [Target doesn't exist / Target was renumbered / Content doesn't match]
   Recommendation: [Update reference to Section X / Remove reference / Verify with user]
```

---

## Step 5: Completeness Check

| Check | What to look for |
|---|---|
| **Orphaned sections** | Sections that are referenced in the table of contents or header but have no content |
| **Empty tables** | Tables with headers but no data rows |
| **Unresolved owner fields** | Action items, dependencies, or questions with no owner assigned |
| **Missing dates** | Target dates that say "TBD" for items that were discussed and given a timeline |
| **Dangling "Phase 2" items** | Items deferred to a future phase that aren't captured in an "Out of Scope" or "Future Enhancements" section |

---

## Step 6: Produce Audit Report

**Save the report first — then summarize in chat.**

### Determine output path (in order of precedence)

1. **Parent skill provided a path** (e.g., called from `/requirements-pipeline` Stage 9b with an established `[output]` folder): save inside that folder as `stage_output/Stage9b-Document-Audit.md`.

2. **No parent path — check for existing reports folder:** Look in the same directory as the audited document for a folder named `report`, `Report`, `reports`, or `Reports` (case-insensitive). If found, use it.

3. **No reports folder found:** Create a `reports/` folder in the same directory as the audited document (`mkdir -p`), then save there.

**File name:** `Audit-Report-[DocumentName].md`
(e.g., auditing `Feature-Requirements-TimeOff.md` → saves as `reports/Audit-Report-TimeOff.md`)

**In chat, present only:** File path, total finding count by category, and the top 3 highest-priority findings. Do NOT dump the full report into chat.

Report format:

```markdown
# Document Audit Report

**Document:** [filename]
**Audit date:** [date]
**Findings:** [N] total — [X] stale markers, [Y] contradictions, [Z] broken references, [W] completeness gaps

## Must Fix (HIGH confidence — clear answer exists)

[List findings with HIGH confidence that can be fixed immediately]

## Review Required (MEDIUM confidence — likely stale but needs user confirmation)

[List findings where the answer is implied but not explicit]

## Informational (LOW priority — minor consistency issues)

[List minor findings]

## Summary

[Table: Category | Count | Findings — followed by recommended fix order]

## Summary of Changes Made

[If auto-fixing was requested: list every change made with before/after]
```

---

## Step 7: Apply Fixes (if requested)

If the user asks to fix issues (or if running as part of the `requirements-pipeline`):

1. Fix all HIGH confidence findings automatically
2. Present MEDIUM findings for user confirmation before fixing
3. Leave LOW findings as-is unless user requests

**Interactive alternative:** Instead of fixing inline, the user can invoke the `review-findings` skill with the audit report from Step 6. This walks through each finding via structured questions, collects decisions, and produces a resolution summary that can be applied via `update-documents` in one pass. This is especially useful when there are many MEDIUM findings that need individual decisions.

**After fixing, re-run Steps 2-5 to verify no new issues were introduced by the fixes.**

---

## Critical Rules

1. **Read the FULL document.** Staleness is only detectable by cross-referencing the entire document. Never audit from a partial read.
2. **Never invent answers.** If a `[PENDING]` marker exists and the answer is NOT in the document or conversation, leave it as-is. Report it as "unresolved — still needs input."
3. **Cite evidence.** Every finding must reference the specific sections where the conflict or staleness exists.
4. **Be conservative on auto-fixes.** Only auto-fix when the correct answer is explicitly stated elsewhere in the document. When in doubt, flag for user review.
5. **Domain-agnostic.** This skill works on any structured document. Do not assume a specific document format.
6. **Re-audit after fixes.** Editing one section to fix a contradiction can introduce new staleness elsewhere. Always re-verify.
