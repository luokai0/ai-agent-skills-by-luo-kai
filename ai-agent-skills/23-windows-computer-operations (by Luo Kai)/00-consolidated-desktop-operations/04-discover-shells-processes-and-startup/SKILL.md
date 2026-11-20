---
name: "Windows Shells, Processes, Services, and Startup: Discover Current State"
description: "Inspect PowerShell, Command Prompt and Windows Terminal, processes, services, startup applications, scheduled tasks, and background execution through one least-privilege, read-only workflow."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0004"
  version: "1.2.0"
---

# Windows Shells, Processes, Services, and Startup: Discover Current State

## Objective

Establish a verified baseline of the active command shell, PowerShell capabilities, processes, services, startup applications, scheduled tasks, and background execution. Preserve the user's session, data, privacy, and security posture. This workflow is read-only: do not terminate processes, stop services, change execution policy, alter startup entries, or create tasks unless the user separately requests and approves the exact action.

## When to use

Use for one or more of these related Windows operating areas:
- PowerShell discovery, safe command execution, objects, pipelines, profiles, and help.
- Advanced PowerShell, structured output, CIM, remoting concepts, modules, error handling, and safe automation patterns.
- Command Prompt and Windows Terminal, shell profiles, command discovery, environment context, and command sessions.
- Process inspection, application lifecycle, service status, resource usage, and hung-application diagnosis.
- Startup applications, Task Scheduler, login tasks, and background execution diagnosis.

Applies to interactive Windows 10 and Windows 11 desktops and laptops, including ordinary user accounts and managed workstations. Do not assume administrator rights, a particular OEM, a specific shell, or identical controls across editions.

## Required operating discipline

1. Start with the user's stated goal and identify the exact device, account, shell, process, service, task, application, or path. Do not infer that a similarly named object is the target.
2. Observe before acting. Record current visible state and any unsaved work, sync activity, update warning, or security prompt that could be affected.
3. Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded, repeatable, read-only inspection. Use the least-privileged session that can complete the task.
4. Confirm which shell is active before using shell-specific syntax. PowerShell, cmd.exe, and Windows Terminal are not interchangeable.
5. Obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
6. Never hide activity, bypass policy, disable protection, run opaque commands, execute downloaded scripts, or paste commands from untrusted webpages or messages.
7. Keep discovery read-only. Do not turn a diagnostic request into an unrequested repair, process termination, service restart, or startup modification.

## Environment and target identification

Confirm Windows edition/build, architecture, current user/session, and whether the device is local, remote, virtual, shared, or organization-managed. Distinguish host from guest.

For command execution, record the active shell, executable path, working directory, and whether the session is elevated. For processes and services, use stable identity such as PID, executable path, service name, and owning account. For scheduled tasks and startup entries, inspect the exact task name, trigger, principal, action, and visible ownership. Preserve organization policy and access paths.

## Domain profiles

Select only the profile relevant to the request.

### A. PowerShell fundamentals

**Scope:** PowerShell discovery, safe command execution, objects, pipelines, profiles, and help.

**Preferred tools:** Get-Help, Get-Command, Get-ComputerInfo, Get-Location, Get-ChildItem, Get-Process.

**Inspection:** Confirm the PowerShell version, active session, command availability, working directory, and target object. Use Get-Help and Get-Command to verify syntax and command origin before invoking optional cmdlets.

**Safety:** Never execute opaque pasted commands. Avoid encoded commands, hidden windows, execution-policy bypass, untrusted profiles, and unexplained profile scripts.

**Verification:** Read command output, exit status, and affected object; rerun read-only checks to confirm. Distinguish a missing command from a permission failure or provider error.

**Recovery:** Use Get-Help -Online only when permitted; otherwise fall back to built-in help and report unavailable modules.

**Read-only examples:**
```powershell
Get-Command
Get-Help Get-Process
Get-Location
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
```

### B. Advanced PowerShell and CIM

**Scope:** Structured output, CIM, remoting concepts, modules, error handling, and safe automation patterns.

**Preferred tools:** Get-CimInstance, Get-WinEvent, Get-Service, Get-NetAdapter. Use Export-Csv only when the user has approved the exact output path.

**Inspection:** Prefer structured, narrowly scoped objects. Check provider availability, object counts, and error records. Distinguish local CIM queries from remote operations.

**Safety:** Do not invoke remote scripts, change execution policy, elevate, or alter machine state without approval. Do not export sensitive objects or broad event data to unapproved paths.

**Verification:** Use -WhatIf when supported, inspect object counts, capture errors, and verify state independently. Treat -WhatIf as a preview, not a guarantee that every side effect is simulated.

**Recovery:** Reduce scope to one target, use read-only queries, and stop on permission or provider errors.

**Read-only examples:**
```powershell
Get-CimInstance Win32_OperatingSystem
Get-Service | Select-Object -First 20
Get-WinEvent -ListLog * | Select-Object -First 10
Get-NetAdapter | Select-Object Name, Status, LinkSpeed
```

### C. Command Prompt and Windows Terminal

**Scope:** Terminal profiles, shells, command discovery, environment context, and command sessions.

