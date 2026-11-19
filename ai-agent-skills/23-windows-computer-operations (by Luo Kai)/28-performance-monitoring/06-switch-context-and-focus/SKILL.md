---
name: "Windows Performance and resource monitoring: Switch Context And Focus"
description: "Perform the Windows switch context and focus workflow for cpu, memory, disk, gpu, network, startup impact, and responsiveness analysis. on Windows 10 or Windows 11, using observable UI state, least privilege, and explicit verification."
license: "Proprietary. Original work by Luo Kai."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-0816"
  version: "1.1.0"
---

# Windows Performance and resource monitoring: Switch Context And Focus

## Objective

Carry out **switch context and focus** for cpu, memory, disk, gpu, network, startup impact, and responsiveness analysis.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

## When to use

Use this skill when the user asks an agent to switch context and focus involving performance and resource monitoring. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

## Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

## Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for cpu, memory, disk, gpu, network, startup impact, and responsiveness analysis.. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, switch context and focus means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** Collect baseline and repeated samples; correlate symptoms with timestamps and workload. Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

## Domain-specific guidance

**Scope:** CPU, memory, disk, GPU, network, startup impact, and responsiveness analysis.

**Preferred tools:** Task Manager, Resource Monitor, Performance Monitor, Get-Counter, Get-Process.

**Task focus:** For **switch context and focus**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** Do not install benchmark/monitoring agents or run stress tests without approval; avoid exposing process command lines containing secrets.

**Verification:** Collect baseline and repeated samples; correlate symptoms with timestamps and workload. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

## Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name,Id,CPU,WorkingSet64; Get-Counter \Processor(_Total)\% Processor Time -SampleInterval 1 -MaxSamples 3
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

## Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** Reduce load safely, close only user-approved apps, and avoid claiming a single sample proves root cause. Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

## Agent execution contract — v1.1

**Skill identity:** `windows-0816` · **Version:** `1.1.0` · **Risk:** MODERATE — interactive navigation; preserve user work and session

**Exact task:** Windows Performance and resource monitoring: Switch Context And Focus. Carry out **switch context and focus** for cpu, memory, disk, gpu, network, startup impact, and responsiveness analysis.. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

**Domain binding:** `28-performance-monitoring`. **Scope:** CPU, memory, disk, GPU, network, startup impact, and responsiveness analysis.; **Preferred tools:** Task Manager, Resource Monitor, Performance Monitor, Get-Counter, Get-Process.; **Task focus:** For **switch context and focus**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.; **Safety boundary:** Do not install benchmark/monitoring agents or run stress tests without approval; avoid exposing process command lines containing secrets.; **Verification:** Collect baseline and repeated samples; correlate symptoms with timestamps and workload. Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.; Use the domain scope and preferred tools already defined in this skill; do not substitute a similarly named Windows control or operate on another account, device, path, or process.

### Execution plan

**Mode:** Focus and session control.

1. **Bind the target.** Confirm the active device, Windows edition/build, signed-in account/session, exact application or object, and full target identity. If the machine is managed, remote, virtual, or shared, record that context and preserve its policy and access path.
2. **Capture a baseline.** Use the read-only probes and native UI already listed above. Check command availability before invoking optional cmdlets; prefer standard-user PowerShell and named accessibility controls. Record only fields relevant to this task.
3. **Apply the task method.** Identify the current foreground window, active user session, and intended destination before sending keystrokes. Use Alt+Tab, Win+Tab, taskbar selection, or an accessible window title; confirm focus after every context switch. Avoid typing into password fields or private conversations unless explicitly requested.
4. **Gate changes.** GUI interaction can affect the active user session. Confirm foreground window and unsaved work before sending input; do not close, restart, or sign out to recover a navigation issue.
5. **Verify independently.** If focus is uncertain, stop input and re-identify the window. Verify the intended surface is foreground and no unrelated control received keystrokes. Compare the result with the baseline using the same account, scope, and measurement method. A zero exit code, click response, or transient toast is not proof.

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
