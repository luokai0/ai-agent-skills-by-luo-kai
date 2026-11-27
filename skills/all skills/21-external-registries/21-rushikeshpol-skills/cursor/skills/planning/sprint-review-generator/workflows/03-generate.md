# Workflow 03: Generate

**Called from:** `SKILL.md` Step 4
**Saves to:** `[sprint-root]/Sprint-[N]-Review.md`

---

## Purpose

Produce the Sprint Review document. Dual-audience: stakeholder summary at the top, team detail below.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 02 complete (T2 gate passed) | |
| Narrative outline confirmed by user | |

---

## Step 1: Generate Review

Load the template:

    templates/sprint-review.md

Fill the template. Follow these writing rules:

**Stakeholder sections (top of document — 5-minute read):**
- Sprint Summary (3-5 bullets)
- Goal Assessment (explicit: met / partially met / not met + why)
- What We Delivered (grouped by feature, demo-focused language)

**Team sections (below the fold — full detail):**
- What Didn't Land (and why — every item has a reason)
- Key Decisions Made This Sprint
- Challenges and How We Addressed Them
- Lessons Learned (specific, actionable)
- Metrics (if provided)
- Next Sprint Preview

**Writing rules:**
- No ticket IDs in stakeholder sections (appendix only)
- No developer jargon in stakeholder sections
- "We delivered" not "we completed ticket #123"
- Honest tone: if the goal wasn't met, say so clearly and say why
- Lessons must be actionable: "Reduce WIP limit to 2 per dev" not "We should focus more"
- Source attribution via Sources section at bottom (inline tags make review docs unreadable)

---

## Step 2: Self-Check

**P1 — Hard gate (regenerate if fails):**
- [ ] Goal assessment explicit: Met / Partially Met / Not Met with reason
- [ ] Every item from planning doc accounted for (delivered, incomplete, or dropped)
- [ ] No required section empty

**P2 — Edit gate (fix before saving):**
- [ ] Every incomplete item has a "why"
- [ ] Review tone matches data (no spin)
- [ ] Lessons are actionable (not "communicate better")

**P3 — Note and proceed:**
- [ ] Stakeholder sections free of ticket IDs and developer jargon
- [ ] Sources section at bottom

---

## Step 3: Save Review

Save to: `[sprint-root]/Sprint-[N]-Review.md`

Update state file: mark all tasks completed.

---

## Completion Gate

- [ ] Review generated with all sections
- [ ] Self-check passed
- [ ] Review saved to file
- [ ] State file updated

**CHECKPOINT (Review gate):** "Sprint review saved to [path]. Review and confirm, or request changes."

**Skill is complete.**
