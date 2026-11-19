#!/usr/bin/env python3
"""Generate the original 1,200-skill Windows computer-operations collection.

Run: python scripts/maintenance/generate_windows_skill_pack.py
Use --force only when intentionally replacing existing skill files.
"""
import os, re, json, textwrap, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CAT='ai-agent-skills/23-windows-computer-operations (by Luo Kai)'
# Each domain supplies concrete scope, safe tools, non-negotiable hazards, verification evidence, and recovery route.
D=[
('desktop-shell','Windows desktop shell','Desktop, Explorer shell, desktop icons, notification area, and shell processes.','UI Automation, keyboard navigation, Task Manager; read-only Get-Process and Get-ComputerInfo.','Do not kill explorer.exe or reset the shell as a first response; unsaved shell dialogs and file operations may be active.','Confirm the desktop remains responsive, focus is visible, and no user window was lost.','Retry with a different navigation route; preserve the session and report shell instability.'),
('windows-navigation','Windows navigation and settings','Settings app, Control Panel, system pages, navigation paths, and search surfaces.','Start search, Settings URI navigation where supported, Control Panel applets, Get-ComputerInfo.','Do not change system-wide settings without a clear request; distinguish viewing a setting from changing it.','Reopen the target page and confirm the displayed value or page identity.','Use the Settings search box or Control Panel equivalent; do not guess hidden URI schemes.'),
('window-multitasking','Window management and multitasking','Window focus, snapping, virtual desktops, task switching, and multi-monitor window placement.','Win+Arrow shortcuts, Alt+Tab, Task View, UI Automation window patterns.','Avoid closing windows to solve focus problems; preserve unsaved work and do not move windows off-screen.','Verify active window, bounds, monitor, and user-visible layout after each action.','Use Task View and keyboard navigation; restore window placement before escalating.'),
('start-taskbar','Start menu, taskbar, and notifications','Start menu, pinned apps, taskbar controls, quick settings, system tray, and notifications.','Start search, taskbar UI Automation, Settings, read-only Get-Process.','Do not unpin, uninstall, or disable startup items unless asked; do not dismiss security alerts without reading them.','Verify the intended app or panel opened and the taskbar remains usable.','Use Start search or Settings directly; preserve notification details for troubleshooting.'),
('file-explorer','File Explorer navigation','Explorer windows, locations, navigation pane, address bar, libraries, and views.','File Explorer UI, address bar, shell namespace; read-only Get-ChildItem and Get-Item.','Confirm full paths; distinguish local, removable, network, cloud-synced, and virtual locations.','Check the address bar path and inspect a representative item before acting.','Use a known folder path or This PC; do not assume a displayed cloud placeholder is local.'),
('file-operations','File and folder operations','Create, copy, move, rename, organize, and safely remove files and folders.','Explorer UI first; read-only Test-Path, Get-Item, Get-FileHash, Get-ChildItem.','Never overwrite, permanently delete, or move large trees without explicit approval and a collision check.','Compare source/destination paths, item counts, sizes, timestamps, and hashes when appropriate.','Stop on conflicts; preserve originals and use Recycle Bin for approved recoverable deletion.'),
('search-metadata','Windows search and file metadata','Search indexing, filters, metadata, file properties, and content discovery.','Explorer search, Windows Search UI, Get-Item, Get-ChildItem, Get-FileHash.','Search results may be stale or incomplete; do not expose private filenames or content in reports unnecessarily.','Open the result and validate its actual path, date, and file identity.','Use a narrower path and extension filter; check indexing status before concluding an item is absent.'),
('archives-transfer','Archives, downloads, and file transfer','ZIP archives, downloads, removable media, and safe local file transfers.','Explorer archive UI, Get-FileHash, Get-Item, Get-Volume.','Treat downloaded archives as untrusted; do not run included executables, macros, shortcuts, or scripts.','Inspect archive listing, destination, extracted file types, and hashes for critical transfers.','Quarantine suspicious content, preserve the archive, and report provenance rather than executing it.'),
('storage-volumes','Storage, partitions, and volumes','Disk space, volumes, removable storage, filesystem health indicators, and storage settings.','Settings Storage, Disk Management for viewing, Get-Volume, Get-PSDrive, Get-Disk (read-only).','Do not initialize, format, partition, clean, or repair-write disks without explicit informed approval and backup.','Confirm disk identity, capacity, free space, filesystem, and drive letter before any approved change.','Stop if disk identity is ambiguous or health is failing; preserve data and recommend backup/professional recovery.'),
('powershell-fundamentals','PowerShell fundamentals','PowerShell discovery, safe command execution, objects, pipelines, profiles, and help.','Get-Help, Get-Command, Get-ComputerInfo, Get-Location, Get-ChildItem, Get-Process.','Never execute opaque pasted commands; avoid encoded commands, hidden windows, execution-policy bypass, and untrusted profiles.','Read command output, exit status, and affected object; rerun read-only checks to confirm.','Use Get-Help -Online only when permitted; fall back to built-in help and explain unavailable modules.'),
('powershell-advanced','Advanced PowerShell administration','Structured output, CIM, remoting concepts, modules, error handling, and safe automation patterns.','Get-CimInstance, Get-WinEvent, Get-Service, Get-NetAdapter, Export-Csv only to approved paths.','Do not invoke remote scripts, change execution policy, elevate, or alter machine state without approval.','Use -WhatIf when supported, inspect object counts, capture errors, and verify state independently.','Reduce scope to one target, use read-only queries, and stop on permission or provider errors.'),
('terminal-cmd','Command Prompt and Windows Terminal','Terminal profiles, shells, command discovery, environment variables, and command sessions.','Windows Terminal UI, cmd /? help, where.exe, set, ver, whoami.','Do not paste commands from untrusted pages; distinguish PowerShell syntax from cmd.exe syntax.','Confirm active shell, working directory, target path, and command exit code.','Open a fresh non-elevated shell and repeat only the read-only diagnostic step.'),
('process-services','Processes, services, and applications','Process inspection, app lifecycle, service status, resource usage, and hung-app diagnosis.','Task Manager, Resource Monitor, Get-Process, Get-Service, Get-CimInstance Win32_Service.','Do not terminate system/security processes or stop services based only on name; protect unsaved app work.','Verify PID, executable path, signer where available, status, and resource trend.','Collect evidence first; use normal app close and restart before considering service intervention.'),
('startup-scheduling','Startup, scheduled tasks, and background execution','Startup apps, Task Scheduler, login tasks, and background execution diagnosis.','Settings Startup, Task Manager Startup, Get-ScheduledTask, Get-CimInstance Win32_StartupCommand.','Do not create persistence, hidden tasks, stealth triggers, or tasks that run without user awareness.','Verify task name, trigger, principal, action, last-run result, and visible ownership.','Disable only user-approved nonessential entries; preserve task XML and prior state for rollback.'),
('registry-policy','Registry and Group Policy inspection','Registry structure, policy state, policy refresh diagnostics, and configuration provenance.','Registry Editor read-only, reg query, gpresult /r, gpresult /h to approved path.','Never modify registry or policy as a shortcut; no security-control weakening, credential edits, or policy bypass.','Record exact hive/key/value and policy source; compare before/after only for approved changes.','Stop on managed-device policy; refer to the administrator instead of fighting organizational controls.'),
('app-installation','Application installation and removal','App discovery, installers, repair, updates, uninstall workflows, and app compatibility.','Settings Installed apps, winget list/search/show, Get-AppxPackage (read-only).','Install only user-approved software from trusted publishers; never use cracks, bundled offers, or silent unknown installers.','Verify publisher, version, install source, signatures when available, and app launch.','Cancel unsigned or unexpected installers; use vendor repair guidance and preserve user data.'),
('package-management','Windows package managers and dependencies','winget, Microsoft Store, package sources, app dependencies, and package inventory.','winget --info, winget list, winget search, winget show; Store UI.','Do not add arbitrary package sources or accept package agreements on behalf of the user without authorization.','Check package ID, publisher, version, source, and post-install inventory.','Refresh source metadata once; if identity is ambiguous, do not install.'),
('windows-updates','Windows Update and update servicing','Update status, history, optional updates, restart planning, and update failure diagnosis.','Settings Windows Update, Get-HotFix, Get-ComputerInfo, Event Viewer.','Never force reboot during active work; do not disable update services or install untrusted update packages.','Confirm KB/version, update history, pending restart, and successful post-reboot health.','Capture error code and event details; use built-in troubleshooter before any servicing repair.'),
('devices-drivers','Device Manager and hardware drivers','PnP devices, driver versions, hardware IDs, device status, and safe driver troubleshooting.','Device Manager, Get-PnpDevice, Get-CimInstance Win32_PnPSignedDriver.','Do not install unsigned drivers, disable security devices, or remove a device package without rollback plan.','Verify hardware ID, provider, version, signer, device status, and restart effect.','Use Windows Update or OEM support; preserve current driver details before approved rollback.'),
('display-audio-input','Displays, audio, cameras, and input devices','Display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices.','Settings Display/Sound, Get-CimInstance, Device Manager, built-in test panels.','Respect camera/microphone privacy indicators; do not activate sensors or record people without consent.','Run a visible test, verify selected device, levels, resolution, refresh rate, and monitor order.','Return to the previous working device/display configuration and test one variable at a time.'),
('wifi-ethernet','Wi-Fi, Ethernet, and network adapters','Adapter state, connection profiles, signal, IP configuration, and connectivity checks.','Settings Network, Get-NetAdapter, Get-NetIPConfiguration, ipconfig /all, ping approved endpoint.','Do not connect to unknown networks, reveal Wi-Fi passwords, or change corporate network settings.','Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately.','Distinguish local link, gateway, DNS, and internet failure; avoid resetting the stack prematurely.'),
('dns-firewall-vpn','DNS, firewall, VPN, and secure connectivity','Name resolution, firewall profile inspection, VPN state, and secure route diagnosis.','Resolve-DnsName, Get-NetFirewallProfile, Get-NetIPConfiguration, VPN Settings UI.','Never disable firewall, bypass VPN, expose internal routes, or weaken TLS to make a connection work.','Check DNS answer, active profile, VPN connection, route, and application-specific reachability.','Preserve security controls; collect exact errors and ask the network administrator for managed settings.'),
('browser-webapps','Browsers, web apps, and downloads','Browser tabs, profiles, downloads, permissions, web app sessions, and browser troubleshooting.','Browser UI, built-in task manager, download history, site permission panels.','Never reveal passwords, session cookies, recovery codes, or private tabs; do not install unknown extensions.','Verify domain, profile, tab, permission, download origin, and final page state.','Use a clean tab or supported private session only when appropriate; preserve the user’s existing session.'),
('office-productivity','Office and productivity applications','Documents, spreadsheets, presentations, mail clients, calendars, and collaboration tools.','Native application UI, accessibility tree, file properties, autosave/version history.','Do not send, share, delete, or overwrite documents or messages without explicit confirmation.','Verify file identity, recipient, sharing scope, save status, and version history.','Recover from autosave/version history; do not claim a send or save succeeded without visible confirmation.'),
('developer-workstations','Developer workstation setup','Editors, SDKs, compilers, runtimes, environment variables, and local development setup.','Get-Command, where.exe, dotnet --info, python --version, node --version, code --version.','Avoid PATH-wide edits, untrusted extensions, arbitrary install scripts, and exposing environment secrets.','Check executable path, version, architecture, project-local config, and reproducible build result.','Prefer project-local environments and reversible settings; capture exact toolchain diagnostics.'),
('git-source-control','Git and source-control operations','Repository discovery, status, branches, diffs, commits, remotes, and conflict resolution.','git status, git remote -v, git diff --check, git log --oneline, Git GUI.','Never force-push, rewrite shared history, discard work, or expose tokens; inspect status before every mutation.','Verify branch, clean/expected diff, commit hash, remote, and pushed state.','Stash or back up only with approval; preserve uncommitted changes and resolve conflicts explicitly.'),
('wsl-virtualization','WSL, virtual machines, and containers','WSL distributions, Hyper-V/virtualization status, VM lifecycle, and container tooling.','wsl --status, wsl --list --verbose, systeminfo, virtualization settings, Docker/Podman UI.','Do not delete distributions, VM disks, containers, or volumes without explicit confirmation and backup.','Verify distro/VM identity, resource allocation, network mode, and guest health.','Export or snapshot before approved destructive maintenance; distinguish host and guest paths.'),
('performance-monitoring','Performance and resource monitoring','CPU, memory, disk, GPU, network, startup impact, and responsiveness analysis.','Task Manager, Resource Monitor, Performance Monitor, Get-Counter, Get-Process.','Do not install benchmark/monitoring agents or run stress tests without approval; avoid exposing process command lines containing secrets.','Collect baseline and repeated samples; correlate symptoms with timestamps and workload.','Reduce load safely, close only user-approved apps, and avoid claiming a single sample proves root cause.'),
('battery-thermal-power','Laptop battery, thermals, and power management','Battery health, charging, power plans, sleep, thermal symptoms, docks, and mobility.','Settings Power & Battery, powercfg /batteryreport, powercfg /energy, Get-CimInstance battery.','Never obstruct vents, force firmware changes, or disable thermal protection; do not change sleep behavior without consent.','Verify AC/battery state, charge rate, battery report, temperatures from trusted OEM tools, and sleep behavior.','Disconnect suspect peripherals, cool the device naturally, and recommend OEM service for swelling or abnormal heat.'),
('logs-diagnostics','Event logs and Windows troubleshooting','Event Viewer, reliability history, crash records, error codes, and diagnostic evidence.','Get-WinEvent with narrow filters, Event Viewer, Reliability Monitor, Problem Reports.','Logs can contain usernames, paths, IPs, and document names; redact before sharing.','Match event time, provider, ID, level, and reproduction window; distinguish correlation from cause.','Export only relevant time-bounded events to an approved location; avoid broad log dumps.'),
('security-defender','Windows security and Microsoft Defender','Defender status, firewall posture, SmartScreen, protection history, and safe threat response.','Windows Security UI, Get-MpComputerStatus, Get-MpThreatDetection, Get-NetFirewallProfile.','Never disable Defender, tamper protection, firewall, SmartScreen, or quarantine; do not restore detections casually.','Verify protection state, detection name, source, timestamp, action, and current remediation status.','Isolate only using approved controls; preserve evidence and escalate suspected compromise.'),
('privacy-permissions','Privacy, permissions, and account access','App permissions, local accounts, sign-in options, sharing, and privacy controls.','Settings Privacy & Security, Settings Accounts, whoami, Get-LocalUser (read-only).','Never collect or reveal passwords, PINs, tokens, biometric data, or recovery codes; no account lockout or bypass.','Verify exact account and app, scope of permission, effective access, and user intent.','Restore previous permissions if an app breaks; refer managed-account changes to the administrator.'),
('accessibility','Accessibility and assistive technology','Narrator, Magnifier, captions, contrast, keyboard access, voice access, and input assistance.','Settings Accessibility, Narrator, Magnifier, UI Automation, on-screen keyboard.','Do not change assistive settings without consent; never assume a user’s disability or preferred modality.','Ask/observe the requested modality, test focus order, speech/caption output, and reversibility.','Use keyboard-only navigation or restore the previous setting; preserve user’s established accessibility setup.'),
('remote-desktop','Remote access and support sessions','Remote Desktop, Quick Assist, remote support, session handoff, and connectivity.','Windows Remote Desktop UI, Quick Assist, Get-NetTCPConnection (read-only).','No covert remote access, unattended persistence, credential sharing, or enabling remote access without explicit consent.','Verify endpoint identity, session owner, encryption/organization policy, visible consent, and disconnect path.','Stop if identity or consent is unclear; end the session visibly and preserve local access.'),
('ui-automation','Reliable Windows UI automation','UI Automation trees, selectors, focus, keyboard/mouse actions, waits, and resilient workflows.','Supported UIA framework, accessibility tree, screenshots, keyboard shortcuts, app-native APIs.','No hidden clicks, security prompt bypass, CAPTCHA circumvention, or actions that conceal activity.','Assert control identity, enabled state, focus, expected text/value, and post-action screen state.','Reacquire controls after layout changes; stop rather than clicking by stale coordinates.'),
('screenshots-ocr','Screenshots, screen reading, and OCR','Screen capture, OCR, visual grounding, region selection, and evidence handling.','Approved screenshot API, Snipping Tool, Windows OCR, UI Automation names.','Capture only relevant windows; redact secrets and personal content; do not record without permission.','Compare OCR with visible source and use UIA for ambiguous labels or values.','Retake a focused crop at readable scale; report uncertainty rather than inventing text.'),
('clipboard-input','Clipboard, text entry, and input reliability','Clipboard inspection, paste, keyboard layouts, IME, text entry, and form interactions.','Clipboard UI, keyboard layout settings, UI Automation ValuePattern, Notepad test.','Clipboard may contain passwords or private data; never dump it wholesale or overwrite it silently.','Verify a harmless sample, target field, character encoding, and final text before submission.','Use direct typing for sensitive fields and restore clipboard only if the original value was safely retained with consent.'),
('printers-peripherals','Printers, scanners, docks, and peripherals','Printer queues, scanner discovery, USB devices, Bluetooth, docks, and peripheral troubleshooting.','Settings Bluetooth & devices, Get-Printer, Get-PrinterQueue, Device Manager.','Do not print confidential material, clear queues, pair unknown devices, or install vendor utilities without approval.','Verify device identity, driver, queue, selected destination, and a non-sensitive test result.','Check connection and queue status first; preserve pending jobs and ask before clearing them.'),
('backup-recovery','Backup, restore, and recovery','File History, OneDrive sync, restore points, recovery environment, and restore planning.','Settings Backup, File History UI, wbadmin get versions (read-only), recovery options.','Never initiate reset, reinstall, restore, disk repair, or overwrite recovery media without explicit informed approval.','Verify backup timestamp, scope, destination, integrity, and restore point before relying on it.','Stop if backup is missing or stale; preserve the current disk and explain recovery choices.'),
('provisioning-accounts','Windows provisioning and account lifecycle','Initial setup, local profiles, device naming, enrollment indicators, and handoff readiness.','Settings System/About, Settings Accounts, dsregcmd /status (read-only), whoami.','Do not bypass enrollment, remove management, create hidden accounts, or alter ownership/activation state.','Verify device identity, account owner, enrollment state, update status, and setup completion.','Pause on organization-owned or enrolled devices and hand off to authorized IT administrators.')]
A=['discover current state','inspect configuration','check health and readiness','open the target surface','close the target safely','switch context and focus','search for a target','filter and narrow results','sort and prioritize results','create a new item','rename an existing item','move an item safely','copy an item safely','remove an item with recovery protection','restore a prior item','configure a default option','change a user preference','inspect access and permissions','inspect dependencies and prerequisites','check compatibility and version support','diagnose a common failure','collect minimal diagnostic evidence','recover from a reversible failure','automate a repeatable workflow','validate an automation workflow','monitor ongoing state','document a configuration or action','compare before and after state','perform routine maintenance','hand off a verified outcome']
# Domain-specific PowerShell read-only probes, selected by domain family.
CMD={
'powershell-fundamentals':'Get-Command; Get-Help Get-Process; Get-Location; Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture',
'powershell-advanced':'Get-CimInstance Win32_OperatingSystem; Get-Service | Select-Object -First 20; Get-WinEvent -ListLog * | Select-Object -First 10',
'process-services':'Get-Process | Sort-Object CPU -Descending | Select-Object -First 10; Get-Service | Where-Object Status -eq Running',
'storage-volumes':'Get-Volume | Select-Object DriveLetter,FileSystemLabel,FileSystem,Size,SizeRemaining,HealthStatus; Get-PSDrive -PSProvider FileSystem',
'wifi-ethernet':'Get-NetAdapter; Get-NetIPConfiguration; ipconfig /all',
'dns-firewall-vpn':'Resolve-DnsName example.com; Get-NetFirewallProfile; Get-NetIPConfiguration',
'devices-drivers':'Get-PnpDevice -PresentOnly | Select-Object -First 30; Get-CimInstance Win32_PnPSignedDriver | Select-Object -First 10 DeviceName,DriverVersion,DriverProviderName',
'windows-updates':'Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10; Get-ComputerInfo | Select-Object WindowsVersion,OsBuildNumber',
'security-defender':'Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled,AntispywareEnabled; Get-NetFirewallProfile',
'battery-thermal-power':'powercfg /batteryreport /output "$env:TEMP\\battery-report.html"; powercfg /getactivescheme',
'logs-diagnostics':'Get-WinEvent -LogName System -MaxEvents 20 | Select-Object TimeCreated,Id,LevelDisplayName,ProviderName',
'git-source-control':'git status --short --branch; git diff --check; git log -5 --oneline',
'wsl-virtualization':'wsl --status; wsl --list --verbose; systeminfo',
'developer-workstations':'Get-Command python,node,dotnet,git -ErrorAction SilentlyContinue | Select-Object Name,Source; python --version; node --version; dotnet --info',
'printers-peripherals':'Get-Printer | Select-Object Name,DriverName,PortName,PrinterStatus; Get-PrinterQueue -ErrorAction SilentlyContinue',
'provisioning-accounts':'whoami; Get-ComputerInfo | Select-Object CsName,WindowsProductName,OsBuildNumber; dsregcmd /status',
'performance-monitoring':'Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name,Id,CPU,WorkingSet64; Get-Counter \\Processor(_Total)\\% Processor Time -SampleInterval 1 -MaxSamples 3'}

