# Feature Requirements: [Feature Name]

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Mode:** [Quick / Comprehensive]
**Owner:** [Product Owner / Team]
**Status:** [Draft / In Review / Approved]

> **Audience:** Product managers, developers, architects, QA engineers
> **Language rule:** Plain English. "System must X" not "System should consider X."
> **Source rule:** Tier 1 items (business rules, performance, compliance) must have sources. Mark unknowns as [TBD — requires [stakeholder]].

---

## 1. Executive Summary

[3–4 sentences covering: What is being built | Why it exists (business value) | Who uses it | Priority/timeline]

---

## 2. Business Context

### Business Goals
- [Goal 1] (Source: [reference])
- [Goal 2] (Source: [reference])

### Success Metrics
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [Metric 1] | [Target] | [How measured] |
| [Metric 2] | [Target] | [How measured] |

(Source: [reference])

### Constraints
- **Timeline:** [deadline or TBD]
- **Budget:** [if known]
- **Regulatory:** [if applicable or N/A]
- **Technical:** [e.g., must use existing infrastructure]

### Stakeholders
| Stakeholder | Role | Interest |
|-------------|------|----------|
| [Name/Role] | [Type] | [What they care about] |

---

## 3. Scope

### In Scope (This Phase)

| Capability | Description | Source |
|---|---|---|
| [Capability 1] | [What it enables — user value] | [SRC-N] |
| [Capability 2] | [What it enables] | [SRC-N] |

### Out of Scope (This Phase)

| Item | Reason / Notes | Source |
|---|---|---|
| [Excluded item 1] | [Why excluded — deferred to Phase N, not needed, etc.] | [SRC-N] |
| [Excluded item 2] | [Why excluded] | [SRC-N] |

---

## 4. User Context

### Primary Personas
**[Persona Name/Role]**
- Goals: [what they want to achieve]
- Pain points: [current frustrations]
- Usage context: [when/where/how]
- Quote: *"[Representative statement]"*

(Source: [reference])

### User Needs
1. [Need 1 — user language, not system language]
2. [Need 2]

### High-Level User Journey
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## 5. UX Context *(Skip for Backend-only features)*

### Design Assets
- [Figma link — add `/m=dev` for dev mode] or [Mockup reference]
- [Additional assets]

### User Flows

**Flow 1: [Flow Name] (Happy Path)**
1. [Step 1]
2. [Step 2]
3. [Step 3] → [Outcome]

**Alternative: [Scenario Name]**
- [Difference from happy path] → [Outcome]

### Visual States

| State | Description | Trigger |
|-------|-------------|---------|
| Empty | [What user sees with no data] | First load / no results |
| Loading | [Skeleton/spinner behavior] | During data fetch |
| Success | [Confirmation] | On completion |
| Error | [Error message, dismiss behavior] | On failure |
| No Data | [Message when query returns 0 results] | On empty result |

### Key Interactions

| Interaction | Trigger | Action | Feedback |
|-------------|---------|--------|----------|
| [Element] | [User action] | [System action] | [User feedback] |

### Responsive Design

| Breakpoint | Layout | Notes |
|------------|--------|-------|
| Desktop (1920px+) | [layout description] | |
| Tablet (768px) | [layout description] | |
| Mobile (375px) | [layout description] | |

---

## 6. Technical Context

### System Architecture
```
[Component A] → [Component B] → [Component C]
```

[Brief description of component roles]

### Technology Stack
- **Frontend:** [Framework, language, key libraries]
- **Backend:** [Framework, language, database]
- **External:** [Key integrations]

### APIs / Endpoints

| Endpoint | Method | EXISTING/NEW | Purpose |
|----------|--------|--------------|---------|
| `/api/[path]` | POST | NEW | [purpose] |

*See API Contract for detailed specifications.*

### Data Model (Key Entities)

**[Entity Name]**
| Field | Type | Description |
|-------|------|-------------|
| [field] | [type] | [description] |

### Integration Points

| System | Interface | Purpose | Owner | SLA |
|--------|-----------|---------|-------|-----|
| [System] | [API/DB] | [purpose] | [team] | [uptime] |

### Performance Requirements
- Response time: [target] (Source: [reference])
- Concurrency: [max concurrent users/requests]
- Data limits: [max payload, rows, file size]
- Timeouts: [frontend timeout / backend timeout]

---

## 7. Compliance & Constraints *(Comprehensive mode only)*

- **Regulatory:** [Requirements or N/A]
- **Security:** [Auth method, data protection, encryption requirements]
- **Accessibility:** [WCAG level or N/A]
- **Browser support:** [Browsers + minimum versions]
- **Device support:** [Desktop / tablet / mobile specifications]
- **Backward compatibility:** [Impact on existing or N/A]

