---
name: requirements-pipeline
description: "A 9-stage discovery and analysis pipeline that takes messy, early-stage inputs — rough ideas, transcripts, designs, legal docs, hypotheses — and produces a production-ready requirements document. Handles brainstorming, scenario mapping, assumption analysis, user flows, and risk analysis with mandatory human checkpoints. Calls complementary skills at each stage. Use when asked to: run the requirements pipeline, build requirements from scratch, start from rough ideas or a transcript, or work through a feature from discovery to requirements."
---

# Generate Detailed Requirements — Pipeline Orchestrator

## NON-NEGOTIABLE (read first)
1. Save every stage artifact to file before presenting in chat. Chat is ephemeral.
2. Never fabricate. Mark unknowns as `[TBD]`, inferences as `[INFERRED]`.
3. Never skip Stage 2 (interpretation) or Stage 9 (validation).
4. Source traceability on every claim. No citation = flag as `(Source: Implicit)`.
5. Requirements describe WHAT, never HOW (solution) or WHAT IT LOOKS LIKE (design).

## Purpose

Orchestrates a full requirements pipeline from messy, diverse inputs to a production-ready requirements document. It coordinates multiple skills and enforces quality gates between stages.

**What makes this different from `generate-requirements`:**
- `generate-requirements` takes well-defined inputs (PRDs, designs, transcripts) and generates a structured Feature Requirements document.
- This skill handles the **earlier, messier phase** — rough ideas, brainstorming, scenario mapping, stakeholder feedback loops — and builds up to the point where `generate-requirements` can take over for the final doc.

**Core principles:**
- **Interpret before editing.** Always summarize understanding and wait for confirmation before producing artifacts.
- **Facts only.** Mark unknowns as `[TBD]`. Never fabricate rules, thresholds, or business logic.
- **Domain-agnostic.** This pipeline works for any feature, any industry, any platform.

---

## Critical Rules

