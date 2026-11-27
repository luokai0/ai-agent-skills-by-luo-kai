# Evaluation Scenarios — sprint-planning-session

Bootstrap evaluation scenarios for verifying skill quality before first real run. These become the harvested regression set as the skill matures.

---

## Scenario 1: Happy Path — Tier 3 Input

**Input:**
- Sprint 1 of a mobile app redesign release
- Release Plan linked with workstreams defined
- 15 tickets exported from ADO (CSV with IDs, titles, descriptions, ACs, estimates)
- Prior Sprint 0 review available showing 2 incomplete infrastructure items
- Full team capacity: 3 iOS + 3 Android, 1 on PTO Day 3-4

**Expected behavior:**
- Tickets normalized into standard table with all fields populated
- 2 carryover candidates detected and presented to user
- Groups follow workstream structure from Release Plan
- Goal-work match validated
- Capacity check passes
- "Done" checklist items all map to tickets
- Output document has no `[TBD]` markers

**Quality checks:**
- No tickets dropped from input to output
- Sprint goal is user-facing
- Carryover items appear in carryover section with prior status

---

## Scenario 2: Minimal Input — Tier 1

**Input:**
- Sprint 2, dates provided verbally
- Sprint goal: "finish the login flow"
- 6 tickets pasted as a bulleted list (title only, no IDs, no categories, no owners)
- No Release Plan linked, no prior sprint review

**Expected behavior:**
- Sequential IDs assigned (T-001 through T-006)
- Categories inferred and marked `[INFERRED]`
- Owners left blank → "Missing owners" guardrail fires
- Carryover detection skipped (no prior docs)
- Tier 1 quality gate passes, Tier 2 gaps noted
- Output document has `[TBD]` markers for missing capacity and owner data

**Quality checks:**
- All 6 tickets appear in output
- Inferred categories are reasonable
- Guardrail warns about missing owners
- Sprint goal reframed to user-facing if needed ("finish the login flow" → "Officers can log in to the app")

---

## Scenario 3: Guardrail Stress Test

**Input:**
- Sprint 3, 20 tickets committed
- Team capacity: 3 devs at full capacity (known to handle ~12-15 tickets)
- 2 tickets have known blockers (API dependency not ready)
- Sprint goal: "Complete the schedule feature" but only 3 of 20 tickets relate to scheduling
- Prior sprint had 4 carryover items, none included in this sprint's list

**Expected behavior:**
- **Capacity breach** guardrail fires (20 tickets > ~15 capacity)
- **Goal-work mismatch** guardrail fires (most tickets unrelated to goal)
- **Blocked item in committed work** guardrail fires for 2 blocked tickets
- **Carryover not acknowledged** guardrail fires for 4 missing items
- All 4 guardrails presented at T2 gate with recommended actions

**Quality checks:**
- All guardrails fire correctly
- Guardrail actions are specific (not generic warnings)
- User is asked to address each before proceeding

---

## Scenario 4: Foundation Sprint (Sprint 0)

**Input:**
- Sprint 0 of a new release
- All tickets are dev-tasks (repos, CI/CD, architecture, tooling)
- No prior sprint data
- Sprint goal: "Team is unblocked and ready to build"

**Expected behavior:**
- All tickets categorized as `dev-task`
- Sprint goal recognized as foundation-appropriate (readiness, not features)
- "Done" checklist focuses on readiness criteria ("CI/CD pipeline runs green", "Design system tokens imported")
- No carryover detection attempted
- No goal-work mismatch (infrastructure work matches foundation goal)

**Quality checks:**
- Goal is NOT reframed to be user-facing (foundation sprints are an exception)
- "Done" items are concrete and testable
- No false guardrail warnings for missing user-facing work

---

## Scenario 5: Mid-Release Sprint with Scope Change

**Input:**
- Sprint 4 of 8
- Release Plan linked, constraint registry has: "Chat deferred to Phase 2"
- Ticket list includes 2 chat-related tickets
- 1 carryover item from Sprint 3

**Expected behavior:**
- Constraint registry loaded, "Chat deferred" constraint noted
- Chat tickets flagged as potentially violating scope constraint
- User asked: "These 2 tickets relate to Chat, which is deferred per constraint CR-3. Should they be removed?"
- Carryover item detected and presented

**Quality checks:**
- Constraint violation detected before document generation
- Carryover acknowledged
- If user keeps chat tickets, constraint registry note added
