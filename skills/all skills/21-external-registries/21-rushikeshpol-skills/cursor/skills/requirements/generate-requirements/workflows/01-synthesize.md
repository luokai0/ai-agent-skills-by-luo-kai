# Workflow 1: Synthesize Feature Context

**Called from:** `SKILL.md` after intake
**Next step:** `workflows/02-generate.md` after user approves Context Summary
**Output file:** `[output-folder]/Context-Summary-[Feature].md`

> `[output-folder]` is the path provided by the user during SKILL.md intake. It is NOT a hardcoded path.

## NON-NEGOTIABLE (read first)
1. Track source for every extracted fact. Unsourced = (Source: Inferred).
2. Save Context Summary to file before presenting. Chat is ephemeral.
3. Never fabricate personas, metrics, or business rules. [TBD] is always better.
4. Stop at 5+ RED gaps in Quick mode. Work through all RED gaps in Comprehensive.
5. Wait for user approval before proceeding to Workflow 2.

## Critical Rules

| Do | Don't |
|-------|---------|
| Track source for every piece of info | Fabricate data, business rules, or field names |
| Flag TBDs with stakeholder routing | Skip Step 0.5 when Swagger + modify keywords detected |
| Save Context Summary to file | Just display in chat without saving |
| Quick: Ask max 2 questions. Comprehensive: ask all RED gaps, grouped. | Ask all questions upfront in a long ungrouped list |
| Quick: Stop if 5+ RED gaps unresolved. Comprehensive: work through all RED gaps with user. | Proceed with major unknown blockers |
| Wait for user approval before proceeding | Auto-proceed to Workflow 2 |

---

## 🎯 Purpose

Analyze all available inputs and synthesize a structured Context Summary that drives document generation.
This file is saved to the workspace so Workflow 2 can read it even if the chat context is long.

---

## 🔧 Execution Mode Rules

| Mode | Contexts | Questions | Attribution | Time |
|------|----------|-----------|-------------|------|
| **Quick** | Business, Product, UX only | Max 2 (RED gaps only) | Tier 1 only | ~10 min |
| **Comprehensive** | All 6 contexts | No limit (all RED gaps) | Tier 1 + Tier 2 (60%+ target) | ~20 min |

Mode was determined in SKILL.md. Do not re-ask.

---

## 📏 Step 0: Input Size Check (Token Budget)

**Budget: 10,000 words total across all inputs**

| Input | Rule if oversized |
|-------|-----------------|
| Transcript > 3,000 words | Focus on decisions, action items, requirements sections only. Say: "Transcript is long — processing key sections." |
| Design files > 10 images | Ask: "Many design files. Please highlight the 3-5 key screens I should focus on." |
| Combined inputs > 10,000 words | Process highest-priority sections first. Report: "Input size is large — processing by priority." |

---

## 🔍 Step 0.5: Verify Existing Reality (CONDITIONAL)

**TRIGGER:** Run this step ONLY IF:
- Swagger/code file was provided, AND
- User's feature description includes keywords: "improve", "modify", "enhance", "change", "update", "add to existing"

**SKIP:** For greenfield features OR no Swagger/code provided.

**IF TRIGGERED — Read Swagger/code first:**

1. Read the Swagger/OpenAPI file completely
2. Document current state:
   - Existing endpoints (method + path)
   - Current request/response structure
   - Auth pattern (Bearer, API key, OAuth)
   - Error handling conventions (status codes, error shape)
   - Naming conventions (camelCase, snake_case, etc.)
   - Pagination pattern (if applicable)
3. Create internal baseline note: "EXISTING SYSTEM as of [date]"
4. For each proposed change, classify:
   - **EXISTING (MODIFY):** Changes to existing endpoints/fields
   - **NEW (ADDITIVE):** Net-new endpoints/fields
   - **BREAKING:** Changes that break existing API consumers
   - **NON-BREAKING:** Backward-compatible additions

> ⚠️ Breaking changes must be flagged for architect approval in the Context Summary.

---

## 📖 Step 1: Read All Inputs Systematically

Read available inputs in this priority order:

