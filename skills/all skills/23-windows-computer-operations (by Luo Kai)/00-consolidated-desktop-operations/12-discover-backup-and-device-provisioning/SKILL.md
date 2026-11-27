---
name: "Windows Backup, Recovery, and Device Provisioning: Discover Current State"
description: "Inspect File History, OneDrive sync, restore points, recovery options, Windows setup, local profiles, device identity, enrollment, and handoff readiness without initiating destructive recovery or bypassing management."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0012"
  version: "1.2.0"
---

# Windows Backup, Recovery, and Device Provisioning: Discover Current State

## Objective

Establish a verified baseline of Windows backup coverage, File History, OneDrive sync, restore points, recovery options, device setup, local profiles, device identity, and organization enrollment. Preserve current disks, backups, account ownership, and management policy. This is a read-only discovery workflow: do not reset, reinstall, restore, repair disks, overwrite recovery media, bypass enrollment, or change ownership without explicit informed approval.

## When to use

Use for:
- File History, OneDrive sync, restore points, recovery environment, and restore planning.
- Initial setup, local profiles, device naming, enrollment indicators, and handoff readiness.

Applies to Windows 10 and Windows 11 desktops and laptops, including organization-owned and enrolled devices.

## Required operating discipline

1. Identify the exact device, user/session, backup destination, recovery point, disk, account, profile, or enrollment state.
2. Observe before acting. Record backup timestamp/scope, sync status, restore-point availability, device identity, and enrollment indicators.
3. Prefer native Settings, File History, recovery options, and bounded read-only commands.
4. Never initiate reset, reinstall, restore, disk repair, or overwrite recovery media without explicit informed approval and a verified backup.
5. Never bypass enrollment, remove management, create hidden accounts, or alter ownership/activation state.
6. Obtain explicit approval before elevated, irreversible, externally visible, or privacy-sensitive changes. Organization-managed device changes belong to authorized IT administrators.
7. Keep discovery read-only and preserve the current disk and local access.

## Environment and target identification

Confirm Windows edition/build, architecture, current user/session, device name/identity, and whether the device is organization-owned, enrolled, remote, or shared.

For backups, identify destination, scope, timestamp, integrity indicator, and restore point. For provisioning, identify the account owner, local profile, enrollment state, update status, and handoff readiness. Do not infer that a sync indicator proves a complete backup or that a restore point covers personal files.

## Domain profiles

### A. Backup, restore, and recovery

**Scope:** File History, OneDrive sync, restore points, recovery environment, and restore planning.

**Preferred tools:** Settings > Backup, File History UI, read-only wbadmin get versions, and Windows recovery options.

**Inspection:** Verify backup timestamp, scope, destination, integrity indicators, sync state, and available restore points before relying on them. Distinguish cloud sync from an independent backup and a system restore point from a personal-file backup.

**Safety:** Never initiate reset, reinstall, restore, disk repair, or overwrite recovery media without explicit informed approval and a verified backup.

**Verification:** Verify backup timestamp, scope, destination, integrity, and restore point before relying on it.

**Recovery:** Stop if backup is missing or stale; preserve the current disk and explain recovery choices.

**Read-only example:**
```cmd
wbadmin get versions
```

### B. Windows provisioning and account lifecycle

**Scope:** Initial setup, local profiles, device naming, enrollment indicators, and handoff readiness.

**Preferred tools:** Settings > System/About, Settings > Accounts, dsregcmd /status in read-only mode, and whoami.

**Inspection:** Verify device identity, account owner, enrollment state, update status, and setup completion. Distinguish local account/profile state from organization enrollment and cloud identity.

**Safety:** Do not bypass enrollment, remove management, create hidden accounts, or alter ownership/activation state.

**Verification:** Cross-check device identity, account owner, enrollment state, update status, and setup completion in native Settings and read-only status output.

**Recovery:** Pause on organization-owned or enrolled devices and hand off to authorized IT administrators.

**Read-only examples:**
```powershell
whoami
Get-ComputerInfo | Select-Object CsName, WindowsProductName, OsBuildNumber
dsregcmd /status
```

## Unified discovery workflow

1. **Bind the request.** Select the relevant profile(s). Confirm exact device/session, backup destination/recovery point, or account/enrollment target.
2. **Capture a baseline.** Observe native UI and record only relevant backup, sync, restore, device, and enrollment state.
3. **Inspect narrowly.** Use read-only queries. Do not open private backup contents or enumerate unrelated profiles.
4. **Resolve ambiguity.** If device ownership, account identity, backup scope, or restore point is unclear, stop and ask for clarification.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, expected effect, backup prerequisites, risk, rollback route, and approval requirements.
6. **Verify independently.** Recheck backup timestamp/scope/destination or device/enrollment identity in a second native surface.
7. **Close the loop.** Report what is backed up, what is not confirmed, current enrollment, blocked steps, and remaining risk. Do not claim data is recoverable without evidence.

## Stop conditions and recovery

Stop if backup is missing/stale, destination is unavailable, disk health is uncertain, device ownership/enrollment is unclear, or a recovery action could overwrite current data.

Preserve the current disk and local access. Retry at most once through a lower-risk documented route. Never initiate reset, reinstall, restore, disk repair, recovery-media overwrite, enrollment bypass, hidden account creation, or ownership changes as an improvised workaround.

## Privacy-safe evidence and handoff

Report minimally identifying device/account context, backup timestamp/scope/destination, restore-point availability, enrollment state, verification evidence, blocked checks, and remaining risk. Redact usernames, private paths, serial numbers, organization identifiers, and unnecessary account details. Never include passwords, tokens, or recovery codes.

## Completion checklist

- [ ] Device/session and exact backup/recovery/account target were confirmed.
- [ ] Backup and sync were distinguished from restore points and independent backups.
- [ ] Backup timestamp, scope, destination, and integrity were checked.
- [ ] Device identity, account owner, and enrollment state were verified.
- [ ] Organization policy and ownership boundaries were preserved.
- [ ] No reset, reinstall, restore, disk repair, or enrollment change was initiated.
- [ ] Findings and limitations were independently verified and accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows backup and provisioning surfaces.
