# Workflow 03: Release Definition

**Called from:** `SKILL.md` Step 6
**Next step:** `workflows/04-analyze-scope.md`
**Saves to:** `[release-root]/Release-Definition.md`

---

## Purpose

Produce the Release Definition document — the anchor artifact that captures the release commitment before any sprint-level planning.

This is a COLLABORATIVE workflow. The skill drafts each section from what it extracted, presents it, and asks: "Does this capture it, or would you reframe it?" It does NOT dump a template and ask the user to fill it out.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 02 complete (T2 gate passed) | |
| Context assessment confirmed by user | |
| Gap-filling answers received | |

---

## Section-by-Section Construction

Build each section below. For each: draft from extracted context, present to user, incorporate feedback.

### Release Goal

Prompt: "In 1-2 sentences, what value does this release deliver to users?"

If inputs contain PRDs or scope docs, draft a goal and ask: "Does this capture it, or would you reframe it?"

**GUARDRAIL:** Goal must be user-facing. If goal mentions technology or architecture ("migrate to new repo", "upgrade API"), reframe: "That's an engineering goal. What does the user get as a result?"

### Success Criteria

Prompt: "How do we know this release succeeded? Give me 3-5 measurable outcomes."

Each criterion must be:
- **Measurable:** has a number or a yes/no test
- **Time-bound:** when do we measure it?
- **Outcome-based:** describes a result, not an activity

GOOD: "80% of officers complete clock-in within 15 seconds on first use"
BAD: "Improve user experience" (not measurable)

If user provides vague criteria, help them sharpen. Recommend at least one criterion from each category: user outcome, quality, delivery.

### Scope — In

Present the normalized feature table from 01-intake. For each item:
- **Priority:** Must (release fails without it) / Should (high value) / Could (nice-to-have)
- **Complexity:** S / M / L / XL (skill proposes based on analysis, user confirms)
- **Type:** new feature / enhancement / tech debt / compliance / infrastructure

**GUARDRAIL:** If total Must items exceed estimated capacity, flag immediately: "The Must-have items alone appear to exceed capacity. Before going further, should we re-prioritize, reduce scope, extend timeline, or add team?"

### Scope — Out

Prompt: "What is explicitly excluded from this release? Every 'not this time' should be listed so it doesn't creep back in."

Each excluded item must have a reason.

### Timeline

Gather: start date, end date/hard deadline, sprint duration (default: 2 weeks), milestones.

Calculate:
- Total available sprints = (end - start) / sprint duration
- Allocate: 1 foundation + N feature + 1 stabilization + 1 release
- Feature sprints available = total - 3

**GUARDRAIL:** If feature sprints < needed for Must-have scope, flag: "You have [N] feature sprints but the Must-have scope estimates [M] sprints."

### Team & Capacity

Gather: headcount by platform/role, seniority levels, availability constraints, team model (dedicated/shared).

**Capacity model:**
- Effective capacity per dev per sprint = sprint days × availability % × focus %
- Focus factor: 100% for dedicated, 60-80% for shared, 50% for leads
- Present: "Based on your team, I estimate [X] effective dev-days per sprint. Does this feel right?"

### Known Constraints

Prompt: "What can't the team change but must work around?"

Probe categories: technical, compliance, organizational, external, legacy.
Each constraint must state: what it is, who/what imposes it, and how it affects the plan.

### Known Risks

Prompt: "What could go wrong?"

The skill also infers risks from gathered data:
- XL feature in Must-have → large feature risk
- External dependency → dependency risk
- New technology → technology risk
- Tight timeline → timeline risk

Each risk: description, likelihood (H/M/L), impact, owner, mitigation.

### Dependencies

Prompt: "What outside the team's control could block or delay delivery?"

Each: what, from whom, by when, what it blocks, fallback.

### Release Strategy

Prompt: "How will this be released to users?"

Capture: release type, legacy app handling, rollback plan, app store considerations.

### UAT & Quality Strategy

Capture: UAT cadence, participants, environment, go/no-go criteria, defect severity definitions, defect handling rules.

### Assumptions

Prompt: "What are we assuming to be true that, if wrong, changes the plan?"

Also extract assumptions from earlier sections. Each: statement, confidence (H/M/L), risk if wrong, validation plan, owner.

**GUARDRAIL:** Any Low-confidence assumption affecting Must-have scope → flag for pre-sprint validation.

---

## Document Assembly

Load the template:

    templates/release-definition.md

Assemble all sections into the template. Save to: `[release-root]/Release-Definition.md`

Create the constraint registry from constraints section: `[release-root]/.meta/constraint-registry.md`

Update state file: mark T3 as completed, T4 as in_progress.

---

## Self-Check Before Saving

**P1 — Hard gate (regenerate if fails):**
- [ ] Release goal is user-facing, not technical
- [ ] At least 3 success criteria, all measurable
- [ ] Every Must-have item has complexity and type
- [ ] Timeline math works (sprints fit between start and end)
- [ ] Capacity model stated and confirmed

**P2 — Edit gate (fix before saving):**
- [ ] Every excluded item has a reason
- [ ] Every risk has owner + mitigation
- [ ] Every dependency has deadline + fallback
- [ ] Every assumption has confidence + risk-if-wrong
- [ ] Go/no-go criteria are specific (not "ensure quality")

**P3 — Note and proceed:**
- [ ] Date formatting consistent (full date for release docs)
- [ ] Source attribution on authoritative claims

---

## Completion Gate

- [ ] All sections built collaboratively with user
- [ ] Self-check passed
- [ ] Release-Definition.md saved
- [ ] Constraint registry created
- [ ] State file updated

**CHECKPOINT (Hard stop — T4 Gate):** "Release definition saved to [path]. This is the anchor document — review and confirm before I start sprint planning."

**STOP and WAIT for user confirmation.**

**When complete, return to `SKILL.md` and proceed to Step 7.**
