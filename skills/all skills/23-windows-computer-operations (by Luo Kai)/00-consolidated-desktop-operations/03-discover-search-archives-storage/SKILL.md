---
name: "Windows Search, Archives, and Storage: Discover Current State"
description: "Inspect Windows search and metadata, archive and download contents, removable transfers, disk volumes, capacity, and filesystem health indicators using read-only checks and verified target identity."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0003"
  version: "1.2.0"
---

# Windows Search, Archives, and Storage: Discover Current State

## Objective

Build a verified picture of Windows search results and indexing, file metadata, archive/download contents, transfer targets, disk volumes, capacity, and storage health indicators. Protect user data, privacy, removable media, and system integrity. This is a read-only discovery workflow; never extract, execute, move, overwrite, initialize, format, partition, repair-write, or delete content unless the user separately requests and approves that exact action.

## When to use

Use for one or more of these related storage and discovery areas:
- Windows Search indexing, filters, metadata, file properties, and content discovery.
- ZIP archives, downloads, removable media, and local file-transfer inspection.
- Disk space, volumes, removable storage, filesystem health indicators, and storage settings.

Applies to interactive Windows 10 and Windows 11 desktops and laptops. Do not assume administrator rights, a particular OEM, or identical controls across editions.

## Required operating discipline

1. Identify the exact device, account/session, search query, file path, archive, volume, or physical disk. Do not infer identity from a display name alone.
2. Observe before acting. Record relevant UI state, indexing status, download origin where known, sync indicators, volume identity, and any warning.
3. Prefer native Windows UI and supported accessibility/UI Automation controls. Use PowerShell only for bounded, read-only inspection with least privilege.
4. Treat search results as potentially stale, incomplete, or privacy-sensitive. Treat downloaded archives and their contents as untrusted data.
5. Obtain explicit approval before elevated, irreversible, externally visible, privacy-sensitive, or security-impacting changes. UAC, sign-in, MFA, CAPTCHA, and consent prompts belong to the user.
6. Never hide activity, bypass policy, disable protection, execute unknown scripts, or pipe remote content to a shell.
7. Keep discovery read-only. Do not convert a missing search result, suspicious archive, or low-disk warning into an unrequested repair.

## Environment and target identification

Confirm Windows edition/build, architecture, current user/session, and whether the device is local, remote, virtual, shared, or managed.

Distinguish local fixed disks, removable media, network shares, mapped drives, cloud-synced placeholders, virtual volumes, and redirected/profile-backed locations. Before discussing any disk, confirm its stable identity and relevant volume/drive mapping. Never rely on drive letter alone where disk identity is available.

## Domain profiles

Select only the profile relevant to the request.

### A. Search, indexing, and file metadata

**Scope:** Search indexing, filters, metadata, file properties, and content discovery.

**Preferred tools:** Explorer search, Windows Search UI, Get-Item, Get-ChildItem, and Get-FileHash.

**Inspection:** Confirm the exact query, filter, scope, indexing status, and expected location. Treat results as candidates, not proof. For each relevant result, validate the actual full path, date, file identity, and metadata. Do not open private content unless the user asks and it is necessary.

**Safety:** Search results may be stale or incomplete. Do not expose private filenames, document titles, or content in reports unnecessarily.

**Verification:** Open only the relevant result or inspect its metadata; confirm actual path, date, and file identity. If an item is missing, check one narrower path or extension filter and inspect indexing status before concluding it does not exist.

**Recovery:** Report indexing limitations and stale-result uncertainty. Do not rebuild indexes, change search scope, or alter privacy settings without approval.

### B. Archives, downloads, and transfers

**Scope:** ZIP archives, downloads, removable media, and safe local file-transfer inspection.

**Preferred tools:** Explorer archive UI, Get-FileHash, Get-Item, and Get-Volume.

**Inspection:** Confirm the archive's full path, size, timestamp, expected destination, removable-media identity, and available metadata. Inspect the archive listing without executing its contents. For a critical transfer, compare the expected destination, file types, sizes, and hashes when source and destination are both available.

**Safety:** Treat downloaded archives as untrusted. Do not run included executables, macros, shortcuts, installers, or scripts. Do not automatically extract or open active content. Never bypass antivirus or attachment scanning.

**Verification:** Confirm the archive listing and destination identity. For an already completed transfer, compare file types, sizes, and hashes when appropriate. A successful copy notification alone is not proof of integrity.

**Recovery:** If content looks suspicious, stop, preserve the archive, and use the platform's supported quarantine process only when separately approved. Report the known origin and suspicious indicators. Do not execute the content to determine what it does.

