---
name: update-documents
description: "Propagates corrections, new information, terminology changes, and scope changes across multiple related documents. Structures changes, verifies with user, performs impact analysis, presents a change manifest for approval, applies edits preserving each document's format and tone, and runs verification as a final consistency check (validate-requirements for requirements docs, document-audit for all others). Use when a fact, assumption, or decision changes and multiple documents need updating, or when new information (e.g., from a design review, stakeholder feedback, or discovery session) must be reflected across a document set."
---

# Update Documents — Cross-Document Change Propagation

## Purpose

Propagates verified corrections and new information across a set of related documents. Ensures every affected document is updated consistently, in the correct order, with user approval at two mandatory checkpoints.

**Execution safety model:** This skill uses a mandatory todo list as an execution control plane. Every phase is represented as a tracked task, and task status must be updated continuously (`pending` → `in_progress` → `completed`/`cancelled`).

**When to use:**
- A fact or assumption was wrong and multiple documents reference it
- New information (design, stakeholder input, discovery) must be reflected across existing docs
- Terminology is changing across a document set
- A feature or scope item is being added, deferred, or removed

**Domain-agnostic.** Works on any document type — requirements, PRDs, meeting notes, design specs, technical docs.

**Supporting files (loaded on demand, never optional):**
- [`reference-tables.md`](./reference-tables.md) — registry templates, decision matrices, impact tables, finding categories, preflights
- [`appendix-update-documents.md`](./appendix-update-documents.md) — prompt templates, output formats, gate YAML blocks

---

## NON-NEGOTIABLE (read first)

1. **Subagents only for target document edits.** The main agent must never call Read/StrReplace/Write on target documents in Step 6.
2. **Silent execution in Step 6.** No progress narration between subagent launch and completion consolidation.
3. **Artifacts, not chat tables.** Change set and manifest must be written to files under `update-workspace/`; chat only carries summary + confirmation gates.
4. **Todo state machine is mandatory.** Maintain `T0`–`T7` with explicit transitions.
5. **No execution before confirmations.** Never execute edits until all mandatory gates are confirmed.
6. **RunState is mandatory.** Every run must maintain `RunState-[YYYYMMDD-HHMM].json`; phase/gate transitions are invalid unless RunState is updated.
7. **Reference files are mandatory reads.** When a step says MANDATORY READ, read that file section before proceeding. Never skip.

---

## Execution Checklist (one-screen reference)

| Task | Step | Artifact / Gate | Reference file sections to read |
|---|---|---|---|
| `T0` Gather | Pre-Step 1 | `Input-Inventory-*.md` + `RunState-*.json` | — |
| `T1` Structure | Step 1 | Change set structured | `reference-tables.md` > Change Set Structure |
| `T2` Gate | Step 2 | `ChangeSet-*.md` + `changeset-confirm` | `appendix` > Change Set Chat Summary + AskQuestion Gate |
| `T3` Analyze | Steps 3–3.5 | Registry + matrix finalized + `registry-confirm` | `reference-tables.md` > Registry Template, Decision Rules, Impact Classification, Blast Radius, Matrix Example |
| `T4` Gate | Step 5 | `Manifest-*.md` + `manifest-confirm` | `appendix` > Manifest Chat Summary + AskQuestion Gate + Manifest Format |
| `T5` Execute | Step 6 | Subagents only, silent, RunState updates | `reference-tables.md` > Batch Grouping, Output Discipline; `appendix` > Execution Subagent Prompt |
| `T6` Verify | Step 7 | validate-requirements / document-audit | — |
| `T7` Report | Step 8 | Update Summary | `appendix` > Update Summary Report Template |

---

## Mode Selection

Before Phase 1, assess change scope for **Steps 1–5 only**. Step 6 always uses subagents.

| Situation | Mode for Steps 1–5 | Rationale |
|---|---|---|
| 1–3 changes, 1–2 files | **Agent** | Small scope; inline analysis is fine |
| 4+ changes, 3+ files, or cross-cutting | **Plan mode** | Keep large planning artifacts out of main chat |

