---
name: "Windows Inspect Access And Permissions across Configuration, Software, and Devices"
description: "Consolidated inspect access and permissions workflow across 5 Windows domains: Configuration, Software, and Devices. Preserves each profile's original procedures, tools, safety rules, examples, verification, and recovery guidance."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-g05-w18"
  version: "1.2.0"
---

# Windows Inspect Access And Permissions across Configuration, Software, and Devices

## Objective

Combine the inspect access and permissions workflows from 5 related Windows domains. Select only the profile that matches the user's target. Each profile retains its complete original workflow body, including task instructions, preferred tools, command examples, approval rules, verification, recovery, and completion criteria.

## When to use

Use when the user needs the inspect access and permissions workflow in any of these domains: Windows Registry and Group Policy inspection; Windows Application installation and removal; Windows package managers and dependencies; Windows Update and update servicing; Windows Device Manager and hardware drivers.

## Required operating discipline

- Confirm the exact device, account/session, target, and applicable domain before acting.

- Select only the relevant domain profile; do not execute every profile by default.

- Preserve each profile's native tools, platform distinctions, approval gates, and recovery rules.

- Prefer least privilege, observable actions, read-only inspection, and independent verification.

- Never bypass security controls, consent, organizational policy, or user approval.

- Do not discard or replace source procedures; use the full domain profile when a task-specific detail is needed.

## Domain profiles

### Profile 1: Windows Registry and Group Policy inspection

**Domain profile:** 15-registry-policy


#### Windows Registry and Group Policy inspection: Inspect Access And Permissions

##### Objective

Carry out **inspect access and permissions** for registry structure, policy state, policy refresh diagnostics, and configuration provenance. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to inspect access and permissions involving registry and group policy inspection. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for registry structure, policy state, policy refresh diagnostics, and configuration provenance. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, inspect access and permissions means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Record exact hive/key/value and policy source; compare before/after only for approved changes. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Registry structure, policy state, policy refresh diagnostics, and configuration provenance.

**Preferred tools:** Registry Editor read-only, reg query, gpresult /r, gpresult /h to approved path.

**Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Never modify registry or policy as a shortcut; no security-control weakening, credential edits, or policy bypass.

**Verification:** Record exact hive/key/value and policy source; compare before/after only for approved changes. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Stop on managed-device policy; refer to the administrator instead of fighting organizational controls. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Version:** `1.1.0` · **Risk:** LOW — read-only inspection or reporting

**Exact task:** Windows Registry and Group Policy inspection: Inspect Access And Permissions. Carry out **inspect access and permissions** for registry structure, policy state, policy refresh diagnostics, and configuration provenance. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `15-registry-policy`. **Scope:** Registry structure, policy state, policy refresh diagnostics, and configuration provenance.; **Preferred tools:** Registry Editor read-only, reg query, gpresult /r, gpresult /h to approved path.; **Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Never modify registry or policy as a shortcut; no security-control weakening, credential edits, or policy bypass.; **Verification:** Record exact hive/key/value and policy source; compare before/after only for approved changes. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Least-privilege access review.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Resolve the exact object and principal, then inspect effective access and inheritance using the read-only tools in this skill. Distinguish explicit entries, inherited entries, group membership, and effective access. Do not print secrets or enumerate unrelated users.
4. **Gate changes.** Keep this run read-only unless the user separately asks for a change. Do not turn a diagnostic result into an unrequested repair.
5. **Verify independently.** Report the minimum permission facts needed to answer the request. Never grant, revoke, take ownership, or rewrite ACLs during an inspection task. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 2: Windows Application installation and removal

**Domain profile:** 16-app-installation


#### Windows Application installation and removal: Inspect Access And Permissions

##### Objective

Carry out **inspect access and permissions** for app discovery, installers, repair, updates, uninstall workflows, and app compatibility. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to inspect access and permissions involving application installation and removal. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for app discovery, installers, repair, updates, uninstall workflows, and app compatibility. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, inspect access and permissions means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify publisher, version, install source, signatures when available, and app launch. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** App discovery, installers, repair, updates, uninstall workflows, and app compatibility.