def slug(s):
 s=s.lower().replace('&','and').replace('/','-').replace(' ','-')
 s=re.sub(r'[^a-z0-9-]+','',s); return re.sub(r'-+','-',s).strip('-')

def make_skill(idx, domain, action, n):
 key,title,scope,tools,hazards,checks,recovery=domain
 name=f'Windows {title}: {action.title()}'
 desc=f'Perform the Windows {action} workflow for {scope.lower()} on Windows 10 or Windows 11, using observable UI state, least privilege, and explicit verification.'
 cmd=CMD.get(key,'Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsArchitecture; Get-Process | Select-Object -First 10 Name,Id; Get-ChildItem -LiteralPath $env:USERPROFILE -Force | Select-Object -First 10 Name,Mode,Length')
 task=action.capitalize()
 return f'''---
name: "{name}"
description: "{desc}"
license: "Proprietary. Original work by Luo Kai."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-{idx:04d}"
  version: "1.0.0"
---

# {name}

## Objective

Carry out **{task.lower()}** for {scope.lower()}. Treat the machine as a real user's working environment: preserve their session, data, privacy, and security posture. The target outcome is a verified state, not merely a successful click or a command that returned without an obvious error.

## When to use

Use this skill when the user asks an agent to {task.lower()} involving {title.lower()}. It is designed for interactive Windows 10/11 desktops and laptops, including ordinary user accounts and managed workstations. It does not assume administrator rights, a particular OEM, a specific shell, or that every Windows edition exposes identical controls.

## Required operating discipline

- Start with the user's stated goal and identify the exact device, account, app, path, adapter, or setting involved. Do not infer that a similarly named object is the target.
- Observe before acting. Record the current visible state and any unsaved-work, sync, update, or security warning that could be affected.
- Prefer native Windows UI and supported accessibility/UI Automation controls for GUI work. Use PowerShell for bounded inspection and repeatable checks. Use the least-privileged session that can complete the task.
- Explain and obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
- Make one small change at a time. Never hide activity, bypass policy, disable protection, or run opaque commands from webpages, downloads, chat messages, or unknown scripts.

## Workflow

1. **Identify the environment.** Confirm Windows edition/build, architecture, interactive session, current user, and whether the device appears organization-managed. If the machine is remote or virtual, distinguish host from guest.
2. **Locate the exact target.** Use the relevant Windows surface for {scope.lower()}. Confirm its full identity (for example path, process ID, device hardware ID, profile, or package ID) before interacting.
3. **Plan the smallest safe action.** For this request, {task.lower()} means changing or inspecting only the target required to satisfy the user. Prefer reversible UI actions and read-only diagnostics first.
4. **Execute visibly.** Use the controls and commands listed below only when relevant. Keep the user informed before a consequential step. Do not retry a failed mutation blindly.
5. **Verify independently.** {checks} Re-open the relevant page or query the resulting state instead of trusting a transient toast or a click response.
6. **Close the loop.** Report what was inspected, what changed, what did not change, evidence of success, and any unresolved limitation. Do not claim completion without verification.

## Domain-specific guidance

**Scope:** {scope}

**Preferred tools:** {tools}

**Task focus:** For **{task.lower()}**, first establish the current state and exact target. Choose the native control that exposes the relevant property; avoid coordinate-only interaction if a stable UI Automation name, keyboard shortcut, or application-native command is available. If the target is not present, report that fact and check one reasonable alternate location rather than creating a substitute without permission.

**Safety boundary:** {hazards}

**Verification:** {checks} Capture only the minimum evidence needed, and redact account names, private paths, IP addresses, document titles, and other personal information from any external report.

## Safe diagnostic commands

These examples are read-oriented probes, not a requirement to use a terminal for every task:

```powershell
{cmd}
```

Run only commands appropriate to the current shell and Windows version. Check command availability with `Get-Command` first. Do not add `-Force`, wildcard targets, elevation, remote execution, or write operations merely to make a command succeed. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, or full event logs.

## Failure handling and recovery

If the action fails, stop and preserve the current state. Capture the exact error text and a narrow timestamped diagnostic. Recheck the target identity and permissions, then try one lower-risk alternate path. **Recovery route:** {recovery} Never improvise a registry edit, service shutdown, driver replacement, security exception, reset, or destructive command as a workaround.

## Completion checklist

- [ ] The exact target and user intent were confirmed.
- [ ] No unrelated files, windows, settings, accounts, or devices were changed.
- [ ] Any consequential step had explicit approval and a recoverable plan where possible.
- [ ] The resulting state was independently verified.
- [ ] Limitations, remaining risks, and the evidence used were reported accurately.

---

*Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Windows and third-party product names are used descriptively; their respective owners retain their rights.*
'''

files=[]
for di,domain in enumerate(D,1):
 key,title,*_=domain
 sub=f'{di:02d}-{slug(key)}'
 for ai,action in enumerate(A,1):
  idx=(di-1)*30+ai
  folder=f'{CAT}/{sub}/{ai:02d}-{slug(action)}'
  files.append({'path':f'{folder}/SKILL.md','content':make_skill(idx,domain,action,ai),'encoding':'utf-8'})
assert len(files)==1200 and len({x['path'] for x in files})==1200
ROOT.mkdir(parents=True,exist_ok=True)
for f in files:
 p=ROOT/f['path']; p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and '--force' not in sys.argv:
  if p.read_text(encoding='utf-8') != f['content']:
   raise SystemExit(f"Existing skill differs; inspect it or rerun with --force: {f['path']}")
 else:
  p.write_text(f['content'],encoding='utf-8')
print('Generated',len(files),'skills across',len(D),'domains; chars',sum(len(x['content']) for x in files))
print('Sample paths:',files[0]['path'],files[29]['path'],files[30]['path'],files[-1]['path'])
print('Sample skill words:',len(files[0]['content'].split()))