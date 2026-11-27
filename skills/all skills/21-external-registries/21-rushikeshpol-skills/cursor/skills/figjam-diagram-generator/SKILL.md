---
name: figjam-diagram-generator
description: >-
  Generates Mermaid.js diagrams in FigJam from requirements documents, user
  flows, state descriptions, or verbal input. Supports flowcharts, sequence
  diagrams, state diagrams, and gantt charts via the Figma MCP generate_diagram
  tool. Applies client-reviewed flow modeling conventions (shape vocabulary,
  actor naming, audit nodes, cross-system handoffs). Runs a 6-priority
  verification gate (accuracy, clarity, readability, completeness, conciseness,
  structure) before generating. Use when asked to: create a FigJam diagram,
  generate a user flow in FigJam, create a flowchart from requirements, build a
  sequence diagram, generate a state diagram, visualize a user flow, or any
  request involving Mermaid diagrams in FigJam.
---

# FigJam Diagram Generator

## Non-Negotiables

- NEVER fabricate flow steps not in the source. Every node must trace to the source document.
- NEVER call `generate_diagram` before completing the Step 4 verification gate.
- NEVER use `create_new_file` before `generate_diagram` — it creates its own FigJam file.
- All flows for one feature go into ONE `generate_diagram` call using subgraphs.
- Read [mermaid-patterns.md](mermaid-patterns.md) before generating any Mermaid syntax.

---

## Step 0: Resolve Input Source

Determine where the flow content comes from:

| Case | Input | Action |
|------|-------|--------|
| A | Requirements document path | Read the file. Proceed to Step 1. |
| B | Verbal description | Capture it. Proceed to Step 1. |
| C | FigJam board URL | Use `get_figjam` MCP tool (server: `user-figma`, fileKey from URL, nodeId `0:1`) to read existing content for context. Optional — only if user wants to reference what's already on a board. |
| D | No input provided | Ask: *"Which requirements doc or flow should I diagram?"* Stop until answered. |

**URL parsing for FigJam boards:**
- `figma.com/board/:fileKey/:fileName?node-id=:nodeId` → `fileKey` is the segment after `/board/`, `nodeId` converts `-` to `:`

---

## Step 1: Identify Flows to Diagram

1. Scan the source for labeled flows (e.g., `**Flow UF-1:**`, `**Flow UF-2:**`, numbered step sequences under flow headings).
2. Present the list to the user via AskQuestion. Ask which to generate (one, some, or all).
3. For each selected flow, extract:
   - Flow name and ID
   - Numbered steps
   - Decision points and branch conditions
   - Actors involved (Officer, System, DM, etc.)
   - Error/alternative paths
   - FR references
   - Notification text and UI copy (verbatim where specified)
   - Audit/compliance data fields mentioned
4. **Multi-actor decomposition:** If a flow involves actors across different systems (e.g., Officer in MyConnect + DM in WFM), split into separate per-actor subgraphs with explicit handoff points. Title each: `[Feature] - [Actor] [action] flow in [System]`.

---

## Step 2: Select Diagram Type

Auto-detect per flow:

| Signal in source | Diagram Type |
|-----------------|--------------|
| Sequential user actions with decision branches | `flowchart LR` |
| System-to-system interactions, request/response | `sequenceDiagram` |
| Entity with named states and transitions | `stateDiagram-v2` |
| Timeline with dates and durations | `gantt` |

User can override. If ambiguous, ask with AskQuestion.

---

## Step 3: Generate Mermaid Syntax

Read [mermaid-patterns.md](mermaid-patterns.md) for shape mapping, edge patterns, and working examples.

### Flowchart conventions

**Shapes:**
- `(["..."])` stadium — start/end states (actor actions that begin or end the flow)
- `{"..."}` diamond — decisions, system checks
- `["..."]` rectangle — actions, screens, system behaviors, notifications
- `[("...")]` cylinder — audit/data storage

**Edges:**
- `-->|"label"|` — decision outcomes, user actions (use descriptive labels, not bare Yes/No)
- `-->` — simple sequential connection
- `-.->|"label"|` — cross-subgraph handoff (dotted)

