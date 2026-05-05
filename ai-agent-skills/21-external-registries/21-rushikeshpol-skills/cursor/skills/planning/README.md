# Planning Plugin — Delivery Lifecycle Skills Suite

A complete sprint delivery management system — 5 interconnected skills that cover the full lifecycle from release definition through sprint execution, review, and iteration.

## Skills

| Skill | Purpose | Tier |
|-------|---------|------|
| `sprint-planning-session` | Turn a ticket list into a structured sprint planning document | 2 |
| `release-sprint-planner` | Define a release and break it into a multi-sprint plan | 1 |
| `sprint-progress-tracker` | Create mid-sprint or close-out progress snapshots | 2 |
| `sprint-review-generator` | Produce stakeholder-facing sprint review documents | 2 |
| `meeting-to-plan-integrator` | Apply meeting decisions to release plan artifacts | 1 |

## The Skill Cycle

```
One-time at release start:
  release-sprint-planner → Release-Definition.md + Release-Plan.md + Scope.md

Every sprint (repeating cycle):
  sprint-planning-session  → Sprint-N-Planning.md
  sprint-progress-tracker  → Sprint-N-Progress.md (mid-sprint and close-out)
  sprint-review-generator  → Sprint-N-Review.md
  meeting-to-plan-integrator → updates Release-Plan.md based on feedback
```

Each skill reads the prior skill's output file. No skill depends on chat context from another skill's run.

## Install

Symlink each skill folder into your skills directory:

```bash
# For Claude Code
ln -s ~/ai-skills/cursor/skills/planning/sprint-planning-session ~/.claude/skills/sprint-planning-session
ln -s ~/ai-skills/cursor/skills/planning/release-sprint-planner ~/.claude/skills/release-sprint-planner
ln -s ~/ai-skills/cursor/skills/planning/sprint-progress-tracker ~/.claude/skills/sprint-progress-tracker
ln -s ~/ai-skills/cursor/skills/planning/sprint-review-generator ~/.claude/skills/sprint-review-generator
ln -s ~/ai-skills/cursor/skills/planning/meeting-to-plan-integrator ~/.claude/skills/meeting-to-plan-integrator

# For Cursor
ln -s ~/ai-skills/cursor/skills/planning/sprint-planning-session ~/.cursor/skills/sprint-planning-session
ln -s ~/ai-skills/cursor/skills/planning/release-sprint-planner ~/.cursor/skills/release-sprint-planner
ln -s ~/ai-skills/cursor/skills/planning/sprint-progress-tracker ~/.cursor/skills/sprint-progress-tracker
ln -s ~/ai-skills/cursor/skills/planning/sprint-review-generator ~/.cursor/skills/sprint-review-generator
ln -s ~/ai-skills/cursor/skills/planning/meeting-to-plan-integrator ~/.cursor/skills/meeting-to-plan-integrator
```

## Shared Resources

The `shared/` folder contains domain knowledge and rules referenced by all 5 skills:

- **`delivery-model.md`** — Release lifecycle phases, sprint anatomy, document chain, commitment model
- **`execution-rules.md`** — Shared NON-NEGOTIABLE rules, quality criteria, self-check structure, provenance model
- **`constraint-registry-template.md`** — Template and rules for the shared constraint registry

Skills reference these via `MANDATORY READ` directives at intake and generate steps.

## Output Folder Structure

All artifacts live under a single release folder:

```
[project]/
  Product Artifacts/
    Delivery Plan/
      Releases/
        [Release-Name]/
          Release-Definition.md
          Release-Plan.md
          Scope.md
          .meta/
            constraint-registry.md
            skill-state-*.json
          Sprint-0/
            Sprint-0-Planning.md
            Sprint-0-Progress.md
            Sprint-0-Review.md
          Sprint-1/
            ...
```

## Build Order

If starting from scratch, build skills in this order — each is immediately usable and the next builds on it:

1. `sprint-planning-session` — needed for the first sprint kickoff
2. `release-sprint-planner` — needed for next major replan
3. `sprint-progress-tracker` — useful from mid-sprint onward
4. `sprint-review-generator` — needed at sprint end
5. `meeting-to-plan-integrator` — needed after first sprint demo feedback
