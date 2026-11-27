# Semantic Checks (1–11) — Content Accuracy

Run these checks in order. Checks 1–4 and 10 require the source index built in Phase 1.
Check 11 must run after Checks 1–10 (it uses their findings).

For each finding, record: location in doc (section + line), the problematic text, the verdict, and the recommendation.

### Incremental Mode

Each check below includes an **Incremental skip condition** block. In incremental mode (Phase 0 detected a prior report), use these conditions to determine whether the check should RE-RUN, RE-RUN (scoped), or CARRY FORWARD. In full mode, ignore these blocks and run every check.

---

## Check 1: Source Accuracy Audit

**Dimension: Is it true?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no source files have changed (Phase 0.3) AND no new or modified `(Source: SRC-N)` citations exist in changed sections (Phase 0.2)
> - **RE-RUN (scoped)** if: sources are unchanged but the document has new or modified SRC citations — run only on the new/modified citations, carry forward findings for unchanged ones
> - **RE-RUN** if: any source file has been modified since the prior report

For every `(Source: SRC-N)` citation in the document:

1. Read the cited source
2. Verify the source actually contains the claimed information
3. Classify each citation:

| Verdict | Meaning |
|---|---|
| **ACCURATE** | Source directly states the claimed fact |
| **PARTIALLY ACCURATE** | Source says something related but the doc generalizes or reinterprets |
| **INACCURATE** | Source does not contain the claimed information |
| **UNVERIFIABLE** | Source is not available or cannot be checked |

For PARTIALLY ACCURATE and INACCURATE findings: show what the source actually says vs. what the doc claims.

For statements tagged `(Source: Implicit)`: flag for user validation — implicit means no source backs it. Determine if it is a valid logical derivation or a gap-fill that should be `[TBD]`.

---

## Check 2: Inference Detection

**Dimension: Is it true?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no FR text, business rule text, or user flow text has changed in the document
> - **RE-RUN (scoped)** if: only specific FRs or sections have changed — run on changed FRs/sections only, carry forward findings for unchanged ones
> - **RE-RUN** if: widespread changes across the document

Scan for statements that appear factual but are actually inferred:

- Statements about "current state" or "currently" — verify against a confirmed current-state source (design description, existing Figma, user confirmation)
- Pain points that assume a user experience not described in any source
- Field lists or data attributes not traceable to any source
- Behavior descriptions with no source citation (especially in user flows and business rules)
- "Confident-sounding" language: definitive statements without `[TBD]` that have no source

For each finding, classify:

| Verdict | Meaning |
|---|---|
| **CONFIRMED** | Inference is backed by a source (may just be missing the citation) |
| **PLAUSIBLE** | Inference is reasonable but not sourced — needs user confirmation |
| **FABRICATED** | No basis in any source — must be removed or tagged `[TBD]` |

---

## Check 3: Requirement Purity Classification

**Dimension: Is it a requirement?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no FR text or business rule text has changed, AND no changes to Executive Summary, UX Context, User Flows, Visual States, or Error Handling sections
> - **RE-RUN (scoped)** if: only specific FRs or non-FR sections have changed — run on changed FRs/sections only, carry forward findings for unchanged ones
> - **RE-RUN** if: widespread changes across the document

For each Functional Requirement and its business rules, classify:

| Classification | Definition | Action |
|---|---|---|
| **REQUIREMENT** | Describes a capability or constraint from the user's perspective. Observable, testable, solution-free. | Keep |
| **SOLUTION** | Prescribes an implementation approach (e.g., "cache locally", "use delta API", "batch hourly", "retry with exponential backoff") | Flag for reframing as the underlying need + "Implementation Note" |
| **DESIGN** | Prescribes a UI pattern, layout, or navigation structure (e.g., "organized as tabs", "show as Past/This Week/Future", "swipe left/right to navigate") | Flag for reframing as the underlying need + "Open Question / Design Decision" |

**Also check these sections** (solutions and design prescriptions often hide outside the FRs):
- Executive Summary
- UX Context
- User Flows
- Visual States
- Error Handling

---

## Check 4: Over-Generalization Detection