1. **Never skip the interpretation checkpoint (Stage 2).** Misunderstanding inputs wastes more time than confirming understanding.
2. **Never skip the quality gates (Stage 9, and 9c if split).** Stage 9 catches both semantic inaccuracies and structural issues in a single pass; Stage 9c catches cross-document conflicts. All applicable gates are required.
3. **Save artifacts at every stage — see Stage Artifact Registry.** Long sessions lose context. Files persist. Never present stage output only in chat. Save the file first, then summarize briefly in chat with the file path.
4. **Mark unknowns honestly.** `[TBD]` is always better than invented data.
5. **Domain-agnostic.** Never assume a specific tech stack, industry, or platform unless the user's inputs specify one.
6. **One stage at a time.** Complete each stage fully before starting the next. Wait for user confirmation at checkpoints. Exception: after Stage 3.5, per-feature stages run in staggered parallel per the Execution Model.
7. **Consolidate inputs upfront.** Process all user-confirmed inputs (from the three-tier scoping gate) in Stage 1 before doing any analysis. Do not process inputs one at a time across multiple rounds.
8. **Source traceability everywhere.** Every requirement, assumption, decision, and constraint in the final document must carry a source tag (`Source: SRC-N, section/decision` or `Source: Implicit`). If you can't trace a statement to an input, tag it as Implicit — this flags it for extra validation.
9. **Never invent the current state.** If existing product capabilities are unknown, tag them as `[CURRENT STATE UNKNOWN]` — do not fabricate a plausible "before" scenario. Always ask about existing product in Step 1.5.
10. **Requirements describe WHAT, never HOW or WHAT IT LOOKS LIKE.** If you catch yourself writing an implementation mechanism (solution) or a UI layout/navigation pattern (design decision), reframe it as the underlying need or flag it as a design decision / open question.
11. **Inferred content must be flagged.** `[INFERRED]` is better than confident-sounding fabrication. When filling a gap, tag it explicitly so the user can verify or reject it. Never present an inference as a stated fact.
12. **Source citations must be accurate.** When citing `(Source: SRC-N)`, verify the source actually contains the claimed information. Do not cite a source for content it does not contain. Run the source verification pass in Stage 7.
13. **Scoped statements stay scoped.** If a source says "X in context A", do not generalize to "X everywhere" without additional sourcing or explicit `[INFERRED — generalized from SRC-N context A]` tagging.
14. **Table indicators must be labeled and sorted.** Never use a bare dot (`🔴`) without a label (`🔴 Critical`). All tables with priority, risk, or severity columns must be sorted highest first. Resolved items sink to the bottom.
15. **Scope inputs to user-provided context.** Never scan the full workspace by default. Use the three-tier scoping gate in Stage 1.1: (1) user-provided files are always included, (2) same-folder discovery with user selection, (3) workspace-wide keyword search only on explicit request. Files not selected by the user are never read.
16. **Each stage must produce unique insight, not reformat prior stages.** Before writing any stage artifact, answer: "What will I know after this stage that I didn't know before?" If the answer is "the same things in a different table format," you are restating, not analyzing. Apply the stage's analytical framework instead. When a stage builds on a prior stage's content, **reference** it (e.g., "See Stage 2, C1-C11") — do not copy it.
17. **Brainstorm stages require collaborative gap-finding.** Stages that involve brainstorming (Stage 3, Stage 4) must surface questions *to the user* before finalizing the artifact. Present an initial analysis, then explicitly ask what's missing. Delivering a finished artifact without user interaction is a presentation, not a brainstorm.
18. **Always run Stage 3.5 (Feature Decomposition).** Even if the feature seems straightforward, produce the decomposition artifact. It may recommend "no split needed" and that is a valid output. Skipping it risks producing a monolithic document that should have been split.
19. **Shared Registry is binding.** When multiple features exist, each shared item (FR, assumption, dependency, open question) has exactly one owner. Other features reference, never duplicate. Subagents must obey their exclusion lists. New shared items discovered during Stages 4-9 are flagged as `[SHARED — assign to Feature X]` and resolved in Stage 9c.
20. **Cross-document consistency over individual completeness.** When producing multiple feature documents, no document should contradict another. If a conflict is detected (same rule with different wording, inconsistent assumption status), resolve it before finalizing. Stage 9c is the enforcement mechanism.

---

## Pipeline Overview

```
Stage 1:   Intake & Classification + Current State Discovery
     ↓
Stage 2:   Interpretation Checkpoint (STOP — wait for user confirmation)
           Includes Inference Register — STATED vs INFERRED separation
     ↓
Stage 3:   Brainstorm — Variables, Constraints, Actors
     ↓
Stage 3.5: Feature Decomposition (STOP — wait for user confirmation)
           Cluster value streams, test independence, build Shared Registry
           If single feature → continue as one stream
           If multiple features → staggered parallel execution below
     ↓
  ┌──────────────────────────────────────────────────────┐
  │ Per-feature stages (run once if single feature,      │
  │ staggered-parallel if multiple — see Execution Model)│
  │                                                      │
  │ Stage 4:  Scenario Matrix                            │
  │ Stage 5:  Assumptions (CHECKPOINT)                   │
  │ Stage 6:  User Flows + Purity Filter                 │
  │ Stage 7:  Requirements Document                      │
  │ Stage 8:  Risk Analysis                              │
  │ Stage 9:  Validation (Semantic + Structural)           │
  └──────────────────────────────────────────────────────┘
     ↓
Stage 9c: Post-Merge Reconciliation (ONLY if multiple features)
          Cross-document deduplication, conflict detection, cross-references
```

**Mandatory checkpoints:** Stages 2, 3.5, 5, and 9 (including dedup). Do not skip them.

---

## Output Folder & Artifact Registry

### Output folder (ask in Stage 1)

At the start of Stage 1, before processing any inputs, ask the user:

> "Where should I save the pipeline output? Please provide a folder path (e.g., `/path/to/project/output`). I'll create subfolders for stage artifacts and final deliverables."

