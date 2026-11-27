# Release Sprint Planner — Reference Tables

Skill-specific reference data. Shared rules (NON-NEGOTIABLE, quality criteria, provenance model, checkpoints, self-checks) live in `../shared/execution-rules.md`.

---

## Input Quality Tiers

| Tier | Requirements | Impact |
|------|-------------|--------|
| **Tier 1** (minimum viable) | Release name + at least a verbal description of what's being built | Skill will produce a plan but many sections will have `[TBD]` markers. User will be prompted heavily. |
| **Tier 2** (recommended) | Tier 1 + feature list + timeline + team size | Skill can produce a solid plan with some gaps. Minor prompting for missing sections. |
| **Tier 3** (comprehensive) | Tier 2 + requirements docs + meeting notes + constraints documented | Skill can produce a comprehensive plan with minimal gaps. Mostly confirmation-based interaction. |

---

## Context Dimensions

| Context | What to extract | Typical sources |
|---------|----------------|-----------------|
| **Business** | Release goal/vision, business drivers, success metrics, stakeholder priorities, regulatory requirements, market timing | Stakeholder meeting notes, PRDs, product session summaries, executive briefs |
| **Product** | Feature list, scope boundaries, user stories/requirements, acceptance criteria, feature priorities, existing feature gaps | Requirements docs, PRDs, epics, scope docs, feature lists |
| **Technical** | Architecture, tech stack, API landscape (existing + new), tech debt, platform constraints, integration points | project-context.md, architecture docs, Swagger specs, dev meeting notes |
| **User** | Personas, key workflows, pain points, usage patterns, accessibility needs | User research, support tickets, analytics, stakeholder proxies, persona docs |
| **UX / Design** | Screen inventory, design readiness, interaction complexity, design system maturity | Figma files, design system docs, design-to-context outputs, design review notes |
| **Project** | Timeline, team composition, capacity, constraints, risks, dependencies, prior sprint data | Delivery plan docs, team rosters, meeting notes, prior sprint reviews |

---

## Context Ratings

| Rating | Definition | Planning impact |
|--------|-----------|----------------|
| **Strong** | Multiple sources confirm. Key facts clear. Minimal gaps. | Plan confidently |
| **Moderate** | Core facts known but some gaps. Single source or partially stale. | Plan with caveats |
| **Weak** | Only fragments or indirect references. Key facts unknown. | `[TBD]` markers expected |
| **Missing** | No input covers this dimension. | Ask user or accept gaps |

---

## Sprint Assignment Rules (apply in order)

1. Foundation work goes to Sprint 0
2. Dependencies satisfied before dependents are scheduled
3. XL features split across sprints with clear "done" criteria per sprint
4. Each feature sprint has a user-facing goal (what can we demo?)
5. No sprint exceeds team capacity
6. UAT cadence matches Release Definition UAT strategy
7. Workstream rules applied if user requested workstream organization
8. Must-have items scheduled before Should-have and Could-have
9. If Should/Could items don't fit, they go to Deferred

---

## Guardrails

| Guardrail | Trigger | Detection | Action |
|-----------|---------|-----------|--------|
| **Capacity overload** | Sprint has more work than team can deliver | Total complexity exceeds capacity × sprint duration | Flag sprint, suggest items to defer |
| **Empty sprint** | Sprint has no meaningful work for 1+ devs | Dev column empty or only "buffer" | Flag as wasted capacity, suggest pulling work forward |
| **Dependency sequencing** | Feature B depends on A but is planned earlier | Dependency field conflicts with sprint assignment | Block: reorder or flag the gap |
| **Goal drift** | Sprint work doesn't connect to sprint goal | Features don't match stated goal | Warn: rewrite goal or reassign features |
| **Back-loading** | Critical features pushed to late sprints | High-risk items in Sprint N-1/N-2 with no buffer | Warn: move critical work earlier |
| **UAT gap** | No UAT planned between feature completion and release | Feature sprints end with no testing sprint | Flag: recommend UAT cadence |
| **Success criteria unreachable** | Sprint plan doesn't meet success criteria | Success criterion has no corresponding feature in plan | Warn: "SC-[N] is not addressed by any sprint" |
| **Scope-time-resources mismatch** | Must-have scope exceeds capacity | Total Must-have effort > available dev-sprints | Block: force scope/timeline/resource conversation |

---

## Release Definition Section Guardrails

| Section | Guardrail |
|---------|-----------|
| **Release Goal** | Must be user-facing. Engineering goals → reframe as user outcome. |
| **Success Criteria** | Each must be measurable, time-bound, outcome-based. Minimum 3. |
| **Scope — In** | Must-have items must not exceed capacity. Flag immediately if they do. |
| **Timeline** | Sprint math must work. Feature sprints < needed for Must-have → flag. |
| **Assumptions** | Low-confidence assumption affecting Must-have → flag for pre-sprint validation. |

---

## Preflight Checks (per workflow)

| Workflow | Preflight |
|----------|-----------|
| 02-context-assessment | 01-intake complete, input inventory saved, project-context loaded if available |
| 03-release-definition | 02-context-assessment complete (T2 gate passed), user confirmed assessment |
| 04-analyze-scope | 03-release-definition complete (T4 gate passed), user confirmed definition |
| 05-draft-plan | 04-analyze-scope complete, analysis artifact saved |
| 06-iterate | 05-draft-plan complete OR UPDATE mode with existing plan loaded + constraint registry loaded |
| 07-finalize | 06-iterate complete, user approved plan |

---

## Self-Check Additions (extends shared P1/P2/P3)

**P1 additions (Release Definition):**
- Release goal is user-facing, not technical
- At least 3 success criteria, all measurable
- Every Must-have item has complexity and type
- Timeline math works (sprints fit between start and end)
- Capacity model stated and confirmed

**P2 additions (Release Definition):**
- Every excluded item has a reason
- Every risk has owner + mitigation
- Every dependency has deadline + fallback
- Every assumption has confidence + risk-if-wrong
- Go/no-go criteria are specific

**P2 additions (Release Plan):**
- Every Must-have feature assigned to exactly one sprint
- No sprint exceeds capacity
- All dependencies satisfied in sprint ordering
- Sprint goals trace to release goal

**P3 additions:**
- Date formatting consistent (full date for release docs)
- Source attribution on authoritative claims
