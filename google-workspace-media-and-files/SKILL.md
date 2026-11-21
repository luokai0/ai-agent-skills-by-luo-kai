---
name: google-workspace-media-and-files
description: Use when handling images, video, audio, PDFs, Docs, Sheets, Slides, or Drive files stored in or exchanged through Google Workspace, especially for organizing, converting, extracting, auditing, or migrating media and file assets.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Google Workspace Media And Files

## Purpose and boundaries

This skill governs work on file-level assets in Google Drive and the media embedded in or attached to Docs, Sheets, and Slides: inventory, naming, format conversion, extraction of embedded media, deduplication, permission-aware sharing review, and migration staging. It does not cover drafting document content, building spreadsheet models, or designing slide narratives. Hand those to the relevant content skill.

Treat every file operation as one of three classes: read-only (listing, metadata, export to a scratch location), reversible (rename, move within a shared drive, add a label), or destructive/external (delete, trash, overwrite, change sharing, publish, bulk export outside the organization). Only the first two may proceed on your own judgment; the third requires explicit user approval per action batch.

## Inputs and assumptions

Before acting, establish:

- Scope: the folder, shared drive, or file IDs in question. Do not infer scope from file names alone.
- Target outcome: inventory, conversion, extraction, cleanup, or migration.
- Access: which account is in use and whether it has read, edit, or manager rights on the scope. Note any files owned by other users.
- Constraints: retention obligations, confidentiality labels, deadlines, and whether originals must be preserved.
- Tooling: the exact connector or API surface available. Google Drive, Docs, Sheets, and Slides interfaces and export formats change. Verify method names, parameters, supported MIME types, and quota limits against current official Google Workspace documentation before relying on them.

Assume originals must be preserved unless the user states otherwise. Assume sharing settings are in force and must not be widened.

## Operating workflow

1. Inventory. List items in scope with ID, name, MIME type, size, owner, last modified, parent path, and sharing status. Record counts by type. Save the inventory as a reference artifact before any change.
2. Classify. Tag each item: native Google format (Docs, Sheets, Slides), uploaded binary (PDF, image, video, audio, Office file), shortcut, or folder. Native formats require export; binaries may be downloaded directly.
3. Plan. Write a numbered change plan listing each operation, its class (read, reversible, destructive/external), item count, and expected output location.
4. Gate. Submit the plan for approval where required (see Decision gates).
5. Execute in batches of no more than 50 items, logging each item ID and result.
6. Verify each batch against the verification checklist before starting the next.
7. Produce the deliverable contract output.

For conversion: export to a new folder, never overwrite the source. Record source ID, output ID, format, and page or slide count. For PDF extraction of images, keep original resolution and note any lossy re-encoding.

For embedded media in Docs and Slides: extract by exporting or inspecting the document structure; do not re-save the document, because re-saving can alter layout, comments, and revision history.

## Decision gates

Stop and request approval when any of these hold:

- Any delete, trash, empty-trash, overwrite, or move out of a shared drive.
- Any change to sharing, link visibility, or ownership transfer.
- Any export or copy to a location outside the organization or to a personal account.
- Any operation affecting more than 50 items or more than 1 GB of data.
- Files flagged as confidential, legal hold, HR, financial, health, or credential-bearing (inspect filenames and content headers; do not open content beyond what the task needs).
- Format conversion that discards information: Sheets to CSV (drops formulas, formatting, multiple tabs), Slides to PDF with speaker notes omitted, video transcoding.

Proceed without approval only for read-only operations and reversible renames or label additions within the approved scope.

## Verification and evidence

Each batch must pass:

- Count match: items out equals items in, minus documented skips. Record skips with reasons.
- Checksum or size match for binary copies where the platform exposes one; otherwise compare size and page or slide count.
- Page and slide counts match for document exports; sheet count and row totals match for spreadsheet exports.
- Spot-check at least 5 percent of converted items, minimum 3, by opening the output and comparing against source.
- Permissions unchanged on source items after operations: record before and after sharing state.
- Naming conforms to the agreed convention with no collisions and no characters that break the target system.

Report evidence as counts and IDs, not assertions. Say "42 of 42 PDFs exported, 2 skipped (permission denied: IDs listed)" rather than "export complete."

## Failure handling

- Permission error: do not escalate access or attempt workarounds. Record the item ID and owner, and report it.
- Quota or rate limit: pause, back off, resume from the last logged ID. Do not restart the batch and risk duplicates.
- Unsupported export format: choose the nearest supported format, label the output as a substitute, and flag it for approval.
- Partial batch failure: retry only failed IDs once; escalate if still failing.
- Duplicate outputs detected: do not delete. Report the duplicates and wait for approval.
- Any unexpected deletion or sharing change: stop all operations immediately and report with the affected IDs.

## Deliverable contract

Return:

1. Scope summary: folder or IDs, item counts by type, and owner distribution.
2. Executed operations: class, count, and output location for each.
3. Verification results: pass or fail per check, with evidence counts and IDs.
4. Exceptions: skipped, failed, or substituted items, each with reason and recommended next action.
5. Pending approvals: a numbered list of gated operations awaiting sign-off.
6. Change log: the inventory and operation log saved as a file or attached artifact.

Do not state that migration is complete, that data is fully preserved, or that compliance requirements are met unless the verification evidence explicitly supports each claim. Scope the claim to what was checked.