**Subgraphs:**
- One subgraph per flow/actor: `subgraph flowId ["Feature - Actor action flow in System"]`
- Cross-flow handoffs as dotted edges between subgraphs

**Content in nodes:**
- Include verbatim UI copy when the source specifies it
- Show affordances: "Click: YES / NO", "Provide Reason: ___"
- Include conditional display logic: "(not shown on subsequent clock-outs)"
- Notification nodes include content summary and follow-up action

**Audit nodes:**
- When the source mentions compliance data, add a cylinder listing stored fields

### Standard Color Palette (flowcharts — always apply)

Every user flow flowchart must include the following `classDef` block and `class` assignments. Do NOT skip this for any flowchart. No color styling in gantt/sequence diagrams.

**Color legend:**

| Class | Fill | Stroke | Text | Shape | Meaning |
|---|---|---|---|---|---|
| `terminus` | `#D4EDDA` | `#28A745` | `#1E4620` | Stadium `(["..."])` | Start / End of a flow |
| `decision` | `#FFF3CD` | `#F59E0B` | `#664D03` | Diamond `{"..."}` | Decision / system check |
| `action` | `#CFE2FF` | `#0D6EFD` | `#084298` | Rectangle `["..."]` | Action / screen / processing |
| `notification` | `#FFE5CC` | `#FB923C` | `#7C2D12` | Rectangle `["..."]` | User-facing notification or in-app reminder |
| `errorPath` | `#F8D7DA` | `#DC3545` | `#58151C` | Rectangle `["..."]` | Error / fallback / degraded path |

**Classification rules:**
- `terminus` — every stadium node (flow start and end)
- `decision` — every diamond node
- `notification` — rectangles that compose/send push notifications, display in-app reminders or alerts to the user
- `errorPath` — rectangles that show offline banners, cached/stale data, fallback states, or paths where the normal flow cannot proceed
- `action` — all remaining rectangles

**Classdefs to append after all subgraphs and cross-subgraph edges:**

```
classDef terminus fill:#D4EDDA,stroke:#28A745,stroke-width:2px,color:#1E4620
classDef decision fill:#FFF3CD,stroke:#F59E0B,stroke-width:2px,color:#664D03
classDef action fill:#CFE2FF,stroke:#0D6EFD,stroke-width:2px,color:#084298
classDef notification fill:#FFE5CC,stroke:#FB923C,stroke-width:2px,color:#7C2D12
classDef errorPath fill:#F8D7DA,stroke:#DC3545,stroke-width:2px,color:#58151C

class <terminus node IDs> terminus
class <decision node IDs> decision
class <action node IDs> action
class <notification node IDs> notification
class <errorPath node IDs> errorPath
```

### MCP hard constraints

- All text in double quotes for flowchart/graph
- No emojis, no `\n`, no `end` as ID/className
- Subgraph IDs: camelCase or underscores, no spaces
- No color styling in gantt/sequence; no notes in sequence
- LR direction default for flowcharts

---

## Step 4: Verify and Fix

**Mandatory gate.** Run all checks in priority order. Fix issues silently. Do NOT call `generate_diagram` until all checks pass.

### Priority 1: Accuracy

The flow must faithfully represent the source.

- [ ] Every decision condition matches the source exactly (thresholds, time windows, actor responsibilities). No invented or rounded values.
- [ ] No fabricated steps. Every node traces to a step, business rule, or FR in the source.
- [ ] Actor attribution is correct. Actions assigned to the right actor (Officer vs System vs DM).
- [ ] Decision branch outcomes match the source logic. Not inverted, not simplified away, not merged.
- [ ] FR references in node labels are correct. "(FR-5)" corresponds to actual FR-5 content.
- [ ] Notification text, UI copy, and conditional logic match the source verbatim where specified.

**Fix:** Correct mismatched values, swap actors, fix FR references by re-reading the source. Remove fabricated steps.

### Priority 2: Clarity

A stakeholder can follow the flow without the requirements doc.

