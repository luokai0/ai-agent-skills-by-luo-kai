---
name: "Windows Configuration, Software, Updates, and Drivers: Discover Current State"
description: "Inspect registry and policy state, installed applications, package sources, Windows Update history, devices, and signed drivers through read-only tools and explicit identity verification."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0005"
  version: "1.2.0"
---

# Windows Configuration, Software, Updates, and Drivers: Discover Current State

## Objective

Establish a verified baseline of Windows configuration and policy, installed applications, package managers and sources, update status, devices, and driver identity. Preserve system integrity, organization policy, user data, and security controls. This is read-only discovery: do not edit the registry or policy, install or uninstall software, accept package agreements, force updates or restarts, or modify drivers during inspection.

## When to use

Use for one or more of these related Windows administration areas:
- Registry structure, Group Policy state, policy refresh diagnostics, and configuration provenance.
- Application discovery, installer status, repair/update/uninstall planning, and compatibility.
- winget, Microsoft Store, package sources, app dependencies, and package inventory.
- Windows Update status, history, optional updates, restart planning, and failure diagnosis.
- Plug-and-Play devices, hardware IDs, driver versions, signatures, and device status.

Applies to interactive Windows 10 and Windows 11 desktops and laptops, including managed workstations. Do not assume administrator rights, a particular OEM, or identical controls across editions.

## Required operating discipline

1. Identify the exact device, account/session, registry hive/key, policy, application/package, update, hardware device, or driver. Do not infer identity from a display name alone.
2. Observe before acting. Record relevant UI state, update/restart warnings, installer prompts, device status, and policy indicators.
3. Prefer native Windows UI and supported accessibility/UI Automation controls. Use bounded, read-only PowerShell or command-line queries only when relevant and available.
4. Preserve the current configuration and capture a baseline before any separately approved change. Do not use undocumented registry keys or hidden policy routes.
5. Obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
6. Never bypass organization policy, disable security controls, accept agreements, install unknown packages, or run unsigned installers/drivers.
7. Keep this workflow read-only. Do not turn discovery into an unrequested repair or update.

## Environment and target identification

Confirm Windows edition/build, architecture, current user/session, and whether the device is organization-managed. Preserve managed policy and refer blocked changes to the authorized administrator.

Use stable identities:
- Registry: exact hive, key, value, type, and policy source.
- Applications/packages: package ID, publisher, version, source, install path, and signature where available.
- Updates: KB identifier, build/version, history entry, pending restart, and error code.
- Devices/drivers: hardware ID, device instance, provider, version, signer, status, and current package.

## Domain profiles

Select only the profile relevant to the request.

### A. Registry and Group Policy inspection

**Scope:** Registry structure, policy state, policy refresh diagnostics, and configuration provenance.

**Preferred tools:** Registry Editor in read-only mode, reg query, gpresult /r, and gpresult /h only to a user-approved output path.

**Inspection:** Identify the exact hive/key/value and distinguish local configuration from policy-controlled values. Use gpresult to identify policy source and scope. Do not infer that a registry value is effective when a managed policy overrides it.

**Safety:** Never modify registry or policy as a shortcut. Do not weaken security controls, edit credentials, bypass policy, or alter managed-device settings.

**Verification:** Record exact hive/key/value and policy source. Compare before/after only for a separately approved change.

**Recovery:** Stop when managed-device policy is involved and refer to the administrator. Do not fight organizational controls.

**Read-only examples:**
```cmd
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion"
gpresult /r
```

### B. Application installation and compatibility

**Scope:** App discovery, installer state, repair/update/uninstall workflows, and application compatibility.

**Preferred tools:** Settings > Installed apps, winget list/search/show, and Get-AppxPackage in read-only mode.

**Inspection:** Confirm application identity, publisher, version, install source, package identity, and signature where available. Check whether an installer or update is already running before proposing another.

**Safety:** Install only user-approved software from trusted publishers. Never use cracks, bundled offers, or silent unknown installers. Do not repair or uninstall during discovery.

**Verification:** Verify publisher, version, install source, signatures when available, and application launch state.

**Recovery:** Cancel unsigned or unexpected installers. Use vendor repair guidance and preserve user data.

**Read-only examples:**
```powershell
winget list
Get-AppxPackage | Select-Object -First 20 Name, Version, Publisher
```

### C. Package managers and dependencies

**Scope:** winget, Microsoft Store, package sources, app dependencies, and package inventory.

**Preferred tools:** winget --info, winget list, winget search, winget show, and Microsoft Store UI.