**Preferred tools:** Settings Installed apps, winget list/search/show, Get-AppxPackage (read-only).

**Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Install only user-approved software from trusted publishers; never use cracks, bundled offers, or silent unknown installers.

**Verification:** Verify publisher, version, install source, signatures when available, and app launch. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Cancel unsigned or unexpected installers; use vendor repair guidance and preserve user data. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Version:** `1.1.0` · **Risk:** LOW — read-only inspection or reporting

**Exact task:** Windows Application installation and removal: Inspect Access And Permissions. Carry out **inspect access and permissions** for app discovery, installers, repair, updates, uninstall workflows, and app compatibility. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `16-app-installation`. **Scope:** App discovery, installers, repair, updates, uninstall workflows, and app compatibility.; **Preferred tools:** Settings Installed apps, winget list/search/show, Get-AppxPackage (read-only).; **Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Install only user-approved software from trusted publishers; never use cracks, bundled offers, or silent unknown installers.; **Verification:** Verify publisher, version, install source, signatures when available, and app launch. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Least-privilege access review.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Resolve the exact object and principal, then inspect effective access and inheritance using the read-only tools in this skill. Distinguish explicit entries, inherited entries, group membership, and effective access. Do not print secrets or enumerate unrelated users.
4. **Gate changes.** Keep this run read-only unless the user separately asks for a change. Do not turn a diagnostic result into an unrequested repair.
5. **Verify independently.** Report the minimum permission facts needed to answer the request. Never grant, revoke, take ownership, or rewrite ACLs during an inspection task. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 3: Windows package managers and dependencies

**Domain profile:** 17-package-management


#### Windows package managers and dependencies: Inspect Access And Permissions

##### Objective

Carry out **inspect access and permissions** for winget, microsoft store, package sources, app dependencies, and package inventory. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to inspect access and permissions involving windows package managers and dependencies. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for winget, microsoft store, package sources, app dependencies, and package inventory. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, inspect access and permissions means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Check package ID, publisher, version, source, and post-install inventory. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** winget, Microsoft Store, package sources, app dependencies, and package inventory.

**Preferred tools:** winget --info, winget list, winget search, winget show; Store UI.

**Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not add arbitrary package sources or accept package agreements on behalf of the user without authorization.

**Verification:** Check package ID, publisher, version, source, and post-install inventory. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Refresh source metadata once; if identity is ambiguous, do not install. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Version:** `1.1.0` · **Risk:** LOW — read-only inspection or reporting

**Exact task:** Windows package managers and dependencies: Inspect Access And Permissions. Carry out **inspect access and permissions** for winget, microsoft store, package sources, app dependencies, and package inventory. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `17-package-management`. **Scope:** winget, Microsoft Store, package sources, app dependencies, and package inventory.; **Preferred tools:** winget --info, winget list, winget search, winget show; Store UI.; **Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not add arbitrary package sources or accept package agreements on behalf of the user without authorization.; **Verification:** Check package ID, publisher, version, source, and post-install inventory. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Least-privilege access review.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Resolve the exact object and principal, then inspect effective access and inheritance using the read-only tools in this skill. Distinguish explicit entries, inherited entries, group membership, and effective access. Do not print secrets or enumerate unrelated users.
4. **Gate changes.** Keep this run read-only unless the user separately asks for a change. Do not turn a diagnostic result into an unrequested repair.
5. **Verify independently.** Report the minimum permission facts needed to answer the request. Never grant, revoke, take ownership, or rewrite ACLs during an inspection task. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 4: Windows Update and update servicing

**Domain profile:** 18-windows-updates


#### Windows Update and update servicing: Inspect Access And Permissions

##### Objective

Carry out **inspect access and permissions** for update status, history, optional updates, restart planning, and update failure diagnosis. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to inspect access and permissions involving windows update and update servicing. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for update status, history, optional updates, restart planning, and update failure diagnosis. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, inspect access and permissions means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Confirm KB/version, update history, pending restart, and successful post-reboot health. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Update status, history, optional updates, restart planning, and update failure diagnosis.

