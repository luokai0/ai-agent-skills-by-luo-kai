# Stage 9: Validation — Dedup + Semantic + Structural (MANDATORY FINAL STEP)

**Called from:** `SKILL.md` (Pipeline Orchestrator)
**Next step:** Return to `SKILL.md` for Stage 9c (if multiple features) or post-pipeline steps
**Saves to:** `[output]/stage_output/Stage9-Validation-Report.md`

---

## 9.0 Within-document deduplication (always runs first)

Before running validation, apply a within-document dedup pass. This catches items introduced or re-introduced by Stage 8 (risk merge) that bypassed Step 3.5 of generate.

Scan the Constraints, Dependencies, Assumptions, Known Limitations, and Open Questions sections. Each item gets exactly one home:

| Classification | Definition | It is NOT also... |
|---|---|---|
| **Hard Constraint** | Non-negotiable system rule (regulatory, legal, timeline) | a dependency or limitation |
| **Dependency** | Deliverable another team must provide before we can build | an assumption or limitation |
| **Assumption** | Something we believe but haven't confirmed; carries risk if wrong | a dependency (if it has an owner and delivery status, it's a dependency) |
| **Known Limitation** | Confirmed gap we are shipping with (accepted trade-off) | a dependency (if it's blocking and has an owner, it's a dependency) |
| **Open Question** | Stakeholder decision needed before proceeding | an assumption or dependency (if it needs a decision, the OQ owns it) |

**Tiebreaker rules:**

1. Assumption + Dependency overlap: keep Dependency, delete Assumption
2. Known Limitation + Dependency overlap: keep Dependency, delete Known Limitation
3. Constraint + Dependency overlap: keep Constraint only if it states a non-negotiable rule; otherwise delete it
4. Assumption + Open Question overlap: keep Open Question, delete Assumption
5. Dependency + Open Question overlap: keep both only if the OQ asks a design/policy question separate from delivery
6. Two OQs on the same topic: merge into one
7. Two Constraint bullets for the same rule: keep the more specific one
8. Confirmed assumption: delete or move to Known Limitations if it creates a trade-off
9. Absorb useful context from deleted duplicates into the surviving instance
10. Update all cross-references after renumbering

Record the count of duplicates resolved. Include in the validation report.

## 9.1 Combined validation (semantic + structural)

**Read and follow the `validate-requirements` skill** on the requirements document (after 9.0 dedup is applied).

This skill performs 15 checks in a single pass:

**Semantic checks (content accuracy):**
- **Is it true?** — Source accuracy, inference detection, over-generalization, actor capability
- **Is it a requirement?** — Requirement purity (not a solution or design decision)
- **Is it actionable?** — Testability, ambiguity detection
- **Is it complete and safe?** — Assumption-requirement dependency, negative path coverage, scope boundary, intra-document consistency

**Structural checks (document integrity):**
- Staleness — `[PENDING]`, `[TBD]`, `[UNKNOWN]` markers answered elsewhere
- Contradictions between sections
- Broken cross-references
- Completeness gaps (orphaned sections, empty tables, missing owners)

**Inputs to provide:**
- The requirements document from Stage 7 (after dedup)
- The source documents folder (meeting summaries, client docs, design descriptions from Stage 1)
- Sibling requirements docs (if multiple feature docs were generated)

**Fix all Critical findings immediately.** Present Should Fix and Verify findings to the user for decision. Include the count of within-document duplicates resolved in 9.0.

**STOP and WAIT for user to review the findings.** Do not mark the document as final until the user confirms all findings are resolved.

---

Stage 9 complete. Return to `SKILL.md` and proceed to Stage 9c (if multiple features) or post-pipeline steps.
