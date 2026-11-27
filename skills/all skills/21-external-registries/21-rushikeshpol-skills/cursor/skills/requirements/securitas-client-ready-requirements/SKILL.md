---
name: securitas-client-ready-requirements
description: "Transforms an internal feature requirements document into a streamlined Securitas client-ready version. Produces an 8-section (or 7-section for net-new features) document by removing redundant context sections, merging scattered constraint/risk information, and stripping internal process scaffolding. Designed for a client who already knows the context and needs a focused, review-friendly document. Use when asked to: produce a Securitas client requirements doc, streamline requirements for Lauren/Securitas review, create a focused version of a feature spec, or prepare requirements for Securitas stakeholder review."
---

# Securitas Client-Ready Requirements

Transforms an internal requirements document into a streamlined, review-friendly version for Securitas. The client already knows the business context, personas, and stakeholders. They do not need to re-read that information. They need: what are the flows, what are the requirements, what are the risks, and what is still open.

**Design principle:** 95% copy-and-relocate, 5% templated assembly. Every sentence in the output must be traceable to a specific sentence in the input. No synthesis, no paraphrasing, no inferred content.

---

## Inputs Required

| Input | Required | Notes |
|-------|----------|-------|
| Internal requirements document | Yes | Path to `Feature-Requirements-*.md` |
| Stage 1 intake file | Yes | Filename contains "Stage1" or "Intake_Classification" for SRC code mapping |

**If Stage 1 file cannot be found:** Ask the user to point to it. If unavailable, proceed and use raw filenames in the References section.

---

## Output Structure: 8-9 Sections

The output document has exactly this structure. Section 3 is conditional. The Appendix is always present.

| # | Section | Content | Transformation type |
|---|---------|---------|---------------------|
| 1 | Overview | Narrative paragraph assembled from existing text — business problem first, then capability, then priority and launch date | TEMPLATE (narrative assembly) |
| 2 | Scope | In Scope + Out of Scope tables | COPY verbatim |
| 3 | What's Changing | Current state vs new capabilities | COPY verbatim (conditional: include only if source has "Current State" content) |
| 4 | User Flows | Flows, alt paths, inline flow error rows; Visual States and Error Handling as callouts to Appendix | COPY verbatim + RELOCATE |
| 5 | Requirements | All FRs with business rules; audit trail tables replaced with Appendix callout | COPY verbatim |
| 6 | Constraints and Risks | Merged from 4+ source sections | RELOCATE (no rephrasing) |
| 7 | Open Questions | Open items only | COPY + DELETE resolved rows |
| 8 | References | Figma links, related docs, sources | COPY + RELOCATE |
| — | Appendix | Visual States (A), Error Handling (B), Audit Trail (C, if present) | COPY verbatim |

---

## Phase 1: Clean

Apply all cleaning rules FIRST, before any restructuring. Work on a mental copy of the source document.

### 1.1 Build Source Registry

Read the Stage 1 intake file. Map every SRC code to its display name, date, and type:

| SRC | Display Name | Date | Type |
|-----|-------------|------|------|
| SRC-N | [from Stage 1] | [date] | Meeting Record / Discovery Session / Client Document / Design Reference / Existing Draft |

Only register SRC codes that appear in the requirements document.

### 1.2 Apply Cleaning Rules