**Dimension: Is it true?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no source files have changed (Phase 0.3) AND no FR scope language or sourced statements have been modified
> - **RE-RUN (scoped)** if: sources are unchanged but FRs with scope-related language have changed — run only on changed sourced statements
> - **RE-RUN** if: any source file has been modified since the prior report

For each sourced statement, check scope alignment:

- Does the source say "X in context A" but the doc says "X in all contexts"?
- Does the source describe a field for one view type but the doc applies it to all views?
- Does the source describe a rule for one actor but the doc applies it to all actors?
- Does the source describe behavior for one scenario but the doc states it as a universal rule?

**Pattern:** Find the source -> check its scope -> compare to the doc's scope -> flag if broader.

---

## Check 5: Scope Boundary Check (Cross-Document)

**Dimension: Is it complete and safe?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no sibling requirements docs have changed (Phase 0.3) AND the document's scope sections (In Scope, Out of Scope, FR list) are unchanged
> - **RE-RUN** if: any sibling doc has been modified, OR the document's scope sections have changed

*Skip if no sibling requirements docs are available. Mark as SKIPPED.*

If sibling requirements docs exist in the same folder:

- Identify overlapping FRs — the same user experience documented in two places
- Identify contradictory rules — different thresholds, different behaviors for the same scenario
- Identify unclear boundaries — where one feature ends and another begins is ambiguous
- Flag for consolidation or cross-referencing

---

## Check 6: Testability

**Dimension: Is it actionable?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no FR text or business rule text has changed
> - **RE-RUN (scoped)** if: only specific FRs have changed — run on changed FRs only, carry forward findings for unchanged ones
> - **RE-RUN** if: widespread FR changes or new FRs added

For each FR and its business rules, check if it can be verified with a pass/fail test:

- **Vague outcomes:** "user-friendly", "fast", "intuitive", "seamless", "easy to use"
- **Missing specifics:** "within a reasonable time" (what time?), "large number of" (how many?), "appropriate error message" (what message?)
- **Undefined conditions:** "if available", "when applicable", "as needed"
- **Unmeasurable qualities:** "improved experience", "better performance", "enhanced security"

Each business rule should be specific enough that a QA engineer could write an acceptance test without asking clarifying questions.

---

## Check 7: Ambiguity Detection

**Dimension: Is it actionable?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no FR text or business rule text has changed
> - **RE-RUN (scoped)** if: only specific FRs have changed — run on changed FRs only, carry forward findings for unchanged ones
> - **RE-RUN** if: widespread FR changes or new FRs added

Scan for language that weakens requirements or defers decisions to developers:

| Pattern | Examples | Recommendation |
|---|---|---|
| **Weak modals** | "should", "may", "could", "might" | Replace with "must" or remove |
| **Vague quantifiers** | "some", "many", "few", "quickly", "periodically", "regularly" | Assign specific values or mark `[TBD]` |
| **Escape hatches** | "appropriate", "relevant", "as needed", "etc.", "and so on", "similar" | Make precise or enumerate explicitly |
| **Passive voice hiding actor** | "the data is processed", "notifications are sent" | Specify which system/actor performs the action |

Each finding gets a recommendation: make it precise, assign a specific value, or explicitly mark as `[TBD]`.

---

## Check 8: Assumption-Requirement Dependency

**Dimension: Is it complete and safe?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: neither the Assumptions table nor any FR dependency references have changed
> - **RE-RUN** if: the Assumptions table has been modified (status changes, new assumptions, removed assumptions) OR any FR text referencing assumptions has changed

For each assumption in the Assumptions table (especially unconfirmed or contradicted ones):

1. Trace which FRs depend on that assumption being true
2. Check if the FR acknowledges the dependency (e.g., "depends on H2" or "blocked by H1")
3. Flag FRs that silently depend on unconfirmed assumptions without acknowledging the risk
4. For contradicted assumptions: are the dependent FRs flagged as blocked or at-risk?

Example: If Assumption H2 (data warehouse availability) is unconfirmed, every FR that needs historical data should acknowledge the blocker.

---

## Check 9: Negative Path Coverage

**Dimension: Is it complete and safe?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no changes to User Flows, Error Handling, or FR business rules sections, AND Stage4 Scenario Matrix is unchanged (Phase 0.3)
> - **RE-RUN** if: User Flows, Error Handling, or FR business rules have been modified, OR Stage4 has changed

