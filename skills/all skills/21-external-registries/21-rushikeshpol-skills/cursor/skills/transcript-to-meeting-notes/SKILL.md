---
name: transcript-to-meeting-notes
description: "Converts meeting transcripts (.vtt, .docx, .md, .txt) into structured meeting summaries. Uses a single unified template for all meeting types (discovery, engineering, technical). Outputs a Discovery Summary with decisions table, topic-by-topic findings with traceability, know/don't-know analysis, assumptions, open questions, and next steps. Topic internal structure adapts based on meeting type. Use when given a transcript file or asked to summarize a meeting, call, sync, or session."
---

# transcript-to-meetingNotes

## Step 0: Assess size and decide whether to delegate

Before reading the transcript, determine whether to process it in the current context or delegate to a subagent. Reading a long transcript consumes context that cannot be reclaimed — and for multi-stage workflows (like the requirements pipeline), that context is needed for later stages.

### When to delegate to a subagent

| Condition | Action |
|-----------|--------|
| **Called from another skill or pipeline** (e.g., `requirements-pipeline`, `generate-requirements`) | **ALWAYS delegate.** The caller's context is precious — it has 9+ stages ahead. Even a short transcript consumes significant context. |
| **Called standalone AND transcript > 500 lines** | **Delegate.** A 1-hour meeting is ~500-1000 lines. Anything longer will dominate the context window. |
| **Called standalone AND transcript ≤ 500 lines** | **Process directly.** Short transcripts are fine in-context. Proceed to Step 1. |

**How to check line count without reading the file:** Run `wc -l <filepath>` in the shell. This returns the line count without loading the content into context.

### How to delegate

Launch a `generalPurpose` Task subagent with a prompt that includes:

**a) The transcript file path** and the **save path** for the output (following the naming convention in Step 5).

**b) The full skill instructions** — copy Steps 1–5 below AND the template from [templates.md](templates.md) into the subagent prompt. The subagent does not have access to skill files.

**c) Any caller-provided context** — e.g., "this is a discovery session about meal break attestation", "focus on decisions about the approval workflow", participant roles if known.

**d) This return instruction** (include verbatim in the subagent prompt):

```
After saving the summary file, return ONLY the following (max 15 lines):
- File path where the summary was saved
- Session date and duration
- Participant count and names
- Meeting type (Discovery / Engineering)
- Number of decisions captured
- Number of topics documented
- 3-5 headline findings (one line each, most important first)
- Number of open questions by severity (🔴/🟡/🟢)
- Number of assumptions needing validation
```

### What the main context receives

Only the brief digest above — never the raw transcript. The main agent can then read the saved summary file if it needs specific details for later stages.

---

## Step 1: Determine meeting type

Read the transcript and identify which type applies. This determines **topic internal structure only** — the overall document structure is the same for both.

| Type | Indicators | Topic style |
|------|-----------|-------------|
| **Discovery / Requirements** | Stakeholder session, requirements gathering, discovery call, regional/Canadian team, product decisions | Fact-gathering bullets with traceability. `**Current state context:**` sub-blocks where relevant. |
| **Engineering / Technical** | Engineering sync, technical discussion, vendor call, dev team, architecture, bug/release planning | Structured sub-sections per topic: **Context**, **Requirements**, **Final Decision** (✅), **Alternatives Considered** (❌/⏸️), **Key Technical Insights** (if non-obvious learnings exist). |

When unclear, use Discovery topic style (more flexible).

---

## Step 2: Core rules (apply to all meetings)

- **Facts only.** NEVER assume. NEVER add outside information.
- **Attribution always.** Every decision/insight tied to a named speaker.
- **Traceability always.** Every bullet links to the transcript line: `[*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)`.
- **Explicitly state "Not discussed"** for topics that weren't covered — do not leave gaps.
- **Current state vs. requirement:** Clearly separate "how things work today" from "what the system must do." Where relevant, embed current-state context within the topic (as a `**Current state context:**` sub-section) rather than a separate top-level section.
- **"Automatic" ≠ system-enforced.** Clarify if a rule is truly automated or an honor system.
- **Unknown = mark it.** Use `[TBD]` or `[UNKNOWN]`, never invent a value.
- **Each fact appears once.** Do not repeat the same information across multiple sections. If a fact is relevant to two sections, state it in the primary topic and cross-reference.
- **Don't remove text if it adds value to the reader.** But cut text that is repetitive or restates what's already clear.
- **Rejected & deferred ideas matter.** When a decision is reached after back-and-forth, briefly capture any ideas that were explicitly rejected (❌) or put on hold (⏸️). Include the reason if stated and attribute to the speaker who raised or dismissed it. Strip the conversational back-and-forth itself, but preserve the outcome of each considered alternative.
- **Corrections matter.** If someone states something incorrect and is corrected during the meeting, note the correction with a `**Correction:**` prefix so readers don't carry the wrong mental model.