1. **PRD / Feature description** — Deep read: goals, scope, user needs, requirements
2. **Design files / Figma URLs** — Focus on: flows (not just static screens), interactions, states (empty, loading, error, success), responsive behavior
3. **Swagger / OpenAPI** — Understand: existing endpoints, data models, auth, error patterns
4. **Meeting transcript / notes** — Extract: decisions made, open questions resolved, requirements stated
5. **Verbal context from user** — Capture as stated; mark uncertain items as [inferred]

**Source tracking rule:** For every piece of information extracted, note its source:
- `(Source: PRD, Section 3)` — for documents with sections
- `(Source: PRD)` — for single-document sources
- `(Source: Design screen-02)` — for design files
- `(Source: User stated)` — for verbal/chat context
- `(Source: Inferred)` — for logical deductions (lower confidence)
- `(Source: TBD — requires [stakeholder type])` — for missing critical info

---

## 🗂️ Step 1.5: Apply Project Context (IF loaded in SKILL.md)

**IF project-context.md was loaded**, apply the following automatically without re-asking:

| Context | What project-context.md provides | What still needs feature-specific input |
|---------|----------------------------------|----------------------------------------|
| Technical | Stack, auth, API conventions, existing integrations | New endpoints, data models, feature-specific performance targets |
| Persona | Defined personas (names, roles, goals, pain points) | Any new personas discovered in this feature's inputs |
| Compliance | Regulatory baseline, security standards, browser support | Feature-specific overrides (e.g., "this feature requires WCAG, others don't") |

**Mark pre-loaded items in the Context Summary as:**
`(Source: project-context.md)` — distinguishing them from feature-specific sources.

**Flag any conflicts:** If a feature's PRD contradicts project-context.md (e.g., different auth method), flag it explicitly:
```
⚠️ Conflict detected: PRD specifies [X] but project-context.md defines [Y].
   Which should apply to this feature?
```

---

## 🧩 Step 2: Extract Contexts

### Quick Mode — Extract 3 Contexts

#### Context 1: Business Context
- **Business goals** — What outcomes does the company want? (measurable where possible)
- **Success metrics** — KPIs (adoption rate, time saved, error reduction, etc.)
- **Constraints** — Budget, timeline, regulatory, technical
- **Stakeholders** — Who cares about this feature?

*Source priority: PRD, meeting transcript, stakeholder statements*

---

#### Context 2: Product Context
- **In-scope** — What IS included (Phase 1)
- **Out-of-scope** — What is explicitly NOT included
- **User needs** — Problems being solved (user language, not system language)
- **Product goals** — How this aligns to product strategy
- **Dependencies** — Other features, systems, or teams this depends on

*Source priority: PRD, product roadmap*

---

#### Context 3: UX Context
*(Skip if backend-only feature)*
- **Design assets** — Figma links, mockup references
- **User flows** — Step-by-step journey (numbered steps)
- **Visual states** — Empty, loading, success, error, no-data states
- **Interactions** — What triggers what (click → action → feedback)
- **Responsive behavior** — Mobile / tablet / desktop differences

*Source priority: Design files, UX specs*

---

### Comprehensive Mode — Extract All 6 Contexts

*(Includes all 3 above, plus:)*

#### Context 4: Persona Context
- **Primary personas** — Specific roles (NOT generic "user"). Include name, role, goals, pain points
- **Secondary personas** — Other affected users
- **User context** — When/where/how often they use this (device, frequency, environment)
- **Representative quote** — A quote capturing their core frustration or goal (from research, or mark [TBD])

*Source priority: User research docs, persona library, interview notes*

---

#### Context 5: Technical Context
- **System architecture** — High-level components involved
- **Technology stack** — Frontend and backend frameworks
- **APIs / Endpoints** — Each one labeled EXISTING or NEW
- **Data model** — Key entities and relationships
- **Integration points** — External systems (name, interface type, owner, SLA)
- **Performance requirements** — Timeouts, limits, concurrency
- **Existing patterns** — Naming conventions, auth, pagination, error shape (from Swagger/Step 0.5)

*Source priority: Swagger, architecture docs, tech lead input*

---