**If the user provides a path:** Use it as `[output]` for the rest of the pipeline.
**If the user says "here" or points to the workspace root:** Use the workspace root as `[output]`.
**If called from another skill that already set an output path:** Use that path without re-asking.

### Folder structure

Final deliverables (internal requirements and client-ready documents) live under `Generated/`. Working artifacts (`stage_output/`, `source_summaries/`) stay at the `[output]` root.

**Single feature (no split):**

```
[output]/
├── stage_output/                          ← Pipeline working artifacts
│   ├── Stage1-Intake.md
│   ├── Stage2-Interpretation.md
│   ├── Stage3-Variables-Actors.md
│   ├── Stage3.5-Feature-Decomposition.md  ← Always produced (may say "no split needed")
│   ├── Stage4-Scenarios-Matrix.md
│   ├── Stage5-Assumptions.md
│   ├── Stage6-User-Flows.md
│   ├── Stage8-Risk-Analysis.md
│   └── Stage9-Validation-Report.md
├── source_summaries/                      ← Processed inputs from Stage 1
│   ├── [Meeting]_Summary_[date].md
│   ├── Context-Summary-[Design].md
│   └── ...
├── Generated/
│   ├── Internal/                          ← Internal requirements + validation reports
│   │   ├── Feature-Requirements-[Feature].md
│   │   └── reports/
│   └── client-ready/                      ← Client-facing documents (created by sub-skills)
│       ├── Securitas-Client-Requirements-[Feature].md
│       └── Client-Requirements-[Feature].md
```

**Multiple features (split at Stage 3.5):**

```
[output]/
├── stage_output/                          ← Shared pipeline artifacts (Stages 1-3.5)
│   ├── Stage1-Intake.md
│   ├── Stage2-Interpretation.md
│   ├── Stage3-Variables-Actors.md
│   ├── Stage3.5-Feature-Decomposition.md  ← Includes Shared Registry
│   └── Stage9c-Reconciliation.md          ← Post-merge reconciliation report
├── [FeatureA]/                            ← Per-feature working artifacts (Stages 4-9)
│   └── stage_output/
│       ├── Stage4-Scenarios-Matrix.md
│       ├── Stage5-Assumptions.md
│       ├── Stage6-User-Flows.md
│       ├── Stage8-Risk-Analysis.md
│       └── Stage9-Validation-Report.md
├── [FeatureB]/                            ← Per-feature working artifacts
│   └── stage_output/
│       └── ... (same structure)
├── source_summaries/                      ← Shared (processed inputs from Stage 1)
│   └── ...
├── Generated/
│   ├── Internal/                          ← All feature requirements (internal)
│   │   ├── Feature-Requirements-[FeatureA].md
│   │   ├── Feature-Requirements-[FeatureB].md
│   │   └── reports/
│   └── client-ready/                      ← Client-facing documents (created by sub-skills)
│       └── (generated when client-ready sub-skills are invoked)
```

Create `stage_output/`, `source_summaries/`, and `Generated/Internal/` subfolders at the start of Stage 1 (use `mkdir -p`). Per-feature working subfolders are created after Stage 3.5 confirms the split. The `Generated/client-ready/` folder is created by the client-ready sub-skills when invoked, not by the pipeline itself.

### Stage Artifact Registry

Every stage MUST save its output to a markdown file before proceeding to the next stage. This is not optional. **Never present stage output only in chat.** Chat output is ephemeral and lost when context fills up; files persist across the entire pipeline.

| Stage | Save To |
|---|---|
| 1 | `[output]/stage_output/Stage1-Intake.md` |
| 2 | `[output]/stage_output/Stage2-Interpretation.md` |
| 3 | `[output]/stage_output/Stage3-Variables-Actors.md` |
| 3.5 | `[output]/stage_output/Stage3.5-Feature-Decomposition.md` |
| 4 | `[output]/stage_output/Stage4-Scenarios-Matrix.md` (or per-feature) |
| 5 | Same pattern as Stage 4 |
| 6 | Same pattern as Stage 4 |
| 7 | `[output]/Generated/Internal/Feature-Requirements-[Feature].md` |
| 8 | Same pattern as Stage 4 |
| 9 | Same pattern as Stage 4 |
| 9c | `[output]/stage_output/Stage9c-Reconciliation.md` |

