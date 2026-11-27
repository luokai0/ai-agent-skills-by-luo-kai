# Workflow 2: Generate Requirements Documents

**Called from:** `workflows/01-synthesize.md` after user approves Context Summary
**Next step:** `workflows/03-validate.md` after documents are generated
**Reads:** `[output-folder]/Context-Summary-[Feature-Name].md`
**Outputs:**
- `[output-folder]/Generated/Internal/Feature-Requirements-[Feature-Name].md`

> `[output-folder]` is the path provided by the user during SKILL.md intake. It is NOT a hardcoded path.

## NON-NEGOTIABLE (read first)
1. Every FR describes WHAT (capability), never HOW (implementation) or WHAT IT LOOKS LIKE (UI).
2. Every (Source: SRC-N) citation must be verified against the actual source content.
3. Save generated document to file before presenting. Chat is ephemeral.
4. Each item lives in exactly one section. Zero cross-section duplicates.
5. Wait for user approval before proceeding to validation.

## Critical Rules

| Do | Don't |
|-------|---------|
| Save the file before presenting | Display only in chat |
| Run inline quality check before presenting | Present documents with known failures |
| Flag all TBDs with stakeholder routing | Leave TBDs without context |
| Keep within word limits | Write exhaustive documents beyond limits |
| Wait for user feedback at the end | Auto-proceed to validation |

---

## 🎯 Purpose

Convert the validated Context Summary into a polished Feature Requirements document.
The document is saved as a file. Mode and scope were determined in SKILL.md.

---

## 🔧 Execution Mode Rules

| Mode | Analysis Depth | Word Limit | Attribution |
|------|---------------|------------|-------------|
| **Quick** | 3 contexts (Business, Product, UX) | 1,500-2,000 words | Tier 1 only |
| **Comprehensive** | 6 contexts (+ Persona, Technical, Compliance) | 2,500-3,000 words | Tier 1 + Tier 2 (60%+) |

---

## 📖 Step 1: Read Context Summary

Read the saved Context Summary file:
```
[output-folder]/Context-Summary-[Feature-Name].md
```

Validate before proceeding:
- [ ] All required contexts are present (3 for Quick, 6 for Comprehensive)
- [ ] Mode is clearly stated
- [ ] Source coverage meets threshold (Tier 1 minimum)
- [ ] EXISTING vs NEW classification present (if applicable)

If the file is missing or incomplete, ask the user to re-run Workflow 1 or provide missing context.

---

## 📊 Step 2: Confirm Scope

This workflow generates one document: **Feature Requirements**. The depth of analysis depends on the mode (Quick: 3 contexts, Comprehensive: 6 contexts) determined in SKILL.md.

> **Note:** API Contracts and System Flows are generated separately after requirements are finalized, using dedicated skills (`rest-api-contract-generator`, etc.).

State upfront which documents you'll generate:
```
📄 Documents to generate:
1. Feature Requirements ✅ (always)
2. API Contract ✅ / ❌ — [reason]
3. System Flow ✅ / ❌ — [reason]
```

---

## 📝 Step 3: Generate Feature Requirements (ALWAYS)

**Template:** `templates/feature-requirements.md`

**Language rules (enforce strictly):**
- ✅ "System must generate the report within 60 seconds" — factual requirement
- ❌ "System should consider performance optimization" — opinion
- ✅ Plain English only
- ❌ No code snippets, SQL, class names, or implementation details
- ✅ "As a [persona], I need [capability] so that [outcome]" for user-facing requirements
- ❌ No vague words: "should", "probably", "might", "could"

**Requirement purity rules (enforce strictly):**
- ✅ Requirements describe WHAT (capability or constraint), never HOW (implementation) or WHAT IT LOOKS LIKE (UI pattern)
- ❌ "Cache schedule data locally for offline access" — this is a SOLUTION. Reframe: "Schedule must remain viewable when offline"
- ❌ "Organize schedule as Past | This Week | Future tabs" — this is a DESIGN DECISION. Reframe: "Officer can navigate across past, current, and future weeks"
- ✅ If a statement prescribes an implementation approach, reframe it as the underlying need and add an **Implementation Note** callout
- ✅ If a statement prescribes a UI pattern or layout, move it to **Open Questions / Design Decisions** unless the user explicitly confirmed the design
- ✅ When citing `(Source: SRC-N)`, the source must actually contain the claimed information — do not attribute content to a source that does not say it

**Sections to include (adapt; skip if not applicable):**

### 1. Executive Summary (3–4 sentences)
- What the feature does
- Why it exists (business value)
- Who uses it
- Priority / timeline (if known)

