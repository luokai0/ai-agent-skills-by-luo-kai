# Structural Checks (S1–S4) — Document Integrity

These checks scan for problems that accumulate during iterative editing — stale placeholders, contradictions between sections, orphaned references, and completeness gaps. They operate on the document alone (no source documents needed).

Run these after all semantic checks (1–11) are complete.

### Incremental Mode

> **All four structural checks (S1–S4) ALWAYS RE-RUN in both full and incremental mode.** They cannot be carried forward from a prior report. Rationale: structural checks are cheap (they operate on the document alone — no source files to read), and any edit — even a targeted fix — can introduce new stale markers, contradictions, broken references, or orphaned sections. Together with Check 11, these form the consistency safety net that makes incremental mode safe.

---

## Check S1: Staleness

For every placeholder marker in the document (`[PENDING]`, `[PENDING CONFIRMATION]`, `[PENDING LEGAL]`, `[TBD]`, `[TBD —`, `[UNKNOWN]`, `[TO BE CONFIRMED]`, `[OPEN]`), check:

| Check | What to look for | Action |
|---|---|---|
| **Answered elsewhere in the doc** | A `[PENDING]` marker in one section, but the answer exists in another section (e.g., a decision was recorded later in the doc) | Flag: "This [PENDING] in Section X is answered in Section Y — recommend removing the marker and updating the text." |
| **Answered in conversation context** | If running within a session where the user has provided additional information that resolves a `[TBD]` | Flag: "This [TBD] was resolved during our conversation — recommend updating." |
| **Outdated note from earlier draft** | Notes like "needs Legal input" when Legal has already provided input (evidenced by later sections referencing Legal's response) | Flag: "This note appears outdated — Section Z references Legal's input on this topic." |
| **Stale decision reference** | A section discusses options A/B as open, but another section records the decision | Flag: "Decision has been made (Section Y) but Section X still presents this as open." |

Also scan for: assumption status mismatches (an assumption marked "Confirmed" in the Assumptions table but still referenced as unconfirmed in the body text or FRs).

---

## Check S2: Contradictions

Scan for statements in one section that conflict with statements in another:

| Check | What to look for |
|---|---|
| **Scope contradictions** | Something listed in "In Scope" that is also listed in "Out of Scope" or deferred |
| **Decision contradictions** | A section saying a decision is pending while another section records the decision as made |
| **Number/threshold contradictions** | Different values for the same threshold in different sections (e.g., "3.5 hours" in one place, "4 hours" in another) |
| **Status contradictions** | An assumption marked "Confirmed" in the assumptions table but still marked `[PENDING CONFIRMATION]` in the body text |
| **Terminology inconsistency** | The same concept referred to by different names in different sections (e.g., "exception" vs. "claim" vs. "penalty request") |
| **FR vs. business rule conflict** | An FR states one behavior but a business rule under a different FR implies the opposite |

---

## Check S3: Cross-References

Verify all internal references resolve correctly:

| Check | What to look for |
|---|---|
| **Section references** | "See Section 5.3" — does Section 5.3 exist? Was it renumbered? |
| **Assumption references** | "Assumption H11" in the body — does H11 exist in the Assumptions table? Does it say what the body claims? |
| **Dependency references** | "Dependency D4" — does it exist in the Dependencies table? |
| **FR references** | "FR-3" in user flows or error handling — does FR-3 exist? Does it describe what the reference claims? |
| **Open Question references** | "OQ-2" — does it exist in the Open Questions table? |
| **Document references** | References to other documents — are the filenames/paths still correct? |

---

## Check S4: Completeness

| Check | What to look for |
|---|---|
| **Orphaned sections** | Sections referenced in the table of contents or headers but containing no content |
| **Empty tables** | Tables with headers but no data rows |
| **Unresolved owner fields** | Dependencies or open questions with no owner assigned |
| **Missing dates** | Target dates that say "TBD" for items that were discussed and given a timeline |
| **Dangling "Phase 2" items** | Items deferred to a future phase that aren't captured in "Out of Scope" or "Future Enhancements" |
| **Unreferenced FRs** | FRs that appear in the FR list but are never mentioned in User Flows, Visual States, or Error Handling |
| **Orphaned error handling rows** | Error handling entries that reference FRs or flows that no longer exist |