| Find | Replace With |
|------|-------------|
| `(Source: SRC-N)`, `(Source: SRC-N, D-N)`, any SRC citation | Remove entirely |
| `(Source: Implicit)`, `(Source: Implicit -- ...)` | Remove; convert uncertain statements to `[TBD]` |
| `(Source: User-confirmed)`, `(Source: User-confirmed, YYYY-MM-DD)` | Remove |
| Inline codes: `(Assumption H2)`, `(H1)`, `(D14)`, `(C9)`, `(M1)` | Remove the code; keep plain English if risk context matters |
| Assumptions table `#` column with `H1`, `M2`, `L4` etc. | Replace with sequential numbers: `1`, `2`, `3` |
| `Pipeline: Generated from Stages 1-N...` | Remove |
| `Audience: Product managers, developers, architects, QA engineers` | Replace with: `Audience: Business, Product, UX, Technology, Executive` |
| `Source rule: All business rules cite source IDs...` | Remove |
| `(Figma node 3244:28360)` etc. | Replace with `(current app design)` |
| Stage artifact references: `Context-Summary-FigJam-SRC18`, `Stage 1`, `Stage 4`, stage filenames | Remove the reference; keep the fact |
| Assumptions status `Contradicted` | Replace with `Open Risk` |
| Dependencies `BLOCKER -- data not available` | Replace with `Required before development, resolution in progress` |
| `> **Engineering Note:** [text]` block inside any FR | Remove entirely. If the note contains a fact the client must know to understand the requirement, convert it to a business rule bullet before removing. |
| `> **Direction ([Name]):** [text]` block inside any FR | Remove. The directional decision must already be reflected in the requirement text; if not, add it as a business rule bullet before removing the block. |
| `[Display layout, Design Decision]`, `[Design Decision]`, `[TBD - Design]` annotation tags inline in business rules | Remove the tag. Keep the business rule fact unchanged. |
| Business rule bullet identical or near-identical to a Hard Constraint already listed in Section 5 | Remove the FR-level bullet. The constraint is stated once in Section 5. Applies universally to payroll non-blocking and any other document-wide rules. |

### 1.3 Collect SRC codes for References

Record every unique SRC code found in the document before removing them. This list drives the References section in Phase 2.

---

## Phase 1.5: Deduplicate

Before restructuring, classify every item that will land in Constraints and Risks (Section 6) or Open Questions (Section 7). Each item gets exactly one home based on what it **is**:

| Classification | Definition | It is NOT also... |
|---|---|---|
| **Hard Constraint** | Non-negotiable system rule (regulatory, legal, timeline) | a dependency or limitation |
| **Dependency** | Deliverable another team must provide before we can build | an assumption or limitation |
| **Assumption** | Something we believe but haven't confirmed; carries risk if wrong | a dependency (if it has an owner and delivery status, it's a dependency) |
| **Known Limitation** | Confirmed gap we are shipping with (accepted trade-off) | a dependency (if it's blocking and has an owner, it's a dependency) |
| **Open Question** | Stakeholder decision needed before proceeding | an assumption or dependency (if it needs a decision, the OQ owns it) |

### Deduplication Rules

1. **If an item appears as both an Assumption and a Dependency:** Keep the Dependency row (it has owner + status). Delete the Assumption row.
2. **If an item appears as both a Known Limitation and a Dependency:** Keep the Dependency row. Delete the Known Limitation bullet.
3. **If an item appears as both a Constraint and a Dependency:** Keep the Constraint only if there is a non-negotiable rule to state (e.g., "payroll must never be blocked"). If the constraint bullet is just restating the dependency, delete it.
4. **If an item appears as both an Assumption and an Open Question:** Keep the Open Question. Delete the Assumption row. The OQ is the primary artifact for items needing decisions.
5. **If an item appears as both a Dependency and an Open Question:** Keep both ONLY IF the OQ asks a different question than "will this be delivered?" If the OQ is just "can X team provide Y?", keep the dependency row and delete the OQ. If the OQ asks a design/policy question dependent on the deliverable, keep both.
6. **If two OQs ask the same question at different scopes** (e.g., "who gets escalation?" and "is escalation multi-tiered?"): Merge into one OQ. Absorb the sub-question into the primary question text.
7. **If two Constraint bullets state the same rule in different words:** Keep one. Prefer the version with more specificity.
8. **Confirmed assumptions are not assumptions.** If status is "Confirmed," delete. If the confirmed fact creates a trade-off, move it to Known Limitations.
9. **When deleting a duplicate, check if the removed instance has useful context** (e.g., risk consequence, impact description) that should be absorbed into the surviving instance's description or "Impact if wrong" column.
10. **Update all cross-references** after deduplication. If Assumption #3 becomes #2, update any FR business rules that reference "Assumption #3."

