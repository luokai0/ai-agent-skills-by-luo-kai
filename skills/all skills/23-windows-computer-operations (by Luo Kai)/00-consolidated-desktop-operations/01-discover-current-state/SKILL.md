---
name: "Windows Desktop and Window Management: Discover Current State"
description: "Inspect the Windows desktop shell, Settings and Control Panel navigation, window focus, snapping, virtual desktops, task switching, and multi-monitor layout through one verified, least-privilege workflow."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0001"
  version: "1.2.0"
---

# Windows Desktop and Window Management: Discover Current State

## Objective
Establish a privacy-conscious, independently verified baseline of the Windows desktop shell, Settings and Control Panel navigation, active windows, virtual desktops, focus, snapping, and monitor placement. Preserve the user's session, open work, data, privacy, accessibility preferences, and security posture. A command completing or a click registering is not proof; report only verified state.

## When to use
Use when inspecting any of these related Windows surfaces:
- Desktop, Explorer shell, desktop icons, notification area, and shell processes.
- Settings app, Control Panel, system pages, navigation paths, and search surfaces.
- Window focus, snapping, virtual desktops, task switching, and multi-monitor window placement.

Applies to interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. Do not assume administrator rights, a particular OEM, or identical controls across editions.

## Required operating discipline
1. Start from the user's stated goal. Identify the exact device, signed-in account, session, application, setting, window, process, or display. Do not infer that a similarly named object is the target.
2. Observe before acting. Record visible state and note unsaved work, active file operations, sync activity, update prompts, sign-in prompts, and security warnings.
3. Prefer native Windows UI and supported accessibility/UI Automation controls for GUI inspection. Use PowerShell only for bounded, relevant, read-oriented checks. Use least privilege.
4. Prefer stable UI Automation names, keyboard navigation, and application-native controls over coordinate-only interaction.
5. Obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
6. Make one small change at a time when a change is separately requested. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.
7. Do not turn an inspection request into an unrequested repair. Keep this skill read-only unless the user separately requests a specific change.

## Environment and target identification
Confirm as applicable:
- Windows edition, build, architecture, current user, and interactive session.
- Whether the device is local, remote, virtual, shared, or organization-managed. Distinguish host from guest.
- Exact target identity: process ID and executable; application and page identity; window title and owning process; or monitor identity and bounds.
- Whether the desktop is responsive and whether focus, dialogs, file operations, or unsaved work are active.

Preserve organizational policy and access paths. Never circumvent restrictions or substitute a different account or device.

## Domain profiles
Select only the profile relevant to the user's target. Do not run every probe by default.

### A. Desktop shell and Explorer
**Scope:** Desktop, Explorer shell, desktop icons, notification area, and shell processes.
**Preferred tools:** UI Automation, keyboard navigation, Task Manager, and read-only Get-Process / Get-ComputerInfo.
**Inspection:** Confirm desktop responsiveness, visible focus, relevant Explorer windows, notification-area state, and the identity/status of any specifically requested shell process. Do not enumerate unrelated personal files.
**Safety:** Do not terminate explorer.exe, restart the shell, or reset the desktop as a first response. Unsaved shell dialogs, file transfers, and file operations may be active.
**Verification:** Confirm the desktop remains responsive, focus is visible, relevant windows remain present, and no user window or active operation was lost.
**Recovery:** Try a different documented navigation route and preserve the session. If instability remains, report the exact symptom. Do not reset the shell or terminate processes as an improvised workaround.

### B. Windows navigation and settings
**Scope:** Settings app, Control Panel, system pages, navigation paths, and search surfaces.
**Preferred tools:** Start search, documented and supported Settings URI navigation, Control Panel applets, and read-only Get-ComputerInfo.
**Inspection:** Locate the exact page or setting, confirm page identity, and read the displayed value without changing it. Distinguish viewing a setting from modifying it.
**Safety:** Do not change system-wide or account-wide settings during discovery. Do not guess undocumented URI schemes or hidden navigation paths.
**Verification:** Reopen the target page and confirm both its identity and displayed value. If unavailable, check one reasonable documented alternative and report the limitation.
**Recovery:** Use Settings search or the corresponding Control Panel surface. Do not improvise registry edits, policy changes, or undocumented URI schemes.

