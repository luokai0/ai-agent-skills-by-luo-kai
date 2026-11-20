---
name: "Windows Validate An Automation Workflow across Input, Output, and Peripherals"
description: "Consolidated validate an automation workflow workflow across 3 Windows domains: Input, Output, and Peripherals. Preserves each profile's original procedures, tools, safety rules, examples, verification, and recovery guidance."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-g06-w25"
  version: "1.2.0"
---

# Windows Validate An Automation Workflow across Input, Output, and Peripherals

## Objective

Combine the validate an automation workflow workflows from 3 related Windows domains. Select only the profile that matches the user's target. Each profile retains its complete original workflow body, including task instructions, preferred tools, command examples, approval rules, verification, recovery, and completion criteria.

## When to use

Use when the user needs the validate an automation workflow workflow in any of these domains: Windows Displays, audio, cameras, and input devices; Windows Clipboard, text entry, and input reliability; Windows Printers, scanners, docks, and peripherals.

## Required operating discipline

- Confirm the exact device, account/session, target, and applicable domain before acting.

- Select only the relevant domain profile; do not execute every profile by default.

- Preserve each profile's native tools, platform distinctions, approval gates, and recovery rules.

- Prefer least privilege, observable actions, read-only inspection, and independent verification.

- Never bypass security controls, consent, organizational policy, or user approval.

- Do not discard or replace source procedures; use the full domain profile when a task-specific detail is needed.

## Domain profiles

### Profile 1: Windows Displays, audio, cameras, and input devices

Former domain: 20-display-audio-input

Former skill ID: windows-0595

#### Windows Displays, audio, cameras, and input devices: Validate An Automation Workflow

##### Objective

Carry out **validate an automation workflow** for display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to validate an automation workflow involving displays, audio, cameras, and input devices. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, validate an automation workflow means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Run a visible test, verify selected device, levels, resolution, refresh rate, and monitor order. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices.

**Preferred tools:** Settings Display/Sound, Get-CimInstance, Device Manager, built-in test panels.

**Task focus:** For **validate an automation workflow**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Respect camera/microphone privacy indicators; do not activate sensors or record people without consent.

**Verification:** Run a visible test, verify selected device, levels, resolution, refresh rate, and monitor order. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Return to the previous working device/display configuration and test one variable at a time. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0595` · **Version:** `1.1.0` · **Risk:** HIGH — state-changing; explicit approval required

**Exact task:** Windows Displays, audio, cameras, and input devices: Validate An Automation Workflow. Carry out **validate an automation workflow** for display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `20-display-audio-input`. **Scope:** Display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices.; **Preferred tools:** Settings Display/Sound, Get-CimInstance, Device Manager, built-in test panels.; **Task focus:** For **validate an automation workflow**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Respect camera/microphone privacy indicators; do not activate sensors or record people without consent.; **Verification:** Run a visible test, verify selected device, levels, resolution, refresh rate, and monitor order. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Test before trusting automation.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Review the script and its dependencies, identify all write operations, and test with a disposable sample or WhatIf/Confirm support. Check error handling, exit codes, idempotence, path boundaries, and behavior when inputs are missing.
4. **Gate changes.** Do not apply a change until the exact target, intended result, impact, and recovery path are stated and the user approves that specific action. Approval for one change does not authorize adjacent cleanup, reboot, or broader automation.
5. **Verify independently.** Verify expected outputs and that out-of-scope objects were untouched. Do not run against production or user data until the user approves the exact scope. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

###### Stop conditions and recovery

Stop if target identity is ambiguous, a command is unavailable and no documented fallback exists, policy blocks the control, unsaved work may be lost, the device becomes unstable, or the observed state differs from the expected state. Preserve the last known-good state and exact error. Retry at most once through a lower-risk documented route; never improvise registry edits, service termination, driver changes, security exceptions, reset, or permanent deletion.

###### Evidence and handoff

Report: **target** (redacted identifier), **baseline**, **actions actually taken**, **before/after state**, **verification evidence**, **blocked steps**, and **remaining risk**. Do not include passwords, tokens, clipboard contents, notification text, browser profile data, private document names, or unrelated personal paths. Mark unknown values as unknown instead of guessing.

##### Completion checklist

- [ ] The exact target and user intent were confirmed.
- [ ] No unrelated files, windows, settings, accounts, or devices were changed.
- [ ] Any consequential step had explicit approval and a recoverable plan where possible.
- [ ] The resulting state was independently verified.
- [ ] Limitations, remaining risks, and the evidence used were reported accurately.

---

*Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Windows and third-party product names are used descriptively; their respective owners retain their rights.*

### Profile 2: Windows Clipboard, text entry, and input reliability

Former domain: 37-clipboard-input

Former skill ID: windows-1105

#### Windows Clipboard, text entry, and input reliability: Validate An Automation Workflow

##### Objective

Carry out **validate an automation workflow** for clipboard inspection, paste, keyboard layouts, ime, text entry, and form interactions. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to validate an automation workflow involving clipboard, text entry, and input reliability. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for clipboard inspection, paste, keyboard layouts, ime, text entry, and form interactions. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, validate an automation workflow means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify a harmless sample, target field, character encoding, and final text before submission. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Clipboard inspection, paste, keyboard layouts, IME, text entry, and form interactions.

**Preferred tools:** Clipboard UI, keyboard layout settings, UI Automation ValuePattern, Notepad test.

**Task focus:** For **validate an automation workflow**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Clipboard may contain passwords or private data; never dump it wholesale or overwrite it silently.

**Verification:** Verify a harmless sample, target field, character encoding, and final text before submission. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Use direct typing for sensitive fields and restore clipboard only if the original value was safely retained with consent. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-1105` · **Version:** `1.1.0` · **Risk:** HIGH — state-changing; explicit approval required

