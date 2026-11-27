---
name: validate-requirements
description: "Validates requirements documents using 15 checks across 2 dimensions: semantic accuracy (11 checks — source truth, inference detection, requirement purity, over-generalization, scope boundaries, testability, ambiguity, assumption dependencies, negative paths, actor capability, intra-document consistency) and structural integrity (4 checks — staleness, contradictions, cross-references, completeness). Supports incremental mode: when a prior validation report is provided, only re-runs checks whose inputs have changed, carries forward findings that remain valid, and detects resolved findings — cutting re-validation effort by 40-60%. Produces a unified report with clear Semantic vs Structural grouping. Use after generating requirements, before sharing with stakeholders, when suspecting inaccuracies, or as a periodic quality sweep."
---

# Validate Requirements — Semantic + Structural Review

## NON-NEGOTIABLE (read first)
1. Never skip a check. Mark unavailable checks as SKIPPED with reason.
2. Show evidence for every finding — problematic text + source quote.
3. Don't fix — flag. This skill identifies issues, never modifies the document.
4. Dual output is mandatory: chat summary + saved report file + next steps.
5. Incremental mode: when in doubt, RE-RUN. Stale carry-forward is worse than a redundant re-run.

## Purpose

Catches both **semantic inaccuracies** (factually wrong, unsourced, over-generalized, solution-prescriptive, untestable content) and **structural issues** (stale placeholders, contradictions, broken cross-references, completeness gaps) in a single pass.

This skill replaces the need to run `validate-requirements` and `document-audit` separately on requirements documents. The standalone `document-audit` skill remains available for non-requirements documents (PRDs, meeting notes, design specs).

## Critical Rules

1. **Never skip a check.** If inputs are missing for a check, mark it SKIPPED with an explanation — do not silently omit it. In incremental mode, CARRY FORWARD is not "skipped" — the check ran in the prior report and its results are being reused because inputs haven't changed.
2. **Show evidence, not just verdicts.** For every finding, show the problematic text and (for source checks) what the source actually says.
3. **Severity matters.** Group findings by severity in the report, not by check number. A single finding may fail multiple checks — list it once under its highest severity with all applicable check numbers.
4. **Dual output + next steps are mandatory.** Always produce the chat summary, the full report file, and prioritized next steps. The chat summary is for quick triage; the report file is for persistent reference; the next steps tell the user exactly what to do next and in what order.
5. **Be conservative with PASS.** A check PASSes only if zero findings — including carried-forward findings. A carried-forward finding still counts.
6. **Don't fix — flag.** This skill identifies issues; it does not modify the requirements document. Fixes are applied separately (by the user or by the pipeline).
7. **Type column is mandatory.** Every finding row must include the Type column (Semantic / Structural) so findings from both dimensions are clearly distinguished in severity-sorted tables.
8. **Read the FULL document.** Structural checks are only effective when cross-referencing the entire document. Never audit from a partial read. In incremental mode, the full document is still read in Phase 1 — only source documents may be skipped if unchanged.
9. **Never invent answers.** If a `[PENDING]` marker exists and the answer is NOT in the document or conversation, leave it as-is. Report it as "unresolved — still needs input."
10. **Incremental mode: when in doubt, re-run.** If it is unclear whether a change affects a check, classify it as RE-RUN. The cost of re-running an unnecessary check is low; the cost of carrying forward a stale finding is high.
11. **Incremental mode: Check 11 and S1–S4 always re-run.** These are the consistency safety net. Any edit — even one that fixes a finding — can introduce new contradictions, stale references, or consistency gaps in other sections. Never carry these checks forward.
12. **Incremental mode: tag carried-forward findings.** Every finding reused from a prior report must include `(carried from [date])` in its Finding cell. The user must be able to distinguish new discoveries from surviving prior findings at a glance.
13. **Checklist is mandatory.** Every run must maintain the six-item control loop (`T0 Gather`, `T1 Understand`, `T2 Analyze`, `T3 Plan`, `T4 Execute`, `T5 Verify`) with explicit status transitions. Do not skip directly from analysis to output.

## Local Traceability Pilot

When local traceability is enabled on this machine, emit hidden semantic checkpoint records for this skill. These traces are operator-facing only and must never be added to the requirements document, the validation report, or the normal chat summary unless the user explicitly asks for trace output.

**Enable check:**
- Check for `/Users/rushi/.cursor/traceability/config.json`
- If it exists and local traceability is enabled for `validate-requirements`, record the checkpoints below
- If the trace write fails, continue the validation workflow; tracing must not block the skill

**Trace command:**

```sh
node "/Users/rushi/.cursor/traceability/bin/record-semantic-trace.mjs" --skill validate-requirements --checkpoint "<checkpoint>" --phase "<phase>" --status "<status>" --mode "<mode>" --artifact-path "<path>" --metadata-json '{"key":"value"}'
```