**Inspection:** Confirm package ID, publisher, version, source, architecture, and dependency details before any later install is considered. Distinguish Store inventory from winget source results.

**Safety:** Do not add arbitrary package sources or accept package agreements on behalf of the user without authorization. Do not install when package identity or publisher is ambiguous.

**Verification:** Check package ID, publisher, version, source, and current inventory.

**Recovery:** Refresh source metadata once. If identity remains ambiguous, do not install.

**Read-only examples:**
```powershell
winget --info
winget list
winget search <confirmed-package-name>
winget show <confirmed-package-id>
```

### D. Windows Update and servicing

**Scope:** Update status, history, optional updates, restart planning, and update failure diagnosis.

**Preferred tools:** Settings > Windows Update, Get-HotFix, Get-ComputerInfo, and Event Viewer.

**Inspection:** Confirm update history, installed KB/version, optional updates, pending restart, and relevant failure codes. Distinguish a download, install, and restart-pending state.

**Safety:** Never force a reboot during active work. Do not disable update services or install untrusted update packages. Preserve the user's current session.

**Verification:** Confirm KB/version, update history, pending restart, and post-reboot health only after an authorized restart has actually occurred.

**Recovery:** Capture error codes and relevant event details. Use the built-in troubleshooter before considering servicing repair.

**Read-only examples:**
```powershell
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 10
Get-ComputerInfo | Select-Object WindowsVersion, OsBuildNumber
```

### E. Devices and signed drivers

**Scope:** Plug-and-Play devices, driver versions, hardware IDs, device status, and safe driver troubleshooting.

**Preferred tools:** Device Manager, Get-PnpDevice, and Get-CimInstance Win32_PnPSignedDriver.

**Inspection:** Confirm hardware ID, device instance, provider, driver version, signer, device status, and any pending restart. Distinguish the physical device from its driver package.

**Safety:** Do not install unsigned drivers, disable security devices, or remove a device package without a verified rollback plan. Do not replace a driver merely because a newer version exists.

**Verification:** Verify hardware ID, provider, version, signer, device status, and restart effect.

**Recovery:** Use Windows Update or the OEM's trusted support channel. Preserve current driver details before any separately approved rollback.

**Read-only examples:**
```powershell
Get-PnpDevice -PresentOnly | Select-Object -First 30
Get-CimInstance Win32_PnPSignedDriver | Select-Object -First 20 DeviceName, DriverVersion, DriverProviderName, IsSigned
```

## Unified discovery workflow

1. **Bind the request.** Select relevant profile(s). Confirm exact device, session, registry key, package ID, KB, hardware ID, or driver identity.
2. **Capture a baseline.** Observe native UI first. Record relevant values, publisher/source, policy origin, update status, or device state.
3. **Inspect narrowly.** Use only read-only queries. Do not export broad registry branches, full package inventories, private event logs, or unrelated device data.
4. **Resolve ambiguity.** If several keys, apps, packages, updates, or devices match, stop and ask for clarification. Do not select by display name alone.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, expected effect, dependencies, risks, backup/rollback plan, and approval requirements.
6. **Verify independently.** Recheck identity and state in a second native surface when practical. A successful command or transient toast is not proof.
7. **Close the loop.** Report what was inspected, what remains unchanged, evidence, blocked checks, and remaining risk. Do not claim completion without verification.

## Stop conditions and recovery

Stop if policy source is unclear, a managed-device restriction appears, an installer is unsigned or unexpected, package identity is ambiguous, a restart could interrupt work, a driver is unsigned, or a device's hardware identity does not match the target.

Preserve the current state and exact error. Retry at most once through a lower-risk documented route. Never improvise registry edits, policy bypass, package-source changes, forced restart, driver replacement, service shutdown, security exceptions, or destructive workarounds.

## Privacy-safe evidence and handoff

Report the target using minimally identifying information, baseline, read-only checks performed, relevant publisher/version/source or policy origin, independent verification, blocked steps, and remaining risk. Redact usernames, private paths, internal policy data, serial numbers, and unnecessary hardware identifiers. Never include passwords, tokens, or credential values. Mark unknown values as unknown.

## Completion checklist

- [ ] User intent, device/session, and exact target identity were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection remained read-only and used least privilege.
- [ ] Managed policy and security controls were preserved.
- [ ] App/package publisher and source were verified.
- [ ] Update and restart state were distinguished accurately.
- [ ] Device and driver identity/signature were checked.
- [ ] No registry, app, package, update, driver, or policy changes were made.
- [ ] Findings and limitations were independently verified and accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows surfaces and tools.
