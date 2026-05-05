# Changelog

## [Unreleased] — 2026-04-20

### New Skills (9) — Planning Plugin + Epics & Stories Plugin ⚠️ Work in Progress

> Both new plugins are work in progress. Core functionality is in place but prompts, templates, and workflows are still being refined through active use.

A new **Planning Plugin** (`cursor/skills/planning/`) adds 5 interconnected delivery lifecycle skills covering the full sprint cycle:

- **release-sprint-planner** — Defines a release (goal, scope, timeline, team, constraints) and produces a formal Release Definition + multi-sprint plan. Assesses context across 6 dimensions, sizes features, maps dependencies, and assigns work to sprints.
- **sprint-planning-session** — Takes a sprint's planned work (from a release plan, ticket board, or verbal list) and produces a structured Sprint Planning Session document with goal validation, grouped work areas, and "done" criteria.
- **sprint-progress-tracker** — Creates a planned-vs-actual progress snapshot for mid-sprint check-ins or sprint close-out. Surfaces risks early and feeds data into sprint review.
- **sprint-review-generator** — Produces a stakeholder-facing sprint review document. Answers: What did we build? Did we hit our goal? What did we learn? What's next? Serves both stakeholders (top sections) and team/PM (full detail).
- **meeting-to-plan-integrator** — Applies decisions from any sprint demo, retro, or stakeholder call back to the release plan and related artifacts. The "decisions become actions" bridge.

A new **Epics & Stories Plugin** (`cursor/skills/epics-and-user-stories/`) adds 4 story lifecycle skills:

- **generate-epic** — Creates a structured epic document from a requirements doc or verbal description. Extracts business goals, success criteria, scope boundaries, and dependencies. Produces a single `Epic-[Feature].md` file ready for story decomposition.
- **generate-user-stories** — Decomposes features into story concepts using the WAHZURT framework, then creates detailed INVEST-compliant user stories one-at-a-time with inline quality gates. Supports 4 modes: create (standard), create (quick/draft), modify existing stories, and decompose-only.
- **validate-user-stories** — Audits existing user stories against 12 validation categories (9 per-story + 2 cross-story + 1 practitioner readability) and fixes failures. Always builds a fresh registry from actual story files — never trusts existing registries.
- **generate-uat** — Generates a client-ready UAT test plan from GitHub issue files or a manual ticket list. Extracts Acceptance Criteria, deduplicates cross-platform (iOS/Android) scenarios, and produces a requirement-pure UAT document with a "Known Limitations" section and "Tickets Without ACs" appendix.

### Structural Change — Category Plugin Layout

The flat `cursor/skills/` structure has been refactored into category plugins:

- **`cursor/skills/requirements/`** — 9 requirements and analysis skills reorganized here (previously at `cursor/skills/<skill>/`)
- **`cursor/skills/planning/`** — 5 new planning skills organized here
- **`cursor/skills/epics-and-user-stories/`** — 4 new story lifecycle skills organized here
- **`cursor/skills/`** (root) — 3 standalone cross-cutting skills remain: `design-to-context`, `figjam-diagram-generator`, `transcript-to-meeting-notes`

Each category folder contains its own `README.md` documenting the plugin structure, skill relationships, install instructions, and output folder layout.

**Shared resources (planning plugin):**
- `planning/shared/delivery-model.md` — Release lifecycle phases, sprint anatomy, document chain, commitment model
- `planning/shared/execution-rules.md` — Shared NON-NEGOTIABLE rules, quality criteria, self-check structure, provenance model
- `planning/shared/constraint-registry-template.md` — Template and rules for the shared constraint registry

### Skill Enhancement — figjam-diagram-generator

- Added mandatory **5-color standard palette** for all flowcharts. Every generated flowchart must now include the full `classDef` block and `class` assignments — no exceptions.
- Color classes: `terminus` (start/end, green), `decision` (diamonds, amber), `action` (rectangles, blue), `notification` (reminders/alerts, orange), `errorPath` (offline/fallback/degraded, red)
- Updated `SKILL.md` with full classification rules, `classDef` template, and new verification gate checklist item
- Updated `mermaid-patterns.md` with a Standard Color Palette reference section, classification rules, and updated subgraph example showing all 5 classes applied
- Removed the old opt-in "Color styling allowed if user requests it" rule — color is now always applied

