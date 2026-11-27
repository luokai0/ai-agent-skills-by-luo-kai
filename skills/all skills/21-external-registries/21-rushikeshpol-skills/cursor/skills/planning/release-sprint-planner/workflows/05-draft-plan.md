# Workflow 05: Draft Plan

**Called from:** `SKILL.md` Step 8
**Next step:** `workflows/06-iterate.md`
**Saves to:** `[release-root]/Release-Plan.md`

---

## Purpose

Assign work to sprints. Produce the first draft of the multi-sprint plan.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 04 complete | |
| Analysis artifact saved | |
| Capacity model stated | |

---

## Step 1: Define Sprint Structure

From the Release Definition timeline:
- Sprint 0: Foundation (repos, architecture, CI/CD, design system, tooling)
- Sprints 1–N: Feature Build (user-facing value each sprint)
- Sprint N+1: Stabilization (E2E testing, hardening, zero new features)
- Sprint N+2: Release (code freeze, UAT, defect fixes, submission)

---

## Step 2: Assign Work to Sprints

Apply sprint assignment rules in order:

1. Foundation work goes to Sprint 0
2. Dependencies satisfied before dependents are scheduled
3. XL features split across sprints with clear "done" criteria per sprint
4. Each feature sprint has a user-facing goal (what can we demo?)
5. No sprint exceeds team capacity (from Release Definition capacity model)
6. UAT cadence matches Release Definition UAT strategy
7. Workstream rules applied if user requested workstream organization
8. Must-have items scheduled before Should-have and Could-have
9. If Should/Could items don't fit, they go to Deferred

For each sprint, produce:
- Sprint number and dates
- Sprint goal (user-facing, 1 sentence)
- Assigned features per dev/workstream with completion criteria
- Dependencies from/to other sprints
- Backend work timeline (if applicable)

---

## Step 3: Run Guardrails

| Guardrail | Trigger | Detection | Action |
|-----------|---------|-----------|--------|
| **Capacity overload** | Sprint has more work than team can deliver | Total complexity exceeds capacity × sprint duration | Flag sprint, suggest items to defer |
| **Empty sprint** | Sprint has no meaningful work for 1+ devs | Dev column empty or only "buffer" | Flag as wasted capacity, suggest pulling work forward |
| **Dependency sequencing** | Feature B depends on A but is planned earlier | Dependency field conflicts with sprint assignment | Block: reorder or flag the gap |
| **Goal drift** | Sprint work doesn't connect to sprint goal | Features don't match stated goal | Warn: rewrite goal or reassign features |
| **Back-loading** | Critical features pushed to late sprints | High-risk items in Sprint N-1/N-2 with no buffer | Warn: move critical work earlier |
| **UAT gap** | No UAT planned between feature completion and release | Feature sprints end with no testing sprint | Flag: recommend UAT cadence |
| **Success criteria unreachable** | Sprint plan doesn't meet success criteria | Success criterion has no corresponding feature in plan | Warn: "SC-[N] is not addressed by any sprint" |

---

## Step 4: Generate Draft Plan

Load the template:

    templates/release-plan.md

Fill the template with the sprint assignments. Save to: `[release-root]/Release-Plan.md`

Update state file: mark T6 as completed, T7 as in_progress.

---

## Completion Gate

- [ ] Every Must-have feature assigned to exactly one sprint (or split with clear criteria)
- [ ] No sprint exceeds capacity
- [ ] All dependencies satisfied
- [ ] Sprint goals are user-facing
- [ ] Guardrails evaluated and results recorded
- [ ] Draft plan saved

**CHECKPOINT (Review gate — T7 Gate):** "Draft plan saved to [path]. I flagged [N] guardrail issues. Review and tell me what to change."

**When complete, return to `SKILL.md` and proceed to Step 9.**
