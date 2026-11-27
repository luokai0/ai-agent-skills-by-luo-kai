# Stage 3: Brainstorm — Variables, Constraints, Actors

## Stage 3 boundary with Stage 2

Stage 2 extracts what the sources say. Stage 3 analyzes what the sources *don't* say.

**DO NOT restate Stage 2 content.** Stage 3's job is to build ON TOP of the confirmed Stage 2 output:
- Stage 2 Actors → Stage 3 starts here and maps **interactions** (who triggers whom, what data flows between them).
- Stage 2 Constraints → Stage 3 starts here and discovers **hidden constraints** not stated in any source.
- Stage 2 has no variables → Stage 3 **creates** the variables table from scratch.

If you find yourself copying a constraint or actor description from Stage 2 into Stage 3, STOP — you are restating, not analyzing. Instead, reference it (`See Stage 2, C3`) and add only what's new.

## 3.0 Anti-momentum gate (MANDATORY)

Before writing ANY output for this stage, answer these three questions in the artifact file header:

```
## Pre-Stage Checkpoint
1. What is this stage's UNIQUE contribution that no other stage produces?
   → Variables table + gap analysis. NOT a restatement of Stage 2.
2. What specifically should I know AFTER this stage that I don't know after Stage 2?
   → Which variable combinations exist, which are impossible, and what gaps the sources are silent on.
3. Am I about to reformat existing content or generate new insight?
   → If reformatting: STOP and apply the gap-finding lenses below instead.
```

## 3.1 Identify variables

Work with the user to define the variables that determine system behavior:

| Variable | Values / Range | Source (SRC-N) | Determines |
|---|---|---|---|
| [Variable 1] | [Possible values] | [SRC-N, section/decision] | [What system behavior it affects] |

## 3.2 Gap-finding: Apply 5 lenses to discover what the sources missed

After drafting the initial variables list from Stage 2's confirmed content, systematically apply each lens below. **Each lens MUST produce at least one question presented to the user** — even if the answer seems obvious. Lenses that produce zero questions indicate the lens was not applied seriously.

### Lens 1: Actor-state combinations
> "For each actor, what states can they be in that nobody discussed?"

For every actor from Stage 2, ask:
- What if this actor is **absent**? (No DM assigned, officer has no schedule, system is offline)
- What if this actor is in a **transitional state**? (Mid-break, mid-shift-change, between clock-in and first action)
- What if this actor **acts unexpectedly**? (Officer force-closes app, DM never responds, system sends duplicate data)

### Lens 2: Boundary conditions per variable
> "For each variable, what happens at min, max, zero, and threshold edges?"

For every variable in the table, ask:
- What is the **minimum** value? The **maximum**? What happens at each?
- What happens at **threshold boundaries**? (e.g., shift length = exactly 5 hours, exactly 10 hours, 4 hours 59 minutes)
- What if the value is **missing, null, or invalid**? (No shift length known, no jurisdiction mapped, no EMS config set)

### Lens 3: Sequence and timing disruptions
> "What if the expected order breaks?"

Walk through the expected happy-path sequence and ask:
- What if a **step is skipped**? (Officer records end time without start time)
- What if **steps happen out of order**? (Officer taps End Shift before ending meal break)
- What if there's an **abnormal time gap** between steps? (Meal break start recorded, but end not recorded for 3 hours)
- What if a step **happens twice**? (Double-tap, accidental re-entry)

### Lens 4: System and integration failures
> "What if a dependency is unavailable, slow, or returns bad data?"

For every external system in the actor map, ask:
- What if it's **down**? (Break rules source unreachable, BI endpoint offline, WFM unavailable)
- What if it returns **stale or wrong data**? (EMS says unpaid but engagement is actually paid)
- What if the **connection is slow**? (Officer waiting 30 seconds for rules lookup at clock-in)
- What if **data is lost in transit**? (Attestation recorded locally but never synced)

### Lens 5: Constraint collisions
> "Can two confirmed constraints from Stage 2 conflict?"

Take every pair of constraints from Stage 2 and ask:
- Can both be satisfied simultaneously in all scenarios?
- If they conflict, which takes priority?
- Does satisfying one constraint create a loophole in another?

## 3.3 Identify NEW constraints (not in Stage 2)

Using the gaps surfaced by the 5 lenses above, identify constraints that **no source mentioned** but that the system must respect. Common categories:

- **Technical:** Offline capability, response time limits, data retention, concurrent sessions
- **Regulatory:** Accessibility requirements, data privacy, audit trail retention periods
- **Operational:** Maximum response time for DM review, notification delivery guarantees
- **UX:** Maximum taps to complete a flow, error recovery without data loss

Present these as:

| # | NEW Constraint | Category | Discovered Via | Impact |
|---|---------------|----------|---------------|--------|
| NC1 | [Constraint not in any source] | [Technical/Regulatory/Operational/UX] | [Which lens surfaced it] | [What it prevents or requires] |

**Do NOT repeat Stage 2 constraints here.** Reference them as "See Stage 2, C1-CN."

## 3.4 Map actor interactions (NOT a flat list)

Stage 2 already listed actors. Stage 3 maps how they **interact**:

| Trigger | From Actor | To Actor | Data Exchanged | Failure Mode |
|---------|-----------|----------|---------------|-------------|
| [Event] | [Actor A] | [Actor B] | [What data flows] | [What happens if this interaction fails] |

The "Failure Mode" column feeds directly into Stage 4's error scenarios.

## 3.5 Present for collaborative brainstorm

Present the variables, lens results, new constraints, and interaction map. Then ask:

```
Questions surfaced by gap analysis:
1. [Question from Lens 1] — affects: [which variable/constraint]
2. [Question from Lens 2] — affects: [which variable/constraint]
...

Are any of these already answered by something I missed?
Are there constraints or failure modes you've seen in practice that I haven't listed?
```

**Wait for user input before finalizing.** This is a brainstorm, not a delivery.

## Save Stage 3 artifact

**Save to:** `[output]/stage_output/Stage3-Variables-Actors.md`

Include: pre-stage checkpoint answers, variables table, lens results (questions surfaced per lens), new constraints table, actor interaction map with failure modes. **Do NOT include any content that duplicates Stage 2 — reference it instead.** End with `## Next Stage → Stage 3.5: Feature Decomposition`.

**Wait for user confirmation before proceeding.**
