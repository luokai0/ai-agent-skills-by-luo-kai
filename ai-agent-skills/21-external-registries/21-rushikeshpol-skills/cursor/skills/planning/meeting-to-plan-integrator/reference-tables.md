# Meeting-to-Plan Integrator — Reference Tables

Skill-specific reference data. Shared rules (NON-NEGOTIABLE, quality criteria, provenance model, checkpoints, self-checks) live in `../shared/execution-rules.md`.

---

## Input Quality Tiers

| Tier | Requirements | Impact |
|------|-------------|--------|
| **Tier 1** (minimum viable) | At least 1 decision described + at least 1 target document | Can apply changes but attribution may be thin. |
| **Tier 2** (recommended) | Tier 1 + structured meeting notes + all affected documents identified | Full change manifest with clear attribution. |
| **Tier 3** (comprehensive) | Tier 2 + transcript-to-meeting-notes output with attribution | Source chain from transcript → decision → edit. |

---

## Decision Types

| Type | Description | Typical target documents |
|------|-----------|------------------------|
| **scope-change** | Feature added, removed, or modified | Release-Definition.md, Release-Plan.md, Scope.md |
| **timeline-change** | Deadline, sprint dates, or milestones changed | Release-Definition.md, Release-Plan.md |
| **priority-change** | Feature priority (Must/Should/Could) changed | Release-Definition.md, Release-Plan.md |
| **team-change** | Dev added, removed, or availability changed | Release-Definition.md, Release-Plan.md |
| **risk-update** | New risk identified or existing risk status changed | Release-Definition.md |
| **new-dependency** | New external dependency discovered | Release-Definition.md, Release-Plan.md |
| **technical-decision** | Architecture or technical approach decided | Release-Plan.md, Sprint Planning docs |

---

## Guardrails

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| **Scope change without impact** | Scope changed but no sprint adjustment proposed | Flag: assess sprint impact |
| **Timeline compression** | Deadline moved closer, same scope | Flag: scope-time-resource tradeoff needed |
| **Contradictory changes** | Two decisions conflict | Block: clarify priority |
| **Orphaned cascade** | A cascade change doesn't have a confirmed source change | Block: verify before applying |

---

## Cascade Confidence Levels

| Level | Definition | Action |
|-------|-----------|--------|
| **High** | Logical necessity (scope removed → must update scope doc) | Present for confirmation, recommend applying |
| **Medium** | Likely needed but context-dependent | Present for confirmation, no recommendation |
| **Low** | Possible ripple, not certain | Flag for review, do not recommend applying |

---

## Preflight Checks

| Workflow | Preflight |
|----------|-----------|
| 02-extract-changes | 01-intake complete, meeting notes loaded, targets identified |
| 03-apply-changes | 02-extract-changes complete (T2 gate passed), user confirmed changes |
| 04-cascade | 03-apply-changes complete, all confirmed edits saved |

---

## Self-Check Additions (extends shared P1/P2/P3)

**P1 additions:**
- Every applied change traces to a specific decision in the manifest
- Source attribution on every edit

**P2 additions:**
- Constraint registry updated if new constraints introduced
- Cross-references in edited documents still valid

**P3 additions:**
- Change manifest saved to `.meta/`
- Cascade effects documented
