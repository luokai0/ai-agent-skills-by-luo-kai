---
name: "Windows Input, Output, and Peripheral Devices: Discover Current State"
description: "Inspect displays, audio, cameras, microphones, keyboard and pointing devices, clipboard and text input, printers, scanners, Bluetooth, docks, and peripheral queues with privacy-aware read-only checks."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0006"
  version: "1.2.0"
---

# Windows Input, Output, and Peripheral Devices: Discover Current State

## Objective

Establish the current state of Windows input and output devices, display configuration, audio/camera selection, clipboard and text-entry behavior, printers, scanners, Bluetooth, docks, and peripheral queues. Preserve accessibility preferences, privacy, confidential work, pending print jobs, and the user's existing device configuration. This is a read-only discovery workflow; do not activate sensors, overwrite clipboard data, print, clear queues, pair devices, or change display/input settings without a separate request and explicit approval.

## When to use

Use for one or more of these related Windows I/O areas:
- Display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices.
- Clipboard inspection, keyboard layouts, IME, text entry, and form interactions.
- Printer queues, scanner discovery, USB devices, Bluetooth, docks, and peripheral troubleshooting.

Applies to interactive Windows 10 and Windows 11 desktops and laptops. Do not assume administrator rights, a particular OEM, or identical controls across editions.

## Required operating discipline

1. Identify the exact device, account/session, monitor, audio endpoint, camera, input method, clipboard action, printer, scanner, or peripheral.
2. Observe before acting. Note privacy indicators, active recordings/calls, unsaved work, pending print jobs, paired-device state, and current display/input configuration.
3. Prefer native Windows UI and supported accessibility/UI Automation controls. Use bounded read-only queries only when relevant.
4. Respect user-selected accessibility and input modalities. Do not assume a preferred device or input method.
5. Obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
6. Never activate microphones/cameras, record people, print confidential material, pair unknown devices, or install vendor utilities without consent.
7. Keep discovery read-only. Do not silently overwrite clipboard content, change display layout, alter input methods, or clear device queues.

## Environment and target identification

Confirm Windows edition/build, architecture, current user/session, and whether the device is local, remote, virtual, shared, or organization-managed.

Identify the exact device or endpoint using its visible name plus hardware/device identity where available. For displays, distinguish physical monitor order from virtual desktop arrangement. For audio, identify input versus output endpoints. For printers, identify queue, driver, port, and selected destination. For clipboard and text entry, identify the target application and field without exposing private clipboard contents.

## Domain profiles

Select only the profile relevant to the request.

### A. Displays, audio, cameras, and physical input

**Scope:** Display arrangement, scaling, sound, microphones, webcams, keyboard, and pointing devices.

**Preferred tools:** Settings > Display/Sound, Get-CimInstance, Device Manager, and built-in test panels.

**Inspection:** Confirm selected devices, input/output levels, display resolution, refresh rate, scaling, monitor order, keyboard layout, and pointer settings as relevant. Use a visible non-recording test when available.

**Safety:** Respect camera and microphone privacy indicators. Do not activate sensors or record people without consent. Do not change accessibility-related input or display settings during discovery.

**Verification:** Verify selected device, levels, resolution, refresh rate, and monitor order. Confirm that the expected endpoint is active.

**Recovery:** Return to the previous working device/display configuration and test one variable at a time.

### B. Clipboard, keyboard layout, and text entry

**Scope:** Clipboard inspection, paste behavior, keyboard layouts, IME, text entry, and form interactions.

**Preferred tools:** Clipboard UI, keyboard layout settings, UI Automation ValuePattern, and a harmless Notepad test.

**Inspection:** Confirm active keyboard layout/IME, target field, focus, and whether a harmless sample is entered with the expected character encoding. Never dump the clipboard wholesale.

**Safety:** Clipboard may contain passwords or private data. Never read it wholesale, overwrite it silently, or paste its contents into a report. Avoid submitting forms during discovery.