Use only the flags that are relevant to the checkpoint. Keep metadata concise and factual.

**Required semantic checkpoints for this pilot:**
- `inputs-gathered` — after `T0 Gather` is completed
- `mode-selected` — after `T1 Understand` is completed
- `incremental-plan-ready` — after Phase 0.5 completes in incremental mode
- `setup-complete` — after Phase 1 setup is completed
- `execution-complete` — after Phase 2a and 2b are completed
- `report-saved` — immediately after the full report file is saved
- `summary-published` — after the chat summary is published and `T5 Verify` is completed

**Recommended metadata by checkpoint:**
- `inputs-gathered`: requirements doc path, source folder provided or missing, sibling docs availability, stage artifacts availability, prior report availability
- `mode-selected`: selected mode and reason (`full` or `incremental`)
- `incremental-plan-ready`: checks re-run, checks carried forward, prior findings resolved, prior findings surviving
- `setup-complete`: source count, sibling doc count, stage artifact availability
- `execution-complete`: finding counts by severity, semantic checks run, structural checks run
- `report-saved`: report path and document path
- `summary-published`: total findings, final status, whether next steps were published

---

## When to Use

- After generating requirements (as part of the pipeline at Stage 9, or standalone)
- When reviewing an existing requirements doc before sharing with stakeholders
- When the user suspects inaccuracies, over-prescription, or unsourced claims
- As a periodic quality sweep across a set of feature docs
- After `update-documents` propagates changes (in the verify step)

## Inputs

Gather these before starting:

1. **Requirements document** — the file to validate (REQUIRED)
2. **Source documents folder** — meeting summaries, client docs, design descriptions, transcripts (REQUIRED for Checks 1, 2, 4, 10)
3. **Sibling requirements docs** — other feature requirement docs in the same folder (OPTIONAL — needed for Check 5: Scope Boundary)
4. **Stage User Flows artifact** — `Stage6_User_Flows.md` or equivalent stage artifact (OPTIONAL — needed for Check 11 cross-check). If not provided, scan for it in the project's Artifacts or stage folders. If found, use it. If not found, note it as unavailable and skip that sub-check only.
5. **Prior validation report** — a previous `Validation-Report-*.md` or `Stage9-Validation-Report.md` file (OPTIONAL). When provided, the skill enters **incremental mode** — only re-running checks whose inputs have changed since the prior report. When absent or when the user says "run full", the skill runs all 15 checks from scratch (full mode).

If source documents are not available, Checks 1 (Source Accuracy) and 4 (Over-Generalization) will be marked SKIPPED with a note explaining why.

---

## Mode Selection

Before beginning, determine which mode to use:

| Condition | Mode | Behavior |
|---|---|---|
| No prior report provided | **Full** | Run all 15 checks from scratch |
| Prior report provided | **Incremental** | Detect changes, selectively re-run checks, carry forward valid prior findings |
| User says "run full" or "full validation" | **Full** | Ignore any prior report, run all 15 checks from scratch |
| First run in the pipeline (Stage 9) | **Full** | No prior report exists yet |
| Re-run after fixes or `update-documents` | **Incremental** (if prior report available) | Typical incremental use case |

---

## Mandatory Todo / Checklist Control Loop

This skill must run with a mandatory checklist that enforces:
**Gather → Understand → Analyze → Plan → Execute → Verify**.

Before Phase 0/1 begins, create and maintain a todo list. This is not optional.

### Required checklist items

1. `T0 Gather` — Build input inventory (requirements doc, source folder/docs, sibling docs, stage artifacts, prior report if any); list missing inputs and availability
2. `T1 Understand` — Confirm validation objective and mode selection basis (Full vs Incremental)
3. `T2 Analyze` — Gather evidence (document read, sources, sibling docs, stage artifacts, change detection in incremental mode)
4. `T3 Plan` — Build check execution plan (which checks run, scoped re-runs, carried-forward findings)
5. `T4 Execute` — Run semantic + structural checks and capture findings with evidence
6. `T5 Verify` — Validate output quality and completeness, save report, publish summary + next steps

### Checklist status rules

- Exactly one item is `in_progress` at a time.
- Every item must transition `pending` → `in_progress` → `completed` (or `cancelled` if truly not applicable).
- Never start `T1 Understand` until `T0 Gather` is `completed`.
- Never start `T4 Execute` until `T3 Plan` is `completed`.
- Never publish final output until `T5 Verify` is `completed`.
- If interrupted, keep the active item `in_progress` and explicitly resume from it.

---

## Execution Workflow