For every happy path described in user flows or FRs:

1. Check if corresponding error/edge cases are covered in Error Handling, Alternative Paths, or business rules
2. Cross-reference the Scenario Matrix (if available) against the FRs — are all scenarios covered by at least one requirement?
3. Flag gaps: "UF-1 has 3 alternative paths, but the Error Handling table only covers 2 of them"
4. Check for missing failure modes:
   - Network failure mid-action
   - Partial data / incomplete responses
   - User abandons the flow
   - Concurrent/conflicting actions
   - Timeout / service unavailability
5. **Intra-document consistency** — see Check 11, which covers all derivative sections in a single sweep.

---

## Check 10: Actor Capability Verification

**Dimension: Is it true?**

> **Incremental skip condition:**
> - **CARRY FORWARD** if: no source files have changed (Phase 0.3) AND no actor references or Persona section content has changed in the document
> - **RE-RUN** if: any source file has been modified, OR actor-related content (Persona section, actor references in FRs) has changed

For each actor referenced in the document:

1. Verify their described capabilities match confirmed reality (from current-state sources, design descriptions, or user confirmation)
2. Flag actions assigned to actors who cannot perform them (e.g., "officer checks WFM" when officers don't have WFM access)
3. Flag assumptions about actor access, tools, or permissions that are not sourced
4. Cross-reference the actor's capabilities with what's described in the Persona section — are they consistent?

---

## Check 11: Intra-Document Section Consistency

**Dimension: Is it complete and safe?**

> **Incremental skip condition:**
> - **ALWAYS RE-RUN.** This check cannot be carried forward. Any change to any section — even a targeted fix to a single FR — can create an inconsistency with a different section (e.g., fixing an FR wording may make the Visual States table or Error Handling stale). This check is the consistency safety net for incremental mode.

A requirements document is not a collection of independent sections — every section is a view of the same feature and must tell a consistent story. This check verifies that all derivative and upstream sections are consistent with the Functional Requirements.

**Run this check after any FR addition, modification, or removal is identified in Checks 1–10. Also run it as a standalone sweep.**

For each section present in the document, check consistency against the FRs:

| Section | Relationship | What to check |
|---------|-------------|---------------|
| **User Flows / UX Flows** | DERIVED | Does it describe every behavior defined in the FRs? Does it omit any? Are all alternative paths and error paths present in the FRs represented here (even if summarised)? |
| **Visual States** | DERIVED | Does it have an entry for every distinct state implied by the FRs? Are any states now obsolete due to removed FRs? |
| **Error Handling** | DERIVED | Does it cover the failure mode of every FR? Are any rows left over from removed FRs? |
| **Executive Summary** | DERIVED | Does it still accurately describe the scope of the feature as defined by the FRs? Did the scope grow or shrink without the summary being updated? |
| **Assumptions** | UPSTREAM / BIDIRECTIONAL | Does each FR have a traceable assumption if it depends on an unconfirmed premise? Are any assumptions now resolved or invalidated by current FR content? |
| **Open Questions** | UPSTREAM / BIDIRECTIONAL | Are any `[TBD]` markers in the FRs already answered elsewhere in the document? Are there new unresolved decisions introduced by the FRs that are not captured as OQs? |
| **Dependencies** | UPSTREAM / BIDIRECTIONAL | Does every external system, team, or data source referenced in the FRs appear in the Dependencies section? Are any listed dependencies now unreferenced? |
| **Risk Analysis / Known Risks** | DERIVED | Does the risk profile reflect the current FR set? Are risks from removed FRs still present? Are new risks from added FRs missing? |

**Also check stage artifacts** (if available in the project):
- **Stage4 Scenario Matrix** — does every FR have at least one test scenario? Are scenarios present for removed FRs?
- **Stage6 User Flows** — the canonical user flow artifact. Does it reflect the latest FR content? If Stage6 is more detailed than the FR doc's User Flows summary, flag the FR doc as a DERIVED gap. If they contradict each other, flag as Critical.

For each gap found: record the section, the specific inconsistency, and classify as:
- **Gap** — the section is missing coverage of an existing FR
- **Should Fix** — the section is stale or inconsistent but not factually misleading
- **Critical** — the section actively contradicts the FRs