---

## Mandatory Todo Control Loop

Create before Phase 1 and keep synchronized. Not optional.

1. `T0` — Gather inputs and context inventory (read `reference-tables.md`: Change Set Structure, Registry Template)
2. `T1` — Structure change set
3. `T2` — Write and confirm change set file (Step 2 gate)
4. `T3` — Build registry + impact classification + matrix (read `reference-tables.md`: Decision Rules, Impact Classification, Blast Radius)
5. `T4` — Write and confirm manifest file (Step 5 gate)
6. `T5` — Execute approved edits via subagents (read `reference-tables.md`: Batch Grouping, Output Discipline)
7. `T6` — Verify modified documents
8. `T7` — Publish final update summary

### Status rules

- Exactly one task `in_progress` at a time.
- Transition: `pending` → `in_progress` → `completed` (or `cancelled`).
- Never start `T1` until `T0` completed. Never start Step 6 unless `T4` completed.
- If interrupted, leave current task `in_progress` and identify resume point.

**Bootstrap:** Set `T0` to `in_progress`, inventory inputs, create `RunState-[YYYYMMDD-HHMM].json`, mark `T0` completed.

---

## Required Run Artifacts and RunState Contract

Every run creates and maintains in `update-workspace/`:

1. `Input-Inventory-[YYYYMMDD-HHMM].md`
2. `ChangeSet-[YYYYMMDD].md`
3. `Manifest-[YYYYMMDD].md`
4. `RunState-[YYYYMMDD-HHMM].json`

**RunState keys:** `run_id`, `current_task`, `task_status_map` (T0..T7 → pending/in_progress/completed/cancelled), `gates_passed` (changeset_confirmed, registry_confirmed, manifest_confirmed), `artifacts` (resolved paths), `documents_pending`, `documents_completed`, `last_updated_utc`.

Update RunState at every phase transition and gate confirmation.

---

## Phase 1: Intake

### Step 1: Receive and structure the change set

**MANDATORY READ before proceeding:** Read `reference-tables.md` > "Change Set Structure" and use the field table and change type reference to structure each change. Do not proceed without a complete structured change set.

If the user provides changes informally, reformat them into the structured table before proceeding.

**T0 Gather artifact:** Before Step 1, write `update-workspace/Input-Inventory-[YYYYMMDD-HHMM].md` with: available inputs, missing inputs, candidate target documents, mode rationale. `T0` is only completed after this file is written. Update RunState with artifact path and `current_task = T1`.

**Todo update:** Set `T1` to `in_progress` at start, `completed` when change set is ready.

---

### Step 2: User verification checkpoint (MANDATORY STOP)

**MANDATORY READ before proceeding:** Run preflight for Step 2 from `reference-tables.md` > "Preflight Reference". All checks must be YES.

Write the full structured change set to `update-workspace/ChangeSet-[YYYYMMDD].md`. Never print the full table in chat.

**MANDATORY READ for output format:** Read `appendix-update-documents.md` > "Change Set Chat Summary Format" and "Change Set AskQuestion Gate". Use these exact formats.

Do NOT proceed until the user confirms. If "modify": update file, re-summarize, re-ask.

Update RunState: set `artifacts.changeset_path`, set `gates_passed.changeset_confirmed` after confirmed, set `current_task = T3`.

**Todo update:** `T2` in_progress before writing; completed only after user confirms.

---

### Step 3: Build the Universal Document Registry

**MANDATORY READ before proceeding:** Run preflight for Step 3 from `reference-tables.md` > "Preflight Reference". Then read `reference-tables.md` > "Universal Document Registry Template" and "Decision Rules Matrix". Use the template to enumerate documents and the matrix to assign decisions. Do not proceed without completing the registry.

Scan the project workspace. For every ❓: read relevant sections, resolve to ✅ or ⬜ with reason. No ❓ in final registry.

