# Workflow 04: Analyze Scope

**Called from:** `SKILL.md` Step 7
**Next step:** `workflows/05-draft-plan.md`
**Saves to:** `[release-root]/.meta/Analysis-[Release].md`

---

## Purpose

Understand the work — size it, sequence it, find the risks. This analysis feeds directly into sprint assignment.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 03 complete (T4 gate passed) | |
| Release Definition confirmed by user | |
| Scope-in table finalized | |

---

## Step 1: Size Each Feature

For each feature/item from the Release Definition scope-in table:
- Confirm or refine complexity: S / M / L / XL
- Identify dependencies: what must come before this? (from other features, external dependencies, infrastructure)
- Identify risks specific to this feature
- Classify type: new feature, enhancement, tech debt, compliance, infrastructure

---

## Step 2: Map Structure

- Group features into natural groupings (workstreams, domains, or value streams)
- Identify the critical path — the longest chain of dependent features
- Calculate total effort vs available capacity (from Release Definition)

---

## Step 3: Assess Scope vs Capacity

- Flag if scope exceeds capacity: "Scope requires [X] dev-sprints, team provides [Y] dev-sprints. [Shortfall] must be resolved."
- Propose a priority cut line: "Everything above this line fits. Below this line requires tradeoffs."

---

## Step 4: Save Analysis

Save to: `[release-root]/.meta/Analysis-[Release].md`

Contents: feature table with sizes, dependency graph, risk register, capacity calculation, scope-vs-capacity assessment, priority cut line.

Update state file: mark T5 as completed.

---

## Completion Gate

- [ ] Every feature sized (S/M/L/XL)
- [ ] Dependencies mapped
- [ ] Critical path identified
- [ ] Scope vs capacity calculated
- [ ] Analysis artifact saved

**CHECKPOINT (Review gate):** "Analysis saved to [path]. Key findings: [X]. Do you agree with the complexity ratings, groupings, and priority cut?"

**When complete, return to `SKILL.md` and proceed to Step 8.**
