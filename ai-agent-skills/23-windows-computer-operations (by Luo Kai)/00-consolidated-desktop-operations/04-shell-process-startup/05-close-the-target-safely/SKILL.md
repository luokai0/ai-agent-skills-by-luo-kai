---
name: "Windows Close The Target Safely across Shells, processes, and startup"
description: "Consolidated close the target safely workflow across 5 Windows domains: Shells, processes, and startup. Preserves each profile's original procedures, tools, safety rules, examples, verification, and recovery guidance."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-g04-w05"
  version: "1.2.0"
---

# Windows Close The Target Safely across Shells, processes, and startup

## Objective

Combine the close the target safely workflows from 5 related Windows domains. Select only the profile that matches the user's target. Each profile retains its complete original workflow body, including task instructions, preferred tools, command examples, approval rules, verification, recovery, and completion criteria.

## When to use

Use when the user requests close the target safely in any of these domains: Windows PowerShell fundamentals; Windows Advanced PowerShell administration; Windows Command Prompt and Windows Terminal; Windows Processes, services, and applications; Windows Startup, scheduled tasks, and background execution.

## Required operating discipline

- Confirm the exact device, account/session, target, and applicable domain before acting.

- Select only the relevant domain profile; do not execute every profile by default.

- Preserve each profile's native tools, platform distinctions, approval gates, and recovery rules.

- Prefer least privilege, observable actions, read-only inspection, and independent verification.

- Never bypass security controls, consent, organizational policy, or user approval.

- Do not discard or replace source procedures; use the full domain profile when a task-specific detail is needed.

## Domain profiles

### Profile 1: Windows PowerShell fundamentals

Former domain: 10-powershell-fundamentals

Former skill ID: windows-0275

#### Windows PowerShell fundamentals: Close The Target Safely

##### Objective

Carry out **close the target safely** for powershell discovery, safe command execution, objects, pipelines, profiles, and help.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to close the target safely involving powershell fundamentals. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for powershell discovery, safe command execution, objects, pipelines, profiles, and help.. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, close the target safely means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Read command output, exit status, and affected object; rerun read-only checks to confirm. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** PowerShell discovery, safe command execution, objects, pipelines, profiles, and help.

**Preferred tools:** Get-Help, Get-Command, Get-ComputerInfo, Get-Location, Get-ChildItem, Get-Process.

**Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Never execute opaque pasted commands; avoid encoded commands, hidden windows, execution-policy bypass, and untrusted profiles.

