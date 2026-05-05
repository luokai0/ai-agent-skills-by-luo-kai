# Appendix — update-documents Templates and Formats

Referenced by `SKILL.md` via MANDATORY READ gates. Each section has a stable heading used as the read-gate target.

---

## Change Set Chat Summary Format

Output this in chat after writing the ChangeSet file (do not print the full table):

```
Change set written to [path].

[N] changes identified:
- Factual corrections: N
- New information: N
- Scope changes: N
- Terminology changes: N

Please open the file to review, then confirm.
```

---

## Change Set AskQuestion Gate

```
AskQuestion:
  id: "changeset-confirm"
  prompt: "Change set reviewed?"
  options:
    - id: "confirmed"
      label: "Confirmed — proceed"
    - id: "modify"
      label: "I need to adjust something"
```

Do NOT proceed until the user confirms. If "modify": ask what to change, update the file, re-summarize, re-ask.

---

## Manifest Chat Summary Format

Output this in chat after writing the Manifest file (do not print the full table):

```
Manifest written to [path].

[N] documents to update — [M] total changes:
| Document | Changes |
|---|---|
| [doc name] | N |
| [doc name] | N |

[K] POTENTIAL items require your decision — see manifest file.

Please review the manifest and confirm.
```

---

## Manifest AskQuestion Gate

```
AskQuestion:
  id: "manifest-confirm"
  prompt: "Manifest reviewed and confirmed?"
  options:
    - id: "confirmed"
      label: "Confirmed — apply all changes"
    - id: "modify"
      label: "I need to adjust something"
```

Do NOT apply edits until the user confirms. If "modify": ask what to change, update the file, re-summarize, re-ask.

---

## Manifest File Format Template

```markdown
# Change Manifest

**Date:** [YYYY-MM-DD]
**Change set:** [path to ChangeSet file]

## Document Registry Decision

| Document | Decision | Reason |
|---|---|---|
| Stage4_Scenario_Matrix | ✅ Update | Scenario MS-3 assumes old behavior |
| Stage5_Assumptions | ✅ Update | Assumption M1 status must be updated |
| Internal FR | ✅ Update | Primary location of affected FRs |
| Client FR | ✅ Update | Downstream derivative of Internal FR |
| Stage8_Risk_Analysis | ⬜ Skip | Risk profile unchanged |
...

[Documents not found in project are noted as ❌ Not found — no action.]

---

## Change Manifest

### [path] (Update order: 1 of N)

| # | Section | Category | Current text | Proposed text | Change ID |
|---|---|---|---|---|---|
| 1 | ... | DIRECT | "..." | "..." | C1 |
| 2 | ... | DERIVED | "..." | "..." | C1 |
...

### [path] (Update order: 2 of N)
...

---

## POTENTIAL Items (require user decision)

| # | Document | Section | Current text | Ambiguity | Proposed if yes |
|---|---|---|---|---|---|
| 1 | ... | ... | "..." | [why ambiguous] | "..." |

---

## Skipped Documents

| Document | Reason |
|---|---|
| ... | ... |
```

---

## Update Summary Report Template

```
## Update Summary

**Documents updated:** [N]
**Total changes applied:** [M]
**Change history entries added:** [K]

### Changes by document:
| Document | Changes applied | Audit status |
|----------|----------------|-------------|
| [path]   | [N]            | Clean / [N] findings |

### Audit findings requiring attention:
[List any HIGH or MEDIUM findings from document-audit]

### Resolved during audit:
[List any findings that were auto-fixed]
```

- HIGH findings: fix immediately and re-audit.
- MEDIUM findings: present to user for decision.
- LOW findings: report only, no action unless user requests.

---

## Discovery Subagent Prompt Template (Step 4)

```text
You are performing a read-only discovery pass on a single document as part of a cross-document change propagation.

TARGET FILE: [absolute path]

SECTIONS TO INSPECT (from section-document matrix — do not inspect sections outside this list):
- [Section name] — Change IDs: [C1, C2]
- [Section name] — Change IDs: [C2]
...

CHANGE SET (full descriptions so you can reason about derived and implied content):
| ID | What is wrong / missing | What is correct / new |
|---|---|---|
| C1 | ... | ... |
| C2 | ... | ... |

YOUR TASK — two passes:

PASS 1 — Intra-document consistency sweep (reasoning, no text search):
For each listed section, reason about whether the section is logically inconsistent with the change — even if it doesn't contain the exact incorrect text. Ask:
- Does this section describe a behavior, state, or premise the change invalidates or extends?
- If a flow is updated, does the visual states table have a matching entry?
- If a scope item is removed, does the executive summary still reference it?
- If a new dependency is introduced, does the dependencies section list it?
- If an assumption is confirmed, is it still marked as "unconfirmed" anywhere?
Output: list of consistency gaps found (section + description of the inconsistency).

PASS 2 — Text search for matches:
For each listed section, search for text matching these categories:
- DIRECT: explicitly states the incorrect information or uses the old term
- DERIVED: implies or builds upon the incorrect fact (only makes sense if the old fact is true)
- CROSS-REFERENCE: references to the affected section/fact that will become stale
- CONSISTENCY GAP: sections flagged in Pass 1 as logically inconsistent

POTENTIAL: if text might be affected but intent is ambiguous, flag it separately.

RETURN (structured):
For each finding:
| Section | Category | Current text (exact quote) | Proposed replacement | Change ID |
|---|---|---|---|---|
| ... | DIRECT/DERIVED/CROSS-REFERENCE/CONSISTENCY GAP/POTENTIAL | "..." | "..." | C1 |

Also return:
- POTENTIAL items list: section, exact quote, reason for ambiguity
- Sections inspected with no findings: list them explicitly (confirms they were checked)
- Any judgment calls or uncertainty you encountered
```

---

## Execution Subagent Prompt Template (Step 6)

```text
You are updating a single document as part of a cross-document change propagation.

TARGET FILE: [absolute path]

DOCUMENT TYPE: [e.g., "Stage 4 Scenario Matrix — internal stage artifact, bullet-style, concise"]

CHANGES TO APPLY:
[Filtered rows from the manifest for this document only]
| # | Section | Category | Current text | Proposed text | Change ID |
|---|---|---|---|---|---|
| 1 | ... | DIRECT | "..." | "..." | C1 |
...

EDITING RULES:
- Read the full document before editing
- Preserve existing format, heading hierarchy, section structure
- Match bullet style, sentence length, and voice of surrounding text
- For table edits: match column format, alignment, row style
- Place new content in the contextually correct existing section
- Do not create new sections unless structure genuinely requires it
- Remove content cleanly — no orphaned references or empty sections

CHANGE HISTORY:
- If the document has a version/changelog section: add a new row with today's date, author "[from manifest source]", and a one-line summary of what changed
- If no changelog exists: skip, do not add one

RETURN when done:
1. List of changes successfully applied (section name + one-line description)
2. List of any edits that failed (string not found or ambiguous match) — include the exact text that could not be matched
3. Any judgment calls you made that the user should review
```
