# Sprint Progress Tracker — Reference Tables

Skill-specific reference data. Shared rules (NON-NEGOTIABLE, quality criteria, provenance model, checkpoints, self-checks) live in `../shared/execution-rules.md`.

---

## Input Quality Tiers

| Tier | Requirements | Impact |
|------|-------------|--------|
| **Tier 1** (minimum viable) | Planning doc + at least a verbal status update | Can produce a high-level health check but status accuracy is limited. |
| **Tier 2** (recommended) | Tier 1 + ticket-level status for all items | Accurate status table with per-ticket tracking. |
| **Tier 3** (comprehensive) | Tier 2 + blocker details + notes on each in-progress item | Full analysis with risk assessment and actionable recommendations. |

---

## Status Normalization Map

| Status | Definition | Requires |
|--------|-----------|----------|
| **Done** | Meets "done" criteria from planning doc | Nothing additional |
| **In Progress** | Started, actively being worked | Nothing additional |
| **Blocked** | Started but cannot proceed | Must state blocker |
| **Not Started** | No work begun | Nothing additional |
| **Dropped** | Removed from sprint scope | Must state reason |
| **Added** | Not in original plan | Must state reason |

---

## Guardrails

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| **Goal at risk** | Goal-critical items are Blocked or Not Started past mid-sprint | Flag with recommendation |
| **Scope creep** | More than 20% of committed items are "Added" | Warn with scope growth percentage |
| **Persistent blocker** | Same blocker in both mid-sprint and close-out | Escalate: needs PM intervention |
| **Silent ticket** | No status update after Day 5 | Flag: check with owner |
| **Carryover accumulation** | Close-out shows >30% carryover | Warn: capacity/scope adjustment needed |

---

## Preflight Checks

| Workflow | Preflight |
|----------|-----------|
| 02-analyze | 01-intake complete, status mapping saved, mode determined |
| 03-generate | 02-analyze complete (T2 gate passed), user confirmed assessment |

---

## Self-Check Additions (extends shared P1/P2/P3)

**P1 additions:**
- Goal status explicitly stated (On Track / At Risk / Not Met)
- Every planned ticket appears in status table
- Source attribution on status data

**P2 additions:**
- Scope changes listed with reasons
- Every blocker has owner or escalation
- Guardrail results addressed

**P3 additions:**
- Health narrative is honest (no spin on bad data)
