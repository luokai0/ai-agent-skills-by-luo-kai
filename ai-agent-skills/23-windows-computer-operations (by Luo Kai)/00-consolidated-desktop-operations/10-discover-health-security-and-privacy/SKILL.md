---
name: "Windows Health, Security, and Privacy: Discover Current State"
description: "Inspect performance, battery and thermal state, event diagnostics, Defender and firewall protection, account access, app permissions, and privacy controls using bounded, read-only evidence."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0010"
  version: "1.2.0"
---

# Windows Health, Security, and Privacy: Discover Current State

## Objective

Establish a verified baseline of Windows performance, battery and thermal state, event diagnostics, Defender and firewall protection, account access, application permissions, and privacy controls. Protect user data, credentials, system integrity, and physical device safety. This is a read-only discovery workflow: do not install monitoring agents, run stress tests, change power settings, disable protection, restore detections, alter permissions, or change accounts without a separate request and explicit approval.

## When to use

Use for:
- CPU, memory, disk, GPU, network, startup impact, and responsiveness analysis.
- Battery health, charging, power plans, sleep, thermal symptoms, docks, and mobility.
- Event Viewer, reliability history, crash records, error codes, and diagnostic evidence.
- Defender status, firewall posture, SmartScreen, protection history, and safe threat response.
- App permissions, local accounts, sign-in options, sharing, and privacy controls.

Applies to Windows 10 and Windows 11 desktops and laptops, including managed devices.

## Required operating discipline

1. Identify the exact device, account/session, workload, battery, event source/time window, security component, app permission, or account.
2. Observe before acting. Record relevant symptoms, workload timestamps, power state, protection status, and user-visible warnings.
3. Prefer native Windows UI and bounded read-only queries. Collect the minimum evidence needed.
4. Do not expose process command lines containing secrets, broad event logs, account names, private paths, IP addresses, or document titles in external reports.
5. Never disable Defender, tamper protection, firewall, SmartScreen, or quarantine. Do not restore detections casually.
6. Never collect or reveal passwords, PINs, tokens, biometric data, recovery codes, or private account material. Do not bypass account controls.
7. Obtain explicit approval before elevated, irreversible, privacy-sensitive, or security-impacting changes. Managed-device settings belong to the authorized administrator.
8. Keep discovery read-only. Do not turn an observation into an unrequested repair.

## Environment and target identification

Confirm Windows edition/build, architecture, current user/session, device type, and whether the device is managed or remote. Identify the exact workload, power source, event provider/time window, protection component, account, and app permission. Distinguish correlation from cause and reported health indicators from verified hardware diagnosis.

## Domain profiles

### A. Performance and resource monitoring

**Scope:** CPU, memory, disk, GPU, network, startup impact, and responsiveness analysis.

**Preferred tools:** Task Manager, Resource Monitor, Performance Monitor, Get-Counter, and Get-Process.

**Inspection:** Capture a baseline and repeated samples. Correlate resource use with timestamps and workload. Check CPU, memory, disk, GPU, network, and responsiveness only as relevant.

**Safety:** Do not install benchmark/monitoring agents or run stress tests without approval. Avoid exposing process command lines that may contain secrets.

**Verification:** Compare repeated samples over the same interval and workload. A single sample does not prove root cause.

**Recovery:** Reduce load safely, close only user-approved apps, and avoid claiming a single sample proves root cause.

**Read-only examples:**
```powershell
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, Id, CPU, WorkingSet64
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 3
```

### B. Battery, thermals, and power

**Scope:** Battery health, charging, power plans, sleep, thermal symptoms, docks, and mobility.

**Preferred tools:** Settings > Power & Battery, powercfg /batteryreport, powercfg /energy, and Get-CimInstance battery where supported.

**Inspection:** Verify AC/battery state, charge rate, active power scheme, battery report, temperatures from trusted OEM tools, and sleep behavior.

**Safety:** Never obstruct vents, force firmware changes, or disable thermal protection. Do not change sleep behavior without consent. A swollen battery or abnormal heat is a physical safety issue, not a tuning exercise.

**Verification:** Cross-check power state and active scheme. Treat third-party temperature readings as estimates unless supplied by trusted OEM diagnostics.

**Recovery:** Disconnect suspect peripherals, cool the device naturally, and recommend OEM service for swelling or abnormal heat. Do not press, puncture, or continue using a visibly swollen battery.

**Read-only example:**
```powershell
powercfg /getactivescheme
```

The following command creates a report file. Use it only when the user approves that local output:
```powershell
powercfg /batteryreport /output "$env:TEMP\battery-report.html"
```

### C. Event logs and diagnostics