**Verification:** Read command output, exit status, and affected object; rerun read-only checks to confirm. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-Command; Get-Help Get-Process; Get-Location; Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Use Get-Help -Online only when permitted; fall back to built-in help and explain unavailable modules. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0275` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows PowerShell fundamentals: Close The Target Safely. Carry out **close the target safely** for powershell discovery, safe command execution, objects, pipelines, profiles, and help.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `10-powershell-fundamentals`. **Scope:** PowerShell discovery, safe command execution, objects, pipelines, profiles, and help.; **Preferred tools:** Get-Help, Get-Command, Get-ComputerInfo, Get-Location, Get-ChildItem, Get-Process.; **Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Never execute opaque pasted commands; avoid encoded commands, hidden windows, execution-policy bypass, and untrusted profiles.; **Verification:** Read command output, exit status, and affected object; rerun read-only checks to confirm. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Graceful close with unsaved-work protection.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the exact window and inspect for unsaved work, active transfers, dialogs, or background operations. Use the application Close command or window control and handle any save/discard prompt according to the user’s explicit instruction. Do not use taskkill or End task as a routine close method.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If the app is hung, collect a minimal diagnostic and ask before force-closing. Verify only the intended window closed and unrelated work remains open. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 2: Windows Advanced PowerShell administration

Former domain: 11-powershell-advanced

Former skill ID: windows-0305

#### Windows Advanced PowerShell administration: Close The Target Safely

##### Objective

Carry out **close the target safely** for structured output, cim, remoting concepts, modules, error handling, and safe automation patterns.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to close the target safely involving advanced powershell administration. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for structured output, cim, remoting concepts, modules, error handling, and safe automation patterns.. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, close the target safely means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Use -WhatIf when supported, inspect object counts, capture errors, and verify state independently. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Structured output, CIM, remoting concepts, modules, error handling, and safe automation patterns.

**Preferred tools:** Get-CimInstance, Get-WinEvent, Get-Service, Get-NetAdapter, Export-Csv only to approved paths.

**Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not invoke remote scripts, change execution policy, elevate, or alter machine state without approval.

**Verification:** Use -WhatIf when supported, inspect object counts, capture errors, and verify state independently. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-CimInstance Win32_OperatingSystem; Get-Service | Select-Object -First 20; Get-WinEvent -ListLog * | Select-Object -First 10
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Reduce scope to one target, use read-only queries, and stop on permission or provider errors. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0305` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows Advanced PowerShell administration: Close The Target Safely. Carry out **close the target safely** for structured output, cim, remoting concepts, modules, error handling, and safe automation patterns.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `11-powershell-advanced`. **Scope:** Structured output, CIM, remoting concepts, modules, error handling, and safe automation patterns.; **Preferred tools:** Get-CimInstance, Get-WinEvent, Get-Service, Get-NetAdapter, Export-Csv only to approved paths.; **Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not invoke remote scripts, change execution policy, elevate, or alter machine state without approval.; **Verification:** Use -WhatIf when supported, inspect object counts, capture errors, and verify state independently. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Graceful close with unsaved-work protection.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the exact window and inspect for unsaved work, active transfers, dialogs, or background operations. Use the application Close command or window control and handle any save/discard prompt according to the user’s explicit instruction. Do not use taskkill or End task as a routine close method.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If the app is hung, collect a minimal diagnostic and ask before force-closing. Verify only the intended window closed and unrelated work remains open. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 3: Windows Command Prompt and Windows Terminal

Former domain: 12-terminal-cmd

Former skill ID: windows-0335

#### Windows Command Prompt and Windows Terminal: Close The Target Safely

##### Objective

Carry out **close the target safely** for terminal profiles, shells, command discovery, environment variables, and command sessions.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to close the target safely involving command prompt and windows terminal. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for terminal profiles, shells, command discovery, environment variables, and command sessions.. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, close the target safely means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Confirm active shell, working directory, target path, and command exit code. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Terminal profiles, shells, command discovery, environment variables, and command sessions.

**Preferred tools:** Windows Terminal UI, cmd /? help, where.exe, set, ver, whoami.

**Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not paste commands from untrusted pages; distinguish PowerShell syntax from cmd.exe syntax.