**Processed inputs** from Stage 1 (meeting summaries, design context docs) save to `[output]/source_summaries/`.

**Rules:**
- Save the file FIRST, then present a brief summary in chat (max 10-15 lines) with the file path.
- At checkpoint stages (2, 5, 9), tell the user to review the file and confirm. Do NOT dump the full content into chat.
- If a stage needs user confirmation, the file is the artifact they review — not a chat message.
- Each file should end with a `## Next Stage` pointer (e.g., "→ Stage 3: Brainstorm").

---

## Stage 1: Intake & Classification

Read the file:

    stages/01-intake.md

Follow that file's instructions completely from start to finish.
When Stage 1 is complete, return here and proceed to Stage 2.

---

## Stage 2: Interpretation Checkpoint (MANDATORY STOP)

Read the file:

    stages/02-interpretation.md

Follow that file's instructions completely from start to finish.
When Stage 2 is complete, return here and proceed to Stage 3.

---

## Stage 3: Brainstorm — Variables, Constraints, Actors

Read the file:

    stages/03-brainstorm.md

Follow that file's instructions completely from start to finish.
When Stage 3 is complete, return here and proceed to Stage 3.5.

---

## Stage 3.5: Feature Decomposition (MANDATORY CHECKPOINT)

Read the file:

    stages/03.5-decomposition.md

Follow that file's instructions completely from start to finish (includes Execution Model for staggered parallel).
When Stage 3.5 is complete, return here and proceed to Stage 4.

---

## Stage 4: Scenario Matrix

Read the file:

    stages/04-scenarios.md

Follow that file's instructions completely from start to finish.
When Stage 4 is complete, return here and proceed to Stage 5.

---

## Stage 5: Assumptions Identification (MANDATORY CHECKPOINT)

Read the file:

    stages/05-assumptions.md

Follow that file's instructions completely from start to finish.
When Stage 5 is complete, return here and proceed to Stage 6.

---

## Stage 6: User Flows

Read the file:

    stages/06-user-flows.md

Follow that file's instructions completely from start to finish.
When Stage 6 is complete, return here and proceed to Stage 7.

---

## Stage 7: Requirements Document Generation

Read the file:

    stages/07-requirements.md

Follow that file's instructions completely from start to finish.
When Stage 7 is complete, return here and proceed to Stage 8.

---

## Stage 8: Risk Analysis

Read the file:

    stages/08-risk-analysis.md

Follow that file's instructions completely from start to finish.
When Stage 8 is complete, return here and proceed to Stage 9.

---

## Stage 9: Validation — Dedup + Semantic + Structural (MANDATORY FINAL STEP)

Read the file:

    stages/09-validation.md

Follow that file's instructions completely from start to finish.
When Stage 9 is complete, return here and proceed to Stage 9c (if multiple features) or post-pipeline steps.

---

## Stage 9c: Post-Merge Reconciliation (ONLY if multiple features)

Read the file:

    stages/09c-reconciliation.md

Follow that file's instructions completely from start to finish.
When Stage 9c is complete, return here and proceed to the post-pipeline steps.

---

## After Stage 9 (or 9c if split): Update or Create Project Context

After the pipeline completes, offer to create or update the project context:

```
This pipeline run discovered new project-level context (personas, systems,
constraints, terminology). To capture it for future sessions, run
/project-context to create or update your project-context.md.

This is optional but recommended -- it saves significant re-discovery time.
```

The `/project-context` skill handles both first-time creation and incremental updates with source confirmation and conflict detection. Do NOT attempt to create or update `project-context.md` inline -- always redirect to the skill.
