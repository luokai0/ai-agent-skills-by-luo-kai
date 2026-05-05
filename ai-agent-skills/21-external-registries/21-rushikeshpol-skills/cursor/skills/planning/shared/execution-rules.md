# Execution Rules — Shared Across All Planning Skills

**Referenced by:** All 5 planning skills via `MANDATORY READ` at intake and generate steps.

---

## NON-NEGOTIABLE Rules (all skills start with these)

1. Save every artifact to file before presenting in chat. Chat is ephemeral.
2. Never fabricate dates, numbers, statuses, or capacity. Unknown = `[TBD]`. Inferred = `[INFERRED]`.
3. Never skip checkpoints. Every CHECKPOINT requires user confirmation before proceeding.
4. Graded provenance: authoritative claims (dates, capacity numbers, statuses, decisions, constraints) require a source tag. Synthesized analysis uses `(Synthesized from: ...)`. Process scaffolding (section framing, transitions) is exempt. Missing source on an authoritative claim = flag as `(Source: Implicit)` for resolution.
5. One stage at a time. Complete and save before starting the next.
6. Re-read upstream documents at the start of every workflow. Never rely on cached context.

---

## Quality Criteria

Every document produced by a planning skill must meet five base criteria:

| Criterion | Standard | Delivery Addition |
|-----------|----------|------------------|
| **Accurate** | All facts sourced and correct | -- |
| **Complete** | No required sections empty, no items silently dropped | -- |
| **Practical** | Actionable by the team | No abstract statements like "ensure quality" — concrete: "QA runs regression suite on iOS 16+ and Android 12+" |
| **Clear** | Readable by the intended audience | Sprint goals written from user perspective, not developer perspective. Two-audience structure: top section for stakeholders, detail sections for the team. |
| **Structured** | Consistent formatting and organization | Ticket tables always include: ID, Title, Status (where applicable), Owner (where applicable). Dates in Mon DD format within sprint docs, full date in release-level docs. |

---

## Self-Check Priority Structure

Every skill's generate stage runs a self-check with priority levels before saving.

### Shared Priority 1 — Hard gate (regenerate if fails)
- [ ] Every input item appears in the output (none dropped)
- [ ] Primary goal/purpose is user-facing, not technical
- [ ] No required section is empty
- [ ] Source attribution present on authoritative claims (dates, numbers, statuses, decisions, constraints)

### Shared Priority 2 — Edit gate (fix before saving)
- [ ] Every risk/blocker has a mitigation or owner
- [ ] Every "done" criterion maps to actual work
- [ ] Guardrail results addressed (not ignored)
- [ ] No unresolved `(Source: Implicit)` on authoritative claims — each must be resolved to a source tag, downgraded to `[TBD]`, or marked `[INFERRED]`

### Shared Priority 3 — Note and proceed
- [ ] Template structure fully followed
- [ ] Date formatting consistent (Mon DD for sprint docs, full date for release docs)
- [ ] Terminology consistent with prior documents in the chain

---

## Graded Provenance Model

Not all content in a planning document carries the same epistemic weight. Apply provenance rules proportionally:

### Content Classes

| Class | Examples | Provenance Required |
|-------|----------|-------------------|
| **Authoritative claims** | Dates, capacity numbers, statuses, decisions, constraints, thresholds | Source tag required: `(Source: [document], [section])` |
| **Synthesized analysis** | Multi-source summaries, clustered insights, pattern identification | Lighter tag: `(Synthesized from: SRC-1, SRC-3)` |
| **Inference** | Gap-fills, extrapolations, probable-but-unconfirmed conclusions | Mark as `[INFERRED]` with reasoning |
| **Process scaffolding** | Section framing, transitions, checkpoint instructions, user prompts | No provenance needed |

### Synthesis vs Inference Boundary

Multi-source summaries that combine stated facts without gap-filling are **synthesized analysis**.
Reserve `[INFERRED]` for conclusions that extrapolate beyond what sources explicitly state.

Example: "Clock-in is highest-priority based on scope doc + ticket count" is synthesis if both sources say so; it is inference if neither source explicitly ranks priorities.

### Resolution Rules

- `(Source: Implicit)` is a temporary warning state, not a final classification
- Every `(Source: Implicit)` on an authoritative claim must be resolved: find the source, downgrade to `[TBD]`, or mark `[INFERRED]`
- `[TBD]` means "we need this information but don't have it yet"
- `[INFERRED]` means "this is our best guess — confirm or correct"

---

## STATED vs INFERRED Pattern

Applied at key gates where a skill infers from data rather than quoting sources. Present an inference register separating extracted context from inferred conclusions:

```
## STATED (extracted from sources)
- [Fact]: "[value]" (Source: [document], [section])

## INFERRED (needs your confirmation)
- [Conclusion]
  → Reasoning: [why this was inferred] (Based on: [evidence])
```

The user must confirm, correct, or reject every INFERRED item before the skill proceeds.

---

## Checkpoint Types

| Type | Behavior | When to Use |
|------|----------|-------------|
| **Hard stop** | STOP and WAIT. Do not proceed until user confirms. | Before irreversible steps (generating final doc, applying changes) |
| **Review gate** | Present output, ask for feedback. May iterate. | After drafts that the user may want to adjust |
| **Notification** | Announce what was done, proceed unless user intervenes. | After intake normalization, intermediate saves |

---

## Anti-Momentum Gate

Before any step that interprets, analyzes, or generates content, pause and verify:
1. Am I acting on confirmed information or my own assumptions?
2. Is the source a user-confirmed artifact, not my earlier reasoning?
3. Could this step be wrong? If yes, flag rather than proceed silently.

This prevents the common failure mode where a skill builds momentum and starts generating plausible-but-unsourced content.