**Preferred tools:** Settings Windows Update, Get-HotFix, Get-ComputerInfo, Event Viewer.

**Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Never force reboot during active work; do not disable update services or install untrusted update packages.

**Verification:** Confirm KB/version, update history, pending restart, and successful post-reboot health. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10; Get-ComputerInfo | Select-Object WindowsVersion,OsBuildNumber
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Capture error code and event details; use built-in troubleshooter before any servicing repair. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Version:** `1.1.0` · **Risk:** LOW — read-only inspection or reporting

**Exact task:** Windows Update and update servicing: Inspect Access And Permissions. Carry out **inspect access and permissions** for update status, history, optional updates, restart planning, and update failure diagnosis. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `18-windows-updates`. **Scope:** Update status, history, optional updates, restart planning, and update failure diagnosis.; **Preferred tools:** Settings Windows Update, Get-HotFix, Get-ComputerInfo, Event Viewer.; **Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Never force reboot during active work; do not disable update services or install untrusted update packages.; **Verification:** Confirm KB/version, update history, pending restart, and successful post-reboot health. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Least-privilege access review.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Resolve the exact object and principal, then inspect effective access and inheritance using the read-only tools in this skill. Distinguish explicit entries, inherited entries, group membership, and effective access. Do not print secrets or enumerate unrelated users.
4. **Gate changes.** Keep this run read-only unless the user separately asks for a change. Do not turn a diagnostic result into an unrequested repair.
5. **Verify independently.** Report the minimum permission facts needed to answer the request. Never grant, revoke, take ownership, or rewrite ACLs during an inspection task. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 5: Windows Device Manager and hardware drivers

**Domain profile:** 19-devices-drivers


#### Windows Device Manager and hardware drivers: Inspect Access And Permissions

##### Objective

Carry out **inspect access and permissions** for pnp devices, driver versions, hardware ids, device status, and safe driver troubleshooting. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to inspect access and permissions involving device manager and hardware drivers. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for pnp devices, driver versions, hardware ids, device status, and safe driver troubleshooting. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, inspect access and permissions means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify hardware ID, provider, version, signer, device status, and restart effect. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** PnP devices, driver versions, hardware IDs, device status, and safe driver troubleshooting.

**Preferred tools:** Device Manager, Get-PnpDevice, Get-CimInstance Win32_PnPSignedDriver.

**Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not install unsigned drivers, disable security devices, or remove a device package without rollback plan.

**Verification:** Verify hardware ID, provider, version, signer, device status, and restart effect. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-PnpDevice -PresentOnly | Select-Object -First 30; Get-CimInstance Win32_PnPSignedDriver | Select-Object -First 10 DeviceName,DriverVersion,DriverProviderName
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Use Windows Update or OEM support; preserve current driver details before approved rollback. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Version:** `1.1.0` · **Risk:** LOW — read-only inspection or reporting

**Exact task:** Windows Device Manager and hardware drivers: Inspect Access And Permissions. Carry out **inspect access and permissions** for pnp devices, driver versions, hardware ids, device status, and safe driver troubleshooting. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `19-devices-drivers`. **Scope:** PnP devices, driver versions, hardware IDs, device status, and safe driver troubleshooting.; **Preferred tools:** Device Manager, Get-PnpDevice, Get-CimInstance Win32_PnPSignedDriver.; **Task focus:** For **inspect access and permissions**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not install unsigned drivers, disable security devices, or remove a device package without rollback plan.; **Verification:** Verify hardware ID, provider, version, signer, device status, and restart effect. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Least-privilege access review.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Resolve the exact object and principal, then inspect effective access and inheritance using the read-only tools in this skill. Distinguish explicit entries, inherited entries, group membership, and effective access. Do not print secrets or enumerate unrelated users.
4. **Gate changes.** Keep this run read-only unless the user separately asks for a change. Do not turn a diagnostic result into an unrequested repair.
5. **Verify independently.** Report the minimum permission facts needed to answer the request. Never grant, revoke, take ownership, or rewrite ACLs during an inspection task. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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
