---
name: browser-desktop-control
description: Use when an agent must operate a web browser or desktop GUI to complete a multi-step task (navigating sites, filling forms, downloading or exporting files, reading on-screen state, or verifying UI outcomes) and needs a disciplined plan, approval gates, and evidence of results.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Browser Desktop Control

## Purpose and boundaries

This skill governs how an agent drives a graphical interface: a browser tab, a web application, or a desktop application window. It covers observation, targeted interaction, state verification, and reporting.

In scope:
- Navigating web applications and reading page or window state.
- Filling forms, selecting options, uploading and downloading files.
- Exporting reports, reconciling values shown on screen against a source, and capturing screenshots as evidence.
- Repetitive UI tasks across a bounded set of records (for example, updating 30 supplier profiles from a spreadsheet).

Out of scope:
- Tasks that have a stable API or export path when the user has not asked for UI driving. Prefer the official interface.
- Bypassing authentication, CAPTCHAs, rate limits, access controls, or anti-bot measures.
- Acting in accounts the user does not own or has not been authorized to operate.
- Financial transfers, purchases, deletions, sending messages, publishing content, or changing permissions, unless the approval gate below is satisfied.

## Inputs and assumptions

Before acting, confirm:
1. The goal in one sentence, and the success condition that can be observed on screen.
2. The target application, environment (production, staging, sandbox), and account identity.
3. Data sources and their authoritative values. Do not treat on-screen text as ground truth when a source file or record exists.
4. Allowed scope: which records, fields, and actions are permitted, and the maximum number of items.
5. Whether the environment is reversible (draft mode, undo, staging copy) or not.

If any item is missing and cannot be inferred safely, ask one consolidated question and stop.

Assumptions must be stated in the first progress note. Do not assume login state, screen resolution, locale, or time zone without checking.

## Operating workflow

1. **Observe.** Capture the current screen state (screenshot or accessibility snapshot where available). Record the URL or window title, the visible account, and any blocking dialog.
2. **Plan.** Write a numbered plan of at most ten steps. Mark each step as read-only or state-changing.
3. **Locate before acting.** Identify each target element by its visible label, role, and surrounding context. Prefer labeled controls over coordinates. Never click by guessing position when a label exists.
4. **Act in small units.** Perform one state-changing action at a time. After each, re-observe and confirm the expected change occurred.
5. **Checkpoint.** After every five to ten records or any major page transition, save a progress log: records completed, records failed, current position, and the next step.
6. **Reconcile.** When the task produces a result, compare on-screen values with the authoritative source using a fixed field list.
7. **Clean up.** Close only dialogs or tabs the agent opened. Leave the environment as it was found, unless the task says otherwise.

Use waits based on observed state changes (element appears, spinner disappears, URL changes), not fixed delays.

## Decision gates

Stop and request explicit user approval, naming the exact action and count, before any of the following:
- Deleting, archiving, overwriting, or bulk-editing existing records.
- Submitting forms that create legal, financial, or customer-facing commitments.
- Sending emails, messages, invitations, or public posts.
- Changing passwords, MFA settings, roles, permissions, or API keys.
- Payments, refunds, subscriptions, or purchases.
- Any action in a production system when the task was described as a test, or any action whose target environment is unclear.
- Any action that would exceed the approved record count or touch fields outside the approved list.

Pause and re-verify rather than proceed when:
- The page shows an unexpected account, environment banner, or different record than the plan.
- A confirmation dialog describes consequences you did not anticipate.
- Two consecutive attempts at the same action produce no observable change.

Approval given for one batch does not extend to later batches unless stated.

## Verification and evidence

Every completed task requires:
- **Per-action confirmation:** the expected post-condition was observed (text, value, status badge, URL, or file appearing on disk).
- **Field-level reconciliation:** for data entry or export tasks, a table of source value versus on-screen value for a sample of at least 10 percent of records, and for all records when the set is 50 or fewer. Any mismatch is a failure until explained.
- **Final-state capture:** a screenshot or snapshot of the summary view showing the count of successes and failures.
- **Log file:** timestamps, record identifiers, action taken, result, and any retries.

Do not report success based on the absence of an error message alone.

## Failure handling

- **Transient failure** (timeout, spinner that never resolves, network error): retry once after re-observing. A second failure becomes a recorded failure, not a third attempt.
- **Element not found:** re-check for scrolling, iframes, modal overlays, or a changed layout before concluding. Record the page state.
- **Session expired or login prompt:** stop. Do not enter credentials you were not given. Ask the user to re-authenticate.
- **Unexpected data:** halt the batch, log the record, and continue only if the remaining records are independent and the user pre-approved skipping.
- **Partial completion:** report exact completed and remaining items so a human can resume without repeating work.

Never retry a state-changing submission blindly; first check whether the previous attempt already succeeded.

## Deliverable contract

Return a single report containing:
1. Outcome: succeeded, partially succeeded, or failed, with one-sentence justification.
2. Scope executed: environment, account, record count attempted, record count completed.
3. Actions taken, in order, with approval references for gated actions.
4. Reconciliation results: sample size, mismatches, and resolution.
5. Failures and skipped items, each with reason and recommended next step.
6. Evidence links or file paths to screenshots, logs, and exported files.
7. Items requiring human decision.

Do not claim capabilities, speed, or accuracy figures that were not measured in the run. Do not state that the process is compliant with any regulation; state only what was verified.