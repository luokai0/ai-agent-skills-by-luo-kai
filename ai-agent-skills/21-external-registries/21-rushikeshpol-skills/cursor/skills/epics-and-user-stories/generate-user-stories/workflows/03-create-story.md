# Workflow 3: Create Stories via Sub-Agents

**Called from:** `workflows/02-decompose.md` after user approves decomposition
**Next step:** `workflows/04-set-review.md` after all stories created and approved
**Reads:** `[output-folder]/.meta/Decomposition-[Feature].md` + `[output-folder]/.meta/story-registry.md` + `[output-folder]/.meta/.pipeline-state.json`
**Saves:** `[output-folder]/[platform]-story-[N]-[name].md` (stories) + `[output-folder]/.meta/` (registry, pipeline state)

---

## 📍 You Are Here
**Skill:** generate-user-stories
**Stage:** 3 of 4 — Create Stories
**Input:** Approved decomposition with story concepts + requirements doc
**Your only job:** Create stories one-at-a-time via sub-agents, run quality checks, present for grouped approval
**DO NOT:** Present a story to the user that failed any quality gate.
**DO NOT:** Compress ACs to meet the ≤ 6 limit — split the story instead.
**DO NOT:** Populate the Dev Notes section — that's for the dev team.
**Audience:** You are writing for a developer and QA engineer who will pick this story up cold with no prior context.

---

## 🤖 Sub-Agent Contract (per story)

### Receives EXACTLY:
1. Relevant requirements section(s) for THIS story (from decomposition requirements mapping — not the full doc)
2. ONE story concept (title + user statement + platform)
3. ONE template (`templates/frontend-story.md` or `templates/backend-story.md`)
4. `[output-folder]/.meta/story-registry.md` (includes Conventions section after first story)
5. Ring 1 rules block (below)

### Returns:
- File path to saved story
- Compact registry entry (title, platform, ACs summary, key fields/endpoints, claimed boundary)
- Source traceability: which requirement section(s) each AC traces to

### Never receives:
Other story concepts, raw inputs, previous full stories, full requirements doc, Ring 2-3 rules.

### Ring 1 Rules Block (~20 lines — given to sub-agent):
```
## Rules (Ring 1 — violating any = trash output)
1. NEVER fabricate. Check each: field names (from requirements/Swagger?), business rules/thresholds (from requirements?), persona names (from project-context?), API paths (from API Contract?), error messages (from requirements/design?). Unknown = [TBD — requires: X] (Route to: Y). 2+ unknowns = STOP, return gap report.
2. NEVER generalize beyond source. "admin users" stays "admin users" not "users". "max 90 days" stays "90 days" not "historical data". Match source scope exactly.
3. Every AC cites source: (Req §X) or (Source: Design, screen-N). No citation = no AC.
4. User statement: specific persona, clear goal, clear business value. Verify persona CAN do what goal says.
5. WHAT not HOW. Design experience IS requirement (dropdown, toast, modal = OK). Implementation IS NOT (component names, CSS, framework refs, SQL = never). Dev Notes empty.
6. NO weak language. Banned: should/may/could/might (use "must"), appropriate/relevant/as needed (be specific), quickly/periodically/regularly (state the number), some/many/few (state count or [TBD]).

## Hard Stops
- Source contradiction → STOP, return both versions
- 2+ critical items missing → STOP, return gap report
- Task requires inventing data → STOP, state what's missing
```

Sub-agent also runs practitioner deliverability check before outputting:
- Developer: can you state what to build after one read?
- QA: can you state how to verify each AC after one read?
If either fails → fix before outputting.

---

## 🔍 Main Context Post-Generation Checks (per story)

After sub-agent saves the story file, main context reads it and verifies:

1. **Source Verification Pass:** For each `(Req §X)` citation, verify the claim exists in that section. Flag `[SOURCE UNVERIFIED]` if not found.
2. **AC Scope:** Count ≤ 6? If > 6 → story too big. Surface split recommendation to user.
3. **Terminology:** Terms match registry conventions? Mismatch → Edit tool fix.
4. **Visual Evidence (FE only):** Design references in ACs? Missing → Edit tool to add or flag.
5. **Structure:** Template sections present? Line count 60-90 (warn 91-120, review 121+)?
6. **Registry accuracy:** Does entry match actual story content?

**If Ring 1 failure detected** (fabricated data, code in ACs, unverified sources) → regenerate via sub-agent.
**If Ring 2-3 issues** → fix via Edit tool (targeted, no regeneration).

---

## 🎯 Spot-Check Protocol (first 2-3 stories)

Full read of saved story file verifying Ring 1 + Ring 2-3 compliance.
- If spot-checks pass → trust sub-agent for Ring 1 on remaining stories, continue Ring 2-3 checks on all.
- If Ring 1 spot-checks fail → switch to inline creation with explicit gate verification.

---

## 👥 Grouped Approval Flow

| Story # | Presentation |
|---------|-------------|
| 1st story | Individual (establishes conventions + spot-check) |
| 2nd story | Individual (spot-check + conventions confirmed) |
| 3rd+ | Groups of 3-5. Ask: "Approve this group? Or review any specific story?" |

**After first story approved:** Extract conventions (key terms, persona names, API naming style). Add Conventions section to `story-registry.md`. All subsequent sub-agents read this.

**Maximum 5-6 approval moments** for a 15-story feature (not 18+).

---

## 📝 Per Story/Group Workflow

1. Sub-agent creates story → saves file → returns path + registry entry
2. Main context reads file → runs post-generation checks → fixes Ring 2-3 via Edit if needed
3. Appends registry entry to `[output-folder]/.meta/story-registry.md`
4. Updates `[output-folder]/.meta/.pipeline-state.json` (stories_written, stories_pending, current_story)
5. Presents file path(s) to user
6. On approval → next story/group
7. On revision for specific AC → Edit tool on saved file (targeted edit, NOT regeneration)
8. On structural revision (different user statement, platform) → re-run sub-agent

**When to use sub-agents vs inline:**
- 1-3 stories total: inline (same context)
- 4+ stories: sub-agent per story

---

## 🔄 After All Stories Created and Approved

Update pipeline state, then **read:** `workflows/04-set-review.md`

---

## ✅ Completion Gate (per group)
- [ ] All story files saved
- [ ] Registry entries match actual story content
- [ ] Post-generation checks passed (or Ring 2-3 fixed via Edit)
- [ ] Pipeline state updated
- [ ] User has explicitly approved group
If any item is unchecked → do NOT proceed to next group.