**Exact task:** Windows Clipboard, text entry, and input reliability: Validate An Automation Workflow. Carry out **validate an automation workflow** for clipboard inspection, paste, keyboard layouts, ime, text entry, and form interactions. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `37-clipboard-input`. **Scope:** Clipboard inspection, paste, keyboard layouts, IME, text entry, and form interactions.; **Preferred tools:** Clipboard UI, keyboard layout settings, UI Automation ValuePattern, Notepad test.; **Task focus:** For **validate an automation workflow**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Clipboard may contain passwords or private data; never dump it wholesale or overwrite it silently.; **Verification:** Verify a harmless sample, target field, character encoding, and final text before submission. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Test before trusting automation.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Review the script and its dependencies, identify all write operations, and test with a disposable sample or WhatIf/Confirm support. Check error handling, exit codes, idempotence, path boundaries, and behavior when inputs are missing.
4. **Gate changes.** Do not apply a change until the exact target, intended result, impact, and recovery path are stated and the user approves that specific action. Approval for one change does not authorize adjacent cleanup, reboot, or broader automation.
5. **Verify independently.** Verify expected outputs and that out-of-scope objects were untouched. Do not run against production or user data until the user approves the exact scope. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

###### Stop conditions and recovery

Stop if target identity is ambiguous, a command is unavailable and no documented fallback exists, policy blocks the control, unsaved work may be lost, the device becomes unstable, or the observed state differs from the expected state. Preserve the last known-good state and exact error. Retry at most once through a lower-risk documented route; never improvise registry edits, service termination, driver changes, security exceptions, reset, or permanent deletion.

###### Evidence and handoff

Report: **target** (redacted identifier), **baseline**, **actions actually taken**, **before/after state**, **verification evidence**, **blocked steps**, and **remaining risk**. Do not include passwords, tokens, clipboard contents, notification text, browser profile data, private document names, or unrelated personal paths. Mark unknown values as unknown instead of guessing.

##### Completion checklist

- [ ] The exact target and user intent were confirmed.
- [ ] No unrelated files, windows, settings, accounts, or devices were changed.
- [ ] Any consequential step had explicit approval and a recoverable plan where possible.
- [ ] The resulting state was independently verified.
- [ ] Limitations, remaining risks, and the evidence used were reported accurately.

---

*Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Windows and third-party product names are used descriptively; their respective owners retain their rights.*

### Profile 3: Windows Printers, scanners, docks, and peripherals

Former domain: 38-printers-peripherals

Former skill ID: windows-1135

#### Windows Printers, scanners, docks, and peripherals: Validate An Automation Workflow

##### Objective

Carry out **validate an automation workflow** for printer queues, scanner discovery, usb devices, bluetooth, docks, and peripheral troubleshooting. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to validate an automation workflow involving printers, scanners, docks, and peripherals. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for printer queues, scanner discovery, usb devices, bluetooth, docks, and peripheral troubleshooting. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, validate an automation workflow means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify device identity, driver, queue, selected destination, and a non-sensitive test result. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Printer queues, scanner discovery, USB devices, Bluetooth, docks, and peripheral troubleshooting.

**Preferred tools:** Settings Bluetooth & devices, Get-Printer, Get-PrinterQueue, Device Manager.

