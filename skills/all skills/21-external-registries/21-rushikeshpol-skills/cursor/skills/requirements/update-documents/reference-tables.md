# Reference Tables — update-documents

Referenced by `SKILL.md` via MANDATORY READ gates. Each section has a stable heading used as the read-gate target.

---

## Change Set Structure

### Field table

| Field | Description |
|-------|-------------|
| **ID** | Sequential identifier (C1, C2, ...) |
| **Type** | One of: Factual correction, Terminology change, Scope change, New information |
| **What is wrong / missing** | The current incorrect or absent content |
| **What is correct / new** | The verified replacement or addition |
| **Source / evidence** | Why the new information is correct — user statement, design file, meeting, data |

### Change type reference

| Type | Propagation pattern | Search strategy |
|------|---------------------|-----------------|
| **Factual correction** | Any section that assumed the wrong fact — personas, pain points, user flows, assumptions, goals, constraints, dependencies | Search for the incorrect fact AND for statements derived from it |
| **Terminology change** | All occurrences of the old term across all documents | Context-aware find-and-replace — match singular/plural, capitalization, possessive forms |
| **Scope change** | Scope sections, feature lists, future enhancements, assumptions, success metrics | Search for the feature/item name in scope tables, requirement lists, and roadmap references |
| **New information** | Additive — new content in contextually correct sections, new rows in tables, new references | Identify which sections in each document should contain the new information |

---

## Universal Document Registry Template

| Document | Type | Found? | Decision | Reason |
|----------|------|--------|----------|--------|
| Stage1_Intake_Classification | Stage artifact | ✅ / ❌ | ✅ Update / ⬜ Skip / ❓ Verify | [one-line reason] |
| Stage2_Interpretation_Checkpoint | Stage artifact | ✅ / ❌ | ... | ... |
| Stage3_Variables_Constraints_Actors | Stage artifact | ✅ / ❌ | ... | ... |
| Stage4_Scenario_Matrix | Stage artifact | ✅ / ❌ | ... | ... |
| Stage5_Assumptions | Stage artifact | ✅ / ❌ | ... | ... |
| Stage6_User_Flows | Stage artifact | ✅ / ❌ | ... | ... |
| Stage7_[if exists] | Stage artifact | ✅ / ❌ | ... | ... |
| Stage8_Risk_Analysis | Stage artifact | ✅ / ❌ | ... | ... |
| Stage9_Document_Audit | Stage artifact | ✅ / ❌ | ... | ... |
| Feature-Requirements-[Feature] (Internal) | Internal FR | ✅ / ❌ | ... | ... |
| Client-Requirements-[Feature] | Client FR | ✅ / ❌ | ... | ... |
| Validation-Report-[Feature] | Report | ✅ / ❌ | ... | ... |
| Design description / Context Summary | Design artifact | ✅ / ❌ | ... | ... |
| project-context.md | Project knowledge | ✅ / ❌ | ... | ... |
| requirements-registry.md | Registry | ✅ / ❌ | ... | ... |

---

## Decision Rules Matrix

| Change type | Stage1 | Stage2 | Stage3 | Stage4 | Stage5 | Stage6 | Stage8 | Stage9 | Internal FR | Client FR |
|---|---|---|---|---|---|---|---|---|---|---|
| Factual correction | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ | ❓ | ✅ | ✅ |
| Terminology change | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Scope change (add) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Scope change (remove) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| New information | ❓ | ✅ | ✅ | ❓ | ✅ | ✅ | ❓ | ⬜ | ✅ | ✅ |

Legend: ✅ = always update | ⬜ = always skip | ❓ = evaluate content (explain decision in Reason column)

For every ❓: read that document's relevant sections and determine if the change content appears, is implied, or has cascading effects. Record the outcome (✅ or ⬜) with a one-line reason. No document may remain ❓ in the final registry.

---

## Impact Classification

| Impact Class | Definition | Section blast radius |
|---|---|---|
| **CROSS-CUTTING** | Affects every document and every section type (e.g., terminology change, actor capability correction, major constraint change) | All sections in all documents |
| **REQUIREMENT-LEVEL** | Adds, removes, or modifies a specific capability or behavioral rule | Executive Summary, User Needs, Business Goals, User Flows, Visual States, Error Handling, Assumptions, Open Questions, Dependencies, Risk/Known Limitations, EXISTING/NEW classification, Scenario Matrix (Stage4), canonical user flows (Stage6) |
| **CONTEXTUAL** | Affects a bounded area — a specific actor, a specific data field, a specific flow — without changing the FR set | Sections whose content is directly about that actor / field / flow |
| **ADDITIVE-ONLY** | New content that does not correct or contradict anything existing | Contextually correct sections where the new content belongs; no deletions or corrections needed |

Assign one impact class per change. If a change spans multiple classes, split it into sub-changes.

---

## Section Blast Radius Table

For each change, fill in all rows — do not skip:

