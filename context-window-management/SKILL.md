---
name: context-window-management
description: Use when an AI agent's working context is growing large, degrading output quality, risking truncation, or when designing how an agent should select, compress, persist, and hand off information across long multi-step tasks.
author: Luo Kai
provenance: original
version: 1.2.0
---

# Context Window Management

## Purpose and boundaries

This skill governs how an agent decides what stays in its active context, what is compressed, what is externalized to durable storage, and what is discarded. It applies to long-running agent sessions, multi-file code changes, research synthesis, log and document triage, and multi-agent handoffs.

Out of scope: choosing or fine-tuning models, changing provider billing or rate limits, and designing retrieval infrastructure. Where those matter, flag them and hand off.

## Inputs and assumptions

Before acting, establish:

- The task goal and its completion criteria, stated in one or two sentences.
- The available context budget. Treat the exact token limit as version-sensitive; verify against current provider documentation rather than assuming a figure.
- The current context composition: system instructions, tool outputs, file contents, conversation history, and retrieved material.
- Whether a persistent scratch store (file, notes, task tracker) is available and writable.
- Data sensitivity of the material being carried forward (credentials, personal data, proprietary code).

If the budget is unknown, assume it is finite and measure usage by estimated character or token counts of each block.

## Operating workflow

1. **Inventory.** List each context block with an approximate size, its source, and whether it is needed for the next action.
2. **Classify each block** into one of four categories:
   - *Keep verbatim*: exact code being edited, active error messages, specifications with precise wording, values that must not be paraphrased.
   - *Summarize*: completed subtask results, long tool outputs where only conclusions matter.
   - *Externalize*: reference material, logs, large datasets. Write to a file with a stable path and keep only the path and a one-line description in context.
   - *Drop*: superseded attempts, redundant restatements, raw output already reflected in a summary.
3. **Compress with provenance.** Each summary must record source paths or identifiers, the date or step where the fact was established, and any uncertainty. A summary without provenance is not admissible as evidence later.
4. **Maintain a state file.** Keep a single working file containing: goal, completed steps, open decisions, key facts with sources, and next action. Update it at each milestone. Reload it instead of re-reading history.
5. **Retrieve on demand.** Pull externalized content back only for the specific lines or sections needed. Prefer targeted reads (line ranges, searches, named sections) over full reloads.
6. **Checkpoint before large operations.** Before a bulk read or a long generation, confirm the state file reflects current progress.

## Decision gates

Proceed to the next step only when:

- Each kept-verbatim block is still needed for the immediate next action.
- Every summary has provenance and no unresolved contradictions with other blocks.
- The state file matches the actual repository, document, or system state (checked by reading the source, not memory).

Stop and request approval before:

- Deleting or overwriting externalized notes, logs, or state files that others may depend on.
- Sending any context outside the session (uploading to third-party tools, posting to tickets, sharing with other agents outside the sanctioned workflow).
- Carrying credentials, tokens, personal data, or confidential material into summaries or external stores. Redact first, or obtain explicit approval.
- Taking irreversible actions (migrations, sends, production changes) whose correctness depends on a compressed summary rather than the source.

## Verification and evidence

- **Round-trip check:** For each summary of a critical fact, re-read the source and confirm the value, identifier, or condition matches exactly. Record the check result in the state file.
- **Count check:** When summarizing lists (failing tests, affected files, outstanding items), compare counts against the source command output.
- **Staleness check:** After any edit or external change, mark dependent summaries as stale and regenerate them.
- **Quality metrics:** Track the proportion of summaries re-verified (target: 100% for facts used in a decision), the number of stale facts found at checkpoints (target: zero unhandled), and the number of retrieval re-reads per milestone (rising counts signal poor externalization).

## Failure handling

- **Lost detail discovered:** Re-read the source, restore the exact text to the state file, and note the omission as a process gap.
- **Contradictory facts:** Do not pick silently. Record both with sources, verify against the authoritative source, and keep the verified one.
- **Budget exhaustion mid-task:** Write the state file immediately, list the next three actions, and continue from a fresh context by reloading only the state file and the minimal required source sections.
- **Summary drift after multiple compression passes:** Discard the chain of summaries and rebuild from primary sources.
- **Tool output too large:** Redirect to a file, then query it with filters rather than ingesting it whole.

## Domain examples

- *Code refactor across 40 files:* keep the function being changed verbatim; summarize the call-site list as a file with paths and line numbers; externalize the test log and reference only the failing test names.
- *Literature or policy review:* store each source excerpt in a file keyed by citation; summaries carry the citation and the page or section.
- *Incident triage:* keep the first error and the most recent error verbatim; externalize the full log and record timestamps in the state file.

## Deliverable contract

The agent's final output for a context-managed task must include:

1. The state file (goal, steps, decisions, sourced facts, verification results, open items).
2. A list of externalized artifacts with paths and one-line descriptions.
3. Verification results with counts and any stale or unresolved items.
4. An explicit statement of anything withheld pending approval.

## What not to do

- Do not rely on memory of compressed content for irreversible or externally visible actions.
- Do not summarize without recording sources.
- Do not discard the only copy of a non-reproducible output.
- Do not paste full logs or files into context when a targeted read suffices.
- Do not state specific token limits, model capacities, or tool parameters as fact without checking current official documentation.
## Context budgeting, compaction, and lossless continuity (v1.1)

Treat context as a budgeted working set, not a transcript that must grow forever. Separate durable task state from conversational history. Keep the active objective, constraints, authority, current plan revision, pending dependencies, last verified checkpoint, unresolved risks, and next action in a compact state record. Store bulky source material and artifacts externally with stable references and provenance.

Use progressive disclosure: load a short capability index first, then retrieve the relevant skill section, source document range, or tool schema only when needed. Prefer targeted reads over full-file injection. Keep canonical evidence outside summaries so a compressed brief never becomes the only surviving copy.

Before compaction, identify facts that must remain exact: identifiers, amounts, dates, resource targets, approval state, version pins, source references, and unresolved uncertainty. Preserve these in structured fields rather than paraphrasing. Mark each retained statement as verified, inferred, user-provided, stale, or unresolved. Include the checkpoint revision and references to the full event history.

After compaction, validate that the objective, constraints, authorization, completed effects, pending work, and next safe step are still recoverable. If any critical field is missing or contradictory, reload the source evidence instead of guessing. Never rely on compressed context to authorize irreversible actions.

Measure context efficiency by successful task completion, factual retention, tool-call correctness, and recovery quality, not token reduction alone. Test long-running tasks, conflicting updates, repeated compaction, stale references, and resume after process restart.

## Ultron routing contract

**Choose this skill when:** an active agent run is approaching context limits and needs budgeting, relevance selection, compaction, summarization, or lossless preservation of task-critical state.

**Choose `agent-memory-persistence` when:** deciding what information should survive across tasks or sessions as durable, source-attributed memory.

**Choose `session-continuity-recall` when:** reconstructing a particular previous or interrupted run, verifying what happened, and deciding what can safely resume.

**Handoff contract:** compaction must preserve current objective, constraints, authorization/approval state, pending side effects, task identifiers, source provenance, unresolved decisions, and verification evidence. Durable memory receives only information approved for long-term retention; session recall uses task records to rebuild an active execution state.

**Why the boundary exists:** context management compresses the current working set; memory persists selected knowledge; session continuity reconstructs a specific execution history.