- [ ] Every node label is self-explanatory. No vague labels ("System processes request", "Next step").
- [ ] Decision diamonds state the specific question ("Shift starts within 60 min?" not "Time check").
- [ ] Edge labels explain "why" when a path skips steps or leads to unexpected outcomes.
- [ ] Actors named consistently throughout. Same term every time.
- [ ] Conditional display notes included where behavior isn't obvious.

**Fix:** Rewrite vague labels using source context. Standardize actor names across all nodes.

### Priority 3: Readability

Visual layout is clean and scannable in FigJam.

- [ ] LR direction. Entry node defined first in code (Mermaid places first-defined leftmost).
- [ ] No back-links (edges from later to earlier nodes). Remove if detected.
- [ ] Node labels are 5-15 words. Not cryptic, not compressed.
- [ ] Balanced branching. If one path has 8 nodes and another has 1, check for missing detail.
- [ ] Total nodes per subgraph does not exceed 20.
- [ ] Consistent label length within a subgraph.

**Fix:** Remove back-links. Truncate long labels. Split oversized subgraphs. Add nodes to short branches if source warrants it.

### Priority 4: Completeness

All paths from the source are represented.

- [ ] Every numbered step in the source has a node or edge.
- [ ] Alternative and error paths from the source are included, not just the happy path.
- [ ] Time-based conditions captured (same-day exceptions, batch windows, pay cycle boundaries).
- [ ] Notification content variants included where source specifies them.
- [ ] Cross-flow handoffs exist where one flow triggers another.
- [ ] Audit/storage nodes present when source mentions compliance data.

**Fix:** Add missing nodes from the source. Report: "Added nodes for [items] from the requirements."

### Priority 5: Conciseness

No redundant or over-detailed nodes.

- [ ] No duplicate nodes conveying the same information differently.
- [ ] No unnecessary intermediate nodes adding no decision or action ("System receives data" + "System processes data" → combine).
- [ ] Labels are tight. Strip filler ("then", "next", "the system will") without losing meaning.
- [ ] Subgraphs with 15+ nodes reviewed for merge opportunities.

**Fix:** Merge duplicates, remove filler nodes, tighten labels. Do not remove nodes carrying distinct meaning.

### Priority 6: Structure/Format

Mermaid syntax is valid and shapes match conventions.

- [ ] All text in double quotes (flowchart/graph).
- [ ] No emojis, no `\n`, no `end` as ID/className.
- [ ] Diagram type is supported: flowchart, graph, sequenceDiagram, stateDiagram-v2, gantt.
- [ ] No color styling in gantt/sequence. No notes in sequence.
- [ ] Subgraph IDs use camelCase/underscores.
- [ ] Correct shapes: stadium for start/end, diamond for decisions, rectangle for actions, cylinder for audit.
- [ ] Subgraph titles follow `[Feature] - [Actor] [action] flow in [System]`.
- [ ] Decision edge labels describe outcomes, not bare "Yes/No".
- [ ] Standard color palette applied: all 5 `classDef` blocks present; every node ID assigned to exactly one class; no node left unclassified.

**Fix:** Add missing quotes, remove emojis, rename reserved IDs, swap wrong shapes, add missing classDef/class assignments. All silent.


**After all checks pass → proceed to Step 5.**

---

## Step 5: Call Figma MCP

Call `CallMcpTool`:
- **server:** `user-figma`
- **toolName:** `generate_diagram`
- **arguments:**
  - `name`: Feature name (e.g., "My Schedule User Flows")
  - `mermaidSyntax`: The verified Mermaid code with subgraphs
  - `userIntent`: Brief description of what was diagrammed

All flows for one feature go into ONE call using subgraphs. Cross-system actor flows get separate subgraphs with dotted handoff edges.

If `generate_diagram` returns an error, check the error message against the MCP constraints in [mermaid-patterns.md](mermaid-patterns.md), fix the syntax, and retry once.

---

## Step 6: Report Results

Present to the user:
- Feature name and flows generated
- Number of subgraphs and total node count
- FigJam link (from the MCP response)
- If fixes were applied in Step 4: "**Fixed:** [list of corrections]"
- Note: `generate_diagram` creates its own FigJam file. To place on an existing board, copy-paste from the generated file.
- Ask: "Would you like any adjustments to readability, detail level, or missing paths?"