**Dependency order:** Stage1 → Stage2 → Stage3 → Stage4 → Stage5 → Stage6 → Stage8 → Stage9 → Internal FR → Client FR. If no Stage artifacts exist, sort by project dependency relationships.

Present registry to user for confirmation (mandatory). After confirmation, update `RunState.gates_passed.registry_confirmed = true` and `current_task = T4`.

**Todo update:** `T3` in_progress at start of Step 3, stays active through Step 3.5, completed when registry + classification + matrix finalized.

---

### Step 3.5: Change Impact Classification (mandatory reasoning step)

**Before searching any document**, reason through the blast radius of each change.

**MANDATORY READ before proceeding:** Read `reference-tables.md` > "Impact Classification" to classify each change. Then read "Section Blast Radius Table" and fill it in for each change. Then read "Section-Document Matrix Example" and produce the consolidated matrix.

Only sections marked 🔴 are searched in Step 4. This matrix is the search plan.

---

## Phase 2: Execute

### Step 4: Targeted search and intra-document consistency pass

Using the section-document matrix as the search plan:

| Documents in matrix | Strategy |
|---|---|
| 1–2 documents | Run Pass 1 and Pass 2 in the main agent sequentially |
| 3+ documents | Launch parallel discovery subagents — one per document |

Step 4 is **read-only discovery**. Subagents cannot corrupt anything; Step 5 manifest review is the accuracy gate.

**For parallel discovery (3+ documents):** Each subagent receives target file path, scoped section list, full change set description, and return instructions.

**MANDATORY READ before building discovery prompts:** Read `appendix-update-documents.md` > "Discovery Subagent Prompt Template (Step 4)". Use this template.

After all discovery subagents complete, consolidate findings, deduplicate cross-document references, resolve conflicts, and use as input for Step 5.

**For sequential path (1–2 documents):**

**Pass 1** — Reason about consistency for each 🔴 section: Does it describe behavior the change invalidates? Do visual states match updated flows? Do dependencies match? Are confirmed assumptions still marked unconfirmed?

**Pass 2** — Search for DIRECT, DERIVED, CROSS-REFERENCE, and CONSISTENCY GAP matches.

**MANDATORY READ before proceeding:** Read `reference-tables.md` > "Finding Categories" for category definitions and required actions. Do not proceed without categorizing every finding.

Record each finding with: document path, section heading, current text, proposed replacement, category, and change ID.

---

### Step 5: Change manifest and user review (MANDATORY STOP)

**MANDATORY READ before proceeding:** Run preflight for Step 5 from `reference-tables.md` > "Preflight Reference". All checks must be YES.

Write the manifest to `update-workspace/Manifest-[YYYYMMDD].md`.

**MANDATORY READ for file format:** Read `appendix-update-documents.md` > "Manifest File Format Template". Use this exact format.

**MANDATORY READ for chat output:** Read `appendix-update-documents.md` > "Manifest Chat Summary Format" and "Manifest AskQuestion Gate". Use these exact formats.

Never print the full registry or manifest in chat. Do NOT apply edits until user confirms. If "modify": update file, re-summarize, re-ask.

Update RunState: set `artifacts.manifest_path`, `gates_passed.manifest_confirmed` after confirmed, `current_task = T5`.

**Todo update:** `T4` in_progress before writing manifest; completed only after user confirms.

---

### Step 6: Apply changes

**MANDATORY READ before proceeding:** Run preflight for Step 6 from `reference-tables.md` > "Preflight Reference". All checks must be YES.

**Per NON-NEGOTIABLE #1:** All edits via subagents, no exceptions. If you are about to call Read/StrReplace/Write on a target document from the main agent: STOP. Use a subagent instead.

**MANDATORY READ before partitioning:** Read `reference-tables.md` > "Batch Grouping Defaults". Use dependency order to partition documents into parallel batches. Documents in same batch must not depend on each other's edited output.

**MANDATORY READ before building prompts:** Read `appendix-update-documents.md` > "Execution Subagent Prompt Template (Step 6)". Each subagent receives only its document's filtered manifest rows.