---

## Phase 2: Restructure

Build the output document section by section. For each section, the instruction specifies the transformation type. Follow it exactly.

### Section 1: Overview

**Transformation type: NARRATIVE ASSEMBLY**

This is the ONLY section where text is assembled (not copied verbatim). Write a short narrative paragraph by extracting and connecting specific phrases from the source. Do not write new prose — every clause must be traceable to the source.

```
# [Feature Name]

**Version:** [from source header]
**Date:** [today's date]
**Owner:** [from source header]
**Status:** [from source header]

> **Audience:** Business, Product, UX, Technology, Executive

[Sentence 1: the business problem or compliance driver — extracted from Business Goals or Executive Summary. State the cost of not having this feature, or the legal/operational obligation. Do NOT open with the feature name.]

[Sentence 2: what the feature delivers, stated in terms of officer/DM outcomes — extracted from Exec Summary. Name the primary actors and the core capabilities they gain.]

[Sentence 3: priority order (if source defines one) + launch date — copied from source priority line and timeline constraint.]
```

**Sequence rules — enforce in this order:**
1. **Open with the problem.** Sentence 1 must state what is broken today or what compliance obligation exists — not what the feature does. Extract from Business Goals or the "Current State" section.
2. **State outcomes, not capabilities.** Sentence 2 names what officers/DMs gain, not what the system does. Extract from Exec Summary.
3. **Close with priorities and date.** Sentence 3 states the priority order and launch date. Copy from source — do not invent.

**Content checks (apply before writing):**
- Can you point to a specific source sentence for every clause? If not, do not include that clause.
- Does Sentence 1 contain the feature name as its subject? If yes, rewrite — the problem must lead, not the feature.
- Does Sentence 2 describe a system capability ("the system checks...") rather than an officer/DM outcome? If yes, rewrite in terms of what the user gains.
- Is the priority order present in Sentence 3 only if the source defines one? If source has no priority ranking, omit it.

**Other rules:**
- No label prefixes (`For:`, `Why:`, `What:`). Plain prose only.
- Maximum 3 sentences. Scope boundary is NOT in the overview — it is fully covered by Section 2.
- If the source Exec Summary mentions a Measurement/Mixpanel event, add one line after the paragraph: `**Measurement:** [event name or metric]`. If none mentioned, omit entirely.
- Do NOT include Business Goals bullets, Success Metrics table, or Stakeholders table.

---

### Section 2: Scope

**Transformation type: COPY verbatim**

```
---

## 2. Scope

### In Scope

[Copy In Scope table from source -- identical rows, identical columns]

### Out of Scope

[Copy Out of Scope table from source -- identical rows, identical columns]
```

**Rules:**
- Tables copied exactly as they appear in the cleaned source
- Do not add, remove, or rephrase any rows

---

### Section 3: What's Changing (CONDITIONAL)

**Transformation type: COPY verbatim**

**Include this section ONLY IF** the source document contains a "Current State" subsection, a "What's changing" subsection, or equivalent content describing what exists today vs. what is new.

```
---

## 3. What's Changing

### Current State
[Copy the "Current State" or "Existing capabilities" content from source as bullet list]

### What's New
[Copy the "What's changing" or "What's new" content from source as bullet list]
```

**Rules:**
- If source has paragraph prose instead of bullets, convert to bullets by extracting one fact per bullet. Do not combine multiple facts into one bullet.
- Do not rephrase. Each bullet must be a verbatim extraction.
- **For net-new features with no "Current State" content:** Omit this section entirely. All subsequent sections shift up by one number.

---

### Section 4: User Flows

**Transformation type: COPY verbatim + RELOCATE**

