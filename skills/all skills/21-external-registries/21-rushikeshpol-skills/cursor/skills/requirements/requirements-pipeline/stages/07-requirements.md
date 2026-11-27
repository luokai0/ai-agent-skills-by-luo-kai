# Stage 7: Requirements Document Generation

**Called from:** `SKILL.md` (Pipeline Orchestrator)
**Next step:** Return to `SKILL.md` for Stage 8: Risk Analysis
**Saves to:** `[output]/Generated/Internal/Feature-Requirements-[Feature].md`

---

**Call the `generate-requirements` skill, skipping its intake step (SKILL.md Steps 1-3).** The pipeline has already gathered all required context. Go directly to Workflow 1 (`workflows/01-synthesize.md`).

**Pipeline provides these values (do not re-ask the user):**
- **Feature name:** determined in Stage 1
- **Mode:** always **Comprehensive** (6 contexts) -- the pipeline is the thorough path
- **Inputs:** all processed inputs from Stage 1, scenario matrix from Stage 4, assumptions from Stage 5, user flows from Stage 6 (after purity filter)
- **Output folder:** use `[output]` path established in Stage 1. Do NOT re-ask.
- **Project context:** loaded from Stage 1.1 (if `project-context.md` existed)
- **Current state:** from Stage 1.5 (if available)
- **New or existing:** determined in Stage 1.5

The skill then runs its 3-workflow pipeline (synthesize → generate → validate) with all context pre-loaded.

**Important:** Pass the scenario matrix and assumptions as explicit inputs -- they contain information that may not be in the original source documents.

**Source traceability:** Instruct the skill to tag every requirement, decision, assumption, and key fact in the output document with its source. Use the source IDs assigned in Stage 1 (e.g., `(Source: SRC-1, Decision 3)`). Requirements that synthesize multiple inputs should list all sources.

**Source verification pass (MANDATORY after generation):** After the requirements document is generated, perform a source verification pass:
- For each `(Source: SRC-N)` citation, go back to the actual source and verify it contains the claimed information.
- Check for **over-generalization** — if a source says "X in context A", the requirement must not say "X in all contexts" without additional sourcing.
- Check for **misattribution** — if a source is cited but does not actually contain the claimed fact, flag it as `[SOURCE UNVERIFIED — SRC-N does not contain this claim]`.
- Any requirement tagged `(Source: Implicit)` should be reviewed: is it truly a logical derivation, or is it a gap-fill that should be `[TBD]`?

**Requirement purity enforcement:** Instruct the skill to apply these language rules:
- Requirements describe WHAT (capability), never HOW (implementation) or WHAT IT LOOKS LIKE (UI pattern).
- If a statement prescribes an implementation approach, reframe it as the underlying need and add an "Implementation Note" callout.
- If a statement prescribes a UI pattern, move it to Open Questions / Design Decisions unless the user explicitly confirmed the design in a prior stage.

---

Stage 7 complete. Return to `SKILL.md` and proceed to Stage 8: Risk Analysis.