### 2. Business Context
- Business goals (with sources)
- Success metrics (measurable KPIs)
- Constraints (budget, timeline, regulatory)

**Tier 1 attribution required: 100%**

### 3. Scope
- **In Scope (This Phase)** — Table: Capability | Description | Source
- **Out of Scope (This Phase)** — Table: Item | Reason/Notes | Source
- Sources from Context Summary Product Context (in-scope/out-of-scope) and pipeline Stage 6 (purity filter)
- Every item must cite a source; items without sources are flagged as [TBD]

### 4. User Context
- Primary personas (specific roles, not "user")
- User needs and pain points
- High-level user journey

**Tier 1 attribution required for persona info**

### 5. UX Context *(Frontend/Mobile only — skip for Backend)*
- Design asset references (Figma links with `/m=dev`)
- User flows (numbered steps)
- Visual states: empty, loading, success, error, no-data
- Key interactions (trigger → action → feedback)
- Responsive behavior (desktop / tablet / mobile)

### 6. Technical Context
- System architecture (high-level)
- Technology stack (relevant)
- APIs / Endpoints summary (detailed specs in API Contract)
- Data model (key entities)
- Integration points (external systems)
- Performance requirements (timeouts, concurrency limits)

**Tier 1 attribution required for performance and constraints**

### 7. Compliance & Constraints *(Comprehensive only)*
- Regulatory requirements or N/A
- Security requirements (auth, data protection)
- Accessibility (WCAG level or N/A)
- Browser/device support
- Backward compatibility statement

**Tier 1 attribution required for regulatory and security**

### 8. Functional Requirements (Detailed)

For each requirement use this structure:

```
#### FR-[N]: [Requirement Name]

**Description:** [What this requirement enables — user value]

**Inputs:** [What goes in]

**Outputs:** [What comes out]

**Business Rules:**
- [Rule 1] (Source: [reference])
- [Rule 2] (Source: [reference])

**Validation:**
- Frontend: [What frontend validates]
- Backend: [What backend validates]

**Source:** [Document/person, date]
```

### 9. Error Handling

```
| Error Type | Cause | User Experience | System Behavior |
|------------|-------|-----------------|-----------------|
| [Type] | [Cause] | [What user sees] | [What system does] |
```

### 10. Backward Compatibility *(include ONLY if EXISTING features modified)*

```
**Changes Overview:** [What's being modified]

**Breaking Changes:** [List any]
- Impact: [Who is affected]

**Non-Breaking Changes:** [List]

**Migration Strategy:** [If breaking changes exist]

**Recommendation:** [Minimum-impact approach]
```

### 11. Known Limitations
- [Limitation — reason]

### 12. Future Enhancements

> Reference Section 3 Out of Scope. Only add detail not already in the scope table (phased roadmap, dependencies between deferred items).

### 13. Assumptions & Dependencies

```
| Dependency | Owner | Status | Risk |
|------------|-------|--------|------|
| [Item] | [Team] | [Status] | HIGH/MED/LOW |
```

### 14. Related Documents
- API Contract: [path if exists]
- System Flow: [path if exists]
- Design files: [links]

---

**Save file:** `[output-folder]/Generated/Internal/Feature-Requirements-[Feature-Name].md`

---

## Step 3.5-4: Quality Gate

After generating all sections, run the deduplication and quality checks:

Read the file:

    workflows/02b-quality-gate.md

Follow that file's instructions completely. When the quality gate passes, return here and proceed to Step 5.

---

## 💬 Step 5: Present Document

Present to user:

```markdown
✅ Generated Feature Requirements:

**Feature Requirements** → [output-folder]/Generated/Internal/Feature-Requirements-[Feature].md
- [X] functional requirements
- [N] TBDs flagged
- Word count: ~[N]

---

**TBDs requiring input:**
🔴 Critical: [list with stakeholder routing]
🟡 Important: [list]

---

**Next:** Run Workflow 3 to validate completeness and readiness for story creation.
- Reply **"validate"** to continue
- Reply **"done"** to stop here
```

**STOP and WAIT for user response.**

---

## 🔄 Step 6: After User Replies

**If "validate" or "yes":**
```
Starting Workflow 3: Validation...
```
Then **read the file:**
```
workflows/03-validate.md
```

**If "done" or any other response:**
```
✅ Requirements generation complete.

Files saved to: [output-folder]/Generated/Internal/

Next steps:
- Review document with stakeholders
- Fill in [TBD] items with relevant teams
- When requirements are finalized, generate API Contracts using `rest-api-contract-generator`
- Use these requirements to generate user stories (Story Creation workflow)
```

---

---

Workflow 2 complete. Return to `SKILL.md` workflow chain.
