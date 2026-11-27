# Stage 6: User Flows

## 6.1 Identify flows needed

Based on actors from Stage 3 and scenarios from Stage 4:

| Flow | Actor | Trigger | Happy Path Steps | Alternative Paths |
|---|---|---|---|---|
| [Flow 1] | [Actor] | [What starts it] | [Count] | [Count] |

## 6.2 Draft each flow

For each flow, produce:
1. **Step-by-step happy path** — numbered steps with actor, action, system response
2. **Decision points** — where the flow branches, with conditions for each branch
3. **Alternative paths** — what happens on each non-happy-path branch
4. **Background processing** — what the system does behind the scenes (data storage, notifications, triggers)
5. **Error handling** — what happens when things go wrong

## 6.3 Flow ordering rationale

If multiple flows exist, explain why they are ordered this way. Consider:
- Which flow is legally or business-critical?
- What happens if the process is interrupted — which data should already be captured?

## 6.4 Present flows for review

Show each flow and ask for feedback before proceeding to full requirements generation.

**Save to:** `[output]/stage_output/Stage6-User-Flows.md`

## 6.5 Requirement Purity Filter

After drafting user flows but before finalizing them, run a classification pass on every element in the flows. For each step, business rule, data field, and behavior description, classify it as:

| Classification | Definition | Action |
|---|---|---|
| **REQUIREMENT** | What the system must enable — observable, testable, solution-free | Keep in the flow and pass to Stage 7 |
| **SOLUTION** | How the system achieves it — implementation mechanism (e.g., "cache locally", "use delta API", "retry with exponential backoff") | Move to an "Implementation Notes" callout. Reframe the underlying need as a requirement. |
| **DESIGN** | What it looks like — UI layout, navigation pattern, visual structure (e.g., "organized as tabs", "swipe left/right") | Move to "Design Decisions [TBD]" or "Open Questions". Reframe the underlying need as a requirement. |
| **DATA** | What information is needed — field lists, data scope | Keep, but verify the source. Flag any data fields not traceable to a source as `[INFERRED — verify]`. |

**Present the classification to the user at the Stage 6 review checkpoint.** This catches solutions and design prescriptions before they enter the requirements document.

**Why this matters:** User flows naturally produce implementation and design details because they describe concrete interactions. Without this filter, those details propagate into Stage 7 as if they were requirements — making the final doc prescribe solutions and designs instead of capabilities.
