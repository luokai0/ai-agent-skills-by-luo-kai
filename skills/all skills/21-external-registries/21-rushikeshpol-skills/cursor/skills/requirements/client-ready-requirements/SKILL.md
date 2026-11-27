---
name: client-ready-requirements
description: "Transforms an internal feature requirements document into a client-ready version suitable for all stakeholder types — business, product, UX, technology, and executive — in a single shared document. Strips internal source citations (SRC codes), process metadata, pipeline stage references, and internal assumption codes. Reframes blocker/risk language, cleans change history, and adds a formatted Sources & Reference Materials section. Use when asked to: produce a client-ready requirements doc, prepare requirements for stakeholder review, create a clean version of a feature spec, strip internal references from a requirements document, or share requirements with a client."
---

# Client-Ready Requirements

Transforms an internal requirements document (output of the requirements pipeline) into a client-safe version. Removes internal process scaffolding without touching any functional content. The requirement statements themselves are never changed.

---

## Inputs Required

| Input | Required | Notes |
|-------|----------|-------|
| Internal requirements document | Yes | User-provided path, or scan workspace for `Feature-Requirements-*.md` |
| Stage 1 intake file | Yes | Filename contains "Stage1" or "Intake_Classification" — maps SRC codes to real document names |

**If Stage 1 file cannot be found:** Ask the user to point to it. If unavailable, proceed and use raw filenames in the Sources section rather than display names.

---

## Step 1: Read Both Files

Read the requirements document and the Stage 1 intake file in full.

From Stage 1, build a **source registry** — every SRC code mapped to its display name, date, and type:

| SRC | Display Name | Date | Type |
|-----|-------------|------|------|
| SRC-N | [Readable title from Stage 1] | [Month Year] | [see types below] |

**Type classification:**
- **Meeting Record** — team meeting summaries, product working sessions, TL syncs
- **Discovery Session** — discovery readouts, deep dive sessions, client calls
- **Client Document** — client-provided requirement docs, written client communications
- **Design Reference** — Figma designs, FigJam boards, design descriptions
- **Existing Draft** — prior requirement drafts used as baseline input

Only register SRC codes that actually appear in the requirements document. Discard the rest.

---

## Step 2: Collect All SRC Codes Referenced

Before transforming, scan the document and record every unique SRC code cited anywhere. This is your working list for the Sources section in Step 5.

---

## Step 3: Transform the Document

Work section by section and apply every rule below. Never change requirement content — only strip or reframe metadata.

### Transformation Rules

| Find | Replace With | Reason |
|------|-------------|--------|
| `(Source: SRC-N)`, `(Source: SRC-N, D-N)`, `(Source: SRC-N, SRC-M, ...)` | Remove entirely | Internal traceability codes — meaningless to clients |
| `(Source: Implicit)`, `(Source: Implicit — ...)` | Remove; if the statement is uncertain, convert to `[TBD]` | "Implicit" signals an unconfirmed inference — undermines confidence |
| `(Source: User-confirmed)` | Remove | Plain assertions need no citation |
| Inline codes in body text: `(Assumption H2 — blocker)`, `(H1)`, `(D14)`, `(C9)`, `(M1)` etc. | Remove the code; if risk context matters, retain as plain English | Opaque to all client stakeholders |
| Assumptions table — `#` column contains risk-tier codes (`H1`, `H2`, `M1`, `L4`, etc.) | Replace with plain sequential numbers (`1`, `2`, `3`, `4`) | Risk-tier prefixes (H/M/L) are internal pipeline classification; meaningless to clients |
| Header line: `Pipeline: Generated from Stages 1–N...` | Remove | Internal process metadata |
| Header line: `Audience: Product managers, developers, architects, QA engineers` | Replace with: `Audience: Business, Product, UX, Technology, Executive` | Correct the audience |
| Header line: `Source rule: All business rules cite source IDs...` | Remove | Internal methodology note |
| Figma node IDs inline: `(Figma node 3244:28360)` | Replace with `(current app design)` | Node IDs are internal |
| Stage artifact references inline: `Context-Summary-FigJam-SRC18`, `Stage 1`, `Stage 4`, stage filenames in body text | Remove; keep the fact, drop the internal reference | Stage outputs are not client-visible |
| Struck-through resolved items in Open Questions table: `~~row~~` | Remove entire row | Resolved; no longer open |
| Assumptions table — status `Contradicted` | Replace with `Open Risk` | "Contradicted" is an internal pipeline state |
| Dependencies table — `BLOCKER — data not available` | Replace with `Required before development — resolution in progress` | "Blocker" is alarming without context |
| FR subsections: Inputs, Outputs, Validation, Performance, Source | Strip entirely. If a Performance fact matters, fold into an Implementation Note. | Engineering-level detail; client needs Description + Business Rules + Implementation Notes only |
| FR numbering gaps (e.g., FR-1, FR-2, FR-3, FR-5, FR-8) | Renumber FRs sequentially (FR-1 through FR-N). Update ALL cross-references in the document. | Gaps from feature splits confuse client readers |
| Implementation/engineering notes inside requirement body (e.g. "Local caching is one approach...") | Wrap in `> **Engineering Note:** [text]` callout | Business/exec skip callouts; tech reads them |
| Change History rows — validation finding IDs (SF-N, V-N), validation report references, "Pipeline (Rushi Pol)" | Strip to: Version \| Date \| Author name \| Plain-English change summary | Internal audit trail |
| Related Documents section — Stage 1–8 pipeline artifact rows | Remove these rows entirely | Internal stage files are not shared |
| Related Documents section — sister feature documents referenced by internal file path | Remove these rows; a client cannot open an internal `.md` path. Only list a sister feature if a client-ready version of that document exists and has an accessible link. | Internal drafts are not client-accessible |
| `> **Engineering Note:** [text]` block inside any FR | Remove entirely. If the note contains a fact the client must know to understand the requirement, convert it to a business rule bullet before removing. | Engineering-level detail; not appropriate for client audience |
| `> **Direction ([Name]):** [text]` attribution block inside any FR | Remove. Ensure the directional decision is already reflected in the requirement text before removing. | Internal stakeholder attribution; not for client documents |
| `[Display layout, Design Decision]`, `[Design Decision]`, `[TBD - Design]` inline tags in business rules | Remove the tag; keep the business rule fact unchanged. | Internal annotation; meaningless to client readers |

