---
name: surface-navigation-and-automation
description: Use when an agent must navigate, read, or act on Windows desktop applications through their visible interface (windows, dialogs, menus, controls, or the accessibility tree) to complete an operator-requested task that has no reliable API or CLI path.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Surface Navigation And Automation

## Purpose and boundaries

This skill covers operating Windows desktop software through its visible surface: locating windows, reading control state, invoking menus and buttons, filling forms, and navigating file dialogs. Use it only when a documented API, command-line interface, or file-based route is unavailable or insufficient.

Out of scope: web browser automation (use a browser-specific skill), kernel or driver work, bypassing license or access controls, credential harvesting, and any action that changes systems the operator has not named.

## Inputs and assumptions

Require these before acting:

- The exact target application, version if known, and the expected window title or process name.
- The end state to reach, stated as observable facts (for example, "invoice status reads Posted").
- Data to enter, with its source and whether it is sensitive.
- Whether the task is read-only. Default to read-only until the operator confirms writes.

Assume the desktop session is interactive, the display scale is unknown until measured, and focus can be stolen by notifications. Do not assume control labels are stable across application versions or languages.

## Operating workflow

1. **Identify the target.** Enumerate top-level windows and match by process name and title. Record the window handle or equivalent identifier. If multiple candidates match, stop and ask.
2. **Read before acting.** Inspect the accessibility tree (Microsoft UI Automation exposes control name, control type, automation ID, value, and enabled state). Prefer automation IDs over display text, and prefer structured value patterns over screenshot reading.
3. **Capture a baseline.** Record the relevant field values and window state. This is required for later comparison.
4. **Act in single steps.** Perform one action (click, type, select), then re-read the control state. Never chain more than two unverified actions.
5. **Use keyboard paths where reliable.** Accelerator keys and tab order are more stable than coordinates. Use coordinates only as a last resort, recomputed after any scale or layout change.
6. **Handle dialogs explicitly.** Each modal dialog is a new decision point. Read its title and buttons before responding. Never press a default button without reading its label.
7. **Stop at the gate** (see Decision gates) before any commit, save-over, delete, send, or submit action.

## Decision gates

Pause and request explicit operator approval before:

- Deleting, overwriting, or moving files or records.
- Submitting forms, sending messages, posting transactions, or publishing anything externally.
- Changing security, permission, licensing, or account settings.
- Entering or displaying credentials, personal data, or regulated data.
- Any action in an application the operator did not name.
- Any step that cannot be undone from within the application.

Proceed without asking only for read-only inspection and for reversible navigation (opening menus, scrolling, expanding tree nodes, typing into an unsaved search box that you will clear).

If a control's label or behavior differs from the instructions, stop. Do not improvise a substitute.

## Verification and evidence

After each write action, confirm the observed state matches the expected state from the baseline plan. Evidence must include:

- The control name, type, and value read before and after the action.
- A screenshot or text dump of the window at the completion point.
- A list of every action taken, in order, with timestamps.

Quality checks for completion:

- Every planned field reads the intended value exactly (compare strings, not visual appearance).
- No unexpected dialogs remain open.
- The target window is the one that was acted upon, confirmed by handle or process ID.
- The end state matches the stated success condition.

Mark any version-sensitive assumption, such as control automation IDs or UI Automation pattern availability, as requiring verification against current official Microsoft documentation for the target OS build.

## Failure handling

- **Control not found:** Re-enumerate once after a short wait. If still absent, report the expected identifier and the nearest matches. Do not guess.
- **Unexpected dialog:** Capture its text, close nothing, and report. Close only if the operator has approved dismissal.
- **Value mismatch after write:** Undo once only if the undo is verified and reversible. Otherwise halt and report.
- **Focus lost mid-sequence:** Abort the sequence, re-verify the target window, and restart from the last verified checkpoint.
- **Application hang or crash:** Stop all input immediately. Do not retry input into an unresponsive window.

Never retry a write action that may have partially committed without first reading the current state.

## Deliverable contract

Return a structured report containing:

1. Target application, window identifier, and version observed.
2. Task outcome: completed, partially completed, or blocked, with the reason.
3. Ordered action log with before/after values.
4. Gates encountered and the operator decisions recorded for each.
5. Evidence artifacts (screenshots or text captures).
6. Open items and any assumptions requiring verification.

Do not claim success without matching evidence. Do not describe the task as secure, compliant, or audited unless the operator provides and you verify the relevant controls.