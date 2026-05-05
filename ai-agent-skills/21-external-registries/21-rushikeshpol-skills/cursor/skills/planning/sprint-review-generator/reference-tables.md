# Sprint Review Generator — Reference Tables

Skill-specific reference data. Shared rules (NON-NEGOTIABLE, quality criteria, provenance model, checkpoints, self-checks) live in `../shared/execution-rules.md`.

---

## Input Quality Tiers

| Tier | Requirements | Impact |
|------|-------------|--------|
| **Tier 1** (minimum viable) | Planning doc + progress report (or raw status) + sprint goal | Can produce a basic review with goal assessment and delivery list. Lessons section will be thin. |
| **Tier 2** (recommended) | Tier 1 + challenges described + demo items listed | Solid review with demo-focused delivery section and challenge analysis. |
| **Tier 3** (comprehensive) | Tier 2 + metrics + lessons learned + key decisions documented | Full review with trends, actionable lessons, and decision trail. |

---

## Guardrails

| Guardrail | Trigger | Action |
|-----------|---------|--------|
| **Goal assessment missing** | No explicit met/not-met statement | Block: must state goal outcome |
| **Incomplete without reason** | Incomplete item has no explanation | Flag: add "why" for every incomplete item |
| **Spin narrative** | Tone implies success when data shows otherwise | Flag: rewrite to match data honestly |
| **Missing next-sprint preview** | No forward-looking section | Warn: stakeholders expect it |

---

## Writing Rules

- No ticket IDs in stakeholder sections (appendix only)
- No developer jargon in stakeholder sections
- "We delivered" not "we completed ticket #123"
- Honest tone: if goal wasn't met, say so clearly and say why
- Lessons must be actionable: "Reduce WIP limit to 2 per dev" not "We should focus more"
- Source attribution via Sources section at bottom

---

## Provenance Rules (skill-specific)

This skill produces synthesized analysis (narrative) from authoritative data (status, metrics). The provenance model applies as follows:

| Content type | Provenance class | Treatment |
|-------------|-----------------|-----------|
| Goal status (Met/Partially Met/Not Met) | Authoritative claim | Source attribution required |
| Metric values (velocity, completion rate) | Authoritative claim | Source attribution required |
| Sprint summary bullets | Synthesized analysis | Sources section at bottom |
| Challenges narrative | Synthesized analysis | Sources section at bottom |
| Lessons learned | Inference (when skill-inferred from patterns) | Mark as `[INFERRED]` if not user-stated |
| Section headings, transitions | Process scaffolding | No attribution needed |

---

## Preflight Checks

| Workflow | Preflight |
|----------|-----------|
| 02-analyze | 01-intake complete, all required inputs loaded |
| 03-generate | 02-analyze complete (T2 gate passed), user confirmed narrative |

---

## Self-Check Additions (extends shared P1/P2/P3)

**P1 additions:**
- Goal assessment explicit: Met / Partially Met / Not Met with reason
- Every item from planning doc accounted for
- No required section empty

**P2 additions:**
- Every incomplete item has a "why"
- Tone matches data (no spin)
- Lessons are actionable

**P3 additions:**
- Stakeholder sections free of ticket IDs and jargon
- Sources section at bottom