---

## Step 4: Clean Open Questions Table

For each row in the Open Questions table:
- Remove internal codes from the question text (e.g. remove `(H2, C9)` but keep the plain English question)
- Keep columns: #, Question, Priority, Stakeholder, Target Date
- Stakeholder names like "Pat MacArthur (WFM)" or "Lauren / UX" are fine — these are real people clients recognize

---

## Step 5: Build Sources Section

At the end of the document, after all other sections, add:

```markdown
---

## Sources & Reference Materials

The following inputs were used to develop this requirements document.

### Meeting Records
- [Display Name] (Meeting Record, [Day Month Year])

### Discovery Sessions
- [Display Name] (Discovery Session, [Day Month Year])

### Client Documents
- [Display Name] (Client Document, [Day Month Year if known])

### Design References
- [Display Name] (Design Reference, [Day Month Year if known])

```

**Section order:** Meeting Records → Discovery Sessions → Client Documents → Design References → Related Feature Documents

**Omit any section that has no entries.**

**Design references (Figma links) belong in Related Documents (§11), not in Sources.** They are active references for implementers, not just research inputs. Do not list Figma links in the Sources section.

**Formatting rules per entry:**
- Full info available → `[Display Name] (Type, Day Month Year)` e.g., `(Meeting Record, January 7, 2026)`
- Date not available → `[Display Name] (Type)`
- Type not determinable → `[Display Name] (Day Month Year)`
- Use the exact date from the Stage 1 `Date` column — do not round to month/year if a full date is present
- Never use raw filenames if a display name is available from Stage 1
- Never include internal stage artifact files (Stage 1–8 pipeline outputs) here

---

## Step 6: Quality Check

Before saving, verify each section against all four quality dimensions:

- [ ] **Accuracy:** Content matches source. No additions, no misattributions, no distortions.
- [ ] **Clarity:** A reader unfamiliar with the internal doc understands without ambiguity.
- [ ] **Completeness:** Full scope of the source material for that section is represented. Nothing significant omitted.
- [ ] **Format:** Section adheres to the transformation rules and structural conventions.

Then verify cleanup:

- [ ] Zero remaining `SRC-N` codes anywhere in the document
- [ ] Zero remaining `(Source: Implicit)` markers
- [ ] Zero remaining internal stage file references in body text
- [ ] Zero struck-through text
- [ ] Zero Engineering Notes (`> **Engineering Note:**`) in FR sections
- [ ] Zero stakeholder direction attribution blocks (`> **Direction (Name):**`) in FR sections
- [ ] Zero inline annotation tags (`[Display layout, ...]`, `[Design Decision]`) in business rules
- [ ] `Audience:` field in header updated to client stakeholder types
- [ ] Sources section present at end of document
- [ ] Change history rows contain only: version, date, author, plain summary
- [ ] Related Documents retains only external links and sister features

Fix any failures before saving.

---

## Step 7: Determine Output Folder

The pipeline defines that client-ready documents live in a `client-ready/` folder parallel to `Internal/`. This skill is responsible for checking and creating that folder.

1. Let `input_dir` = the directory containing the input document.
2. If `basename(input_dir)` is `Internal`:
   - Set `output_dir` = `input_dir/../client-ready/` (sibling of `Internal`).
3. Otherwise:
   - Set `output_dir` = `input_dir/client-ready/`.
4. If `output_dir` does not exist, create it (`mkdir -p`).

## Step 8: Save and Report

Save the transformed document as:
```
[output_dir]/Client-Requirements-[Feature].md
```

Report the transformation summary:
```
✅ Client-ready document saved: Client-Requirements-[Feature].md

Transformations applied:
- Removed N source citations (SRC codes)
- Removed N "Implicit" source markers
- Removed N inline assumption/constraint codes
- Reframed N risk/blocker items
- Cleaned change history to N entries
- Sources section: N documents across N categories
```

---

## Critical Rules

1. **Never change requirement content.** Strip citations and codes only. Requirement statements must be word-for-word identical to the source.
2. **Never remove [TBD] items.** These are still open — clients need to see them.
3. **Never fabricate display names.** If a SRC code has no Stage 1 entry, use the filename as-is.
4. **Keep document structure.** Same section numbers and headings as the input. Do not reorganize.
5. **One pass.** Apply all transformations before saving. Do not create intermediate versions.
6. **No em dashes.** Do not use "—" anywhere in the output. Replace with a comma, colon, or rewrite the sentence. Exception: if the source document contains an em dash inside a quoted string (e.g., notification text like "Your schedule was updated — check now"), preserve it exactly as written since that is requirement content.