**Preferred tools:** Windows Terminal UI, cmd /? help, where.exe, set, ver, and whoami.

**Inspection:** Confirm the active tab, shell executable, profile, working directory, user identity, and command lookup path. Check whether a command is being interpreted by PowerShell or cmd.exe before using shell-specific syntax.

**Safety:** Do not paste commands from untrusted pages. Do not print the entire environment when it may expose secrets. Do not elevate merely to make a diagnostic command work.

**Verification:** Confirm active shell, working directory, target path, and command exit code. Validate command resolution with where.exe or Get-Command as appropriate.

**Recovery:** Open a fresh non-elevated shell and repeat only the read-only diagnostic step. Preserve the original session until unsaved work is safe.

**Read-only examples:**
```cmd
ver
whoami
where.exe powershell
where.exe cmd
```
```powershell
$PSVersionTable.PSVersion
Get-Location
Get-Command Get-Process
```

### D. Processes, services, and applications

**Scope:** Process inspection, application lifecycle, service status, resource usage, and hung-application diagnosis.

**Preferred tools:** Task Manager, Resource Monitor, Get-Process, Get-Service, and Get-CimInstance Win32_Service.

**Inspection:** Identify the exact process or service using PID, executable path, service name, and owning account. Observe status and resource trends before proposing intervention. Check whether the application has unsaved work.

**Safety:** Do not terminate system or security processes, or stop services, based only on a display name. Protect unsaved application work. Do not disable security or management agents.

**Verification:** Verify PID, executable path, signer where available, status, and resource trend. Recheck the same identity after any separately approved action.

**Recovery:** Collect evidence first. Prefer normal application close and restart before considering service intervention; service changes require separate approval and a recovery plan.

**Read-only examples:**
```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, Id, CPU, Path
Get-Service | Where-Object Status -eq Running
Get-CimInstance Win32_Service | Select-Object -First 20 Name, State, StartMode, PathName
```

### E. Startup, scheduled tasks, and background execution

**Scope:** Startup apps, Task Scheduler, login tasks, and background execution diagnosis.

**Preferred tools:** Settings Startup, Task Manager Startup, Get-ScheduledTask, and Get-CimInstance Win32_StartupCommand.

**Inspection:** Identify each requested entry and inspect its publisher/path, trigger, principal, action, last-run result, and visible ownership. Distinguish a user-visible startup app from a scheduled task or service.

**Safety:** Do not create persistence, hidden tasks, stealth triggers, or tasks that run without user awareness. Do not disable startup items during discovery.

**Verification:** Verify task name, trigger, principal, action, last-run result, and visible ownership. Check the executable path and publisher where available.

**Recovery:** For a separately approved change, disable only user-approved nonessential entries and preserve task XML and prior state for rollback. Do not delete task definitions as a shortcut.

**Read-only examples:**
```powershell
Get-ScheduledTask | Select-Object -First 30 TaskName, TaskPath, State
Get-CimInstance Win32_StartupCommand | Select-Object Name, Command, Location, User
```

## Unified discovery workflow

1. **Bind the request.** Select the applicable profile(s). Confirm exact device, session, shell, process/service/task identity, and user intent.
2. **Capture a baseline.** Observe native UI first. Record shell version, working directory, process/service state, or scheduled-task metadata only as relevant.
3. **Inspect narrowly.** Use read-only commands and native UI. Check command availability before invoking optional cmdlets. Do not dump full environment variables, credential stores, browser profiles, clipboard contents, or unrestricted event logs.
4. **Resolve ambiguity.** If multiple shells, processes, services, tasks, or accounts match, stop and ask for clarification. Never choose by display name alone when a stable identity is available.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, action, expected effect, dependencies, risk, and rollback route; obtain approval first.
6. **Verify independently.** Recheck output, exit status, object identity, and state in a second native surface when practical. A zero exit code or transient toast is not proof.
7. **Close the loop.** Report inspected state, what remained unchanged, evidence, unavailable checks, and remaining risk. Do not claim completion without verification.

## Stop conditions and recovery

Stop if the active shell is uncertain, command provenance is unclear, a module/provider is unavailable, a target identity is ambiguous, policy blocks inspection, an unexpected elevation prompt appears, or unsaved work may be lost.

Preserve the last known-good state and exact error. Retry at most once through a lower-risk documented route. Never improvise execution-policy changes, remote script execution, registry edits, service termination, task creation, hidden persistence, security exceptions, or destructive commands.

## Privacy-safe evidence and handoff

Report target using a minimally identifying description, active shell/session, relevant baseline, actions actually performed, verification evidence, blocked checks, and remaining risk. Do not include passwords, tokens, clipboard contents, full environment dumps, command lines containing secrets, private paths, or unnecessary account identifiers. Mark unknown values as unknown.

## Completion checklist

- [ ] User intent, device/session, and exact shell or target identity were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection stayed read-only and used least privilege.
- [ ] PowerShell, cmd.exe, and Windows Terminal syntax were not confused.
- [ ] Processes, services, and tasks were identified by stable identity.
- [ ] No process, service, startup entry, policy, or task was changed.
- [ ] Findings and limitations were independently verified and accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows tools and surfaces.