**Task focus:** For **validate an automation workflow**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not print confidential material, clear queues, pair unknown devices, or install vendor utilities without approval.

**Verification:** Verify device identity, driver, queue, selected destination, and a non-sensitive test result. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-Printer | Select-Object Name,DriverName,PortName,PrinterStatus; Get-PrinterQueue -ErrorAction SilentlyContinue
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Check connection and queue status first; preserve pending jobs and ask before clearing them. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-1135` · **Version:** `1.1.0` · **Risk:** HIGH — state-changing; explicit approval required

**Exact task:** Windows Printers, scanners, docks, and peripherals: Validate An Automation Workflow. Carry out **validate an automation workflow** for printer queues, scanner discovery, usb devices, bluetooth, docks, and peripheral troubleshooting. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `38-printers-peripherals`. **Scope:** Printer queues, scanner discovery, USB devices, Bluetooth, docks, and peripheral troubleshooting.; **Preferred tools:** Settings Bluetooth & devices, Get-Printer, Get-PrinterQueue, Device Manager.; **Task focus:** For **validate an automation workflow**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not print confidential material, clear queues, pair unknown devices, or install vendor utilities without approval.; **Verification:** Verify device identity, driver, queue, selected destination, and a non-sensitive test result. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Test before trusting automation.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Review the script and its dependencies, identify all write operations, and test with a disposable sample or WhatIf/Confirm support. Check error handling, exit codes, idempotence, path boundaries, and behavior when inputs are missing.
4. **Gate changes.** Do not apply a change until the exact target, intended result, impact, and recovery path are stated and the user approves that specific action. Approval for one change does not authorize adjacent cleanup, reboot, or broader automation.
5. **Verify independently.** Verify expected outputs and that out-of-scope objects were untouched. Do not run against production or user data until the user approves the exact scope. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

###### Stop conditions and recovery

Stop if target identity is ambiguous, a command is unavailable and no documented fallback exists, policy blocks the control, unsaved work may be lost, the device becomes unstable, or the observed state differs from the expected state. Preserve the last known-good state and exact error. Retry at most once through a lower-risk documented route; never improvise registry edits, service termination, driver changes, security exceptions, reset, or permanent deletion.

###### Evidence and handoff

Report: **target** (redacted identifier), **baseline**, **actions actually taken**, **before/after state**, **verification evidence**, **blocked steps**, and **remaining risk**. Do not include passwords, tokens, clipboard contents, notification text, browser profile data, private document names, or unrelated personal paths. Mark unknown values as unknown instead of guessing.

##### Completion checklist

- [ ] The exact target and user intent were confirmed.
- [ ] No unrelated files, windows, settings, accounts, or devices were changed.
- [ ] Any consequential step had explicit approval and a recoverable plan where possible.
- [ ] The resulting state was independently verified.
- [ ] Limitations, remaining risks, and the evidence used were reported accurately.

---

*Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Windows and third-party product names are used descriptively; their respective owners retain their rights.*

## Unified discovery workflow

1. Bind the request to the exact device, session, target, and one or more relevant domain profiles.

2. Capture the baseline using the profile's native UI and bounded diagnostics.

3. Follow that profile's original workflow and task-specific safety boundary.

4. Stop when identity, permission, policy, or expected state is unclear.

5. Obtain explicit approval before consequential or externally visible changes.

6. Verify the result independently using the profile's stated evidence.

7. Report actions, unchanged state, evidence, limitations, and remaining risk.

## Stop conditions and recovery

Stop if target identity is ambiguous, a command or control is unavailable without a documented fallback, policy blocks the action, unsaved work may be lost, or the observed state differs from expectations. Preserve the last known-good state and exact error. Use the relevant profile's recovery route; do not improvise destructive workarounds.

## Privacy-safe evidence and handoff

Use the evidence and handoff requirements in the selected profile. Redact passwords, tokens, private paths, account identifiers, IP addresses, clipboard contents, and unrelated personal information. Mark unknown values as unknown.

## Completion checklist

- [ ] The exact target and applicable profile(s) were confirmed.

- [ ] Original domain-specific procedures and safety rules were followed.

- [ ] No unrelated files, settings, accounts, devices, or processes were changed.

- [ ] Any consequential action had explicit approval and a recoverable plan.

- [ ] The resulting state was independently verified.

- [ ] Limitations, remaining risks, and evidence were reported accurately.

---

Copyright (c) 2026 Luo Kai. All rights reserved for original material in this consolidated skill.
