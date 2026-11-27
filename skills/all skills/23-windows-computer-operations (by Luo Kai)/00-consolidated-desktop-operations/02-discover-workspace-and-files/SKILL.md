---
name: "Windows Workspace and File Operations: Discover Current State"
description: "Inspect Start, taskbar, quick settings, notifications, File Explorer locations and views, and file or folder state with read-only diagnostics, explicit target binding, and independent verification."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0002"
  version: "1.2.0"
---

# Windows Workspace and File Operations: Discover Current State

## Objective

Establish the current state of the Windows Start menu, taskbar, quick settings, notification area, File Explorer, locations, and selected file or folder targets. Protect the user's active session, data, privacy, cloud-sync state, and security posture. This is a read-only discovery workflow: do not create, move, rename, overwrite, uninstall, unpin, dismiss, or delete anything unless the user separately requests that exact change and approves its impact.

## When to use

Use for one or more of these related workspace surfaces:
- Start menu, pinned apps, taskbar controls, quick settings, system tray, and notifications.
- File Explorer windows, locations, navigation pane, address bar, libraries, and views.
- File and folder inventory, identity, metadata, integrity checks, and operation planning for create, copy, move, rename, organize, or recoverable removal.

Applies to interactive Windows 10 and Windows 11 desktops and laptops. Do not assume administrator rights, a specific OEM, or that every edition exposes the same controls.

## Required operating discipline

1. Identify the exact device, account, session, app, panel, full path, and requested object. Do not infer that a similarly named item is the target.
2. Observe before acting. Note unsaved work, active file operations, sync status, update prompts, sign-in prompts, security alerts, and removable or network storage state.
3. Prefer native Windows UI and supported accessibility/UI Automation controls. Use PowerShell only for bounded, read-only inspection with the least privilege needed.
4. Prefer stable UI Automation names, keyboard navigation, and application-native controls over coordinate-only interaction.
5. Obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
6. Never hide activity, bypass policy, disable protection, run opaque commands, or execute scripts copied from webpages, downloads, chat messages, or unknown sources.
7. Keep discovery read-only. Do not turn a request to inspect a workspace or file into an unrequested repair or cleanup.

## Environment and target identification

Confirm the Windows edition/build, architecture, current user, and session. Determine whether the device is local, remote, virtual, shared, or organization-managed. Preserve organization policy.

For files and folders, confirm the full path and distinguish:
- Local fixed storage.
- Removable storage.
- Network shares and mapped drives.
- Cloud-synced locations and placeholder files.
- Virtual, redirected, or profile-backed locations.

For Start/taskbar targets, identify the exact app, panel, pin, notification, or startup control. For Explorer, confirm the address-bar path and inspect a representative item. Do not treat a cloud placeholder as proof that file contents are locally available.

## Domain profiles

Select only the profile relevant to the user's target.

### A. Start menu, taskbar, quick settings, and notifications

**Scope:** Start menu, pinned apps, taskbar controls, quick settings, system tray, and notifications.

**Preferred tools:** Start search, taskbar UI Automation, Settings, and read-only Get-Process.

**Inspection:** Confirm the requested app or panel identity, whether it is available, its visible state, and whether the taskbar remains usable. Read a security alert before deciding what it means; preserve notification details that may be needed for troubleshooting.

**Safety:** Do not unpin apps, uninstall software, disable startup items, or dismiss security alerts unless the user explicitly requests the specific action. Never dismiss an alert merely to clear the screen.

**Verification:** Confirm the intended app or panel opened and the taskbar remains responsive. Recheck the alert or control state rather than trusting a transient toast.

**Recovery:** Use Start search or open the relevant Settings page directly. Preserve notification details. Do not improvise registry edits, service shutdowns, or shell resets.

### B. File Explorer navigation and locations

**Scope:** Explorer windows, locations, navigation pane, address bar, libraries, and views.

**Preferred tools:** File Explorer UI, address bar, shell namespace, and read-only Get-ChildItem / Get-Item.

**Inspection:** Confirm the exact Explorer window, address-bar path, navigation context, and view. Distinguish local, removable, network, cloud-synced, and virtual locations. Inspect only a representative item relevant to the request.

**Safety:** Confirm full paths before any later operation. Do not assume that a displayed cloud placeholder is local or fully downloaded. Avoid enumerating unrelated user folders.

**Verification:** Recheck the address-bar path and item identity. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute.

