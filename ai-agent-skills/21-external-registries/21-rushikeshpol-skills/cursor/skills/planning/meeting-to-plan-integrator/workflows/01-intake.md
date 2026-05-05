# Workflow 01: Intake

**Called from:** `SKILL.md` Step 2
**Next step:** `workflows/02-extract-changes.md`

---

## Purpose

Load meeting decisions and identify target documents.

---

## Step 1: Gather Inputs

- **Meeting notes** (any format — verbal, file, or `transcript-to-meeting-notes` output)
- **Target document(s) to update** (at least 1 required)
- **Release root folder** (to find related artifacts)
- **Constraint registry:** load `.meta/constraint-registry.md` if available

---

## Step 2: Processing Verification Gate

When input is `transcript-to-meeting-notes` output, verify:
- Is the routing correct? (right meeting → right decisions)
- Is the extraction accurate? (decisions match what was actually discussed)

If input is verbal or raw notes, this gate is N/A.

---

## Step 3: Quality Gate — Tier Check

| Tier | Requirements | Status |
|------|-------------|--------|
| **Tier 1** (minimum viable) | At least 1 decision described + at least 1 target document | ✅ / ❌ |
| **Tier 2** (recommended) | Tier 1 + structured meeting notes + all affected documents identified | ✅ / ❌ |
| **Tier 3** (comprehensive) | Tier 2 + transcript-to-meeting-notes output with attribution | ✅ / ❌ |

If Tier 1 is not met, STOP: "I need at minimum one decision and one target document to update."

---

## Completion Gate

- [ ] Meeting notes loaded and read
- [ ] Target documents identified
- [ ] Release root located
- [ ] Constraint registry loaded (if available)
- [ ] Processing verification gate passed (if applicable)
- [ ] Quality tier assessed

**CHECKPOINT (Notification):** "Found [N] decisions. Target documents: [list]. Proceed?"

**When complete, return to `SKILL.md` and proceed to Step 3.**