**Verification:** Confirm active shell, working directory, target path, and command exit code. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Open a fresh non-elevated shell and repeat only the read-only diagnostic step. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0335` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows Command Prompt and Windows Terminal: Close The Target Safely. Carry out **close the target safely** for terminal profiles, shells, command discovery, environment variables, and command sessions.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `12-terminal-cmd`. **Scope:** Terminal profiles, shells, command discovery, environment variables, and command sessions.; **Preferred tools:** Windows Terminal UI, cmd /? help, where.exe, set, ver, whoami.; **Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not paste commands from untrusted pages; distinguish PowerShell syntax from cmd.exe syntax.; **Verification:** Confirm active shell, working directory, target path, and command exit code. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Graceful close with unsaved-work protection.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the exact window and inspect for unsaved work, active transfers, dialogs, or background operations. Use the application Close command or window control and handle any save/discard prompt according to the user’s explicit instruction. Do not use taskkill or End task as a routine close method.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If the app is hung, collect a minimal diagnostic and ask before force-closing. Verify only the intended window closed and unrelated work remains open. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 4: Windows Processes, services, and applications

Former domain: 13-process-services

Former skill ID: windows-0365

#### Windows Processes, services, and applications: Close The Target Safely

##### Objective

Carry out **close the target safely** for process inspection, app lifecycle, service status, resource usage, and hung-app diagnosis.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to close the target safely involving processes, services, and applications. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for process inspection, app lifecycle, service status, resource usage, and hung-app diagnosis.. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, close the target safely means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify PID, executable path, signer where available, status, and resource trend. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Process inspection, app lifecycle, service status, resource usage, and hung-app diagnosis.

**Preferred tools:** Task Manager, Resource Monitor, Get-Process, Get-Service, Get-CimInstance Win32_Service.

**Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not terminate system/security processes or stop services based only on name; protect unsaved app work.

**Verification:** Verify PID, executable path, signer where available, status, and resource trend. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10; Get-Service | Where-Object Status -eq Running
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Collect evidence first; use normal app close and restart before considering service intervention. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0365` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows Processes, services, and applications: Close The Target Safely. Carry out **close the target safely** for process inspection, app lifecycle, service status, resource usage, and hung-app diagnosis.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `13-process-services`. **Scope:** Process inspection, app lifecycle, service status, resource usage, and hung-app diagnosis.; **Preferred tools:** Task Manager, Resource Monitor, Get-Process, Get-Service, Get-CimInstance Win32_Service.; **Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not terminate system/security processes or stop services based only on name; protect unsaved app work.; **Verification:** Verify PID, executable path, signer where available, status, and resource trend. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Graceful close with unsaved-work protection.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the exact window and inspect for unsaved work, active transfers, dialogs, or background operations. Use the application Close command or window control and handle any save/discard prompt according to the user’s explicit instruction. Do not use taskkill or End task as a routine close method.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If the app is hung, collect a minimal diagnostic and ask before force-closing. Verify only the intended window closed and unrelated work remains open. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 5: Windows Startup, scheduled tasks, and background execution

Former domain: 14-startup-scheduling

Former skill ID: windows-0395

#### Windows Startup, scheduled tasks, and background execution: Close The Target Safely

##### Objective

Carry out **close the target safely** for startup apps, task scheduler, login tasks, and background execution diagnosis.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to close the target safely involving startup, scheduled tasks, and background execution. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for startup apps, task scheduler, login tasks, and background execution diagnosis.. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, close the target safely means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify task name, trigger, principal, action, last-run result, and visible ownership. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Startup apps, Task Scheduler, login tasks, and background execution diagnosis.

**Preferred tools:** Settings Startup, Task Manager Startup, Get-ScheduledTask, Get-CimInstance Win32_StartupCommand.

**Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not create persistence, hidden tasks, stealth triggers, or tasks that run without user awareness.

**Verification:** Verify task name, trigger, principal, action, last-run result, and visible ownership. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Disable only user-approved nonessential entries; preserve task XML and prior state for rollback. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0395` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows Startup, scheduled tasks, and background execution: Close The Target Safely. Carry out **close the target safely** for startup apps, task scheduler, login tasks, and background execution diagnosis.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `14-startup-scheduling`. **Scope:** Startup apps, Task Scheduler, login tasks, and background execution diagnosis.; **Preferred tools:** Settings Startup, Task Manager Startup, Get-ScheduledTask, Get-CimInstance Win32_StartupCommand.; **Task focus:** For **close the target safely**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not create persistence, hidden tasks, stealth triggers, or tasks that run without user awareness.; **Verification:** Verify task name, trigger, principal, action, last-run result, and visible ownership. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Graceful close with unsaved-work protection.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the exact window and inspect for unsaved work, active transfers, dialogs, or background operations. Use the application Close command or window control and handle any save/discard prompt according to the user’s explicit instruction. Do not use taskkill or End task as a routine close method.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If the app is hung, collect a minimal diagnostic and ask before force-closing. Verify only the intended window closed and unrelated work remains open. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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