**Verification:** Verify a harmless sample, target field, character encoding, and final text before any separately approved submission.

**Recovery:** Use direct typing for sensitive fields. Restore clipboard content only if the original value was safely retained with consent.

### C. Printers, scanners, docks, and peripherals

**Scope:** Printer queues, scanner discovery, USB devices, Bluetooth, docks, and peripheral troubleshooting.

**Preferred tools:** Settings > Bluetooth & devices, Get-Printer, Get-PrinterQueue, and Device Manager.

**Inspection:** Confirm device identity, connection state, driver, port, queue status, selected destination, and pending jobs. Use only a non-sensitive test result when a test is separately approved.

**Safety:** Do not print confidential material, clear queues, pair unknown devices, or install vendor utilities without approval.

**Verification:** Verify device identity, driver, queue, selected destination, and non-sensitive test result. Preserve pending jobs.

**Recovery:** Check connection and queue status first. Preserve pending jobs and ask before clearing them.

**Read-only examples:**
```powershell
Get-Printer | Select-Object Name, DriverName, PortName, PrinterStatus
Get-PrinterQueue -ErrorAction SilentlyContinue
Get-PnpDevice -PresentOnly | Select-Object -First 30 FriendlyName, Class, Status
```

## Safe diagnostic commands

These examples are optional, read-oriented probes. Check availability with Get-Command first.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
Get-Process | Select-Object -First 10 Name, Id
Get-Printer | Select-Object Name, DriverName, PortName, PrinterStatus
Get-PrinterQueue -ErrorAction SilentlyContinue
Get-PnpDevice -PresentOnly | Select-Object -First 30 FriendlyName, Class, Status
```

Do not query or export clipboard contents, private keystrokes, camera frames, microphone audio, or confidential print data. Avoid unrelated home-directory listings and broad environment dumps.

## Unified discovery workflow

1. **Bind the request.** Select relevant profile(s). Confirm device/session and exact endpoint, monitor, field, queue, or peripheral identity.
2. **Capture a baseline.** Observe native UI first. Note active devices, privacy indicators, pending jobs, current configuration, and any ongoing call or recording.
3. **Inspect narrowly.** Use only the relevant settings page, accessibility control, or read-only query. Do not capture private media or clipboard contents.
4. **Resolve ambiguity.** If multiple endpoints or devices match, stop and ask for clarification. Do not choose by display name alone when stable identity is available.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, effect, privacy implications, and rollback route; obtain approval first.
6. **Verify independently.** Recheck device identity and visible state in a second native surface when practical. A click response or transient toast is not proof.
7. **Close the loop.** Report inspected state, what remained unchanged, evidence, blocked checks, and remaining risk.

## Stop conditions and recovery

Stop if device identity is ambiguous, a camera/microphone privacy indicator appears unexpectedly, a call or recording is active, confidential content could be printed, clipboard sensitivity is unknown, or pending jobs may be lost.

Preserve the current configuration and exact error. Retry at most once through a lower-risk documented route. Never activate sensors, record people, overwrite clipboard content, submit forms, clear queues, pair unknown devices, or change drivers/settings as an improvised workaround.

## Privacy-safe evidence and handoff

Report only the minimum redacted device identity, relevant configuration, checks performed, verification evidence, blocked steps, and remaining risk. Do not include clipboard contents, passwords, tokens, keystrokes, audio/video, private document names, confidential print data, or unnecessary serial numbers.

## Completion checklist

- [ ] User intent and exact device/endpoint/field/queue were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection remained read-only and used least privilege.
- [ ] Accessibility preferences and privacy indicators were respected.
- [ ] No camera/microphone recording or confidential printing occurred.
- [ ] Clipboard data was not exposed or overwritten.
- [ ] Pending jobs and existing device configuration were preserved.
- [ ] Findings and limitations were independently verified and accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows surfaces and tools.