```
---

## 4. User Flows

**Design reference:** [Figma link(s) from source Design Assets subsection]

[Copy ALL user flow content from source UX Context section:]
- Happy path flows (numbered steps, verbatim)
- Alternative paths tables (verbatim)
- Error handling tables that are embedded within flows (verbatim)
- Flow-specific design constraint callouts (verbatim)

### Visual States

> See [Appendix A: Visual States](#appendix-a-visual-states) for the complete state table. Key states: [list 4-6 key state names, verbatim from source table].

### Error Handling

> See [Appendix B: Error Handling](#appendix-b-error-handling) for the complete error table.
```

**Rules:**
- All flow steps, alternative path tables, and inline error handling rows embedded within individual flows are copied word-for-word
- Visual States and Error Handling tables move to the Appendix (see Appendix rules below). In their place, add a one-line summary callout with the key state names so reviewers know what states exist without reading the full table
- Design constraint callouts (e.g., "Timesheets use a non-standard Thu-Fri week boundary...") are kept in the flow where they appear
- Inline error notes within Alternative Paths rows (e.g., "See Error Handling table") are kept verbatim

---

### Section 5: Requirements

**Transformation type: COPY verbatim**

```
---

## 5. Requirements

[Copy FR content from source Functional Requirements section:]
- Cross-cutting display rules (e.g., overnight shifts) precede the FR list
- Each FR: heading, description, business rules (all bullets), engineering notes
- FR-level dependency callouts

[Strip from each FR:]
- Inputs subsection (e.g., "Officer identity (from session)") — engineering-level detail
- Outputs subsection (e.g., "Confirmation with request ID") — engineering-level detail
- Validation subsection (e.g., "Dates: valid calendar dates") — engineering-level detail
- Performance subsection — fold into an Implementation Note if the fact matters
- Source line (e.g., "Source: SRC-1, SRC-4") — already removed by Phase 1 cleaning

Keep: Description, Business Rules, Implementation Notes.

[For any FR that contains an Audit Trail table:]
- Keep the business rule bullet that states where audit data is stored (e.g., "All audit trail events are stored in BI/Snowflake")
- Replace the full audit trail table with: > See [Appendix C: Audit Trail Lifecycle](#appendix-c-audit-trail-lifecycle) for the complete event table.
```

**Rules:**
- **ZERO changes to requirement content.** Every FR description, business rule bullet, and engineering note must be word-for-word identical to the cleaned source.
- Cross-cutting rules that precede FRs in the source stay in the same position
- Descoped FRs (struck-through in source) are included as-is for decision trail
- Engineering Notes (`> **Engineering Note:**` blocks) are stripped from all FRs in the client version. Convert any client-relevant fact to a business rule bullet before stripping.
- Cross-FR constraint deduplication: remove business rule bullets that restate a Hard Constraint already defined in Section 5. Do not repeat document-wide rules (e.g., payroll non-blocking) in individual FRs.
- **Renumber FRs sequentially** (FR-1, FR-2, FR-3, ...) if the source has gaps from a feature split. Gaps confuse client readers. Update ALL cross-references (Regional Applicability, business rule bullets, risk mitigations) to use the new numbers. Internal-to-client FR mapping is implicit; no mapping table needed.
- Audit trail tables move to Appendix C. The inline callout bullet referencing the table destination is kept in the FR where the table originally appeared.

---

### Section 6: Constraints and Risks

**Transformation type: RELOCATE (no rephrasing)**

This section consolidates content from up to 4 source sections. Each bullet/row is copied verbatim from its source location and placed into the correct subsection below. No merging of bullets, no summarizing, no rephrasing.

```
---

## 6. Constraints and Risks

### Hard Constraints
[Collect from: source "Constraints" subsection + source "Compliance & Constraints" section]
- [bullet copied verbatim from source]
- [bullet copied verbatim from source]

### Blockers and Dependencies
[Collect from: source "Dependencies" table + any FR-level dependency callouts]

| Dependency | Owner | Status | Risk |
|---|---|---|---|
[rows copied verbatim from source Dependencies table]

### Assumptions
[Collect from: source "Assumptions" table. Include unconfirmed/open items only. Omit resolved assumptions.]

| # | Assumption | Status | Impact if wrong |
|---|---|---|---|
[rows copied from source. Renumber sequentially. Add "Impact if wrong" by copying the "Dependent FRs" column if present, or leave blank.]

### Known Limitations
[Collect from: source "Known Limitations" section + source "Known Issues" table if present]
- [bullet copied verbatim from source]
- [bullet copied verbatim from source]

[If source has a Known Issues table, copy it here under a "Known Issues" subheading]
```

