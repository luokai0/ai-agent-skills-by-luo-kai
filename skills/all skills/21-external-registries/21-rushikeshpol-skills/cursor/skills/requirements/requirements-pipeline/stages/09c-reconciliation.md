# Stage 9c: Post-Merge Reconciliation (ONLY if multiple features)

This stage runs only when Stage 3.5 produced a split and multiple feature documents exist. It is the final quality gate that ensures the set of documents is consistent, not just individually correct.

## 9c.1 Cross-document deduplication scan

> **Note:** Within-document dedup already ran in Stage 9b.0 for each feature document. This stage focuses exclusively on cross-document duplicates.

For each pair of feature documents, check:
- **Duplicate assumptions:** Same assumption stated in two documents (even with different wording). Keep the one owned per the Shared Registry. Delete the duplicate and add a cross-reference.
- **Duplicate dependencies:** Same dependency row in two documents. Keep the one owned per the Shared Registry.
- **Duplicate open questions:** Same question asked in two documents. Keep the one owned per the Shared Registry.
- **Duplicate FR business rules:** Same business rule bullet appearing in two FRs across different features (e.g., notification delivery mechanism described in both Feature A and Feature B). Keep the framework rule in the owner feature; replace the duplicate with a cross-reference.

## 9c.2 Conflict detection

Scan for:
- **Same rule, different wording:** Two features describe the same behavior using different language. Standardize to one phrasing (use the primary feature's version).
- **Contradictory rules:** Two features state conflicting behavior for the same scenario. Flag for user resolution.
- **Inconsistent status:** An assumption marked "Confirmed" in Feature A but "Not confirmed" in Feature B. Align to the most current status.

## 9c.3 Resolve [SHARED] flags

During Stages 4-9b, subagents may have flagged new items as `[SHARED — assign to Feature X]`. For each:
1. Confirm which feature should own it
2. Move it to the owning feature's document
3. Add cross-references in the other feature documents
4. Update the Shared Registry

## 9c.4 Add cross-references

For every cross-reference placeholder ("See Feature A, Section N"), resolve to the actual section number in the final document. Verify the target section exists and contains the expected content.

## 9c.5 Present reconciliation report

**Save to:** `[output]/stage_output/Stage9c-Reconciliation.md`

Include:
- Number of cross-document duplicates found and resolved (from 9c.1)
- Number of conflicts found (resolved + unresolved, from 9c.2)
- Number of [SHARED] flags resolved (from 9c.3)
- Number of cross-references added (from 9c.4)
- Any unresolved conflicts requiring user decision

**STOP and WAIT for user to review.** If unresolved conflicts exist, the user must decide before documents are finalized.
