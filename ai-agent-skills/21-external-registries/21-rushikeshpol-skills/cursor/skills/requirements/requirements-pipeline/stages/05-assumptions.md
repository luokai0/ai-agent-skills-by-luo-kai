# Stage 5: Assumptions Identification (MANDATORY CHECKPOINT)

**Called from:** `SKILL.md` (Pipeline Orchestrator)
**Next step:** Return to `SKILL.md` for Stage 6: User Flows
**Saves to:** `[output]/stage_output/Stage5-Assumptions.md`

---

**Read and follow the `identify-assumptions` skill** with the following context:
- The variables and constraints from Stage 3
- The scenario matrix from Stage 4
- All processed inputs from Stage 1
- Any assumptions already surfaced by `transcript-to-meeting-notes` (if transcripts were processed in Stage 1). Note: meeting notes produce a simpler 3-field assumption format (STATUS, VALIDATE WITH / BY WHEN, RISK IF WRONG). The `identify-assumptions` skill will enrich these with RISK AREA, EVIDENCE, and SUGGESTED TEST fields, and may identify additional assumptions not discussed in the meeting.

**Present all assumptions to the user.** Group by priority (HIGH / MEDIUM / LOW), then by risk area (Value, Usability, Viability, Feasibility) within each group. Highest risk first.

**Table formatting rule (applies to all tables in all pipeline artifacts):**
- Every priority/risk/severity indicator must include a label, never a bare dot: `🔴 Critical` not `🔴`, `🟡 Important` not `🟡`, `🟢 Low` not `🟢`
- Tables must be sorted by highest priority/risk/severity first. Resolved items sink to the bottom.

## 5.5 Classification Filter (post-processing)

After the `identify-assumptions` skill runs but before saving, classify each surfaced item to ensure it is truly an assumption and not mistyped. Apply these rules:

| If the item... | Then it is a... | Action |
|---|---|---|
| Has an owner and delivery status (someone must deliver something) | **Dependency** | Flag as `[RECLASSIFY: Dependency]`. It will land in the Dependencies table in Stage 7. |
| Needs a stakeholder decision before the team can proceed | **Open Question** | Flag as `[RECLASSIFY: Open Question]`. It will land in the OQ table in Stage 7. |
| Is confirmed and creates a trade-off | **Known Limitation** | Flag as `[RECLASSIFY: Known Limitation]`. Move to Known Limitations in Stage 7. |
| Is confirmed and creates no trade-off | **Not an assumption** | Delete it. Confirmed facts are not assumptions. |
| Is genuinely unconfirmed and carries risk if wrong | **Assumption** | Keep it. This is a valid assumption. |

Include the `[RECLASSIFY: ...]` tags in the Stage 5 artifact so Stage 7 (generate-requirements) can route each item to the correct section. Do not remove reclassified items from the Stage 5 file — they serve as the audit trail for why the item was moved.

## Save Stage 5 artifact

**Save to:** `[output]/stage_output/Stage5-Assumptions.md`

Include: all items grouped by priority (HIGH/MEDIUM/LOW) then by risk area, with STATUS, VALIDATE WITH, BY WHEN, RISK IF WRONG, any enrichment from the `identify-assumptions` skill, and `[RECLASSIFY: ...]` tags where applicable. End with `## ACTION REQUIRED` section.

**Wait for user to confirm, correct, or add assumptions before proceeding.**

---

Stage 5 complete. Return to `SKILL.md` and proceed to Stage 6: User Flows.
