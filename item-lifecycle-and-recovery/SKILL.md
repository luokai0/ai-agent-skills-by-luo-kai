---
name: item-lifecycle-and-recovery
description: Use when a Windows user or administrator must trace, retain, restore, or recover deleted, overwritten, moved, or misplaced files and folders, or must define how items move through create, modify, archive, delete, and purge stages on a Windows machine or user profile.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Item Lifecycle And Recovery

## Purpose and boundaries

This skill covers the lifecycle of user files and folders on Windows endpoints and user profiles: where items live, how they are removed or overwritten, what recovery paths exist, and how to restore them with evidence. It applies to local NTFS volumes, user profiles, and OneDrive or network shares as they affect a local item.

It does not cover: forensic imaging for legal matters, ransomware incident response beyond restoring affected items, server-side mailbox or database recovery, or changing retention policy for an organization. Those require a different owner.

## Inputs and assumptions

Collect before acting:

- Item path, name pattern, and approximate time of loss or change.
- Last known state: created, edited, moved, renamed, or deleted.
- Storage location: local fixed disk, removable media, OneDrive folder, mapped share.
- Available recovery sources: Recycle Bin, File History, Windows Backup or image backups, Previous Versions (shadow copies), application autosave or version history, cloud recycle bins.
- Whether the volume has been written to since the event. Every write reduces recovery odds.
- Authority to restore: owner of the data, and whether the restore overwrites current data.

Assume nothing about which recovery features are enabled. Verify each one.

## Operating workflow

1. Freeze writes. Ask the user to stop saving to the affected volume or folder. If the loss is recent and on a system disk, recommend no further installs or large downloads.
2. Identify the lifecycle stage. Determine whether the item was deleted (sent to Recycle Bin or removed permanently), overwritten, moved, renamed, or corrupted.
3. Check sources in order of cost and fidelity:
   a. Recycle Bin: restore in place if the original path is intact. Check the original location for name conflicts first.
   b. Previous Versions: right-click the parent folder, open Properties, and review the Previous Versions tab. This depends on prior restore points or shadow copies existing. Confirm availability on the specific volume.
   c. File History or backup target: browse by date to the nearest point before the event. Restore to an alternate location first.
   d. Application version history, OneDrive version history, or cloud recycle bin: follow the provider's current documented steps, since interfaces change.
4. Restore to a staging folder, not the original path, unless the user has approved overwriting.
5. Compare the recovered item against the expected state (size, modified time, hash if a reference exists, opens without error).
6. Promote the verified item to its final location only after approval.
7. Record the event: source used, timestamps, paths, and any remaining gaps.

## Decision gates

- Gate A, stop and escalate: the loss involves encrypted volumes without available recovery keys, a suspected malware-driven change, or regulated or personal sensitive data outside the user's authority. Do not attempt bulk file scanning or third-party recovery tools without explicit approval.
- Gate B, approval required: any restore that overwrites existing data, any purge of Recycle Bin or shadow copies, any disk cleanup, any change to backup or File History settings, and any action that uploads data to external services.
- Gate C, choose the source: prefer the source with the smallest time gap to the event and the highest fidelity. A Previous Versions copy from the right hour beats a backup from last week. If two candidates conflict, restore both to separate staging folders and compare.
- Gate D, partial recovery: if only part of a folder tree is recoverable, report exact counts recovered versus expected and do not present the result as complete.

## Verification and evidence

- Name, path, and size match the expected item or the user confirms the version.
- Modified timestamp matches the chosen restore point.
- File opens in its native application without repair prompts.
- For folders: item count matches the source inventory where one exists. Record counts before and after.
- Keep a short log: source, restore point timestamp, staging path, final path, verifier, and outstanding items.
- Do not claim recovery is guaranteed or complete without these checks.

Mark version-sensitive behavior (menu labels, File History defaults, shadow copy schedules, OneDrive retention windows) as requiring verification against current Microsoft documentation before stating it to the user.

## Failure handling

- Recycle Bin item missing: check whether it was permanently deleted, emptied, or excluded by size settings. Move to the next source without retrying the same one.
- No Previous Versions entries: the volume may lack restore points or shadow copies. Do not create new ones to "force" recovery without approval, since that writes to the disk.
- Restored file is corrupt: retain the copy, try the next older restore point, and do not overwrite the original attempt.
- Backup restore fails midway: stop, keep the partial output, and report the error text and time.
- Recovery tool suggests bulk scanning: decline without approval. Scanning writes logs and increases the risk of overwriting unrecovered data.

## Deliverable contract

Provide:

1. Summary of the loss stage and the chosen recovery source with timestamp.
2. Ordered list of actions taken, with approvals obtained.
3. Verification results against each check above.
4. Final locations of recovered items, and staging copies retained.
5. Remaining gaps, the reason for each, and the next recommended source.
6. Any version-sensitive steps flagged for documentation verification.

Do not: restore over originals without approval, empty Recycle Bin or delete shadow copies as cleanup, run unverified third-party recovery software, promise full recovery, or store recovered sensitive data outside the approved location.