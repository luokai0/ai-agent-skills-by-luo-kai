# Design Context Document Templates

---

## Template A: User Flow Document

```markdown
# [Feature] - [Flow Name]

**Flow Type:** [e.g., Onboarding / Checkout / Settings / Error recovery / etc.]
**Trigger:** [What initiates this flow — e.g., user taps X, system event, deep link]
**Precondition:** [Any state that must be true before the flow starts — e.g., logged in, item in cart, or N/A]
**Screens:** [N screens (N+1 if [conditional case])]
**Source:** Design images from [folder/file name]

---

## Flow Overview

[1-2 sentences: what this flow covers, who it's for, what the end state is.]

---

## Scope

### In Scope — This Flow
- [condition 1]
- [condition 2]

### Out of Scope — Other Flows
- **[Scenario]** — See [Flow Name / Doc Name]
- **[Scenario]** — See [Flow Name / Doc Name]

---

## User Flow Diagram

```
[Screen 1: Name]
    ↓ (User action)
[Screen 2: Name]
    ↓ (User action)
[Screen 2a: Name] ← [CONDITIONAL — describe when]
    ↓ (User action)
[Screen 3: Name]
    ...
```

---

## Screen-by-Screen Breakdown

### Screen 1: [Name]

**Screen Purpose:** [One sentence.]

**Key Elements:**
- [Section/element: description]
- [Section/element: description]

**Primary User Action:**
- Tap "[Button label]" → Navigate to Screen 2

**Secondary Actions:**
- Tap [element] → [result]

**State:** [What state is the system/user in on this screen]

---

### Screen 2: [Name]

**Screen Purpose:** [One sentence.]

**Key Elements:**
- [element: description]

**Primary User Action:**
- Tap "[Button label]" → [result]

**Secondary Actions:**
- [element] → [result]

**State:** [State description]

---

### Screen 2a: [Name] ([CONDITIONAL SCREEN])

**Screen Purpose:** [One sentence.]

**Key Elements:**
- [element]

**Primary User Action:**
- Tap "[Button label]" → Navigate to Screen 3

**Secondary Actions:**
- [element] → [result]

**State:** [State description]

**Display Logic:**
- **Show:** [Condition under which this screen appears]
- **Skip:** [Condition under which this screen is bypassed]

---

<!-- Repeat for all screens -->

---

## State Transitions

### [State Type — e.g., Location Monitoring Status]

1. **Screen 1:** [State value] — [Explanation]
2. **Screen 2:** [State value] — [Explanation]
3. **Screens 5 & 6:** [State value] — [Explanation]

### [State Type — e.g., Shift Status]

1. **Screen 1:** [State]
2. **Screen 5:** [State]

---

## Key User Interactions Summary

| Screen | Primary Action | Secondary Actions |
|--------|---------------|-------------------|
| Screen 1 | [action] | [actions] |
| Screen 2 | [action] | [actions] |

---

## Required User Actions

1. [Step — required action]
2. [Step — required action]

**Critical Path:** [Note any steps that cannot be skipped.]
**Conditional Steps:** [Note any steps that only appear under certain conditions.]

---

## Error Handling & Edge Cases

### 1. [Error Category — e.g., Network Errors]

#### Error Scenario 1.1: [Name]
**When:** [Trigger condition]

**System Response:**
- [What the system does]

**User Actions:**
- [What the user can do]

**Recovery Path:** [How the user gets back on track]

---

### 2. [Error Category]

#### Error Scenario 2.1: [Name]
**When:** [Trigger]

**System Response:**
- [Response]

**User Actions:**
- [Actions]

**Recovery Path:** [Path]

---

### Error Handling Principles

1. [Principle]
2. [Principle]

---

## Design Notes

- **Color Scheme:** [observations]
- **Typography:** [observations]
- **Icons:** [observations]
- **Spacing/Layout:** [observations]
- **Accessibility:** [observations]

---

## Dependencies & Assumptions

### Technical Dependencies
- [dependency]

### Business Dependencies
- [dependency]

### Assumptions
- [assumption]

---

## Related Flows & Documentation

- **[Flow/Doc Name]:** [what it covers]
- **[Flow/Doc Name]:** [what it covers]

---

**Document Version:** 1.0
**Last Updated:** [date]
**Source:** Design images from [folder/file name]
```

---

## Template B: Design Description

```markdown
# [Feature / Screen Name] - Design Description

## Overview

[1-2 sentences: what this screen/feature is, who uses it, where it lives in the app.]

---

## [Screen Name] Interface Components

### [Section — e.g., Header Area]

- [Element: description]
- [Element: description]

### [Section — e.g., Main Content Area]

- [Element: description]
- [Element: description]

### [Section — e.g., Bottom Navigation Bar]

**Navigation Items:**
- **"[Label]"** ([position]): [icon description], [active state: highlighted in X color]
- **"[Label]"**: [icon description]

---

## [Feature] Components

### [Component Name]

**Visual Design:**
- Position: [location in layout]
- Icon: [icon description]
- Label: "[label text]" in [color] [style]

**States:** *(document each visible state — omit any not shown in designs)*
- Default: [description]
- Active / Selected: [description or `[TBD]`]
- Disabled: [description or `[TBD]`]
- Loading: [description or `[TBD]`]
- Empty: [description or `[TBD]`]
- Error: [description or `[TBD]`]

**Purpose:** [What this component enables the user to do.]

**Navigation:**
- Tapping navigates to [destination]
- [Any conditional navigation logic]

**Behavior:**
- [Interaction detail]
- [State change on user action]

**Back Button Behavior:**
- [Condition] → returns to [screen]
- [Condition] → returns to [screen]

---

<!-- Repeat for each component -->

---

## Destination Screens

### [Screen Name]

#### Interface Components

**Header/Navigation Bar:**
- [element]

**[Section]:**
- [element]
- [element]

**[Empty State / Loading State / Error State — if visible]:**
- [description]

#### Interactions and Behavior

**[Interaction Type]:**
- [Detail]

**Navigation:**
- Back button → [destination based on entry point]

---

<!-- Repeat for each destination screen -->

---

## [Special Logic Section — e.g., Navigation Context Management]

[Document any non-obvious logic governing back button, deep links, or context tracking.]

1. **[Logic Name]:** [explanation]
2. **[Logic Name]:** [explanation]

---

## User Experience Considerations

### Consistency
- [observation]

### Accessibility
- [observation]

### Efficiency
- [observation]
```

