# Epic: [Feature/Area] -- [Goal/Capability]

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Owner:** [Product Owner / Team]
**Status:** Draft

> **Audience:** Product Owner + Team Lead, during sprint planning and roadmap review.
> **Source rule:** Every claim traces to source. Mark unknowns as `[TBD — requires: {need}] (Route to: {role})`.

---

## Description

[Core value this epic delivers and why it matters. 2-3 sentences. Sourced.]

---

## Outcomes / Success Criteria

- [Outcome 1 — measurable: number, percentage, or observable condition] (Source: [reference])
- [Outcome 2] (Source: [reference])

---

## Context

- **Initiative/Release:** [how it fits]
- **Key decisions:** [decisions already made] (Source: [reference])
- **Discovery docs:** [links to requirements, PRDs]
- **Constraints:** [timeline, budget, regulatory, technical] (Source: [reference])

---

## Designs

- [Figma link with /m=dev — annotated flows or wireframes]
- [Mobile + desktop variants if relevant]
- **Open design questions:** [list any unresolved design decisions]

---

## Scope

[High-level capabilities covered. Features, not technical tasks. Each sourced.]

- [Capability 1] (Source: [reference])
- [Capability 2] (Source: [reference])

---

## Out of Scope

[Explicitly NOT included in this epic. Manages expectations.]

- [Exclusion 1]
- [Exclusion 2]

---

## Risks & Dependencies

[Blockers and cross-team impacts that might delay delivery.]

| Risk / Dependency | Type | Impact | Owner |
|-------------------|------|--------|-------|
| [Item] | Risk / Dependency | [Impact description] | [Team/Person] |

---

## Technical Considerations

[Reserved for architect/dev lead notes — not populated by this skill.]

---

## Milestones

| Milestone | Target Date |
|-----------|------------|
| [Milestone 1] | [Date or TBD] |

---

## Change History

| Date | Change |
|------|--------|
| [YYYY-MM-DD] | Initial creation |

---

## Reference Example

> Match the specificity and sourcing pattern below, not the content.

### Product Discovery -- Browse Clothing with Details (MVP)

**Description:**
Allow shoppers (guest or logged-in) to browse clothing items by category with clear visibility into product name, price, size availability, and key attributes. (Source: PRD, §1)

**Outcomes / Success Criteria:**
- 80% of users view at least 3 products per session (Source: PRD, §Success Metrics)
- Bounce rate on product list page < 40% (Source: PRD, §Success Metrics)
- Page load time for category listing < 1.5s on 3G (Source: PRD, §Performance)

**Context:**
- **Initiative:** MVP Launch — Validate $50+ orders in GTA
- **Key decisions:** No filtering or search in MVP. Category-driven. Mobile-first, desktop parity required. (Source: PRD, §Scope Decisions)

**Scope:**
- Display products by selected category (Source: PRD, §3.1)
- Show name, image, price, availability (Source: PRD, §3.2)
- Support pagination/infinite scroll (Source: PRD, §3.3)
- Handle loading, empty, and error states (Source: Design, screen-05)

**Out of Scope:**
- Product filtering, search bar, sorting, personalized recommendations

> **Why this works:** Every outcome is measurable and sourced. Scope items traced to source. Out-of-scope explicit. Context cites decisions, doesn't repeat PRD.
