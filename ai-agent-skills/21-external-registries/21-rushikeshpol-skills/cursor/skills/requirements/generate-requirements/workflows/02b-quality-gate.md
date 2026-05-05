# Step 3.5-4: Quality Gate (Deduplication + Inline Checks)

**Called from:** `workflows/02-generate.md` after all sections are generated
**Next step:** Return to `workflows/02-generate.md` Step 5: Present Document

---

## Step 3.5: Cross-Section Deduplication

After generating all sections, scan the document for items that appear in more than one section. Each item gets exactly one home based on what it **is**:

| Classification | Definition | It is NOT also... |
|---|---|---|
| **Hard Constraint** | Non-negotiable system rule (regulatory, legal, timeline) | a dependency or limitation |
| **Dependency** | Deliverable another team must provide before we can build | an assumption or limitation |
| **Assumption** | Something we believe but haven't confirmed; carries risk if wrong | a dependency (if it has an owner and delivery status, it's a dependency) |
| **Known Limitation** | Confirmed gap we are shipping with (accepted trade-off) | a dependency (if it's blocking and has an owner, it's a dependency) |
| **Open Question** | Stakeholder decision needed before proceeding | an assumption or dependency (if it needs a decision, the OQ owns it) |

**Scan these sections for overlap:**
- Section 2 (Business Context / Constraints)
- Section 7 (Compliance & Constraints)
- Section 11 (Known Limitations)
- Section 13 (Assumptions & Dependencies)
- Section 15 (Open Questions / TBD Items)

**Tiebreaker rules (apply in order):**

1. **Assumption + Dependency overlap:** Keep the Dependency row (it has owner + status). Delete the Assumption row.
2. **Known Limitation + Dependency overlap:** Keep the Dependency row. Delete the Known Limitation bullet.
3. **Constraint + Dependency overlap:** Keep the Constraint only if there is a non-negotiable rule to state (e.g., "payroll must never be blocked"). If the constraint bullet is just restating the dependency, delete it.
4. **Assumption + Open Question overlap:** Keep the Open Question. Delete the Assumption row. The OQ is the primary artifact for items needing decisions.
5. **Dependency + Open Question overlap:** Keep both ONLY IF the OQ asks a different question than "will this be delivered?" If the OQ is just "can X team provide Y?", keep the dependency row and delete the OQ. If the OQ asks a design/policy question dependent on the deliverable, keep both.
6. **Two OQs on the same topic at different scopes:** Merge into one OQ. Absorb the sub-question into the primary question text.
7. **Two Constraint bullets stating the same rule:** Keep one. Prefer the version with more specificity.
8. **Confirmed assumptions are not assumptions.** If status is "Confirmed," delete. If the confirmed fact creates a trade-off, move it to Known Limitations.
9. **When deleting a duplicate, absorb useful context** (risk consequence, impact description) into the surviving instance.
10. **Update all cross-references** after deduplication. If Assumption #3 becomes #2, update any FR business rules that reference "Assumption #3."

**After this pass, every fact in the document must appear in exactly one of the five categories.** Proceed to Step 4.

---

## Step 4: Inline Quality Check

Before presenting the document to the user, run these checks:

**Completeness:**
- [ ] All required sections present
- [ ] No [TBD] without explanation and stakeholder routing
- [ ] Source attribution meets threshold (Tier 1 = 100%, Tier 2 = 60%+ target)

**Clarity:**
- [ ] Plain English throughout (no code, no jargon without explanation)
- [ ] All requirements are specific and testable ("System must X within Y seconds")
- [ ] No vague language ("should consider", "might", "probably")

**Requirement Purity:**
- [ ] No FR contains implementation mechanisms (HOW) — solutions belong in Implementation Notes
- [ ] No FR prescribes UI layout or navigation patterns (WHAT IT LOOKS LIKE) — design decisions belong in Open Questions
- [ ] Each business rule is testable — a QA engineer could write a pass/fail test without asking clarifying questions

**Source Accuracy:**
- [ ] Every `(Source: SRC-N)` citation was verified against the actual source content
- [ ] No source is cited for content it does not contain
- [ ] Statements tagged `(Source: Implicit)` are genuinely logical derivations, not gap-fills that should be `[TBD]`
- [ ] No scoped statement has been over-generalized (source says "X in context A" but doc says "X everywhere")

**Cross-Section Deduplication:**
- [ ] Zero items appear in more than one of: Constraints (section 2 + 7), Known Limitations (section 11), Assumptions (section 13), Dependencies (section 13), Open Questions (section 15)
- [ ] Zero items appear in both Assumptions and Open Questions (if it needs a decision, the OQ owns it)
- [ ] Zero Known Limitation bullets restate a Dependency that has an owner and delivery status
- [ ] All cross-references are current (assumption/OQ numbers updated after any renumbering from dedup)

**Table Formatting:**
- [ ] Every priority/risk/severity indicator uses a labeled format, never a bare dot:
  - `🔴 Critical` not `🔴`
  - `🟡 Important` not `🟡`
  - `🟢 Nice to have` not `🟢`
- [ ] Tables are sorted by highest priority/risk/severity first:
  - **Open Questions** -- sorted by priority (🔴 Critical → 🟡 Important → 🟢 Nice to have). Resolved questions sink to the bottom.
  - **Dependencies** -- sorted by risk (🔴 Critical → 🟡 Medium → 🟢 Low)
  - **Assumptions** -- sorted by risk tier (H = High → M = Medium → L = Low)
  - **Risks** -- sorted by impact (highest first)

**Fix any failures before presenting.** Do not present documents with known quality failures.

**FR Verbosity:**
- [ ] (P1) No intra-FR duplicate bullets: scan each FR's Business Rules list. If two bullets state the same fact in different words, merge into the more complete version. Keep the version that specifies what happens, not just that it happens.
- [ ] (P5) No inline annotation tags in business rules: flag and remove `[Display layout, Design Decision]`, `[Design Decision]`, `[TBD - Design]` tags. The fact behind the tag is kept; the tag itself is stripped.
- [ ] (P5) No working notes masquerading as business rules: flag any bullet that reads as an unresolved observation ("In some situations X might...") rather than a stated rule. Either convert to a rule with a condition or move to Open Questions.
- [ ] (P6) Single fact per bullet: flag compound bullets containing two unrelated facts joined by a semicolon. Split into two separate bullets unless the facts are causally inseparable (cause → effect is fine to keep together).
- [ ] (P6) Rules in the right section: audit trail access control (who can view audit data) belongs in Compliance & Constraints, not inside individual FRs. Flag and relocate.

---

Quality gate complete. Return to `workflows/02-generate.md` and proceed to Step 5: Present Document.