**Checklist bootstrap (mandatory):** Before Phase 0/1, set `T0 Gather` to `in_progress`, collect and inventory all provided/discovered inputs, mark `T0 Gather` `completed`, then set `T1 Understand` to `in_progress`. Mark `T1 Understand` `completed` only after mode (Full vs Incremental) is explicitly justified from gathered inputs.

**Trace checkpoint:** After `T0 Gather` completes, record `inputs-gathered`. After `T1 Understand` completes, record `mode-selected`.

### Phase 0: Change Detection (incremental mode only)

*Skip this phase entirely in full mode — proceed directly to Phase 1.*

Read the file:

    incremental-detection.md

Follow that file's instructions completely. When Phase 0 is complete, return here and proceed to Phase 1.

### Phase 1: Setup

1. Read the requirements document end-to-end. Do not skim.
2. Identify and read all source documents (from the provided folder path). **Incremental mode optimization:** if Phase 0.3 determined sources are unchanged AND only CARRY FORWARD checks need them, skip re-reading source files — they are only needed for checks that are actually running.
3. Identify sibling requirements docs (if any, in the same folder)
4. Build a source index: map each SRC-N to its file and key content. **Incremental mode:** build only for sources referenced by checks that are RE-RUN or RE-RUN (scoped).
5. Locate stage artifacts: scan for `Stage4_Scenario_Matrix.md` and `Stage6_User_Flows.md` (or equivalent) in the project's Artifacts or stage folders. Note whether each is found or unavailable.

**Checklist update:** In full mode (where Phase 0 is skipped), set `T2 Analyze` to `in_progress` at Phase 1 start and mark `completed` after setup evidence collection is finished. Then set `T3 Plan` to `in_progress` and `completed` once the check run plan is explicit (all checks in full mode; selective plan in incremental mode).

**Trace checkpoint:** After Phase 1 setup is completed, record `setup-complete`. In full mode, include the final check run plan in concise metadata.

### Phase 2a: Semantic Checks (content accuracy)

Read and follow:

    checks/semantic-checks.md

**Full mode:** Run all 11 checks (1–11) in order.

**Incremental mode:** For each check, consult the execution plan from Phase 0.4:
- **RE-RUN** — run the check fully, as in full mode
- **RE-RUN (scoped)** — run the check only on changed FRs/sections; merge results with SURVIVING findings carried from the prior report for unchanged FRs/sections
- **CARRY FORWARD** — do not run the check; use SURVIVING findings from Phase 0.5 as the check's results

For each finding (whether new or carried forward), record:
- Location in doc (section + line)
- The problematic text
- The verdict
- The recommendation

Classify severity:
- **Critical** — factually wrong or misleading (must fix before sharing)
- **Should Fix** — reframe, relocate, or make precise (improves quality)
- **Verify** — needs user confirmation (may be correct, can't determine automatically)
- **Gap** — missing coverage (negative paths, uncovered scenarios)

**Checklist update:** Set `T4 Execute` to `in_progress` before running Check 1 and keep it active through Phase 2b.

### Phase 2b: Structural Checks (document integrity)

Read and follow:

    checks/structural-checks.md

Run all 4 checks (S1–S4) in order. **Structural checks always run in both full and incremental mode** — they are cheap, operate on the document alone, and catch editing artifacts that are invisible to the change manifest. Use the same severity classifications as Phase 2a.

**Trace checkpoint:** After Phase 2b completes, record `execution-complete`.

### Phase 3: Generate Output

Produce two outputs: a chat summary and a full report file.

**Checklist update:** Set `T5 Verify` to `in_progress` before composing outputs. Verify that:
- all required checks are represented as PASS/FAIL/SKIPPED with rationale,
- severity tables include required columns (including Type),
- carried-forward findings are tagged (incremental mode),
- output file path rules were followed.

Mark `T5 Verify` as `completed` only after report is saved and chat summary is published.

**Trace checkpoints:**
- Immediately after the full report file is saved, record `report-saved`
- After the chat summary is published and `T5 Verify` is completed, record `summary-published`

Read the file:

    output-templates.md

Follow that file's instructions to produce both the chat summary and the full report file.

---

## Integration with Other Skills

| Context | Mode | How it's called |
|---|---|---|
| **Standalone (first run)** | Full | Run against any requirements doc + its source folder. No prior report exists. |
| **Standalone (re-run)** | Incremental | User provides the prior validation report. Skill detects changes and selectively re-runs. |
| **Pipeline (Stage 9)** | Full | Called by `requirements-pipeline` as the combined accuracy + integrity review. No prior report exists at this stage. The report it produces becomes the prior report for future incremental runs. |
| **After updates** | Incremental | Called by `update-documents` in its Phase 3 verify step. The pre-update validation report serves as the prior report. |
| **Interactive resolution** | — | After report is generated, user invokes `review-findings` with the report file to walk through findings and collect decisions |