---

## 8. Functional Requirements

### FR-1: [Requirement Name]

**Description:** [What this enables — user value, not technical implementation]

**Inputs:**
- [Input 1: field name, type, source]

**Outputs:**
- [Output 1: what the system returns]

**Business Rules:**
- [Rule 1] (Source: [reference])
- [Rule 2] (Source: [reference])

**Validation:**
- Frontend: [What the UI validates before submission]
- Backend: [What the API validates on receipt]

**Source:** [Document/person, date]

---

### FR-2: [Requirement Name]
*(Repeat structure above)*

---

## 9. Error Handling

### Error Scenarios

| Error Type | Cause | User Experience | System Behavior |
|------------|-------|-----------------|-----------------|
| Validation (422) | [Cause] | [Specific message user sees] | [System response] |
| Auth (401) | [Cause] | [Redirect/message] | [System response] |
| Permission (403) | [Cause] | [Message] | [System response] |
| Service down (503) | [Cause] | [Retry suggestion] | [System response] |
| Timeout (504) | [Cause] | [Retry suggestion] | [System response] |
| Internal (500) | [Cause] | [Contact support + requestId] | [Log + alert] |

### Exact Error Messages
- Validation: "[Exact text]" (field: [field name])
- Timeout: "[Exact text]"

---

## 10. Backward Compatibility *(Include ONLY if modifying existing features)*

### Changes Overview
- [What is being modified]

### Breaking Changes
| Change | Affected Consumers | Impact |
|--------|--------------------|--------|
| [Change] | [Who uses this] | [What breaks] |

> ⚠️ Breaking changes require architect approval before implementation.

### Non-Breaking Changes
- [Change 1 — why it's backward compatible]

### Migration Strategy
- [How to handle transition]
- [Deprecation timeline if applicable]

### Recommendation
- [Minimum-impact approach]

---

## 11. Known Limitations

> **Classification rule:** Items here are confirmed gaps the team is shipping with (accepted trade-offs). If an item has an owner and delivery status, it belongs in Dependencies (section 13). If it is a non-negotiable rule, it belongs in Constraints (section 2/7).

- [Limitation 1] — Reason: [why this constraint exists]
- [Limitation 2] — Reason: [why]

---

## 12. Future Enhancements

> See **Section 3: Out of Scope** for the full exclusion list with sources.

Items below add detail beyond what the scope table captures (e.g., phased roadmap, dependencies between deferred items):

- [Enhancement 1] — [additional detail not in scope table]
- [Enhancement 2]

---

## 13. Assumptions & Dependencies

> **One item, one home.** An item is either an Assumption or a Dependency, never both. If it has an owner and delivery status, it is a Dependency. If it needs a stakeholder decision, it is an Open Question (section 15), not an Assumption. Confirmed assumptions should be deleted or moved to Known Limitations (section 11) if the confirmed fact creates a trade-off.

### Assumptions

> Something we believe but haven't confirmed; carries risk if wrong.

| # | Assumption | Status | Source |
|---|------------|--------|--------|
| H1 | [High-risk assumption] | [Status] | [SRC-N] |
| M1 | [Medium-risk assumption] | [Status] | [SRC-N] |
| L1 | [Low-risk assumption] | [Status] | [SRC-N] |

### Dependencies

> A deliverable another team must provide before we can build.

| Dependency | Owner | Status | Risk |
|------------|-------|--------|------|
| [Item] | [Team] | [Status] | 🔴 Critical |
| [Item] | [Team] | [Status] | 🟡 Medium |
| [Item] | [Team] | [Status] | 🟢 Low |

---

## 14. Related Documents

| Document | Location | Status |
|----------|----------|--------|
| Design Files | [Figma URL] | [status] |
| [Other related docs] | [path or URL] | [status] |

---

## 15. Open Questions / TBD Items

> **Classification rule:** Items here are stakeholder decisions needed before proceeding. If an item is also listed as an Assumption, keep the OQ and delete the Assumption. If an item is just "can X team provide Y?", it belongs in Dependencies (section 13), not here.

*Sorted by priority, highest first.*

| # | Question | Priority | Stakeholder | Target Date |
|---|----------|----------|-------------|-------------|
| 1 | [TBD item] | 🔴 Critical | [PM/Architect/Designer/Legal] | [date] |
| 2 | [TBD item] | 🟡 Important | [PM/Architect/Designer/Legal] | [date] |
| 3 | [TBD item] | 🟢 Nice to have | [PM/Architect/Designer/Legal] | [date] |

---

## 16. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | [name] | Initial requirements |