**Rules:**
- Every bullet and table row must be traceable to a specific bullet or row in the source
- Do not combine two source bullets into one output bullet
- Do not split one source bullet into two
- Remove struck-through items (already resolved)
- Remove struck-through rows from dependencies table
- If a constraint bullet duplicates a Known Limitation bullet (same fact stated in both source sections), include it once in the most specific subsection (prefer Known Limitations over Hard Constraints for operational items)

---

### Section 7: Open Questions

**Transformation type: COPY + DELETE resolved rows**

```
---

## 7. Open Questions

| # | Question | Priority | Stakeholder | Target Date |
|---|----------|----------|-------------|-------------|
[Copy open (non-struck-through) rows from source Open Questions table]
```

**Rules:**
- Remove all struck-through (resolved) rows entirely
- Remove internal codes from question text (e.g., `(H2, C9)`) but keep the plain English question
- Keep columns: #, Question, Priority, Stakeholder, Target Date
- Preserve original question numbering (do not renumber; gaps from removed rows are fine)
- If the source has a "Resolution" or "Comments" column, drop it from the client version

---

### Section 8: References

**Transformation type: COPY + RELOCATE**

```
---

## 8. References

### Design Assets
- [Figma link(s) from source, with display text]

### Related Documents
[Copy any non-internal document rows from source Related Documents table]

### Source Materials
The following inputs were used to develop this requirements document.
- [Display Name] ([Type], [Date])
- [Display Name] ([Type], [Date])
```

**Rules:**
- Figma links from the source "Design Assets" subsection go here
- Related Documents: keep only rows with external links (Figma, etc.). Remove rows referencing internal `.md` file paths.
- Source Materials: use the SRC registry built in Phase 1. Group by type (Meeting Records, Discovery Sessions, Client Documents, Design References, Existing Drafts). Format: `[Display Name] ([Type], [Date])`. Omit any group with no entries.
- Do not include internal stage artifact files (Stage 1-8)

---

### Appendix (Always Present)

**Transformation type: COPY verbatim + RELOCATE**

The Appendix is always the last section. Add it after References. It contains tables that are supporting detail for reviewers who need them, but are not required to review or approve the main requirements.

```
---

## Appendix

> These sections contain supporting detail. They are not required to review or approve the requirements above. Move to a sub-page as needed.

---

### Appendix A: Visual States

[Copy the full Visual States table from the source UX Context section, verbatim]

---

### Appendix B: Error Handling

[Copy the full Error Handling table from source, verbatim. If the source has multiple separate error tables (e.g., one per flow), combine them under this single heading.]

---

### Appendix C: Audit Trail Lifecycle

[Only include this appendix if the source document contains an Audit Trail table or audit event lifecycle table.]

[Copy the full Audit Trail / audit event lifecycle table from the source, verbatim, including any notes below the table]
```

**Rules:**
- Always include Appendix A (Visual States) and Appendix B (Error Handling)
- Only include Appendix C (Audit Trail) if the source has an audit trail table
- Each table is copied verbatim from source. No modifications, no additions.
- If the source has a "Known Issues" table inside Constraints, it stays in Section 6 (Constraints and Risks) under Known Limitations, not in the Appendix

---

## Phase 3: Verify

Before saving, run every check below. Fix failures before saving.

### Quality Dimensions (apply to every section)

Each section must pass all four:

