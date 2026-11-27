# Stage 1: Intake & Classification

**Called from:** `SKILL.md` (Pipeline Orchestrator)
**Next step:** Return to `SKILL.md` for Stage 2: Interpretation Checkpoint
**Saves to:** `[output]/stage_output/Stage1-Intake.md`

---

## 1.0 Establish output folder

Before processing anything, ask the user for the output folder path (see **Output Folder & Artifact Registry** in SKILL.md). Create the `stage_output/`, `source_summaries/`, and `Generated/Internal/` subfolders.

## 1.1 Gather inputs (Three-Tier Scoping Gate)

**Never scan the full workspace by default.** Inputs are gathered through a progressive, user-confirmed scoping approach. This avoids reading irrelevant files, keeps the pipeline fast in large workspaces, and ensures every input is explicitly approved by the user.

### 1.1.1 Tier 1: User-Provided Files (always included)

Collect everything the user explicitly provided:
- Files or folders referenced in their message (e.g., `@Meal_and_Rest_attestation/`)
- URLs pasted in chat (Figma, FigJam, etc.)
- Verbal descriptions or rough ideas typed directly

These are primary inputs -- **no confirmation needed, no scanning needed.** If the user provides a folder, all files within it are Tier 1.

Read and list the Tier 1 files:
```
Tier 1 — User-provided inputs:
- [filename] (from [folder])
- [filename] (from [folder])
- [URL or verbal input]

Total: [N] files + [M] URLs/verbal inputs
```

### 1.1.2 Tier 2: Same-Folder Scan (low cost, high relevance)

Glob ONLY the parent folder(s) of the user-provided files. Do NOT recurse beyond those folders.

- Exclude files already in Tier 1
- If no additional files are found, skip this tier silently and proceed to the Tier 3 offer

Present discovered files grouped by type with modification dates:
```
I found these additional files in the same folder(s):

Meeting Notes / Summaries:
- [filename] (modified: [date])
- [filename] (modified: [date])

Requirements / Specs:
- [filename] (modified: [date])

Design Docs / Context:
- [filename] (modified: [date])

Other:
- [filename] (modified: [date])

Which of these should be included in this pipeline run?
Select the relevant ones. Unselected files will be ignored.
```

**Rules:**
- Present files grouped by type (meeting notes, requirements, API specs, design docs, legal, other)
- Show modification dates prominently so the user can spot stale files
- User explicitly selects which to include; unselected files are never read
- If the user selects none, proceed with only Tier 1 inputs

### 1.1.3 Tier 3: Workspace-Wide Search (only on explicit opt-in)

After the user confirms Tier 2 selections, offer a broader search:

```
Would you like me to search the rest of the workspace for related files?
I'll use targeted keyword search based on the inputs above — not a full scan.
(If no, I'll proceed with just the files selected above.)
```

**If the user declines:** Proceed with Tier 1 + Tier 2 selections. Do NOT scan further.

**If the user accepts:**
1. Extract 5-10 key terms from Tier 1 and Tier 2 files (feature name, actor names, system names, domain terms)
2. Use Grep with these terms across the workspace to find files that mention them -- this searches file content without reading entire files
3. Also search filenames with Glob patterns derived from the key terms
4. Exclude files already in Tier 1 or Tier 2, and exclude common non-input paths (e.g., `node_modules/`, `.git/`, `build/`, `dist/`)

Present matches grouped by type with modification dates:
```
I searched the broader workspace for files related to: [term1, term2, term3, ...]

Found these potentially related files:

Meeting Notes / Summaries:
- [filename] (modified: [date]) — matched: [term]
- [filename] (modified: [date]) — matched: [term]

Requirements / Specs:
- [filename] (modified: [date]) — matched: [term]

Other:
- [filename] (modified: [date]) — matched: [term]

Which of these should be included?
Select the relevant ones. Unselected files will be ignored.
```

**Rules:**
- Never auto-triggered -- only runs if the user explicitly opts in
- Show which search term matched each file so the user can judge relevance
- User explicitly selects; unselected files are never read

### 1.1.4 Final input set

After the scoping gate completes, the pipeline's input set is locked:

```
Final input set for this pipeline run:
- [N] files from Tier 1 (user-provided)
- [M] files from Tier 2 (same-folder, user-selected)
- [P] files from Tier 3 (workspace search, user-selected) [if applicable]

Total: [N+M+P] inputs
```

No additional files will be read unless the user explicitly provides them later.

### 1.1.5 Load project context

**Check for `project-context.md` in the workspace root.**

**IF found:** Read it completely and extract:
- Tech stack (frontend, backend, DB, mobile)
- API conventions (auth, naming, error shape)
- Defined personas (names, roles, pain points)
- System components and integrations
- Known limitations and constraints
- Compliance baseline
- Glossary / terminology

Announce what was loaded:
```
Project context loaded from project-context.md:
- Stack: [stack summary]
- Personas: [list]
- Systems: [list]
- Constraints: [count] known

This context will be applied throughout all pipeline stages.
```

This pre-loaded context informs:
- Stage 2 (Interpretation) -- known actors and systems don't need re-discovery
- Stage 3 (Variables/Constraints) -- pre-populated with known constraints
- Stage 4 (Scenarios) -- system-level edge cases already known
- Stage 6 (User Flows) -- personas and system interactions pre-loaded
- Stage 7 (Requirements) -- passed directly to `generate-requirements`

