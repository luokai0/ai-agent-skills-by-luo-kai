# [Release Name] — Release Definition

**Last updated:** [date]
**Status:** [Draft / Confirmed / In Execution]

---

## Release Goal

> **[1-2 sentence user-facing goal: what value does this release deliver?]**

[Optional expansion: 2-3 sentences of context — why this matters now, what business problem it solves.]

---

## Success Criteria

How we know this release succeeded. Measured at [release / 30 days / 90 days].

| # | Criterion | Metric | Target | Measured When |
|---|-----------|--------|--------|---------------|
| SC-1 | [User outcome] | [specific metric] | [target number] | [when] |
| SC-2 | [Quality] | [specific metric] | [target] | [when] |
| SC-3 | [Delivery] | [specific metric] | [target] | [when] |

---

## Scope — In

| # | Feature / Item | Priority | Complexity | Type | Dependencies |
|---|---------------|----------|-----------|------|-------------|
| F-1 | [Feature name] | Must | L | New feature | F-3 must complete first |
| F-2 | [Feature name] | Should | M | Enhancement | None |
| F-3 | [Feature name] | Must | S | Infrastructure | None |

**Priority key:** Must = release fails without it. Should = high value, plan for it. Could = nice-to-have, only if capacity allows.

---

## Scope — Out

| # | Item | Reason | Planned For |
|---|------|--------|------------|
| X-1 | [Excluded item] | [Why it's out] | Phase 2 |
| X-2 | [Excluded item] | [Why it's out] | TBD |

---

## Timeline

| Milestone | Date | Notes |
|-----------|------|-------|
| Sprint 0 start | [date] | Foundation sprint |
| Feature build starts | [date] | Sprint 1 |
| UAT 1 | [date] | After Sprint [N] |
| Code freeze | [date] | Sprint [N+2] start |
| Stakeholder UAT | [date range] | Final validation |
| Release to users | [date] | App store submission by [date] |

**Sprint duration:** [N] weeks
**Total sprints:** [N] (1 foundation + [N] feature + 1 stabilization + 1 release)
**Feature sprints available:** [N]

---

## Team & Capacity

| Platform / Role | Headcount | Seniority | Availability | Notes |
|----------------|-----------|-----------|-------------|-------|
| iOS | [N] | [1 L5 lead + N devs] | [%] | [Lead drives architecture] |
| Android | [N] | [1 L5 lead + N devs] | [%] | -- |
| Backend | [N] | -- | [%] | [Shared with other projects] |
| QA | [N] | -- | [%] | -- |
| Product | [N] | -- | [%] | -- |

**Capacity model:** [N] effective dev-days per sprint ([calculation basis]).

---

## Known Constraints

| # | Constraint | Imposed By | Impact on Plan |
|---|-----------|-----------|---------------|
| C-1 | [Description] | [Source] | [How it affects planning] |

---

## Known Risks

| # | Risk | Likelihood | Impact | Owner | Mitigation |
|---|------|-----------|--------|-------|-----------|
| R-1 | [Description] | [H/M/L] | [What breaks] | [Name] | [Action] |

---

## Dependencies

| # | What | From Whom | Needed By | Blocks | Fallback |
|---|------|----------|-----------|--------|---------|
| D-1 | [Deliverable] | [Team/vendor] | [Date] | [Features] | [If late...] |

---

## Release Strategy

**Release type:** [Full release / Phased rollout / Beta / Feature-flagged]
**Legacy app:** [Coexists / Replaced / N/A]
**Rollback plan:** [Description]
**App store:** [Submission timeline, review buffer]

---

## UAT & Quality Strategy

**UAT cadence:** [Every 2 sprints / Every sprint / End-only]
**Participants:** [QA, PM, stakeholders, end users]
**Environment:** [TestFlight, internal track, staging]

### Go / No-Go Criteria

The release ships when ALL of the following are true:

| # | Criterion | Measured By |
|---|-----------|-------------|
| G-1 | Zero P0 defects in production scope | QA regression report |
| G-2 | Zero P1 defects in Must-have features | UAT sign-off |
| G-3 | All Must-have features pass UAT | Stakeholder confirmation |
| G-4 | [Performance threshold met] | Performance test results |
| G-5 | [Compliance requirement met] | [Audit/review] |

### Defect Severity Definitions

| Severity | Definition | Sprint Impact | Release Impact |
|----------|-----------|---------------|---------------|
| **P0** | Crash, data loss, security vulnerability | Stop current work, fix immediately | Release blocked |
| **P1** | Core flow broken, no workaround | Pull into current sprint | Release blocked |
| **P2** | Feature degraded, workaround exists | Plan into next sprint if capacity | Ship with known issue |
| **P3** | Minor, cosmetic, edge case | Backlog | Fix in next release |

---

## Assumptions

| # | Assumption | Confidence | Risk if Wrong | Validate By | Owner |
|---|-----------|-----------|---------------|-------------|-------|
| A-1 | [Statement] | [H/M/L] | [What changes] | [How/when] | [Name] |

---

## Context Assessment Summary

Assessment performed on [date] from [N] input sources.

| Context | Rating | Sources Used | Key Gaps |
|---------|--------|-------------|----------|
| Business | [Strong/Moderate/Weak/Missing] | [list] | [gaps] |
| Product | [rating] | [list] | [gaps] |
| Technical | [rating] | [list] | [gaps] |
| User | [rating] | [list] | [gaps] |
| UX / Design | [rating] | [list] | [gaps] |
| Project | [rating] | [list] | [gaps] |

---

## Context Needed at Sprint Level

| Sprint | Context Needed | Dimension | Source / Owner |
|--------|---------------|-----------|---------------|
| [N] | [Specific context needed] | [Technical/UX/Product/etc.] | [Who to ask] |

---

## Change Log

| Date | Change | Reason | Impact |
|------|--------|--------|--------|
| [date] | Initial definition | -- | -- |