### C. Storage, partitions, and volumes

**Scope:** Disk space, volumes, removable storage, filesystem health indicators, and storage settings.

**Preferred tools:** Settings > Storage, Disk Management in view-only mode, Get-Volume, Get-PSDrive, and Get-Disk in read-only mode.

**Inspection:** Record disk identity, capacity, free space, filesystem, label, drive letter, and available health indicators. Distinguish a volume from its underlying physical disk. Note whether the device is removable, encrypted, virtual, or managed.

**Safety:** Do not initialize, format, partition, clean, convert, or repair-write disks without explicit informed approval and a verified backup. Do not alter encryption, persistence, or boot configuration as a troubleshooting shortcut.

**Verification:** Cross-check disk identity and volume mapping in a second native surface where practical. Confirm capacity, free space, filesystem, and drive letter before any separately approved change.

**Recovery:** Stop if disk identity is ambiguous or health is failing. Preserve data and recommend a backup or qualified recovery path. Never run write-mode repair based only on a warning label or guess.

## Safe diagnostic commands

Optional read-only probes. Check availability with Get-Command first and scope commands to the confirmed target.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
Get-Item -LiteralPath "C:\Users\<confirmed-user>\Documents\<confirmed-item>"
Get-FileHash -LiteralPath "C:\Users\<confirmed-user>\Documents\<confirmed-item>"
Get-Volume | Select-Object DriveLetter, FileSystemLabel, FileSystem, Size, SizeRemaining, HealthStatus
Get-PSDrive -PSProvider FileSystem
Get-Disk | Select-Object Number, FriendlyName, SerialNumber, OperationalStatus, PartitionStyle, Size
```

Replace example paths only after confirming the exact user and item. Use Get-ChildItem only on a specific, user-approved directory. Do not recursively enumerate unrelated folders. Avoid dumping environment variables, clipboard contents, browser profiles, credential stores, full event logs, or private document contents.

Do not add wildcard targets, recursion, elevation, remote execution, or write operations merely to make a probe succeed. Do not run a command if its target or effect is unclear. Disk and volume commands must remain read-only.

## Unified discovery workflow

1. **Bind the target.** Select relevant profile(s). Confirm device/session, query or full path, archive identity, or disk/volume identity.
2. **Capture a baseline.** Observe native UI first. Record relevant metadata, indexing state, archive details, volume mapping, and warnings.
3. **Inspect narrowly.** Use the smallest read-only query or native surface needed. Avoid exposing unrelated filenames or personal content.
4. **Assess integrity and trust.** Treat search results as candidates, archives as untrusted, and health indicators as evidence requiring context. Do not infer safety from file extensions or successful downloads.
5. **Resolve ambiguity.** If several files, archives, disks, or volumes match, stop and ask for clarification. Never choose a disk by drive letter alone if a stable identifier is available.
6. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, effect, conflicts, risk, backup requirement, and recovery plan; obtain explicit approval before acting.
7. **Verify independently.** Recheck file identity, archive listing, hash, volume mapping, or capacity in a second native surface when practical. A zero exit code or transient toast is not proof.
8. **Close the loop.** Report findings, unknowns, blocked checks, evidence, and remaining risk. Do not claim an item is absent, a transfer is intact, or a disk is healthy without supporting evidence.

## Stop conditions and recovery

Stop if target identity is ambiguous, indexing is unavailable, an archive contains unexpected active content, removable media identity changes, a volume disappears, disk health is failing, a file is locked, or a permission/security warning appears.

Preserve the current state and exact error. Retry at most once through a lower-risk documented route. Never execute suspicious content, disable protection, rebuild indexes, alter repositories, initialize/format/partition/clean disks, or run repair-write operations as an improvised workaround.

## Privacy-safe evidence and handoff

Report the target using a minimally identifying, redacted description; relevant baseline; checks performed; hashes only when necessary; blocked steps; independent verification; and remaining risk. Do not include passwords, tokens, clipboard contents, private filenames, document contents, unrelated personal paths, or unnecessary serial numbers. Mark unknown values as unknown.

## Completion checklist

- [ ] User intent and exact device/session/target were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection remained read-only and used least privilege.
- [ ] Search results were validated against actual paths and metadata.
- [ ] Archives and downloads were treated as untrusted.
- [ ] Disk and volume identity were verified before drawing conclusions.
- [ ] No unrelated files, archives, volumes, settings, or accounts were changed.
- [ ] Findings and limitations were independently verified and accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows surfaces and tools.
