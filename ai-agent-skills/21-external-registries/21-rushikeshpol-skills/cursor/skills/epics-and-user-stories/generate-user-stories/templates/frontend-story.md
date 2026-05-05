# Frontend/Mobile User Story Template

## Structure

```markdown
# User Story [N]: [Platform] -- [Feature Name] -- [Context]

## User Statement
As a [specific persona], I want [goal], so that [business value].

## Background
[2-3 sentences max. WHY this story exists + links. Never repeat epic prose.]
→ Epic: [path]
→ Requirements: [path, §section]

**Design Reference:** [Figma link with /m=dev]

## Acceptance Criteria

**AC1: [Behavior Name]** (Req §X)
Given [precondition]
When [action]
- Then [observable result with specific detail]
- And [visual requirement]

[Image: screenshot/mockup showing this AC's visual state]

**AC2: [Behavior Name]** (Req §Y)
Given [precondition]
When [action]
- Then [observable result]

[Image: screenshot/mockup]

[5-6 ACs maximum. Each: one behavior, Given/When/Then, source citation, visual evidence.]

## Dependencies
- [Story ID] — [what it provides]

## Dev Notes
[EMPTY — for dev team to populate during refinement]

## Change History
| Date | Version | Change | Reason |
|------|---------|--------|--------|
```

## Rules
- **5-6 ACs max** — more means the story is too big. Split, don't compress.
- **WHAT not HOW** — design experience IS requirement (pill, toast, modal = OK). Component names, CSS, framework refs = never.
- **Visual evidence in every AC** — image showing what the user sees for that behavior.
- **Precise terminology** — pill vs button, banner vs alert, toast vs notification. Match the design.
- **60-90 lines target** — 91-120 warning, 121+ review for split.
- **Dev Notes always empty** — never populated by this skill.
- **Source citation on every AC** — `(Req §X)` or `(Source: Design, screen-N)`.
- **Background: reference, don't repeat** — links to epic/requirements for depth.

---

## Reference Example

> Match the specificity, sourcing, and conciseness below.

```markdown
# User Story 6: FE -- Display Status Alert Indicator -- Entity Status Widget

## User Statement
As an Operations Manager, I want to see prominent alerts when there are status violations in the Entity Status widget, so that I can immediately identify operational issues requiring action.

## Background
Adds critical alert system for status violations to Entity Status widget. Status violations indicate activities missing required updates.
→ Epic: epics/entity-monitoring/Epic-Entity-Monitoring.md
→ Requirements: requirements/entity-monitoring/Feature-Requirements-Entity-Monitoring.md, §4.2

**Design Reference:** Primary: https://figma.com/design/abc123?node-id=456&m=dev

## Acceptance Criteria

**AC1: Status Alert Banner Display** (Req §4.2.1)
Given API response with `statusAlerts > 0`
When displaying the status widget
- Then show red border alert banner above the widgets
- And display "You currently have X Status Alert(s). Your Operations Manager has been alerted."
- And use exact count from `statusAlerts` field in bold
- And show alert regardless of chart state (empty or filled)

[Image: Banner with red border above widget area]

**AC2: In-Widget Status Alert Indicator** (Req §4.2.2)
Given API response with `statusAlerts > 0`
When displaying the status widget
- Then show red pill indicator inside the widget
- And display "1 status alert" (singular) or "X status alerts" (plural)
- And ensure indicator is visible at all times regardless of chart state

[Image: Red pill indicator inside widget]

## Dependencies
- BE-story-03 — Status API must return `statusAlerts` count

## Dev Notes
[EMPTY]

## Change History
| Date | Version | Change | Reason |
|------|---------|--------|--------|
| 2026-03-31 | 1.0 | Initial creation | — |
```

## Anti-Pattern

**Bad AC (prescribes implementation):**
```
Given status violations exist
When rendering the alert
- Then use MUI Alert component with severity="error"
- And apply CSS border: 2px solid #d32f2f
- And use useEffect hook to poll for updates every 30 seconds
```
**Why bad:** Prescribes component, CSS, and framework. Developer can't choose tools. The requirement is WHAT the user sees (red alert banner), not HOW it's built.
