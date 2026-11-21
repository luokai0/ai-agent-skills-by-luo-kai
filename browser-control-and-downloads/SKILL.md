---
name: browser-control-and-downloads
description: Use when an agent must drive a web browser to navigate sites, fill forms, read pages, or retrieve files and downloads for a professional task, and needs disciplined control over sessions, approvals, file handling, and verification.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Browser Control And Downloads

## Purpose and boundaries

This skill governs how an agent operates a browser to complete a bounded web task: locating information, retrieving files, and submitting routine forms. It covers navigation, page reading, download capture, file validation, and handoff of results.

Out of scope: bypassing authentication or CAPTCHAs, scraping at volumes that violate a site's terms, accessing accounts the user has not authorized, installing browser extensions or software, and any action that spends money, sends messages, deletes data, or changes account settings without explicit approval.

## Inputs and assumptions

Before acting, confirm:

- Goal statement: the exact artifact or fact required (for example, "the Q3 invoice PDF from vendor portal X").
- Start URL or the domain allowed for the task. Treat any other domain as requiring a decision gate.
- Session state: whether the user is already logged in, and whether the agent may use that session.
- Output location: a named directory for downloads, with a free-space estimate if files are large.
- Stop conditions: maximum page count, maximum time, maximum files.

If any item is missing and cannot be inferred with high confidence, ask one consolidated question rather than guessing.

Assume the browser automation tool available in the environment exposes navigation, element inspection, typing, clicking, and download events. Do not assume specific method names or flags; check the tool's current documentation before scripting, since these are version-sensitive.

## Operating workflow

1. Restate the goal and list the planned domains and expected file types.
2. Open the start URL in a fresh context unless the user has named an existing session to reuse.
3. Read the page before interacting: note the title, the visible headings, login state, and any cookie or consent banner. Dismiss consent banners only if they block the task and dismissing them is non-committal.
4. Navigate by visible labels and links, not by guessed URLs. Record each step's URL and the element used.
5. For forms, fill fields from the user-supplied data only. Read back each field value before submission.
6. Before triggering any download, confirm the link text, file type, and size indicator match the goal.
7. Save downloads to the designated directory with a descriptive name: `<vendor>_<document-type>_<YYYY-MM-DD>.<ext>`. Do not overwrite existing files; append a numeric suffix.
8. Validate each file (see Verification).
9. Write a run log and deliver the result.

## Decision gates

Stop and request explicit approval before:

- Submitting any form that creates, modifies, cancels, pays, or sends something.
- Entering credentials, two-factor codes, or payment or identity data.
- Accepting terms of service, license agreements, or consent prompts on behalf of the user.
- Downloading executable files (.exe, .msi, .dmg, .pkg, .app, .sh, .bat, .ps1, browser extensions), archives over 100 MB, or files from a domain not in the approved list.
- Navigating to a domain outside the approved list, or following redirects that leave it.
- Any action on an account the user did not name.

Proceed without approval for read-only navigation within the approved domains and downloads of documents (PDF, CSV, XLSX, DOCX, PNG, JPG) under 100 MB that match the goal.

If a page requests a credential or code, stop. Never type credentials that were not explicitly supplied for this task, and never store them in logs or files.

## Verification and evidence

Each downloaded file must pass:

- Presence: the file exists in the target directory and its size is greater than zero.
- Type: the magic bytes match the expected format (for example, `%PDF` for PDF, `PK` for OOXML containers). Mismatch means quarantine, not use.
- Completeness: for PDFs, the page count matches the count shown on the source page when displayed; for CSV or XLSX, the row count or a total row matches the stated total when available.
- Identity: the document title, date, or identifier visible inside the file matches the goal statement.
- Freshness: the date is within the period the user requested.

Record evidence for every claim: source URL, timestamp, filename, byte size, SHA-256 hash, and the visible text or element that justified the choice. A result without a source URL is not complete.

Take a screenshot of the source page at the point of download when the tool supports it, and store it beside the file.

## Failure handling

- Page does not load or times out: retry once after a short wait, then record the URL and error and stop that branch.
- Element not found: re-read the page; labels often change. Do not click coordinates blindly.
- Download starts but never completes: check the download state once; if incomplete, do not repeat more than twice and report.
- Unexpected login wall, MFA, or CAPTCHA: stop and hand off to the user.
- File fails validation: quarantine it in a `_rejected` subfolder and report the reason.
- Site behaves differently from documentation: trust the observed page and report the discrepancy.

Never work around access controls, rate limits, or blocks by changing identity, rotating addresses, or spoofing clients.

## Deliverable contract

Return:

1. Result summary: what was obtained, in one paragraph.
2. File manifest: a table with filename, source URL, size, SHA-256, validation status.
3. Run log: ordered steps taken, with timestamps and any skipped items and why.
4. Open items: anything requiring user approval, credentials, or a decision.
5. Confidence statement: which claims are directly verified from files or pages and which are inferred.

Do not claim completion unless every requested artifact is either delivered and validated or explicitly listed as unobtained with a reason.\n\n## Ultron routing contract

**Choose this skill when:** the objective is browser-based information retrieval or file acquisition: navigate approved sites, read pages, locate documents, download bounded files, validate file types and contents, and hand over organized artifacts.

**Choose `browser-desktop-control` when:** the objective requires stateful interaction with a graphical application, especially multi-step forms, record updates, uploads, exports, reconciliation, or desktop windows where each action must be observed and verified.

**Handoff contract:** send the desktop-control skill the approved account/domain, task objective, input data, expected record or artifact count, and side-effect boundaries. Return file paths or verified artifact references, hashes, source URLs, and retrieval timestamps. Prefer a stable documented API over UI driving when it is available and authorized.

**Why the boundary exists:** browser retrieval is optimized for reading and acquiring evidence; desktop control is optimized for controlled state transitions in a user interface.
