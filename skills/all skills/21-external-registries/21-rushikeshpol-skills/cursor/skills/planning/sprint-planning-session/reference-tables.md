# Reference Tables — sprint-planning-session

**Referenced by:** `SKILL.md` and workflow files via `MANDATORY READ` at gate steps.

---

## Input Quality Tiers

| Tier | Requirements |
|------|-------------|
| **Tier 1** (minimum viable) | Sprint number + dates + goal + at least 1 ticket |
| **Tier 2** (recommended) | Tier 1 + categorized tickets + team capacity confirmed |
| **Tier 3** (comprehensive) | Tier 2 + Release Plan linked + prior sprint review linked + full ticket details (descriptions, ACs, estimates) |

---

## Guardrails

| Guardrail | Trigger | Detection | Action |
|-----------|---------|-----------|--------|
| **Goal-work mismatch** | Committed tickets don't achieve the sprint goal | Tickets categorized but none map to the stated goal | Warn: either the goal is wrong or the tickets are wrong |
| **Capacity breach** | More tickets than team can reasonably deliver | Ticket count or story points exceed capacity model | Warn: identify stretch vs committed, or reduce scope |
| **Missing owners** | Tickets have no assigned owner | Owner column blank for >50% of tickets | Warn: list unassigned tickets, suggest assignment |
| **Carryover not acknowledged** | Items from prior sprint not included | Prior Sprint Progress Report shows incomplete items not in this sprint's ticket list | Warn: list missing carryover items, ask if intentional |
| **Blocked item in committed work** | A committed item has a known blocker | Dependency or blocker field filled, no mitigation stated | Flag: move to stretch or add mitigation plan |

---

## Preflight Checks

| Step | Preflight checks (all must be YES) |
|------|-------------------------------------|
| T1 Organize | T0 complete; normalized ticket table saved; sprint goal stated; capacity stated |
| T3 Generate | T2 complete; user confirmed groups; guardrail alerts addressed; template loaded |

---

## Self-Check — Skill-Specific Additions

Beyond the shared self-check (see `../shared/execution-rules.md`):

| Priority | Check |
|----------|-------|
| **P1** (hard gate) | Sprint goal is user-facing; every "Done" checklist item maps to a ticket |
| **P2** (edit gate) | Carryover items acknowledged |

---

## Normalized Ticket Categories

| Category | When to use |
|----------|------------|
| `user-story` | User-facing feature work |
| `dev-task` | Technical/infrastructure work not directly user-facing |
| `bug` | Defect fix |
| `carryover` | Incomplete item from prior sprint |
| `stretch` | Nice-to-have, only if capacity allows |