| Section | Relationship | Question to answer | Verdict |
|---|---|---|---|
| **Executive Summary** | DERIVED | Does the change affect the scope or capability description? | 🔴 Affected / ⬜ Clear |
| **User Needs / Business Goals** | DERIVED | Does the change affect what users need or what the product achieves? | 🔴 / ⬜ |
| **User Flows / UX Flows** (in FR doc) | DERIVED | Does the narrative of how the feature works need to change? | 🔴 / ⬜ |
| **Visual States** | DERIVED | Is there a new UI state, or is an existing state now obsolete? | 🔴 / ⬜ |
| **Error Handling** | DERIVED | Is there a new failure path, or is an existing one now invalid? | 🔴 / ⬜ |
| **Assumptions** | UPSTREAM | Does the change confirm, invalidate, or introduce an assumption? | 🔴 / ⬜ |
| **Open Questions** | UPSTREAM | Does the change resolve a `[TBD]` or introduce a new one? | 🔴 / ⬜ |
| **Dependencies** | UPSTREAM | Does the change introduce or remove a system/team/data dependency? | 🔴 / ⬜ |
| **Known Limitations** | DERIVED | Does the change add, remove, or alter a known limitation? | 🔴 / ⬜ |
| **Risk Analysis** | DERIVED | Does the change alter the risk profile? | 🔴 / ⬜ |
| **EXISTING/NEW Classification** | DERIVED | Does the change affect what's in scope vs. out of scope? | 🔴 / ⬜ |
| **Change History** | METADATA | Always update if the document has a changelog | 🔴 Always |
| **Stage4 Scenario Matrix** | Stage artifact | Does the change require new or modified scenarios? Are any scenarios now obsolete? | 🔴 / ⬜ |
| **Stage6 User Flows** | Stage artifact | Does the canonical flow artifact need updating to match? | 🔴 / ⬜ |

Only sections marked 🔴 are searched in Step 4. Sections marked ⬜ are skipped.

---

## Section-Document Matrix Example

```
| Document | Section | Change IDs | Priority |
|---|---|---|---|
| Internal FR | Executive Summary | C1, C2 | HIGH |
| Internal FR | User Flows | C2 | HIGH |
| Internal FR | Visual States | C2 | MEDIUM |
| Stage6 | UF-1 | C2 | HIGH |
| Stage5 | Assumption M1 | C1 | MEDIUM |
| Client FR | Executive Summary | C1, C2 | HIGH |
...
```

This matrix is the search plan for Step 4. Only listed (document, section) pairs are searched.

---

## Finding Categories

### What to search for

| Category | What to find |
|---|---|
| **DIRECT** | Text that explicitly states the incorrect information, uses the old term, or directly describes the feature/behavior being changed |
| **DERIVED** | Text that is based on or implies the incorrect information — a pain point, goal, or flow that only makes sense if the old fact is true |
| **CROSS-REFERENCE** | References to the affected section, document, or fact from other sections or documents |
| **CONSISTENCY GAP** | Sections identified in Pass 1 as internally inconsistent, even without a direct text match |

### Category actions

| Category | Meaning | Action |
|---|---|---|
| DIRECT | Text explicitly contains the incorrect or outdated information | Will be updated |
| DERIVED | Text implies or builds upon the incorrect fact | Will be updated (rewritten to reflect correct fact) |
| CROSS-REFERENCE | A reference that will become stale after the primary change | Will be updated |
| CONSISTENCY GAP | Section is logically inconsistent with the change, even if it doesn't directly state the old fact | Will be updated or flagged for user decision |
| POTENTIAL | Text might be affected but intent is ambiguous — cannot determine automatically | Presented as a question to user in Step 5 |

---

## Batch Grouping Defaults

| Batch | Documents | Constraint |
|---|---|---|
| Batch 1 | Stage4, Stage5, Stage6 (all Stage artifacts that need updating) | Independent — run in parallel |
| Batch 2 | Internal FR + Client FR (if changes are independent of each other's output) | Can run in parallel if both receive the same change set |

Rule: Documents in the same batch must not depend on each other's edited output. When in doubt, split into separate batches.

---

## Output Discipline Table

| Rule | What it means |
|---|---|
| **Silent execution** | The main agent outputs **zero chat text** between launching subagents and receiving their completion reports. No narration, no progress updates. |
| **No direct editing** | The main agent never calls Read, StrReplace, or Write on any target document. Edits happen inside subagents. |
| **Single output point** | After all subagents complete, the main agent outputs Step 7/8 verification summary. Exception: if Step 6.5 surfaces failed edits or judgment calls, pause once to request user decision. |

---

## Preflight Reference

| Step | Preflight checks (all must be YES) |
|---|---|
| **Step 2** | T1 complete; Input inventory artifact exists; RunState exists and current; Change IDs and sources structured |
| **Step 3** | T2 complete; changeset-confirm = confirmed; ChangeSet artifact path in RunState |
| **Step 5** | T3 complete; Registry decision confirmed; Section-document matrix finalized |
| **Step 6** | T4 complete; manifest-confirm = confirmed; RunState.gates_passed.manifest_confirmed = true; Execution method = subagents_only |
| **Step 7** | T5 complete; All edit subagents finished; RunState document completion lists current |
| **Step 8** | T6 complete; Verification outputs captured; All artifacts and gate statuses present in RunState |