---

## Template C: Context Summary

```markdown
# Context Summary - [Feature Name]

**Feature Name:** [name]
**Date Created:** [date]
**Mode:** [Full Mode / Quick Mode]
**Input Sources:** [list image files or describe source]

---

## 1. Six-Context Summary

### Business Context
- **Goal:** [what this feature achieves for the business]
- **Problem:** [what user/business problem it solves]
- **Business Value:** [measurable or strategic value]
- **Scope:** [what's included]
- **Target Users:** [who uses this]

*(Source: [image file(s)] + [any user clarifications])*

### Product Context
- **Feature:** [feature description]
- **Entry Points:** [how users get to this feature]
- **Flow Type:** [modal / inline / full screen / etc.]
- **Navigation Pattern:** [how users move through it]
- **Content Areas:** [what content/functionality is included]
- **Completion:** [how the feature ends/exits]

*(Source: [image file(s)])*

### Persona Context
**[N/A — Quick Mode (skipped)]**
OR
- **Primary Persona:** [name / role]
- **Goals:** [what they're trying to do]
- **Pain Points:** [what's hard for them today]

*(Source: [source])*

### UX Context

**UI Pattern:** [modal / card / form / carousel / etc.]
- [Visual pattern observation]
- [Color/branding observation]

**[Flow/Screen Name] ([N] screens):**
1. **[Screen Name]:** [description — elements, actions]
2. **[Screen Name]:** [description]
...

**Interactive Elements:**
- [element type]

**Content Tone:** [friendly / formal / instructional / etc.]

*(Source: [image file(s)])*

### Technical Context
**[N/A — Quick Mode (skipped)]**
OR
- **Platform:** [iOS / Android / Web]
- **Dependencies:** [APIs, SDKs, services referenced in designs]
- **Data:** [what data is displayed or submitted]

*(Source: [source])*

### Compliance/Constraints Context
**[N/A — Quick Mode (skipped)]**
OR
- **Regulatory:** [privacy, legal requirements visible in designs]
- **Constraints:** [limitations noted in designs]

*(Source: [source])*

---

## 2. Source Attribution

*How to calculate coverage: Count items in each tier. Coverage = items with a confirmed image/user source ÷ total items × 100. An item counts as sourced only if you can point to a specific image or explicit user statement — inference does not count.*

### Tier 1 Items (100% required — business rules, critical behaviors)
- **[Item]:** [description] → *(Source: [image / user clarification])*
- **[Item]:** [description] → *(Source: [image / user clarification])*

**Tier 1 Coverage:** [sourced count] / [total count] = [X]% [✅ if 100% / ⚠️ if <100%]

### Tier 2 Items (60%+ target — functional requirements, interactions)
- **[Item]:** [description] → *(Source: [image])*

**Tier 2 Coverage:** [sourced count] / [total count] = [X]% [✅ if ≥60% / ⚠️ if <60%]

### Tier 3 Items (optional — UI details, copy, styling)
- [item] → *(Source: [image — visible / not visible])*

---

## 3. EXISTING vs NEW Classification

**NEW (greenfield / net-new functionality):**
- [component or behavior]

**EXISTING (modifications to existing screens/flows):**
- [screen or component]: [what changes]

**Backward Compatibility:** [No breaking changes / Breaking change — describe]

---

## 4. Unresolved Gaps

### 🔴 RED (Critical — blocks requirements generation)
[None ✅]
OR
1. **[Gap]:** [what's unknown] → *(Requires: [who can answer])*

### 🟡 YELLOW (Important — reduces quality)
1. **[Gap]:** [what's unknown] → *(Requires: [who can answer])*

### 🟢 GREEN (Optional — nice-to-have)
1. **[Gap]:** [what's unknown] → *(Requires: Design handoff / Product decision)*

---

## 5. Source Traceability Report

- **Tier 1 source coverage:** [sourced] / [total] = [X]% [✅ if 100% / ⚠️ if <100%]
- **Tier 2 source coverage:** [sourced] / [total] = [X]% [✅ if ≥60% / ⚠️ if <60%]
- **Total items with confirmed sources:** [sourced T1+T2] / [total T1+T2] = [X]%
- **Unresolved gaps:** [N] RED, [N] YELLOW, [N] GREEN

---

## 6. Summary Statistics

- **Contexts analyzed:** [N] ([list which ones])
- **Input sources:** [N] design images [+ user clarifications if any]
- **Total screens documented:** [N]
- **Critical gaps resolved:** [N] of [N]
- **Quality score:** [High / Medium / Low] ([reason])

---

## Ready for Next Step

**Status:** [✅ Ready / ⚠️ Blocked by RED gaps]

**Recommended output:**
- [Document type, e.g., Feature Requirements Document]
- Document type: [new feature / feature enhancement / bug fix]
- Estimated length: [X–Y words]

---

**Generated:** [date]
**Source:** [image file names]
**Next Workflow:** Requirements generation
```
