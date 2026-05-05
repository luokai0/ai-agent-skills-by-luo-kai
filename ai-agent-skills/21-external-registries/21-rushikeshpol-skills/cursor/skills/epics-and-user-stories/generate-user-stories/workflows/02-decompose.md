# Workflow 2: Decompose Feature into Story Concepts

**Called from:** `workflows/01-prepare.md` after user approves preparation
**Next step:** `workflows/03-create-story.md` after user approves decomposition
**Reads:** `[output-folder]/.meta/Story-Prepare-[Feature].md` + `[output-folder]/.meta/.pipeline-state.json`
**Saves to:** `[output-folder]/.meta/Decomposition-[Feature-Name].md`

---

## 📍 You Are Here
**Skill:** generate-user-stories
**Stage:** 2 of 4 — Decompose
**Input:** Epic or requirements doc context (extracted in Stage 1)
**Your only job:** Apply WAHZURT framework → generate story concepts → refine (merge overlaps, split oversized) → build coverage map → present for approval
**DO NOT:** Write detailed acceptance criteria — that's Stage 3.
**DO NOT:** Create story files — that's Stage 3.
**DO NOT:** Skip WAHZURT dimensions by defaulting to obvious section splits from the document. Every dimension must be explicitly evaluated, even if it produces zero stories.
**Audience:** You are planning work for developers and QA engineers. Each concept must become an independent, deliverable story.

---

## 📖 Step 1: Apply WAHZURT Framework

Analyze the feature through ALL 7 dimensions. For each, document what story concepts emerge. Never skip a dimension — explicitly note if it produces zero concepts.

| Dimension | What to look for | Key questions |
|-----------|-----------------|---------------|
| **W — Workflow** | Distinct steps in the user journey | What steps does the user take? Where are natural breaks? |
| **A — Acceptance Criteria** | Complex ACs that could be separate stories | Which behaviors are complex enough to warrant their own story? |
| **H — Happy/Unhappy** | Success paths + error/edge cases | What can go right? What can go wrong? Empty states? Failures? |
| **Z — Zero/One/Many** | Data quantity edge cases | What happens with no data? One item? Many items? Pagination? |
| **U — User Roles** | Different personas/permissions | Which roles interact? Do they see different things? Different permissions? |
| **R — Rules** | Business rules, validations, constraints | What rules apply? Validation logic? Limits? Compliance? |
| **T — Touchpoints** | Platforms, system boundaries | Web? Mobile? API? Third-party integrations? Responsive breakpoints? |

---

## 🧩 Step 2: Generate Story Concepts

Per concept, capture: **Title** (`[Platform] -- [Feature] -- [Context]`), **User statement** (`As a [specific persona], I want [goal], so that [value]`), **Platform** (FE/BE/Mobile), **WAHZURT source**, **Requirements mapping** (`Req §X, §Y`).

Validate each against INVEST: Independent? Valuable? Small (one sprint)? Testable?

**Quick mode:** Lighter analysis. Mark concepts `[DRAFT]`. Skip detailed requirements mapping.

---

## 🔄 Step 3: Refine Concepts

1. **Group and merge overlaps** — if two concepts describe different behaviors for the same user need, combine them (with multiple ACs planned)
2. **Separate edge cases** — if incorporating edge case logic makes a concept too large, split it
3. **Check conjunction splitting** — if any user statement contains "and", "or", "but" joining distinct actions → split into separate concepts
4. **Plan creation order** — dependencies first, then by workflow sequence

---

## 🔬 Step 4: Inference Register

Flag any story concept NOT directly stated in the epic/requirements but inferred from scope:
```
INFERRED story concepts (needs your confirmation):
- [Concept title] — inferred from [source basis]. Include? (Y/N)
```

User confirms before inferred concepts enter the creation pipeline. Rejected concepts are dropped.

---

## 🗺️ Step 5: Build Coverage Map (mandatory)

### WAHZURT Dimension Coverage
```
| Dimension | Stories produced | Notes |
|-----------|-----------------|-------|
| W — Workflow | [count] | [which concepts] |
| A — Acceptance | [count] | [which concepts] |
| H — Happy/Unhappy | [count] | [which concepts] |
| Z — Zero/One/Many | [count] | [which concepts] |
| U — User Roles | [count] | [which concepts] |
| R — Rules | [count] | [which concepts] |
| T — Touchpoints | [count] | [which concepts] |
```

### Requirements-to-Story Traceability
```
| Requirement | Story Concept(s) | Status |
|-------------|-----------------|--------|
| [FR-1 or §X] | [concept title(s)] | ✅ Covered |
| [FR-5 or §Y] | [none] | ❌ GAP — no story covers this |
```

Flag any requirement section with NO corresponding story concept.

---

## 💾 Step 6: Save Decomposition

Save to: `[output-folder]/.meta/Decomposition-[Feature-Name].md`

Include: all story concepts with titles, user statements, platforms, WAHZURT source, requirements mapping, creation order, coverage map, inference register results.

Update `[output-folder]/.meta/.pipeline-state.json`: stage "02-decompose", stages_completed.

---

## 💬 Step 7: Present for Approval

Present: story count, creation order list (title + platform + requirements ref + WAHZURT source), coverage summary (dimensions hit, requirements covered, gaps), file path.

Ask: "Approve this decomposition to proceed with story creation? Or provide feedback to adjust."

**STOP and WAIT for user response.**

---

## 🔄 After User Approves

Update pipeline state, then **read:** `workflows/03-create-story.md`

**If DECOMPOSE-only mode:** Mark as complete. Suggest: "Run `/generate-user-stories` later to create detailed stories from this decomposition."

---

## ✅ Completion Gate
- [ ] All 7 WAHZURT dimensions explicitly evaluated
- [ ] Story concepts have titles, user statements, platforms, requirements mapping
- [ ] INVEST validation applied to each concept
- [ ] Coverage map shows WAHZURT dimensions + requirements traceability
- [ ] Inferred concepts confirmed by user
- [ ] Decomposition file saved
- [ ] Pipeline state updated
- [ ] User has explicitly approved
If any item is unchecked → do NOT proceed.