- [ ] **Accuracy:** Content matches source. No additions, no misattributions, no distortions.
- [ ] **Clarity:** A reader unfamiliar with the internal doc understands without ambiguity.
- [ ] **Completeness:** Full scope of the source material for that section is represented. Nothing significant omitted. If the source covers two regions, both appear. If the source lists 7 business rules, all 7 are present.
- [ ] **Format:** Section adheres to its transformation type (COPY, RELOCATE, or NARRATIVE ASSEMBLY) and structural rules defined in Phase 2.

### Content Integrity Checks

- [ ] **FR diff:** Every FR heading and every business rule bullet in the output exists word-for-word in the cleaned source. Zero additions, zero omissions, zero rephrasings.
- [ ] **Scope diff:** In Scope and Out of Scope tables are identical to source.
- [ ] **Visual States diff:** Visual States table is identical to source.
- [ ] **User Flow diff:** Every numbered flow step and every alternative path row is identical to source.
- [ ] **Open Questions count:** Number of open rows in output <= number in source (merges may reduce count).
- [ ] **Constraints count:** After deduplication, every source fact is represented exactly once across Hard Constraints, Dependencies, Assumptions, Known Limitations, or Open Questions.
- [ ] **Dependencies count:** Number of dependency rows in output matches source (minus struck-through rows, minus items reclassified as OQs).

### Cleanup Checks

- [ ] Zero remaining `SRC-N` codes anywhere
- [ ] Zero remaining `(Source: Implicit)` or `(Source: User-confirmed)` markers
- [ ] Zero remaining internal stage file references in body text
- [ ] Zero struck-through text anywhere in the document (except descoped FRs in Section 5)
- [ ] Zero remaining `(Assumption H2)` or similar internal codes
- [ ] No Change History section exists
- [ ] No standalone Success Metrics table exists
- [ ] No Stakeholders table exists
- [ ] No Personas/User Context section exists
- [ ] No Business Context section exists
- [ ] No standalone UX Context section exists (flows are in Section 4; Visual States and Error Handling are in Appendix)
- [ ] No standalone Sources section exists (collapsed into References)

### FR Verbosity Checks

- [ ] Zero Engineering Note blocks (`> **Engineering Note:**`) in Section 5 FRs
- [ ] Zero stakeholder direction blocks (`> **Direction (Name):**`) in Section 5 FRs
- [ ] Zero inline annotation tags (`[Display layout, ...]`, `[Design Decision]`) in FR business rules
- [ ] Zero FR business rule bullets that duplicate a Hard Constraint from Section 5 (e.g., "Payroll NOT blocked" must not appear inside individual FRs)
- [ ] Zero intra-FR duplicate bullets (same fact stated twice within one FR in different words)

### Deduplication Checks

- [ ] **Zero items appear in more than one subsection** of Constraints and Risks. Scan every Hard Constraint bullet, every Dependency row, every Assumption row, and every Known Limitation bullet. If the same fact appears in two places, delete the less specific instance.
- [ ] **Zero items appear in both Constraints and Risks AND Open Questions.** If an item is an open question (needs a stakeholder decision), it must not also be an assumption or dependency row restating the same uncertainty.
- [ ] **All cross-references are current.** If assumption or OQ numbers changed due to deduplication or merges, update all references in FR business rules, Known Limitations, and notes.

### Structure Checks

- [ ] Document has exactly 8 numbered sections (net-new feature) or 9 numbered sections (enhancing existing feature with "What's Changing"), plus Appendix
- [ ] Section numbering is sequential and correct
- [ ] `Audience:` field in header is set to `Business, Product, UX, Technology, Executive`
- [ ] Overview opens with the business problem or compliance driver — not the feature name
- [ ] Overview Sentence 2 states officer/DM outcomes — not system capabilities
- [ ] Overview contains no label prefixes (`For:`, `Why:`, `What:`)
- [ ] Overview is 3 sentences maximum
- [ ] Scope boundary is NOT mentioned in the overview (it belongs in Section 2 only)
- [ ] Every clause in the overview is traceable to a specific sentence in the source
- [ ] Visual States table is in Appendix A (not in Section 4 body)
- [ ] Error Handling table is in Appendix B (not in Section 4 body)
- [ ] Audit Trail table (if present) is in Appendix C (not in Section 5 body)
- [ ] Section 4 has a `### Visual States` callout pointing to Appendix A
- [ ] Section 4 has a `### Error Handling` callout pointing to Appendix B