Launch Batch 1 subagents simultaneously. Wait for completion. Launch Batch 2. Wait for completion. Use `generalPurpose` subagents with write access.

After all batches, collect reports. Surface failed edits or judgment calls to user. Update `RunState.documents_completed` and `documents_pending` after each batch. If partially interrupted, persist remaining document list.

**MANDATORY READ before any chat output:** Read `reference-tables.md` > "Output Discipline Table". Per NON-NEGOTIABLE #2: zero chat text between launch and completion. Self-check before every tool call.

**Todo update:** `T5` in_progress before first subagent launch; completed after all results consolidated.

---

## Phase 3: Verify

### Step 7: Run verification on all modified documents

**MANDATORY READ before proceeding:** Run preflight for Step 7 from `reference-tables.md` > "Preflight Reference".

- **Requirements documents** (Feature-Requirements-*, Client-Requirements-*): invoke `validate-requirements`.
- **All other documents**: invoke `document-audit`.

Focus on: contradictions, broken cross-references, resolved stale markers, terminology inconsistencies, cascading staleness. If 5+ documents, prioritize downstream first.

**Todo update:** `T6` in_progress at start; completed when verification done.

---

### Step 8: Report and close

**MANDATORY READ before proceeding:** Run preflight for Step 8 from `reference-tables.md` > "Preflight Reference". Then read `appendix-update-documents.md` > "Update Summary Report Template". Use this format.

- HIGH findings: fix immediately and re-audit.
- MEDIUM findings: present to user.
- LOW findings: report only.

**Todo update:** `T7` in_progress before report; completed after publishing. Confirm all todos completed or cancelled.

---

## Resume Workflow (mandatory when run is interrupted)

Do not continue from memory. This section is self-contained — no reference file needed.

1. Locate latest `RunState-[YYYYMMDD-HHMM].json`.
2. Load artifacts listed in RunState (`Input-Inventory`, `ChangeSet`, `Manifest` when present).
3. Reconcile with workspace: confirm documents modified vs pending, confirm gate confirmations in `gates_passed`.
4. If interrupted during Step 6, re-run Step 6 preflight before launching any new subagent.
5. If a required confirmation is missing, re-open that gate.
6. Resume from `current_task` only; do not skip ahead.
7. Update `last_updated_utc` and persist RunState before any new execution step.

---

## Critical Rules

### Hard Constraints

1. **Per NON-NEGOTIABLE #1:** Subagents only for all target document edits. No exceptions.
2. **Per NON-NEGOTIABLE #2:** Silent execution between subagent launch and completion.
3. **Per NON-NEGOTIABLE #3:** Change set and manifest are files under `update-workspace/`, not chat tables.
4. **Per NON-NEGOTIABLE #4:** Todo list with explicit T0–T7 transitions for every run.
5. **Per NON-NEGOTIABLE #5–6:** No edits before gate confirmations; RunState updated at every transition.
6. **Never invent corrected text.** Flag "needs user input" instead of guessing.

### Execution Model Rules

7. **Dependency order matters.** Upstream first, Client FRs last.
8. **Each subagent receives only its document's changes.**
9. **Subagents are independent.** No cross-batch dependencies within same batch.
10. **Main agent context stays clean.** During Step 6: launch, monitor, consolidate only.
11. **Parallel discovery subagents are read-only.** They return structured findings; never write files.
12. **No document skipped silently.** Every discovered document must have explicit registry status with reason.
13. **Reason before searching.** Step 3.5 is never optional.

### Quality and Consistency Rules

14. **Preserve document voice.** Match tone, format, detail level.
15. **Domain-agnostic.** No industry/format/technology assumptions.
16. **Additive by default.** Use existing sections unless new structure truly required.
17. **Change history is not optional.** Update changelog if document has one.
18. **Read before editing.** Each subagent reads full document before editing.
19. **One change at a time.** Sequential edits within each subagent.
20. **DERIVED requires judgment.** Escalate uncertainty instead of guessing.