**Scope:** Event Viewer, reliability history, crash records, error codes, and diagnostic evidence.

**Preferred tools:** Get-WinEvent with narrow filters, Event Viewer, Reliability Monitor, and Problem Reports.

**Inspection:** Match event time, provider, ID, level, and reproduction window. Distinguish correlation from cause. Query only the relevant log and time range.

**Safety:** Logs can contain usernames, paths, IPs, document names, and other private data. Redact before sharing. Avoid broad log dumps.

**Verification:** Confirm provider, event ID, timestamp, level, and reproduction window. Compare related events without asserting causation from timing alone.

**Recovery:** Export only relevant time-bounded events to an approved location; avoid broad log dumps.

**Read-only example:**
```powershell
Get-WinEvent -LogName System -MaxEvents 20 | Select-Object TimeCreated, Id, LevelDisplayName, ProviderName
```

### D. Windows Security and Defender

**Scope:** Defender status, firewall posture, SmartScreen, protection history, and safe threat response.

**Preferred tools:** Windows Security UI, Get-MpComputerStatus, Get-MpThreatDetection, and Get-NetFirewallProfile.

**Inspection:** Verify protection state, detection name, source, timestamp, action, and current remediation status. Do not expose threat details beyond what is needed to answer the request.

**Safety:** Never disable Defender, tamper protection, firewall, SmartScreen, or quarantine. Do not restore detections casually or weaken security to make a warning disappear.

**Verification:** Cross-check protection status in Windows Security and read-only status queries where available.

**Recovery:** Isolate only using approved controls; preserve evidence and escalate suspected compromise.

**Read-only examples:**
```powershell
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntispywareEnabled
Get-NetFirewallProfile
```

### E. Privacy, permissions, and account access

**Scope:** App permissions, local accounts, sign-in options, sharing, and privacy controls.

**Preferred tools:** Settings > Privacy & Security, Settings > Accounts, whoami, and Get-LocalUser in read-only mode when available.

**Inspection:** Verify exact account and app, permission scope, effective access, and user intent. Distinguish a permission toggle from actual effective access.

**Safety:** Never collect or reveal passwords, PINs, tokens, biometric data, or recovery codes. Do not trigger account lockout, bypass sign-in, or weaken access controls.

**Verification:** Confirm account identity and permission scope through the relevant native Settings surface. Report only the minimum redacted account detail.

**Recovery:** Restore previous permissions only after a separate approved change. Refer managed-account changes to the administrator.

**Read-only examples:**
```powershell
whoami
Get-LocalUser | Select-Object Name, Enabled, LastLogon
```

## Unified discovery workflow

1. **Bind the request.** Select relevant profile(s). Confirm device/session, workload, event window, protection component, account, or app.
2. **Capture a baseline.** Observe native UI and record only relevant state and timestamps.
3. **Inspect narrowly.** Use read-only queries and trusted native panels. Avoid stress tests, broad log exports, and unnecessary account enumeration.
4. **Resolve ambiguity.** If the workload, event source, device, detection, account, or permission is unclear, stop and ask for clarification.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, expected effect, risks, backup/rollback route, and approval requirements.
6. **Verify independently.** Compare repeated samples or cross-check status in a second native surface. A warning label or single sample is not a complete diagnosis.
7. **Close the loop.** Report evidence, what remains unknown, blocked checks, and remaining risk. Do not claim root cause without evidence.

## Stop conditions and recovery

Stop if the device overheats, a battery appears swollen, an unexpected security alert appears, a suspected compromise is active, an account identity is ambiguous, or private logs/credentials could be exposed.

Preserve the current state and exact error. Retry at most once through a lower-risk documented route. Never disable security, restore quarantined files, run stress tests, change power settings, dump private logs, alter permissions, or bypass account controls as an improvised workaround.

## Privacy-safe evidence and handoff

Report only the minimally identifying device/account context, relevant baseline, timestamps, bounded checks, independent verification, blocked steps, and remaining risk. Redact usernames, private paths, IP addresses, serial numbers, document titles, event message details, process command lines, and account identifiers. Never include passwords, PINs, tokens, biometrics, or recovery codes.

## Completion checklist

- [ ] Device/session and exact workload/event/security/account target were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection remained read-only and used least privilege.
- [ ] Performance conclusions used repeated samples and workload context.
- [ ] Battery/thermal safety indicators were respected.
- [ ] Logs were narrow and privacy-redacted.
- [ ] Defender, firewall, SmartScreen, and quarantine were not weakened.
- [ ] Credentials and sensitive account data were not exposed.
- [ ] Findings, limitations, and remaining risks were independently verified.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows diagnostics and security components.
