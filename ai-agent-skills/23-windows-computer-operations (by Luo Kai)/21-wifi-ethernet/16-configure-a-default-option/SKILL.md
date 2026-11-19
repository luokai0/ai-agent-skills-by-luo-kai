---
name: "Windows Wi-Fi, Ethernet, and network adapters: Configure A Default Option"
description: "Perform the Windows configure a default option workflow for adapter state, connection profiles, signal, ip configuration, and connectivity checks. on Windows 10 or Windows 11, using observable UI state, least privilege, and explicit verification."
license: "Proprietary. Original work by Luo Kai."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-0616"
  version: "1.1.0"
---

# Windows Wi-Fi, Ethernet, and network adapters: Configure A Default Option

## Objective

Carry out **configure a default option** for adapter state, connection profiles, signal, ip configuration, and connectivity checks.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

## When to use

Use this skill when the user asks an agent to configure a default option involving wi-fi, ethernet, and network adapters. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

## Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

## Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for adapter state, connection profiles, signal, ip configuration, and connectivity checks.. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, configure a default option means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

## Domain-specific guidance

**Scope:** Adapter state, connection profiles, signal, IP configuration, and connectivity checks.

**Preferred tools:** Settings Network, Get-NetAdapter, Get-NetIPConfiguration, ipconfig /all, ping approved endpoint.

**Task focus:** For **configure a default option**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not connect to unknown networks, reveal Wi-Fi passwords, or change corporate network settings.

**Verification:** Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

## Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-NetAdapter; Get-NetIPConfiguration; ipconfig /all
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

## Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Distinguish local link, gateway, DNS, and internet failure; avoid resetting the stack prematurely. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

## Agent execution contract — v1.1

**Skill identity:** `windows-0616` · **Version:** `1.1.0` · **Risk:** HIGH — state-changing; explicit approval required

**Exact task:** Windows Wi-Fi, Ethernet, and network adapters: Configure A Default Option. Carry out **configure a default option** for adapter state, connection profiles, signal, ip configuration, and connectivity checks.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `21-wifi-ethernet`. **Scope:** Adapter state, connection profiles, signal, IP configuration, and connectivity checks.; **Preferred tools:** Settings Network, Get-NetAdapter, Get-NetIPConfiguration, ipconfig /all, ping approved endpoint.; **Task focus:** For **configure a default option**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not connect to unknown networks, reveal Wi-Fi passwords, or change corporate network settings.; **Verification:** Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

### Execution plan

**Mode:** Scoped default configuration.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify whether the default is per-user, per-application, per-file type, or device-wide. Record the current value and the exact requested replacement; inspect policy and dependencies first. Obtain approval before changing the default because it may affect future actions beyond the current task.
4. **Gate changes.** Do not apply a change until the exact target, intended result, impact, and recovery path are stated and the user approves that specific action. Approval for one change does not authorize adjacent cleanup, reboot, or broader automation.
5. **Verify independently.** Change one setting through the supported UI/API, then test with a harmless sample. Verify the new default and retain the previous value for rollback. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

### Stop conditions and recovery

Stop if target identity is ambiguous, a command is unavailable and no documented fallback exists, policy blocks the control, unsaved work may be lost, the device becomes unstable, or the observed state differs from the expected state. Preserve the last known-good state and exact error. Retry at most once through a lower-risk documented route; never improvise registry edits, service termination, driver changes, security exceptions, reset, or permanent deletion.

### Evidence and handoff

Report: **target** (redacted identifier), **baseline**, **actions actually taken**, **before/after state**, **verification evidence**, **blocked steps**, and **remaining risk**. Do not include passwords, tokens, clipboard contents, notification text, browser profile data, private document names, or unrelated personal paths. Mark unknown values as unknown instead of guessing.

## Completion checklist

- [ ] The exact target and user intent were confirmed.
- [ ] No unrelated files, windows, settings, accounts, or devices were changed.
- [ ] Any consequential step had explicit approval and a recoverable plan where possible.
- [ ] The resulting state was independently verified.
- [ ] Limitations, remaining risks, and the evidence used were reported accurately.

---

*Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Windows and third-party product names are used descriptively; their respective owners retain their rights.*