---

## Step 3: Document structure (same for all meeting types)

Follow the template in [templates.md](templates.md).

### Sections in exact order

1. **Header** — Title (`[Feature/Topic] — Meeting Summary`), session date, source transcript (relative link), participants with roles.
2. **Decisions Made table** — Top-level table of all decisions made in the session. Each row: #, Decision (bold), Alternatives Considered (❌/⏸️ with attribution), Source (transcript link). If no decisions were made, write "No decisions reached — all topics remain open."
3. **Topics** — One `## Topic N: [Title]` section per major discussion area. Internal structure varies by meeting type (see Step 4).
4. **WHAT WE KNOW VS WHAT WE DON'T KNOW** — Table with columns: Topic | What We Know | What We Don't Know | Confidence (🟢🟡🔴). One row per major topic. Include speaker attribution in "What We Know" column. Confidence meaning: 🟢 = can act on now; 🟡 = can draft with caveats; 🔴 = blocked, must resolve first.
5. **ASSUMPTIONS THAT NEED VALIDATION** — Each as `### ⚠️ ASSUMPTION: [statement]` with STATUS / VALIDATE WITH + BY WHEN / RISK IF WRONG. Mark confirmed assumptions with ✅. Only include assumptions that, if wrong, change the system design or block a decision.
6. **OPEN QUESTIONS** — Grouped by severity with sub-headers that state what they block:
   - `### 🔴 HIGH — Block design`
   - `### 🟡 MEDIUM — Block detailed requirements`
   - `### 🟢 LOWER — Don't block Phase 1`
   - Each question: numbered bold title, 1-2 context bullets, Owner + Due.
7. **AGREED NEXT STEPS** — Table with columns: Owner | Action | Trace (transcript link). Every action item must have a named owner.
8. **Footer** — Two-line disclaimer: "All content derived directly from the session transcript. No assumptions or external information added." + Source transcript link.

---

## Step 4: Topic internal structure by meeting type

### Discovery / Requirements topics

Each topic:
- Opens with a 1-sentence context line (what this topic is about).
- Bullet points with transcript traceability links.
- `**Current state context:**` sub-block if relevant (embeds current state within the topic).
- Rejected/deferred alternatives inline with ❌/⏸️ icons.
- Corrections noted with `**Correction:**` prefix.
- `**Concern:**` prefix for concerns raised.

### Engineering / Technical topics

Each topic:
- **Context:** 1-2 sentences on why this was discussed. Traceability link.
- **Requirements:** Bullet list of what must be true. Traceability links.
- **Final Decision:** ✅ bullets — outcome only. Traceability links.
- **Alternatives Considered:** ❌ rejected / ⏸️ deferred — one line each with reason and attribution. Omit this block if no alternatives were raised.
- **Key Technical Insights:** Numbered list of non-obvious learnings relevant to this topic. Only include if the insight adds value beyond what's in the requirements/decisions. Omit if none.

### Guidance that applies to both

- Number topics sequentially.
- Keep bullets tight — one fact per bullet.
- Bold key terms.
- Topics with only 1-2 bullets should be merged into a related topic.
- Empty or "Not discussed" topics should be removed entirely (don't create placeholder topics).

---

## Step 5: After drafting

1. **Deduplication check** — Does any fact appear in more than one section? If yes, keep it in the primary topic and remove from elsewhere.
2. **Traceability check** — Does every bullet in Topics and Next Steps have a transcript link? Add any missing.
3. **Attribution check** — Does every key decision/insight have a speaker name?
4. **Facts check** — Scan for any invented values, assumptions, or outside information. Remove or flag as `[TBD]`.
5. **Length check** — Target 150–250 lines for a 1-hour meeting. If over, cut redundancy. If under, check for missing topics.
6. **Filename** — Use format: `[Feature]_Discovery_Summary_[YYYYMMDD].md` or `[Feature]_Meeting_Summary_[YYYYMMDD].md`.

---

## Additional resources

- For the template, see [templates.md](templates.md)