---

## Step: Determine Output Folder

The pipeline defines that client-ready documents live in a `client-ready/` folder parallel to `Internal/`. This skill is responsible for checking and creating that folder.

1. Let `input_dir` = the directory containing the input document.
2. If `basename(input_dir)` is `Internal`:
   - Set `output_dir` = `input_dir/../client-ready/` (sibling of `Internal`).
3. Otherwise:
   - Set `output_dir` = `input_dir/client-ready/`.
4. If `output_dir` does not exist, create it (`mkdir -p`).

## Step: Save and Report

Save the transformed document as:
```
[output_dir]/Securitas-Client-Requirements-[Feature].md
```

Report the transformation summary:
```
Securitas client-ready document saved: Securitas-Client-Requirements-[Feature].md

Structure: [N] sections (down from [M] in source)
Lines: [N] (down from [M] in source)

Sections:
1. Overview (narrative paragraph: problem → outcomes → priorities + launch date)
2. Scope (copied verbatim)
3. What's Changing (copied verbatim) [or "Omitted -- net-new feature"]
4. User Flows (copied + relocated; Visual States and Error Handling → Appendix)
5. Requirements (copied verbatim -- [N] FRs; Audit Trail → Appendix C)
6. Constraints and Risks (relocated from [N] source sections)
7. Open Questions ([N] open items, [M] resolved items removed)
8. References ([N] source materials)
Appendix A: Visual States ([N] rows)
Appendix B: Error Handling ([N] rows)
[Appendix C: Audit Trail ([N] events) -- if present]

Verification:
- FR content: identical to source
- Open questions: [N] open / [M] resolved removed
- Constraints: [N] items consolidated from [M] source sections
- Cleaning: [N] SRC codes removed, [N] internal markers removed
```

---

## Critical Rules

1. **Never change requirement content.** FR headings, descriptions, business rules, and engineering notes must be word-for-word identical to the cleaned source. This is non-negotiable.
2. **Never remove [TBD] items.** These are still open and the client needs to see them.
3. **Never synthesize or paraphrase.** Every sentence in the output (except the Overview) must exist verbatim in the source. If you cannot point to the source sentence, do not write it.
4. **Overview: problem first, outcomes second, priorities third.** The Overview paragraph opens with the business problem or compliance driver, states officer/DM outcomes in Sentence 2, and closes with priorities and launch date in Sentence 3. No label prefixes. No scope boundary (Section 2 covers it). Maximum 3 sentences. Every clause must be traceable to the source.
5. **Relocate, do not merge.** When consolidating constraints/risks from multiple sections, copy each bullet individually. Do not combine two bullets into one.
6. **Keep "What's Changing" when the feature modifies an existing screen.** This section is valuable to the client and is explicitly requested.
7. **No Change History** in client documents. This is internal revision tracking.
8. **No Success Metrics** unless a specific Mixpanel event or metric is identified in the source.
9. **No Stakeholders table.** The client knows who the stakeholders are.
10. **No Personas, User Context, or Business Context section.** These sections are removed entirely. The Overview narrative paragraph orients new readers in 3 sentences: problem, outcomes, priorities + date.
11. **Visual States and Error Handling go in the Appendix**, not in the main body. Add a one-line callout in Section 4 pointing to Appendix A and Appendix B. This keeps the flows section readable while preserving the detail for those who need it.
12. **Preserve descoped items** (struck-through FRs) for decision trail. Only remove struck-through items from Open Questions, Assumptions, and Dependencies.
13. **No em dashes.** Replace with a comma, colon, or rewrite. Exception: em dashes inside quoted notification text (that is requirement content) are preserved exactly.
14. **One pass.** Apply all transformations before saving. Do not create intermediate versions.
