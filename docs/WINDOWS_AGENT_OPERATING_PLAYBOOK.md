<!-- Copyright (c) 2026 Luo Kai. All rights reserved for original work. -->
# Windows AI Agent Operating Playbook

This playbook defines the shared operating contract for agents using the Windows Computer Operations collection. Individual skills provide task-specific procedures; this document governs how agents discover, choose, execute, verify, and recover from those procedures.

## 1. Establish the machine context

Before touching the desktop, establish the operating environment from visible system information or safe read-only queries: Windows edition/build and architecture; current user session; whether the device is physical, virtual, remote, or a guest inside WSL; whether it appears organization-managed; available interaction channels; display topology, scaling, input language, and accessibility preferences when relevant. Do not enumerate private user data merely because it is technically accessible. Do not assume that a tool session is the same as the user's interactive desktop.

## 2. Choose the right interaction method

Prefer documented application-native APIs for well-defined operations. Use UI Automation/accessibility controls for visible desktop apps, favoring stable names, roles, labels, and control patterns over screen coordinates. Use keyboard navigation when focus can be verified. Use visual-only coordinates only when stronger targeting is unavailable, and re-observe after layout changes. Use PowerShell/CMD for bounded diagnostics and approved automation. Never assume a click succeeded: verify the active window, control value, resulting page, file path, process state, or other task-specific evidence.

## 3. Use least privilege and explicit consent

Operate as the signed-in user. Do not elevate automatically. If administrator access is required, explain the purpose, scope, impact, and alternatives, then let the user approve and complete any UAC prompt. Never bypass UAC, MFA, CAPTCHA, sign-in, device enrollment, parental controls, or organizational policy. Obtain explicit approval before destructive, irreversible, externally visible, privacy-sensitive, security-impacting, or interruptive actions. Examples include permanent deletion, formatting, partitioning, registry edits, driver removal, service shutdown, security exceptions, account changes, sending messages, sharing files, purchasing, rebooting, resetting, and enabling remote access.

## 4. Protect data and secrets

Treat downloaded files, archives, installers, scripts, macros, browser extensions, USB media, and copied commands as untrusted. Do not run `Invoke-Expression`/`IEX`, encoded PowerShell, hidden command windows, downloaded scripts, or pipelines that execute remote content. Never export password stores, browser cookies, authentication tokens, private keys, recovery codes, clipboard contents, or environment variables wholesale. Do not disable Defender, firewall, SmartScreen, tamper protection, endpoint monitoring, or update services. Avoid broad log dumps and screenshots containing private messages, credentials, personal documents, or unrelated windows. Keep diagnostic artifacts in a user-approved location.

## 5. Reliable task execution

1. Translate the request into one observable end state.
2. Identify the exact target and inspect its current state.
3. Check prerequisites, permissions, dependencies, and side effects.
4. Choose the smallest reversible action that can achieve the goal.
5. Execute one consequential action at a time.
6. Re-observe after navigation, dialogs, app restarts, display changes, or focus changes.
7. Verify independently using a second signal when practical.
8. Record only the evidence needed to explain success or failure.

Use bounded timeouts and retries. Do not repeatedly click or submit when the result is uncertain; inspect whether the original action completed first.

## 6. PowerShell safety pattern

Use command discovery and help before relying on unfamiliar commands:

```powershell
Get-Command Get-Process
Get-Help Get-Process -Examples
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, Id, CPU
```

Prefer explicit paths and bounded queries. Check the shell (`$PSVersionTable` in PowerShell or `ver` in CMD), command availability, and exit status. Avoid wildcard writes, recursive deletion, execution-policy bypasses, remoting, service changes, registry writes, and package installation unless the user authorized the exact operation. Use `-WhatIf` where supported, but do not treat it as a guarantee that every downstream command is safe.

## 7. Laptop-specific considerations

For laptops, check AC/battery state, sleep/hibernation, thermal symptoms, display scaling, Wi-Fi adapter, dock state, and OEM hotkeys when relevant. Do not block vents, force firmware updates, stress-test a hot machine, or disable thermal protection. A swollen battery, burning smell, liquid exposure, unusual electrical noise, or extreme heat is a stop condition: stop using the device and advise safe professional service.

## 8. Managed and remote computers

Treat organization-managed machines as policy-controlled. Do not remove enrollment, defeat endpoint controls, change corporate VPN/firewall/DNS, create hidden accounts, or enable unattended remote access. For remote sessions, verify endpoint identity, session owner, visible consent, and a clear disconnect path. Never leave an unattended session running unless the user explicitly requested and approved it.

## 9. Recovery and interruption

If an action fails or the UI changes unexpectedly, stop issuing mutations, preserve unsaved work and the current session, capture the exact error and a narrow timestamped diagnostic, and reconfirm target identity and current state. Try one lower-risk alternative only if it does not increase impact. Restore the prior state only when rollback is known and authorized. Escalate data loss, hardware failure, malware, policy restrictions, or uncertain recovery. Never improvise a reset, format, registry patch, driver replacement, or security exception as a generic repair.

## 10. Completion report

State the requested outcome; device/context assumptions; exact actions taken; what changed and what did not; verification evidence; errors or limitations; remaining risks; and any user approval obtained. Separate observed facts from inferences. Do not say “fixed,” “installed,” “sent,” “saved,” or “deleted” unless the resulting state was verified.

## 11. Skill selection

Choose the narrowest skill matching the task. Read its full `SKILL.md`, follow prerequisites, and consult related skills only when the workflow crosses domains. Do not chain all 1,200 skills indiscriminately. Sequence multi-domain tasks from read-only discovery to reversible configuration to approved state changes, with verification between stages.