### C. Window management and multitasking
**Scope:** Window focus, snapping, virtual desktops, task switching, and multi-monitor window placement.
**Preferred tools:** Win+Arrow shortcuts, Alt+Tab, Task View, and UI Automation window patterns.
**Inspection:** Identify active window, focus owner, window bounds, assigned monitor, virtual desktop, and user-visible layout. Check whether the target is minimized, off-screen, obscured, or on another desktop before proposing a change.
**Safety:** Do not close windows to solve focus problems. Preserve unsaved work, avoid moving windows off-screen, and do not rearrange unrelated windows or monitors.
**Verification:** Confirm active window, focus, bounds, monitor, and visible layout after each requested action. Verify original work remains open.
**Recovery:** Use Task View and keyboard navigation. Restore visible placement before escalating. Do not terminate the process or close the window as a shortcut.

## Safe diagnostic commands
These are optional, read-oriented probes. Use only those relevant to the selected profile and current shell. Check availability with Get-Command first.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
Get-Process | Select-Object -First 10 Name, Id
Get-Location
```

For a specifically requested directory inspection, scope the read to the exact confirmed path:

```powershell
Get-ChildItem -LiteralPath "C:\Users\<confirmed-user>\" | Select-Object -First 10 Name, Mode, Length
```

Do not enumerate hidden or protected content by default. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, full event logs, unrelated home directories, or private document names. Do not add wildcard targets, elevation, remote execution, or write operations merely to make a probe succeed. Never run a command if its target or effect is unclear.

## Unified inspection workflow
1. **Bind the request.** Select relevant profile(s). Confirm exact device, session, target, and identity.
2. **Capture a baseline.** Observe native UI first. Use only minimum read-only probes. Record relevant values and unavailable commands; do not install tools for optional inspection.
3. **Inspect the correct surface.** Keep shell, settings, and window-layout observations distinct so one result is not mistaken for another.
4. **Resolve ambiguity safely.** If multiple windows, pages, processes, displays, or accounts match, ask for clarification or stop. Never choose by display name alone when a stable identity is available.
5. **Gate mutations.** For discovery, make no changes. If a separate change is requested, state exact target, action, expected effect, dependencies, risk, and rollback route; obtain approval first.
6. **Verify independently.** Confirm through a second native surface when practical. Reopen the page, recheck process identity, or inspect window bounds. Compare using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.
7. **Close the loop.** Report what was inspected, what changed (normally nothing), what could not be inspected, evidence, and limitations. Never claim completion without verification.

## Stop conditions and recovery
Stop if target identity is ambiguous, a command is unavailable with no documented fallback, policy blocks the control, unsaved work may be lost, the desktop becomes unstable, an unexpected prompt appears, or observed state differs from expectations.

Preserve the last known-good state and exact error. Capture only a narrow, timestamped diagnostic relevant to the task. Retry at most once through a lower-risk documented route. Never improvise registry edits, service shutdown, driver replacement, security exceptions, shell resets, process termination, permanent deletion, or destructive workarounds.

## Privacy-safe evidence and handoff
Report target (minimally identifying, redacted description), baseline, actions actually performed, result, independent verification, blocked steps, and remaining risk. Do not include passwords, tokens, clipboard contents, notification text, browser profile data, private document names, unrelated personal paths, or unnecessary account identifiers. Mark unknown values as unknown.

## Completion checklist
- [ ] User intent, exact device/session, and target identity were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection stayed in scope and used least privilege.
- [ ] No unrelated files, windows, settings, accounts, devices, or processes were changed.
- [ ] Any consequential change had explicit approval and a recoverable plan.
- [ ] Resulting state was independently verified.
- [ ] Limitations, risks, and evidence were reported accurately.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows surfaces and tools.