### Documentation Updates

- **README.md** — Updated skill count from 12 to 21; restructured repository tree to show category plugin layout; added Planning Skills and Epics & Stories Skills tables; updated install instructions to use `find -mindepth 2 -maxdepth 3` to handle both flat and nested skill paths; updated Contributing section with category guidance

---

## [0.5.0] — 2026-04-14

### New Skills (2)

- **figjam-diagram-generator** — Generates Mermaid.js diagrams (flowcharts, sequence, state, gantt) in FigJam via Figma MCP `generate_diagram` tool. Includes `mermaid-patterns.md` reference for MCP-compatible Mermaid syntax. Runs a 6-priority verification gate before generating.
- **securitas-client-ready-requirements** — Transforms internal requirements into a streamlined Securitas client-ready format (7-8 sections). Enforces strict "copy/relocate, no paraphrase" rules on FR body text, with Phase 1 cleaning, Phase 1.5 dedup, Phase 2 section assembly, and Phase 3 verification.

### Major Skill Rewrites (3)

- **validate-requirements** — Expanded from 11 semantic checks to 15 checks across 2 dimensions (11 semantic + 4 structural). Now replaces the need to run `document-audit` separately on requirements documents. Added incremental mode: when a prior validation report is provided, only re-runs checks whose inputs changed, carries forward valid findings (40-60% effort reduction). Checks are split into separate files (`checks/semantic-checks.md`, `checks/structural-checks.md`). Added `incremental-detection.md` (Phase 0 change detection) and `output-templates.md` (report and chat summary formats). Added mandatory checklist control loop (T0-T5).
- **update-documents** — Complete rewrite with subagent-based execution model. All target document edits now performed by subagents (NON-NEGOTIABLE). Added: RunState contract (`RunState-*.json`), mandatory todo control loop (T0-T7), silent execution model, artifact-based workflow (`update-workspace/` directory), mode selection (agent vs plan), resume workflow for interrupted runs. Supporting files split out: `reference-tables.md` (registry templates, decision matrices, impact tables) and `appendix-update-documents.md` (prompt templates, output formats, gate YAML blocks).
- **requirements-pipeline** — Added Stage 3.5 (Feature Decomposition) as a mandatory checkpoint. Stages 4-9 now run per-feature with staggered-parallel execution for multi-feature splits. Stages 9a+9b merged into Stage 9 (combined validation using updated `validate-requirements`). Added Stage 9c (Post-Merge Reconciliation) for multi-feature. All stage content extracted to individual files (`stages/02-interpretation.md` through `stages/09c-reconciliation.md`). Added 20 Critical Rules (up from 15). Added multi-feature folder structure and Shared Registry concept.

### Skill Enhancements (5)

- **generate-requirements**
  - Added NON-NEGOTIABLE rules and Critical Rules sections at top of SKILL.md and all workflow files
  - Added new Section 3 (Scope — In Scope/Out of Scope tables) to feature-requirements template; all subsequent sections renumbered (now 16 sections, up from 15)
  - Added Section 12 (Future Enhancements) with cross-reference to Scope table
  - Added classification rules to Known Limitations, Assumptions & Dependencies, and Open Questions sections to prevent cross-section duplication
  - Added `workflows/02b-quality-gate.md` — post-generation deduplication and inline quality checks extracted from the inline Step 4
  - Added Pipeline Mode: Skip directive to Workflow 3 (validation) when called from pipeline
  - Added cross-section deduplication check (Step 4) to Workflow 3
  - Critical Rules moved from bottom to top of each workflow file for visibility
  - Archived 3 templates to `archive/` folder: `api-contract.md` (use `rest-api-contract-generator`), `system-flow.md` (use separate skill), `project-context.md` (use `project-context` skill)

- **document-audit**
  - Added file output path logic: parent skill path → existing reports folder → auto-create `reports/`
  - Added chat output discipline: show only file path, total count by category, and top 3 findings
  - Added Summary section to report format (Category | Count | Findings table)

- **review-findings**
  - Updated to handle combined semantic + structural report format from `validate-requirements`
  - Added legacy format detection (`# Requirements Accuracy Review` → treat same as new format)
  - Added Type column (Semantic / Structural) to finding category tables
  - Updated integration context descriptions for combined validation model

