---
name: identify-assumptions
description: "Identify and structure risky assumptions for a feature using multi-perspective analysis (PM, Designer, Engineer) across four risk areas (Value, Usability, Viability, Feasibility). Outputs assumptions in structured format with STATUS, VALIDATE WITH, BY WHEN, and RISK IF WRONG — consistent with the transcript-to-meeting-notes assumption format. Use when stress-testing a feature idea, preparing for stakeholder review, or running assumptions analysis as part of a requirements pipeline."
---

# Identify Assumptions — Structured Risk Analysis

## Purpose

Surface risky assumptions that could undermine a feature if left unvalidated. Outputs in a structured, actionable format that integrates directly into requirements documents and meeting summaries.

**Domain-agnostic.** Works for any feature, any industry, any platform.

---

## Step 1: Gather context

Read all available inputs:
- Feature description, PRD, or requirements document
- Scenario matrix (if available from a prior pipeline stage)
- User flows (if available)
- Meeting transcripts or summaries (if available)
- Any constraints, variables, or rules already identified

If running as part of the `requirements-pipeline`, these inputs are passed from Stage 4 (Scenario Matrix).

---

## Step 2: Multi-perspective analysis

Think through the feature from three perspectives, specifically looking for what could go wrong:

### Product Manager perspective
- Does this solve a real problem? Is the problem validated?
- Will the target users actually use this? Is there adoption risk?
- Does this align with business strategy? Could priorities shift?
- Are the success metrics realistic? Can we actually measure them?
- Are there regulatory, legal, or compliance assumptions?

### Designer perspective
- Will users understand how to use this without training?
- Are there accessibility barriers?
- Does the flow handle all states (empty, error, loading, edge cases)?
- Are there assumptions about user behavior that haven't been validated?
- Is the cognitive load reasonable for the target user?

### Engineer perspective
- Can this be built with existing infrastructure, or does it require new systems?
- Are there performance assumptions (response time, data volume, concurrency)?
- Are there integration dependencies that could delay or block delivery?
- Are there assumptions about data availability, format, or quality?
- Are there assumptions about third-party system behavior or SLAs?

---

## Step 3: Categorize by risk area

Group assumptions into four risk areas:

| Risk Area | What It Covers | Key Question |
|---|---|---|
| **Value** | Will it create value? Does it solve a real problem? | "If this assumption is wrong, does anyone want this feature?" |
| **Usability** | Will users figure out how to use it? | "If this assumption is wrong, will users fail or abandon the flow?" |
| **Viability** | Can the business support it? (Legal, ops, finance, marketing) | "If this assumption is wrong, can we ship or sustain this?" |
| **Feasibility** | Can it be built? (Tech, integrations, data, performance) | "If this assumption is wrong, can we build this on time and budget?" |

---

## Step 4: Structure each assumption

**Every assumption MUST use this format:**

```markdown
### ASSUMPTION: [Clear, falsifiable statement]
- **SOURCE:** [Where this assumption originated — e.g., "March 11 transcript, Decision 3", "FigJam flow, Screen 2", "PRD v0.1, Section 4", "Engineer brainstorm", or "Implicit — not stated in any input"]
- **STATUS:** [Not confirmed / Partially confirmed / Confirmed / Contradicted]
- **RISK AREA:** [Value / Usability / Viability / Feasibility]
- **EVIDENCE:** [What supports this assumption — cite source document and section, or "None — untested"]
- **VALIDATE WITH:** [Specific person, role, or team] | **BY WHEN:** [Date, milestone, or "Before [stage]"]
- **RISK IF WRONG:** [Concrete consequence — what changes in the design, what gets blocked, what breaks]
- **SUGGESTED TEST:** [How to validate — question to ask, data to check, experiment to run]
```

### Rules for good assumptions:
- **Falsifiable.** "Users will like this" is not falsifiable. "Officers will complete the attestation in under 10 seconds" is.
- **Specific.** "The system works" is not specific. "WFM API returns penalty pay records within 3 seconds" is.
- **One assumption per block.** Don't combine multiple assumptions into one.
- **Traceable.** Every assumption must have a SOURCE. If it came from a meeting, cite the meeting date and decision number. If it came from a design, cite the screen or flow. If it was surfaced during analysis (not in any input), say "Implicit" — this flags it for extra validation.

---

## Step 5: Prioritize assumptions

After identifying all assumptions, sort them by risk level:

| Priority | Criteria | Action |
|---|---|---|
| **HIGH** | If wrong, blocks the feature or creates legal/compliance/financial exposure | Must validate before design begins |
| **MEDIUM** | If wrong, degrades quality or requires significant rework | Should validate before development begins |
| **LOW** | If wrong, minor impact — can be corrected post-launch | Track and validate opportunistically |

Present assumptions grouped by priority, then by risk area within each priority group.

---

## Step 6: Cross-reference with scenario matrix (if available)

If a scenario matrix exists from a prior pipeline stage:

| Check | What to look for |
|---|---|
| **Uncovered scenarios** | Are there scenarios in the matrix that depend on an unvalidated assumption? Flag them. |
| **Boundary assumptions** | Are the threshold values in the matrix assumed or confirmed? (e.g., "3.5 hours" — is this validated?) |
| **Missing actor assumptions** | Does the matrix assume an actor will behave a certain way without validation? |

---

## Step 7: Present for review

Present the full assumptions list to the user:

```markdown
## Assumptions Analysis: [Feature Name]

**Total assumptions identified:** [N]
**By priority:** [X] HIGH, [Y] MEDIUM, [Z] LOW
**By risk area:** [N] Value, [N] Usability, [N] Viability, [N] Feasibility

---

### HIGH — Must validate before design

[Assumption blocks in structured format]

### MEDIUM — Should validate before development

[Assumption blocks]

### LOW — Track and validate opportunistically

[Assumption blocks]
```

**Save the output as:** `[Feature]-Assumptions.md`

---

## Step 8: Integration with requirements document

When assumptions are incorporated into a requirements document:

1. **Assumptions table** — Add each assumption as a numbered row in the document's assumptions section, preserving the SOURCE / STATUS / VALIDATE WITH / BY WHEN fields. The SOURCE column links the assumption back to its origin (transcript, design, stakeholder, or "Implicit").
2. **Inline references** — Where an assumption affects a specific requirement or flow, add `(See Assumption [N])` inline.
3. **Dependencies** — HIGH-priority unvalidated assumptions should also appear in the Dependencies & Blockers section with an owner and impact statement.
4. **Source traceability** — Every requirement, decision, and assumption in the final document should be traceable to its origin input. Use the format `(Source: [input name, section/decision])` — e.g., `(Source: March 11 transcript, Decision 3)` or `(Source: FigJam flow, Screen 2)`. Assumptions surfaced during analysis that were not in any input should be tagged `(Source: Implicit — surfaced during assumption analysis)`.

---

## Critical Rules

1. **Never fabricate evidence.** If an assumption has no supporting evidence, say "None — untested." Don't invent sources.
2. **Be constructive.** The goal is to strengthen the feature, not kill it. Every assumption should have a suggested test.
3. **Falsifiable statements only.** If you can't imagine evidence that would disprove the assumption, it's not specific enough.
4. **Domain-agnostic.** Don't assume a specific industry, tech stack, or regulatory environment unless the inputs specify one.
5. **Consistent format.** Every assumption uses the exact template from Step 4. No exceptions. This ensures downstream skills (document-audit, requirements generation) can parse and cross-reference them.
