---
name: storage-recovery-continuity
description: Use when a Linux host has degraded or failed storage (filesystem errors, read-only remounts, failed RAID or LVM members, disk I/O errors, full volumes, corrupted boot or data partitions) and service continuity or data preservation must be restored with a documented, evidence-based recovery plan.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Storage Recovery Continuity

## Purpose and boundaries

This skill guides diagnosis and recovery of storage faults on Linux systems so that data is preserved, service continuity is restored or planned, and every change is traceable. It covers: block device health, partition tables, software RAID (md), LVM, local filesystems (ext4, XFS, Btrfs, vfat), mount state, and filesystem-level repair decisions.

It does not cover: SAN or cloud volume provisioning, hypervisor storage, database-internal page repair, backup product administration, or forensic evidence handling for legal matters. Hand those to the owning team with the evidence package defined below.

## Inputs and assumptions

Collect before acting:

- Hostname, distribution, kernel version (`uname -r`), and whether the host is physical, VM, or container-hosted.
- Symptoms with timestamps: kernel log excerpts, application errors, mount failures.
- Current layout: `lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,RO`, `findmnt`, `cat /proc/mdstat` if md is used, `pvs`/`vgs`/`lvs` if LVM is used.
- Recent changes: patches, firmware updates, power events, disk replacements, resizes.
- Backup status: most recent verified backup time and whether it has been restored in a test.

Assumptions to state explicitly in the plan: the host may be in a degraded state, writes may worsen damage, and the most recent good backup is unknown until verified.

## Operating workflow

1. **Freeze writes.** If the affected filesystem is still mounted read-write and showing errors, remount read-only or stop the consuming service. Record the action and time.
2. **Capture state before touching anything.** Save `dmesg -T`, `journalctl -k -b`, SMART data (`smartctl -a`, from the smartmontools package), md and LVM status, and `lsblk` output to a directory on a different device.
3. **Assess hardware.** Check SMART attributes such as reallocated, pending, and uncorrectable sectors, plus controller and cable errors (CRC counts). Treat rising counts as active failure.
4. **Image failing media first.** If a disk shows read errors or SMART failure, clone it with a tool that tolerates read errors (for example `ddrescue` with a mapfile) to a healthy target. Repair operations run on the clone, never on the original.
5. **Assess the software stack bottom-up.** Confirm md arrays are assembled and clean or degraded with a known-good member set; confirm LVM physical volumes are present; then check the filesystem.
6. **Run filesystem checks only on unmounted or read-only devices** using the matching tool in dry-run or no-change mode first (for example `e2fsck -n`, `xfs_repair -n`, `btrfs check` without `--repair`). Read the dry-run output before deciding.
7. **Apply the approved repair** on the clone or, if approved, on the original.
8. **Verify and restore service** using the checks below, then return to normal operations and schedule follow-up.

## Decision gates

Stop and request explicit written approval before any of the following:

- Running any repair mode (`--repair`, `-y`, fix flags) against the original device.
- Running `mkfs`, `wipefs`, `pvremove`, `vgreduce`, `lvremove`, `mdadm --create`, or any command that rewrites metadata.
- Replacing, removing, or failing a RAID member, or forcing array assembly with `--force`.
- Restoring from backup over existing data, or restoring to a location that holds live data.
- Any action that affects other hosts, shared storage, tenants, or external customers.
- Anything touching data classified as sensitive or regulated, including sending copies off-host.

Choose the recovery path using these criteria:

- **Clone-and-repair** when hardware errors are active or SMART is failing. Mandatory first.
- **Metadata-only repair** when hardware is healthy and the dry-run reports superblock or journal inconsistencies with a clear fix.
- **Restore from backup** when dry-run shows damage to a large fraction of inodes or extent trees, or when the repaired result would be unverifiable. Restore to a new target, then cut over.
- **Escalate** when a RAID set has lost more members than its redundancy allows, or when the vendor controller holds the metadata.

## Verification and evidence

A recovery is complete only when all of these hold:

- Post-repair filesystem check returns clean, and the dry-run and repair logs are archived.
- `dmesg` shows no new I/O or filesystem errors for at least one full business cycle or a defined observation window agreed in the plan. Record the window length.
- md arrays report all members active and sync complete (`/proc/mdstat`), or the degraded state is accepted and documented with a replacement ticket.
- LVM volumes are active and the expected sizes match `lvs` output.
- Checksums or application-level consistency checks match on a sample of critical files or records, with sample size and method stated.
- A restore test has been performed from the current backup set if a restore was used.

Measurable quality checks: zero unacknowledged I/O errors in the observation window; 100% of expected mounts present in `findmnt`; sample verification pass rate of 100% on the defined critical set.

## Failure handling

- If the clone fails repeatedly on the same sector range, stop, record the LBA range, and escalate to hardware replacement or a specialist service. Do not retry in a loop.
- If a repair tool reports it cannot proceed, do not force it. Keep the output and re-run dry-run against a fresh clone.
- If service is restored but errors recur, treat the recovery as failed, re-freeze writes, and return to step 2.
- If backup verification fails, do not declare the backup valid; locate the next older set.
- If a command produces unexpected output not covered here, stop and report the exact output rather than improvising.

## Deliverable contract

Produce a written recovery record containing:

1. Incident summary: host, time of first symptom, time writes were frozen, current service state.
2. Evidence bundle: the captured logs, SMART output, and layout listings, with paths.
3. Chosen recovery path and the decision gate reasoning.
4. Approval record: who approved each gated action and when.
5. Actions taken, in order, with exact commands and their exit status.
6. Verification results against each check above, with measured values.
7. Residual risk, open items, and owner for each.
8. Follow-up: replacement orders, backup policy changes, and a scheduled re-verification date.

Mark any command syntax or tool behavior as version-sensitive and confirm it against current official documentation for the installed distribution before execution.