**IF not found:** Proceed without it. The pipeline will discover context from inputs. At the end of the pipeline (after Stage 9b), offer to create `project-context.md` from everything learned during this session.

## 1.2 Classify each input

| Input Type | How to Identify | Route To |
|---|---|---|
| Meeting transcript (.vtt, .md, .txt, .docx) | Filename contains "transcript", "meeting", "notes"; content has speaker names + timestamps | `transcript-to-meeting-notes` skill |
| Design file / Figma / FigJam URL | Image files, `figma.com` URLs | `design-to-context` skill |
| High-level requirements, ideas, hypotheses | User describes in chat or provides rough notes; no formal structure | Capture directly — processed in Stage 3 |
| Legal docs, policy docs, reference material | Formal language, regulatory content, compliance references | Read and extract key rules, constraints, thresholds |
| Existing requirements doc (for iterative update) | Structured doc with sections like Scope, Assumptions, Dependencies | Read as baseline — delta updates only |
| Swagger / OpenAPI spec | `.yaml`, `.json` with endpoint definitions | Read and extract integration points, data models, constraints. API contracts are generated separately after requirements are finalized using `rest-api-contract-generator`. |

## 1.3 Assign source IDs and report

Every input gets a short **source ID** used throughout the pipeline for traceability.

```
Inputs identified:
- [SRC-1] [filename] → [classification] → [will be processed by: skill name or "directly"]
- [SRC-2] [filename] → [classification] → [will be processed by: ...]
- [SRC-3] User-provided context → [rough ideas / hypotheses / requirements]

Processing order: [list in priority order]
```

**Source ID format:** `SRC-N` for files and user input. Within processed outputs, use finer-grained tags: `SRC-1, Decision 3` or `SRC-2, Screen 4`. For facts surfaced during analysis (not in any input), use `Implicit`.

## 1.4 Process routed inputs

Run complementary skills on their respective inputs:
- Transcripts → `transcript-to-meeting-notes` → produces structured meeting summary
- Designs (Figma URLs, FigJam URLs, screenshots, images) → `design-to-context` → produces a Context Summary, Design Description, or User Flow Document
- All other inputs → read and extract key information directly

**Save all processed outputs to `[output]/source_summaries/` before proceeding.**

## 1.4.1 Processing Verification Gate (MANDATORY)

Before moving to Step 1.5, verify that every input classified for skill processing in Step 1.2 has a corresponding saved output file. Present a checklist:

```
Processing verification:
- [SRC-1] transcript.vtt → ✅ Produced: Meeting-Summary-[name].md
- [SRC-2] figma.com/board/... → ✅ Produced: Context-Summary-[name].md
- [SRC-3] screenshot.png → ❌ NOT PROCESSED — design-to-context was not run
```

**Rules:**
- Every input routed to a skill MUST have a saved output file. A URL or filename alone is not a processed output.
- If any input shows ❌, run the skill on it immediately before proceeding. Do NOT treat unprocessed inputs as valid sources -- a URL without a processed output means the content was never actually read or analyzed.
- If a skill cannot process an input (e.g., Figma MCP is unavailable, image is unreadable), flag it explicitly: `[SRC-N] ⚠️ COULD NOT PROCESS — [reason]. Content is unavailable for analysis. Any citations to SRC-N will be unverifiable.` Present this to the user and ask how to proceed (provide alternative input, skip, or proceed with gap).
- Do NOT proceed to Step 1.5 until all routed inputs are either ✅ processed or ⚠️ explicitly flagged with user acknowledgment.

**Why this matters:** Without this gate, URLs and filenames get assigned source IDs and cited throughout the pipeline as if their content was analyzed, when in reality the content was never fetched or read. This leads to unverifiable citations, fabricated interpretations of what the source "says," and findings like "SRC-N is unverifiable" surfacing much later in validation (Stage 9a) -- wasting significant rework effort.

## 1.5 Current State Discovery (MANDATORY)

Before proceeding to Stage 2, determine whether this feature is new or enhances something that already exists.

**Ask the user:**
- "Is this a new feature (greenfield) or an enhancement to something that already exists?"
- If enhancement: "What exists today? Describe or provide: existing screens, current capabilities, known limitations. Figma links, screenshots, or verbal description all work."

**If the user provides current-state inputs:**
- Process Figma links or screenshots through `design-to-context` to produce a current-state design description
- Assign a source ID (e.g., `SRC-CS-1`) and save the output
- This becomes the baseline for identifying what is EXISTING vs NEW in the requirements

**If no current-state information is available:**
- Flag it explicitly: `[CURRENT STATE UNKNOWN — do not assume what exists today]`
- Carry this flag into Stage 2 so the interpretation checkpoint surfaces it
- Do NOT invent or assume current capabilities, pain points about current tools, or "before" scenarios

**Why this matters:** Without confirmed current state, the pipeline will fabricate a plausible "before" scenario (e.g., assuming users have no existing tool when they do). This leads to incorrect pain points, wrong framing (new feature vs. enhancement), and requirements that ignore existing capabilities.

## 1.6 Save Stage 1 artifact

**Save to:** `[output]/stage_output/Stage1-Intake.md`

Include: source registry table, input classification, processing verification checklist, current state summary, list of output files created. End with `## Next Stage → Stage 2: Interpretation Checkpoint`.

---

Stage 1 complete. Return to `SKILL.md` and proceed to Stage 2: Interpretation Checkpoint.