- **generate-requirements/INSTALL.md**
  - Updated file tree: added `02b-quality-gate.md`, replaced template files with `archive/` references

- **generate-requirements/templates/feature-requirements.md**
  - Added Scope section (Section 3) with In Scope / Out of Scope tables
  - All sections renumbered 4-16
  - Added classification rules to Known Limitations, Assumptions & Dependencies, and Open Questions
  - Split Assumptions & Dependencies into separate sub-sections with definitions

### New Files (29)

**Pipeline stage files (extracted from SKILL.md inline content):**
- `requirements-pipeline/stages/02-interpretation.md`
- `requirements-pipeline/stages/03-brainstorm.md`
- `requirements-pipeline/stages/03.5-decomposition.md`
- `requirements-pipeline/stages/04-scenarios.md`
- `requirements-pipeline/stages/05-assumptions.md`
- `requirements-pipeline/stages/06-user-flows.md`
- `requirements-pipeline/stages/07-requirements.md`
- `requirements-pipeline/stages/08-risk-analysis.md`
- `requirements-pipeline/stages/09-validation.md`
- `requirements-pipeline/stages/09c-reconciliation.md`

**Validate-requirements supporting files:**
- `validate-requirements/checks/semantic-checks.md`
- `validate-requirements/checks/structural-checks.md`
- `validate-requirements/incremental-detection.md`
- `validate-requirements/output-templates.md`

**Update-documents supporting files:**
- `update-documents/reference-tables.md`
- `update-documents/appendix-update-documents.md`

**Generate-requirements files:**
- `generate-requirements/workflows/02b-quality-gate.md`
- `generate-requirements/archive/api-contract.md` (archived from templates/)
- `generate-requirements/archive/system-flow.md` (archived from templates/)
- `generate-requirements/archive/project-context.md` (archived from templates/)

**FigJam diagram generator:**
- `figjam-diagram-generator/SKILL.md`
- `figjam-diagram-generator/mermaid-patterns.md`

**Securitas client-ready requirements:**
- `securitas-client-ready-requirements/SKILL.md`

### Deleted Files (3)

- `generate-requirements/templates/api-contract.md` — moved to `archive/`; use `rest-api-contract-generator` skill instead
- `generate-requirements/templates/system-flow.md` — moved to `archive/`; system flows generated by separate skill
- `generate-requirements/templates/project-context.md` — moved to `archive/`; use `project-context` skill instead

### Documentation Updates

- **README.md** — Updated skill count from 10 to 12; added repo structure entries for `archive/` and `checks/`; updated skill table with new skills and revised descriptions
- **docs/skill-catalog.md** — Added `figjam-diagram-generator` and `securitas-client-ready-requirements` entries; updated `validate-requirements` to 15 checks with incremental mode; updated `document-audit` scope to non-requirements docs; updated `update-documents` with subagent execution model; updated `requirements-pipeline` stages and checkpoints
- **docs/workflow-guide.md** — Updated skill count to 12; updated pipeline diagram with Stage 3.5, combined Stage 9, and Stage 9c; updated stage table; updated relationship map; added new post-pipeline skills
- **docs/invocation-guide.md** — Added trigger prompts for `figjam-diagram-generator` and `securitas-client-ready-requirements`; updated pipeline walkthrough to include Stage 3.5 and combined Stage 9

### Architecture Changes

- **Pipeline validation model:** `validate-requirements` now handles both semantic accuracy and structural integrity for requirements documents in a single pass. The standalone `document-audit` skill is reserved for non-requirements documents. This eliminates the previous Stage 9a/9b split.
- **Feature decomposition:** Stage 3.5 introduces mandatory feature decomposition before per-feature analysis begins. Even single-feature pipelines produce this artifact ("no split needed" is valid). Multi-feature pipelines use staggered-parallel execution with a Shared Registry for cross-feature items.
- **Subagent execution:** `update-documents` now exclusively uses subagents for all target document edits, with RunState-based tracking for resumability and batch execution for parallel editing.
- **Incremental validation:** `validate-requirements` supports incremental mode that detects what changed since a prior report and only re-runs affected checks, carrying forward valid findings from the prior run.
