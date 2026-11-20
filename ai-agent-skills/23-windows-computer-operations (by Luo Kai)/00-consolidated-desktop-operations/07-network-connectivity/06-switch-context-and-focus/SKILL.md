---
name: "Windows Switch Context And Focus across Network and Secure Connectivity"
description: "Consolidated switch context and focus workflow across 2 Windows domains: Network and Secure Connectivity. Preserves each profile's original procedures, tools, safety rules, examples, verification, and recovery guidance."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-g07-w06"
  version: "1.2.0"
---

# Windows Switch Context And Focus across Network and Secure Connectivity

## Objective

Combine the switch context and focus workflows from 2 related Windows domains. Select only the profile that matches the user's target. Each profile retains its complete original workflow body, including task instructions, preferred tools, command examples, approval rules, verification, recovery, and completion criteria.

## When to use

Use when the user needs the switch context and focus workflow in any of these domains: Windows Wi-Fi, Ethernet, and network adapters; Windows DNS, firewall, VPN, and secure connectivity.

## Required operating discipline

- Confirm the exact device, account/session, target, and applicable domain before acting.

- Select only the relevant domain profile; do not execute every profile by default.

- Preserve each profile's native tools, platform distinctions, approval gates, and recovery rules.

- Prefer least privilege, observable actions, read-only inspection, and independent verification.

- Never bypass security controls, consent, organizational policy, or user approval.

- Do not discard or replace source procedures; use the full domain profile when a task-specific detail is needed.

## Domain profiles

### Profile 1: Windows Wi-Fi, Ethernet, and network adapters

Former domain: 21-wifi-ethernet

Former skill ID: windows-0606

#### Windows Wi-Fi, Ethernet, and network adapters: Switch Context And Focus

##### Objective

Carry out **switch context and focus** for adapter state, connection profiles, signal, ip configuration, and connectivity checks. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to switch context and focus involving wi-fi, ethernet, and network adapters. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for adapter state, connection profiles, signal, ip configuration, and connectivity checks. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, switch context and focus means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Adapter state, connection profiles, signal, IP configuration, and connectivity checks.

**Preferred tools:** Settings Network, Get-NetAdapter, Get-NetIPConfiguration, ipconfig /all, ping approved endpoint.

**Task focus:** For **switch context and focus**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not connect to unknown networks, reveal Wi-Fi passwords, or change corporate network settings.

**Verification:** Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-NetAdapter; Get-NetIPConfiguration; ipconfig /all
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Distinguish local link, gateway, DNS, and internet failure; avoid resetting the stack prematurely. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0606` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows Wi-Fi, Ethernet, and network adapters: Switch Context And Focus. Carry out **switch context and focus** for adapter state, connection profiles, signal, ip configuration, and connectivity checks. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `21-wifi-ethernet`. **Scope:** Adapter state, connection profiles, signal, IP configuration, and connectivity checks.; **Preferred tools:** Settings Network, Get-NetAdapter, Get-NetIPConfiguration, ipconfig /all, ping approved endpoint.; **Task focus:** For **switch context and focus**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not connect to unknown networks, reveal Wi-Fi passwords, or change corporate network settings.; **Verification:** Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Focus and session control.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the current foreground window, active user session, and intended destination before sending keystrokes. Use Alt+Tab, Win+Tab, taskbar selection, or an accessible window title; confirm focus after every context switch. Avoid typing into password fields or private conversations unless explicitly requested.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If focus is uncertain, stop input and re-identify the window. Verify the intended surface is foreground and no unrelated control received keystrokes. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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

### Profile 2: Windows DNS, firewall, VPN, and secure connectivity

Former domain: 22-dns-firewall-vpn

Former skill ID: windows-0636

#### Windows DNS, firewall, VPN, and secure connectivity: Switch Context And Focus

##### Objective

Carry out **switch context and focus** for name resolution, firewall profile inspection, vpn state, and secure route diagnosis. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

##### When to use

Use this skill when the user asks an agent to switch context and focus involving dns, firewall, vpn, and secure connectivity. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

##### Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

##### Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for name resolution, firewall profile inspection, vpn state, and secure route diagnosis. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, switch context and focus means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Check DNS answer, active profile, VPN connection, route, and application-specific reachability. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

##### Domain-specific guidance

**Scope:** Name resolution, firewall profile inspection, VPN state, and secure route diagnosis.

**Preferred tools:** Resolve-DnsName, Get-NetFirewallProfile, Get-NetIPConfiguration, VPN Settings UI.

**Task focus:** For **switch context and focus**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Never disable firewall, bypass VPN, expose internal routes, or weaken TLS to make a connection work.

**Verification:** Check DNS answer, active profile, VPN connection, route, and application-specific reachability. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

##### Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Resolve-DnsName example.com; Get-NetFirewallProfile; Get-NetIPConfiguration
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

##### Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Preserve security controls; collect exact errors and ask the network administrator for managed settings. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

##### Agent execution contract — v1.1

**Former skill identity (retired):** `windows-0636` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows DNS, firewall, VPN, and secure connectivity: Switch Context And Focus. Carry out **switch context and focus** for name resolution, firewall profile inspection, vpn state, and secure route diagnosis. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `22-dns-firewall-vpn`. **Scope:** Name resolution, firewall profile inspection, VPN state, and secure route diagnosis.; **Preferred tools:** Resolve-DnsName, Get-NetFirewallProfile, Get-NetIPConfiguration, VPN Settings UI.; **Task focus:** For **switch context and focus**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Never disable firewall, bypass VPN, expose internal routes, or weaken TLS to make a connection work.; **Verification:** Check DNS answer, active profile, VPN connection, route, and application-specific reachability. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

###### Execution plan

**Mode:** Focus and session control.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the current foreground window, active user session, and intended destination before sending keystrokes. Use Alt+Tab, Win+Tab, taskbar selection, or an accessible window title; confirm focus after every context switch. Avoid typing into password fields or private conversations unless explicitly requested.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If focus is uncertain, stop input and re-identify the window. Verify the intended surface is foreground and no unrelated control received keystrokes. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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