#### Context 6: Compliance / Constraints Context
- **Regulatory** — GDPR, HIPAA, SOC2, or N/A
- **Security** — Auth requirements, data protection, encryption
- **Accessibility** — WCAG level required or N/A
- **Browser/device support** — Specific requirements
- **Backward compatibility** — Impact on existing consumers (especially if EXISTING features modified)

*Source priority: Legal, security team, compliance docs*

---

## 🚩 Step 3: Identify and Categorize Gaps

For every context, classify each item:
- ✅ **Known** — Clearly stated in source
- ⚠️ **Inferred** — Logically deduced (mark with lower confidence)
- ❌ **TBD** — Missing; must be gathered

**Categorize TBDs by severity:**

| Severity | Color | Rule | Example |
|----------|-------|------|---------|
| Blocks generation | 🔴 RED | Quick: 5+ RED gaps → stop and request input. Comprehensive/pipeline: present all RED gaps, work through with user. | Performance timeout not specified |
| Reduces quality | 🟡 YELLOW | Document gap, proceed with caution | Persona not confirmed by research |
| Nice to have | 🟢 GREEN | Document gap, proceed normally | Future enhancement scope |

**For each TBD, include:**
```
[TBD — {gap description}] (Suggested stakeholder: {PM / Architect / Designer / Legal / Data Team})
```

**Question rule:**
- **Quick mode:** Ask max **2 critical questions** (RED gaps only)
- **Comprehensive mode:** No question limit. Ask about all RED gaps. Group related questions together rather than asking one at a time.
- **When called from `/requirements-pipeline`:** Most RED gaps should already be resolved by Stage 2. Ask about any that remain without a cap.
- Provide context for WHY each question is needed

**Improvement over original:** If 5+ RED gaps exist in Quick mode, do NOT attempt generation. Report blockers and ask user to provide more input or reduce scope. In Comprehensive mode or pipeline calls, present all RED gaps and work through them with the user.

---

## 📌 Step 4: Source Attribution Check

Before generating Context Summary, verify coverage:

| Tier | Items | Required coverage | On failure |
|------|-------|------------------|------------|
| **Tier 1** | Business goals, metrics, performance requirements, compliance, technical constraints | 100% | Block generation — ask user |
| **Tier 2** | Functional requirements, user needs, UX flows, integration points | 60%+ target | Flag gaps as [TBD] |
| **Tier 3** | Background context, examples, future enhancements | Optional | Skip attribution |

---

## 📄 Step 5: Generate Context Summary

Using the template at `templates/context-summary.md`, generate a Context Summary with all extracted information.

**File naming:** `[output-folder]/Context-Summary-[Feature-Name].md`

**Improvement over original:** Save this file immediately. Don't just display it in chat. The next workflow reads it from the file.

> Save the Context Summary file before presenting to user.

---

## 💬 Step 6: Present Summary and Ask Critical Questions

Present the synthesis to the user:

```markdown
✅ Context Summary created

**Feature:** [name]
**Mode:** [Quick / Comprehensive]
**Inputs processed:** [list]
**File saved:** [output-folder]/Context-Summary-[Feature-Name].md

---

**Coverage:**
- Contexts analyzed: [N] / [3 or 6]
- Tier 1 sources: [X]%
- Tier 2 sources: [Y]% (target: 60%+)
- TBDs: [N] 🔴 critical, [M] 🟡 important, [P] 🟢 optional

---

**Critical Questions** (needed before generating docs):
1. [Question — why needed — which context it unblocks]
2. [Question — why needed — which context it unblocks]

---

Ready to proceed to document generation?
- Reply **"yes"** to generate with current information (TBDs will be flagged)
- Reply **"[answer to Q1]"** to fill in gaps first
```

**STOP and WAIT for user response.**

---

## 🔄 After User Approves

1. Update Context Summary with any answers the user provided
2. Re-save the file
3. Confirm:
```
✅ Context Summary finalized.
📄 Saved: [output-folder]/Context-Summary-[Feature-Name].md

Starting Workflow 2: Document Generation...
```

Then **read the file:**
```
workflows/02-generate.md
```

---

---

Workflow 1 complete. Return to `SKILL.md` workflow chain.
