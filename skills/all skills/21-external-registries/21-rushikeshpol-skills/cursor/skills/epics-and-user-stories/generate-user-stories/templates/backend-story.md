# Backend/API User Story Template

## Structure

```markdown
# User Story [N]: [BE/API/Integration] -- [Feature Name] -- [Context]

## User Statement
As a [stakeholder or consuming service], I want [backend capability], so that [business/system value].

## Background
[2-3 sentences max. WHY this service/endpoint exists + links.]
→ Epic: [path]
→ Requirements: [path, §section]
→ API Contract: [path, if exists]

**API Details:** [HTTP method, route, auth requirements]
— OR —
**Integration Details:** [External service, auth, data sync requirements]

## Acceptance Criteria

**AC1: [Behavior Name]** (Req §X)
Given [precondition]
When [action/request]
- Then [system behavior with specific detail]
- And [validation requirement]

**AC2: [Behavior Name]** (Req §Y)
Given [precondition]
When [action/request]
- Then [system behavior]

[5-6 ACs maximum. Each: one behavior, Given/When/Then, source citation.]

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
- **WHAT not HOW** — data contract and behavior ARE requirements. Architecture/implementation IS NOT.
- **No code** — no SQL, class names, framework refs. Performance targets are WHAT; caching strategy is HOW.
- **60-90 lines target** — 91-120 warning, 121+ review for split.
- **Dev Notes always empty** — never populated by this skill.
- **Source citation on every AC** — `(Req §X)` or `(Source: API Contract, §Y)`.
- **Background: reference, don't repeat** — links to epic/requirements for depth.

---

## Reference Example

> Match the specificity, sourcing, and conciseness below.

```markdown
# User Story 3: BE -- Historical Data Aggregation Service -- Activity Reports

## User Statement
As an Operations Manager, I want a data aggregation service that retrieves and processes historical activity data from multiple sources, so that Activity Reports can generate comprehensive CSV reports with accurate record summaries.

## Background
Creates data aggregation for Activity Reports, enabling historical reporting for compliance. Integrates multiple data sources for complete activity history.
→ Epic: epics/activity-reports/Epic-Activity-Reports.md
→ Requirements: requirements/activity-reports/Feature-Requirements-Activity-Reports.md, §3

**API Details:** POST /api/reports/aggregate — Bearer auth — returns aggregated dataset

## Acceptance Criteria

**AC1: Retrieve Historical Schedule Data** (Req §3.1)
Given validated report request with date range and entity selection
When aggregating historical data
- Then return schedule data for all days in date range
- And include record IDs, activity times, and assignment details
- And handle multiple activities per entity per day

**AC2: Retrieve Historical Status Tracking Data** (Req §3.2)
Given schedule data with record IDs and date range
When aggregating status tracking data
- Then return status data for all days in date range
- And include start/end times and duration periods
- And identify incomplete records (scheduled activities missing status updates)

**AC3: Provide Aggregated Data by Record and Date** (Req §3.3)
Given all historical data from multiple sources
When processing aggregated data
- Then return data organized by record ID and date
- And include daily summaries: hours scheduled, tracked, compliant, non-compliant
- And ensure data integrity: Total Tracked = Hours Compliant + Hours Non-Compliant

**AC4: Handle Large Datasets and Failures** (Req §3.4, §3.5)
Given date ranges up to 365 days or up to 100 entities
When processing historical data
- Then complete processing within 5 minutes or return timeout error
- And if critical source fails (schedule, status) → return error with specific message
- And if optional source fails (location) → continue with defaults and flag partial data

## Dependencies
- BE-story-01 — Report Generation API must accept and validate requests

## Dev Notes
[EMPTY]

## Change History
| Date | Version | Change | Reason |
|------|---------|--------|--------|
| 2026-03-31 | 1.0 | Initial creation | — |
```

## Anti-Pattern

**Bad AC:** `"Use Entity Framework with LINQ... implement repository pattern... cache in Redis with 15-min TTL... log to Application Insights"`
**Why bad:** Prescribes ORM, pattern, caching, logging. The requirement is WHAT data to return. Developer chooses tools.
