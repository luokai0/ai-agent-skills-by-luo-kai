# Workflow 02: Context Assessment

**Called from:** `SKILL.md` Step 5
**Next step:** `workflows/03-release-definition.md`
**Saves to:** `[release-root]/.meta/Context-Assessment.md`

---

## Purpose

Assess what the skill already knows across six context dimensions, identify gaps, and ask targeted questions — so the release definition is grounded in real information, not generic templates.

The skill should EXTRACT context from existing documents, not ask the user to produce context from scratch. The user has already done the work — it lives in their PRDs, meeting notes, designs, and project-context.md.

---

## Preflight Checks

| Check | Status |
|-------|--------|
| Workflow 01 complete | |
| Input inventory saved | |
| project-context.md loaded (if available) | |

---

## Step 1: Read and Extract

For every input gathered in 01-intake, read it and extract context into six dimensions:

| Context | What to extract | Typical sources |
|---------|----------------|-----------------|
| **Business** | Release goal/vision, business drivers, success metrics, stakeholder priorities, regulatory requirements, market timing | Stakeholder meeting notes, PRDs, product session summaries, executive briefs |
| **Product** | Feature list, scope boundaries, user stories/requirements, acceptance criteria, feature priorities, existing feature gaps | Requirements docs, PRDs, epics, scope docs, feature lists |
| **Technical** | Architecture, tech stack, API landscape (existing + new), tech debt, platform constraints, integration points, infrastructure | project-context.md, architecture docs, Swagger specs, dev meeting notes |
| **User** | Personas, key workflows, pain points, usage patterns, accessibility needs, localization requirements | User research, support tickets, analytics, stakeholder proxies, persona docs |
| **UX / Design** | Screen inventory, design readiness, interaction complexity, design system maturity, design dependencies | Figma files, design system docs, design-to-context outputs, design review notes |
| **Project** | Timeline, team composition, capacity, constraints, risks, dependencies, release strategy, prior sprint data | Delivery plan docs, team rosters, meeting notes, prior sprint reviews |

---

## Step 2: Rate Each Context

| Rating | Definition | What it means for planning |
|--------|-----------|--------------------------|
| **Strong** | Multiple sources confirm. Key facts clear. Minimal gaps. | Can plan confidently in this dimension. |
| **Moderate** | Core facts known but some gaps. Single source or partially stale. | Can plan with caveats. Specific questions needed. |
| **Weak** | Only fragments or indirect references. Key facts unknown. | Plan will have `[TBD]` markers in this dimension. |
| **Missing** | No input covers this dimension. | Must ask user or accept significant gaps. |

---

## Step 3: Present Assessment

Show the user what the skill knows and doesn't know:

```
Context Assessment — [Release Name]

| Context | Rating | What I found | Key gaps |
|---------|--------|-------------|----------|
| Business | [rating] | [summary] | [gaps] |
| Product | [rating] | [summary] | [gaps] |
| Technical | [rating] | [summary] | [gaps] |
| User | [rating] | [summary] | [gaps] |
| UX/Design | [rating] | [summary] | [gaps] |
| Project | [rating] | [summary] | [gaps] |
```

---

## Step 4: Targeted Gap-Filling

Ask questions ONLY for gaps that affect release-level planning. Do not ask about sprint-level detail.

| Gap type | Ask now? | Why |
|----------|---------|-----|
| Release goal unclear | Yes | Can't plan without knowing what we're building |
| Success criteria missing | Yes | Can't assess if the plan achieves the goal |
| Scope unclear (features unknown) | Yes | Can't estimate sprints without scope |
| Feature-level AC or detailed flows | No — sprint level | Sprint planning will pull this in per-feature |
| API readiness dates | Yes (if dependency) | Affects sprint sequencing |
| Detailed API contracts | No — sprint level | Needed when the feature is being built |
| Design completion status | Yes (high level) | Affects sprint readiness |
| Detailed screen-by-screen design review | No — sprint level | Needed during sprint planning |
| Team availability | Yes (known PTO/conflicts) | Affects capacity model |
| Individual task assignments | No — sprint level | Team decides in sprint planning |
| Compliance requirements | Yes (if they constrain scope) | May affect priority and sequencing |

For each gap that matters now, ask a SPECIFIC question:
- Not: "Tell me about your technical architecture"
- Instead: "The new Schedule API is a dependency for Sprint 3 features. Do you have a timeline from the backend team on when it will be ready?"

---

## Step 5: Note Context Needed Later

Record what context will be needed at sprint level, so the sprint-planning-session skill can prompt for it:

```
Context needed at sprint level (not blocking release definition):
- Sprint [N]: [Specific context needed] ([Dimension])
```

This list is saved in the Release Definition as an appendix.

---

## Step 6: Present STATED vs INFERRED Register

Separate extracted facts from inferred conclusions:

```
## STATED (extracted from sources)
- Release goal: "..." (Source: PRD, section 1)
- Team: 3 iOS, 3 Android (Source: user-confirmed)

## INFERRED (needs your confirmation)
- Clock-in is highest-priority feature
  → Reasoning: most tickets, appears in proposed sprint goal (Based on: scope doc)
- Schedule API dependency may delay Sprint 3
  → Reasoning: no confirmed delivery date from backend team (Based on: absence of data)
```

---

## Step 7: Save Assessment

Save to: `[release-root]/.meta/Context-Assessment.md`

Update state file: mark T1 as completed, T2 as in_progress.

---

## Completion Gate

- [ ] All inputs read and context extracted into 6 dimensions
- [ ] Each dimension rated (Strong/Moderate/Weak/Missing)
- [ ] Release-level gaps identified and questions asked
- [ ] Sprint-level context needs recorded
- [ ] STATED vs INFERRED register presented
- [ ] Assessment saved to file
- [ ] State file updated

**CHECKPOINT (Hard stop — T2 Gate):** "Context assessment complete. [N] of 6 dimensions are Strong or Moderate. I have enough to build the release definition. Key gaps noted for sprint-level follow-up. Confirm or correct before I proceed."

**STOP and WAIT for user confirmation.** Do not proceed until the user confirms.

**When complete, return to `SKILL.md` and proceed to Step 6.**
