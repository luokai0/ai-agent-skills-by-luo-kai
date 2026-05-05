# Meeting Summary Template

One template for all meeting types. The overall structure is always the same. Only the **topic internal structure** changes based on meeting type — see the two variants below.

---

## Full Template

```markdown
# [Feature/Topic] — Meeting Summary

**Session Date:** [day], [full date], [time range]
**Source Transcript:** [transcript filename](relative/path/to/transcript.md)
**Participants:** [Name (Role), Name (Role), ...]

---

## [N] Decisions Made

| # | Decision | Alternatives Considered | Source |
|---|----------|------------------------|--------|
| 1 | **[Decision statement]** | ❌ [Rejected option] — [reason]. *(Speaker)* | [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>) |
| 2 | **[Decision statement]** | ⏸️ [Deferred option] — [reason]. *(Speaker)* | [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>) |
| 3 | **[Decision statement]** | — | [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>) |

<!-- If no decisions were made: "No decisions reached — all topics remain open." -->

---

<!-- ============================================================
     TOPICS — use the variant that matches the meeting type.
     Discovery topics and Engineering topics can be mixed in
     the same document if the meeting covered both styles.
     ============================================================ -->

<!-- VARIANT A: Discovery / Requirements topic -->

## Topic 1: [Topic Title]

[1-sentence context line — what this topic is about.]

- [Fact with **key terms** bolded.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- [Fact.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- **Concern:** [Concern raised.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- ⏸️ **Deferred — [Idea name]:** [What was proposed and why it was deferred.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- **Correction:** [Incorrect statement] → [Corrected fact.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)

**Current state context:**
- [How things work today.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- [Pain point or process detail.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)

---

<!-- VARIANT B: Engineering / Technical topic -->

## Topic 2: [Topic Title]

**Context:** [1-2 sentence background on why this was discussed.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)

**Requirements:**
- [Bullet.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- [Bullet.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)

**Final Decision:**
- ✅ [Decision — outcome only.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- ✅ [Decision.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)

**Alternatives Considered:**
- ❌ [Rejected option] — [reason.] *(Speaker)*
- ⏸️ [Deferred option] — [reason / when to revisit.] *(Speaker)*

**Key Technical Insights:**
1. [Non-obvious insight with context.]

<!-- Omit "Alternatives Considered" if none were raised. -->
<!-- Omit "Key Technical Insights" if no non-obvious learnings. -->

---

<!-- VARIANT C: Mixed topic (discovery facts + a final decision) -->

## Topic 3: [Topic Title]

[1-sentence context line.]

- [Fact.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- [Fact.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- ❌ **Rejected:** [Option] — [reason.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)
- ✅ **Agreed:** [What was agreed.] [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>)

---

<!-- Repeat Topic N sections as needed -->

---

## WHAT WE KNOW VS WHAT WE DON'T KNOW

| **Topic** | **What We Know** | **What We Don't Know** | **Confidence** |
|-----------|------------------|------------------------|----------------|
| **[Topic]** | [Facts with *(Speaker)* attribution] | [Gaps that block next step] | 🟢 High |
| **[Topic]** | [Facts] | [Gaps] | 🟡 Medium |
| **[Topic]** | [Facts] | [Gaps] | 🔴 Low |

---

## ASSUMPTIONS THAT NEED VALIDATION

### ⚠️ ASSUMPTION: [Statement]
- **STATUS:** [Not confirmed / Partially confirmed / Conflicting signals]
- **VALIDATE WITH:** [Name] | **BY WHEN:** [date or TBD]
- **RISK IF WRONG:** [Consequence]

### ⚠️ ASSUMPTION: [Statement]
- **STATUS:** ✅ Confirmed — [evidence] *(Speaker)*

---

## OPEN QUESTIONS

### 🔴 HIGH — Block design

**1. [Question]**
- [Context / trade-offs]
- Owner: [Name] | Due: [TBD — before design]

**2. [Question]**
- [Context]
- Owner: [Name] | Due: [TBD]

### 🟡 MEDIUM — Block detailed requirements

**3. [Question]**
- [Context — Option A vs Option B]
- Owner: [Name] | Due: [TBD — before design]

**4. [Question]**
- [Context]
- Owner: [Name] | Due: [After specific event]

### 🟢 LOWER — Don't block Phase 1

**5. [Question]**
- Owner: [Name] | Due: [TBD]

---

## AGREED NEXT STEPS

| Owner | Action | Trace |
|-------|--------|-------|
| **[Name]** | [Action] | [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>) |
| **[Name]** | [Action] | [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>) |
| **[Name & Name]** | [Action] | [*(Speaker, timestamp)*](relative/path/to/transcript.md#L<line>) |

---

*All content derived directly from the session transcript. No assumptions or external information added.*
*Source:* [transcript filename](relative/path/to/transcript.md)
```
