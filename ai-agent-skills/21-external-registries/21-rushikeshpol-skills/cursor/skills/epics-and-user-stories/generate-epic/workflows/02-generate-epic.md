# Workflow 2: Generate Epic Document

**Called from:** `workflows/01-prepare.md` after user approves preparation
**Next step:** Complete. Suggest `/generate-user-stories` to decompose into stories.
**Reads:** `[output-folder]/.meta/Epic-Prepare-[Feature].md` + `[output-folder]/.meta/.pipeline-state.json`
**Saves to:** `[output-folder]/Epic-[Feature-Name].md` (epic) + appends quality results to `[output-folder]/.meta/Epic-Prepare-[Feature].md`

---

## 📍 You Are Here
**Skill:** generate-epic
**Stage:** 2 of 2 — Generate
**Input:** Approved preparation from Stage 1
**Your only job:** Create the epic document using the template, run quality checks, save file
**DO NOT:** Decompose the epic into stories — that's `generate-user-stories`.
**DO NOT:** Write generic outcomes that sound good but aren't measurable. Every outcome must have a concrete success criterion from source.
**DO NOT:** Present the epic if any quality check has failed — fix first, present second.
**Audience:** You are writing for a PO and team lead who need to understand the feature's business value, scope, and decomposability.

---

## 📖 Step 1: Read Prepared Context

Read BOTH files:
1. `[output-folder]/.meta/.pipeline-state.json` — confirm Stage 1 complete and approved
2. `[output-folder]/.meta/Epic-Prepare-[Feature].md` — ALL extracted context lives here

Validate:
- [ ] Stage 1 marked as completed and approved
- [ ] Prepare file exists with extracted context, confirmed inferences, gap analysis

If missing or incomplete → stop. Ask user to re-run Stage 1.

**Use the prepare file as your source — do not rely on chat history.**

---

## 📝 Step 2: Generate Epic

Using `templates/epic.md`, generate the epic document.

**Section-by-section guidance:**

| Section | Key rules |
|---------|-----------|
| **Title** | Format: `[Feature/Area] -- [Goal/Capability]` |
| **Description** | 2-3 sentences. Every claim sourced. |
| **Outcomes** | **Priority 1.** Each must be measurable + sourced. Not measurable from source → `[TBD — requires: measurable target from PO] (Route to: Product Owner)`. Never fill with generic statements. |
| **Context** | Release fit, key decisions `(Source: §X)`, links to requirements, constraints. |
| **Designs** | Figma links with `/m=dev`. Mobile + desktop. Open design questions. |
| **Scope** | High-level capabilities (features, not tasks). Each sourced. |
| **Out of Scope** | **Priority 3.** Explicit exclusions. If not in source → `[TBD — requires: PO confirmation] (Route to: Product Owner)`. |
| **Risks & Dependencies** | External services, other epics, UX gaps, security/legal/performance. |
| **Technical Considerations** | `[Reserved for architect/dev lead — do not populate]` |
| **Milestones** | Timeline if known, otherwise `[TBD]`. |
| **Change History** | Empty on creation. |

Follow the template structure and reference example in `templates/epic.md` for formatting.

---

## ✅ Step 3: Quality Checks (Epic Priority Order)

Run these checks before presenting. Fix failures before showing to user.

**Priority 1 — Business Outcome (Ring 1):**
- [ ] Outcomes section exists and is non-empty
- [ ] Each outcome is measurable (has a number, percentage, or observable condition)
- [ ] Each outcome traces to a source — no invented metrics
- [ ] If outcome cannot be measured → marked `[TBD]` with routing, NOT filled with a generic statement
- **If missing entirely → flag as RED gap. Do not present.**

**Priority 2 — Decomposability (Ring 1):**
- [ ] Scope section lists distinct capability areas
- [ ] No single scope item that would take > 1 sprint to deliver (suggests it needs splitting)
- [ ] No circular dependencies visible between scope items
- **If monolithic (single massive scope item) → flag as RED gap.**

**Priority 3 — Scope Boundaries (Ring 2):**
- [ ] Out-of-scope section exists
- [ ] At least 2-3 explicit exclusions listed (or marked `[TBD]`)
- **If vague → warn but proceed.**

**Priority 4 — Format (Ring 3):**
- [ ] All template sections present and in order
- [ ] Title follows format: `[Feature/Area] -- [Goal/Capability]`
- [ ] Source attributions present throughout
- [ ] `[TBD]` markers use standardized format with routing

**Hard presentation gate:** Never present the epic if Priority 1 or 2 checks failed. Fix first.

---

## 💾 Step 4: Save Files

1. Save epic: `[output-folder]/Epic-[Feature-Name].md`
2. Append quality check results to `[output-folder]/.meta/Epic-Prepare-[Feature].md` under a `## Quality Check Results` section (verdict per priority, evidence, pass/fail)
3. Update `[output-folder]/.meta/.pipeline-state.json`: stage "02-generate-epic", stages_completed, quality_check results

---

## 💬 Step 5: Chat Output (minimal)

**Only this goes to chat:**

```
Epic generated: [✅ PASS / ⚠️ PASS WITH WARNINGS / ❌ FAIL]
File: [epic file path]
Preparation & quality notes: [prepare file path]
[N] outcomes ([M] measurable, [K] TBD) | [N] scope items | [N] TBDs | [N] risks
Review the epic. When approved → /generate-user-stories to decompose.
```

**All quality check details, evidence, and per-priority breakdowns stay in the prepare file.** Chat is for decisions and navigation only.

**STOP and WAIT for user response.**

---

## ✅ Completion Gate
- [ ] Epic file saved to: `[output-folder]/Epic-[Feature-Name].md`
- [ ] File contains all template sections
- [ ] All Priority 1 + 2 checks passed (or gaps explicitly marked)
- [ ] Source attributions present throughout
- [ ] Pipeline state file updated
- [ ] User has explicitly reviewed
If any item is unchecked → do NOT mark as complete.