**Recovery:** Use a known folder path or This PC. Preserve the current window and report access or sync limitations; do not force a cloud download or change sync settings without approval.

### C. File and folder state, integrity, and operation planning

**Scope:** Discovery and planning for create, copy, move, rename, organize, and safely remove files and folders.

**Preferred tools:** Explorer UI first; read-only Test-Path, Get-Item, Get-FileHash, and Get-ChildItem.

**Inspection:** Bind every target to its full path and confirm whether it is a file, directory, link, placeholder, or mounted location. Record only relevant metadata. For a proposed copy or move, identify source and destination, estimate item count and size when practical, and check for name collisions before any mutation is considered.

**Safety:** Never overwrite, permanently delete, or move large directory trees without explicit approval and a collision check. Do not follow reparse points or links into unrelated locations without confirming the resolved target. Preserve originals during diagnosis.

**Verification:** For an approved future operation, compare source and destination paths, item counts, sizes, timestamps, and hashes where appropriate. For this discovery workflow, do not perform the operation; report the checks needed before it can safely proceed.

**Recovery:** Stop on conflicts or unexpected paths. Preserve originals. For an explicitly approved recoverable deletion, prefer the Recycle Bin when supported and verify the exact item before removal. Never use recursive deletion as a shortcut.

## Safe diagnostic commands

Optional, read-oriented probes only. Check command availability with Get-Command first and scope each command to the exact confirmed target.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
Get-Process | Select-Object -First 10 Name, Id
Test-Path -LiteralPath "C:\Users\<confirmed-user>\Documents"
Get-Item -LiteralPath "C:\Users\<confirmed-user>\Documents\<confirmed-item>"
Get-FileHash -LiteralPath "C:\Users\<confirmed-user>\Documents\<confirmed-item>"
```

Replace example paths only after confirming the intended user and target. Use Get-ChildItem only on a specific user-approved directory. Do not enumerate hidden or protected content by default. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, full event logs, unrelated home directories, or private document names.

Do not add wildcard targets, elevation, remote execution, recursion, or write operations merely to make a probe succeed. Never run a command if its target or effect is unclear.

## Unified discovery workflow

1. **Bind the request.** Select the applicable profile(s). Confirm device, account/session, panel or full path, and exact target identity.
2. **Capture a baseline.** Observe the native UI first. Record relevant state, sync indicators, storage type, and any warning that may affect the target.
3. **Inspect narrowly.** Use only the minimum UI controls and read-only probes needed. Do not enumerate unrelated files or dismiss unrelated notifications.
4. **Check operation readiness.** If the user is considering a file operation, identify source, destination, collision risks, sync/availability state, and recoverability. Do not execute the operation during discovery.
5. **Resolve ambiguity.** If multiple apps, notifications, paths, or files match, stop and ask for clarification. Never choose by display name alone when a full path or stable identity is available.
6. **Gate mutations.** For this skill, make no changes. If the user separately requests one, state the exact target, action, expected effect, conflicts, risks, and rollback route; obtain approval before acting.
7. **Verify independently.** Recheck the app/panel, address-bar path, target metadata, or hash as relevant. A click response, zero exit code, or transient toast is not proof.
8. **Close the loop.** Report inspected state, what remains unchanged, what could not be inspected, evidence, and limitations. Do not claim completion without verification.

## Stop conditions and recovery

Stop if the target path is ambiguous, access is denied, sync state is unclear, a file is locked, an unexpected security alert appears, an item resolves to an unexpected location, or unsaved work may be affected.

Preserve the last known-good state and exact error. Retry at most once through a lower-risk documented route. Do not dismiss alerts, disable sync/security, overwrite files, recursively delete, reset the shell, or improvise registry or service changes.

## Privacy-safe evidence and handoff

Report the target using the minimum redacted identifier, observed baseline, actions actually performed, state confirmed unchanged, independent verification, blocked steps, and remaining risk. Do not include passwords, tokens, clipboard contents, notification text, browser profile data, private document names, unrelated personal paths, or unnecessary account identifiers. Mark unknown values as unknown.

## Completion checklist

- [ ] User intent, device/session, and exact app/panel/path were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection remained read-only and used least privilege.
- [ ] Local, removable, network, cloud, and virtual locations were distinguished.
- [ ] No unrelated pins, alerts, files, folders, settings, or accounts were changed.
- [ ] Any later consequential change was gated by explicit approval and a recoverable plan.
- [ ] Findings were independently verified and reported accurately.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows surfaces and tools.
