# Delivery Model

This file defines the domain model that all planning skills operate within. Every skill must understand this model to produce accurate, coherent documents.

**Referenced by:** All 5 planning skills at intake via `MANDATORY READ`.

---

## Release Lifecycle

A release is a bounded commitment: a goal, a scope, a team, and a deadline. It moves through 4 phases. Every sprint belongs to exactly one phase.

**Phase 1 — Foundation (Sprint 0):**
Setup sprint. Repos, architecture, CI/CD, design system, tooling. No feature velocity expected. The only deliverable is: "the team is unblocked."

**Phase 2 — Feature Build (Sprints 1–N):**
Core delivery sprints. Each sprint delivers demonstrable, user-facing capability. Sprint goals are written from the user's perspective ("Officers can log in and clock in") not the team's ("Implement login API integration"). Every sprint in this phase must produce something that can be shown to stakeholders.

**Phase 3 — Stabilization (Sprint N+1):**
No new feature work. E2E testing, performance testing, bug fixes, security hardening, offline validation. The sprint goal is: "the app is stable, performant, and ready for UAT." If a team has no stabilization work, they pull in deferred items or help others test.

**Phase 4 — Release (Final Sprint):**
Code freeze, internal regression, stakeholder UAT, defect fixes, release candidate prep, app store submission. This sprint is often longer (2.5–3 weeks) to accommodate UAT feedback cycles.

**The skill must understand which phase a sprint belongs to** because:
- Foundation sprints have different "done" criteria (readiness, not features)
- Feature sprints need goal-based planning and demo-able outcomes
- Stabilization sprints need test coverage metrics and bug triage rules
- Release sprints need go/no-go criteria and a defect severity threshold

---

## Sprint Anatomy

A sprint is not "2 weeks of work." It has 5 distinct phases with specific activities and artifacts (day counts assume 10 working days / 2 weeks):

| Day | Phase | Activity | Artifact |
|-----|-------|----------|----------|
| Day 1 | **Planning** | Sprint kickoff. Team reviews sprint goal, committed work, capacity. Assignments confirmed. | **Sprint Planning Session doc** |
| Days 2–7 | **Execution** | Building. Daily standups. Blockers surfaced and resolved. | -- |
| Day 5–6 | **Mid-sprint check** | PM reviews progress against sprint goal. At-risk items flagged. Scope adjustments if needed. | **Sprint Progress Report** — mid-sprint mode |
| Days 8–9 | **Hardening** | Feature complete. Testing, bug fixes, polish. No new feature starts. | -- |
| Day 10 | **Review + Retro** | Sprint demo to stakeholders. Retro with team. Next sprint preview. | **Sprint Review doc** + **Sprint Progress Report** — close-out mode |

Each skill produces its artifact at a specific moment in the sprint lifecycle. The skill must understand what came before it and what comes after.

---

## The Document Chain

Documents produced by this system form a chain. Each document is both an output of one phase and an input to the next.

```
Release Definition
  ├──→ Release Plan ──→ Sprint Planning Session ──→ Sprint Progress Report ──→ Sprint Review
  │                                                                              │
  └── success criteria ────────────────────────────────────────────────────────→ Sprint Review
                                                                                 │
Sprint Review ──→ Meeting-to-Plan Integrator ──→ updated Release Plan ──→ Next Sprint Planning
                                              ──→ scope changes to Release Definition
Prior Sprint Review ──→ carryover items ──→ Next Sprint Planning Session
```

**The Release Definition is the anchor.** Every downstream document traces back to it:
- Release Plan draws its scope, timeline, and capacity from the definition
- Sprint Planning Sessions draw their goals from the release plan, which traces to the release goal
- Sprint Reviews assess progress against the release definition's success criteria
- When scope or timeline changes, the Release Definition is updated first, then the Release Plan

**Data contract between skills:** Each skill defines:
1. What it **requires** from upstream (minimum fields, format)
2. What it **produces** for downstream (guaranteed sections, field names)
3. What it **optionally consumes** if available

A weakness in one document cascades. If the sprint planning session doc doesn't clearly define "done" for each item, the progress tracker can't accurately assess completion. If the progress tracker doesn't flag carryover, the next sprint planning session underestimates scope.

---

## The Commitment Model

The team commits to a **sprint goal**, not to individual tickets.

- **Sprint Goal:** A 1-sentence statement of user-facing value. Written from the user's perspective. This is the contract.
- **Committed Work:** The tickets the team believes will achieve the sprint goal. These can change mid-sprint as long as the goal is still met.
- **Stretch Goals:** Items that would be nice to finish but are not part of the commitment. Only picked up if committed work is done early.

**Why this matters:** The progress tracker assesses "are we on track for the goal?" not "are all tickets done?" The review document evaluates "did we achieve the goal?" not "did we close all tickets?" This prevents the common failure mode where 12 of 15 tickets are done but the sprint goal isn't met because the 3 incomplete tickets were the critical ones.
