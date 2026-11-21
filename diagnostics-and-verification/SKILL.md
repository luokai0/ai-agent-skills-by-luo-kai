---
name: diagnostics-and-verification
description: Use when diagnosing a Windows machine problem (crashes, slowness, service failures, network or driver faults, update errors) or verifying that a change actually fixed it, and the work needs read-only evidence collection, a hypothesis, and a measured before-and-after result.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Diagnostics And Verification

## Purpose and boundaries

This skill covers finding the cause of a Windows fault from evidence and confirming the result with measurements. It covers the investigation phase, the decision to change anything, and the post-change check.

It does not cover building new automation, hardening policy, forensic imaging, or incident response on a suspected compromise. If evidence points to malicious activity, stop and escalate.

## Inputs and assumptions

Collect before acting:

- Exact symptom, with timestamps and frequency.
- Windows edition and build (`winver` or `Get-ComputerInfo`), and what changed recently (updates, drivers, software, hardware, policy).
- Whether the session is elevated, and whether the machine is managed (domain, MDM, endpoint agent). Managed devices may have a change process you must follow.
- Whether a restore point, backup, or recovery media exists.

Assume nothing about cmdlet parameters or tool switches. Confirm them with `Get-Help <cmdlet> -Full` or the current Microsoft Learn documentation, because behavior varies across Windows builds and PowerShell versions. Mark any detail you could not verify as unverified in your report.

## Operating workflow

1. **Reproduce or bound the symptom.** Write a one-line problem statement: what, when, how often, who is affected.
2. **Collect read-only evidence.** Use Event Viewer or `Get-WinEvent` filtered by time window and level (System, Application, and relevant operational logs), Reliability Monitor, `Get-Service` state, `Get-CimInstance` for hardware and OS data, Device Manager or `pnputil /enum-devices` for driver status, `Test-NetConnection` for connectivity, and Task Manager or Resource Monitor for resource pressure. For crashes, note bugcheck codes and faulting modules from minidump metadata.
3. **Form ranked hypotheses.** List at most three candidate causes, each tied to a specific log entry or measurement. Rank by evidence strength, not by familiarity.
4. **Test the cheapest discriminating hypothesis.** Prefer a check that separates two hypotheses over one that merely confirms a favorite. Examples: boot into safe mode to test a driver; compare behavior on a second user profile to test profile corruption; check whether the fault follows the network or the machine.
5. **Stop at the decision gate** before any change.
6. **Apply the minimal reversible fix**, one change at a time, recording the exact command or setting and the prior state.
7. **Verify** using the criteria in the verification section.
8. **Document** cause, evidence, change, and residual risk.

## Decision gates

Pause and obtain explicit user approval before:

- Deleting, moving, or overwriting files, registry keys, or user data.
- Changing boot configuration, BitLocker state, partitions, or firmware.
- Installing, uninstalling, or rolling back drivers, updates, or security software.
- Altering services, scheduled tasks, firewall rules, or startup items on a shared or managed device.
- Anything that restarts a production system, disconnects a user, or sends data off the machine.
- Running repair tools that modify system files (for example, `sfc /scannow` or DISM repair operations) on a machine without a current backup.

Proceed without approval only for read-only collection and for reversible changes to your own test user profile.

## Verification and evidence

A fix is verified only when:

- The original symptom no longer reproduces across the same conditions, over a defined observation window (for example, 24 hours of normal use or a specific number of repeated operations).
- The triggering error event does not recur in the same log channel within that window.
- The metric that was abnormal (CPU, disk latency, boot time, connection success rate) returns to a baseline you recorded before the change.
- Unrelated services and functions still work.

Record evidence as: command or query used, timestamp, raw output excerpt, and interpretation. Separate observed facts from inferences.

## Failure handling

- **No cause found after evidence collection:** report what was checked and ruled out, state confidence, and recommend the next data to collect. Do not guess-and-change.
- **Change made but symptom persists:** revert the change, confirm reversion, then test the next hypothesis.
- **Change made and something else breaks:** revert immediately, then check whether the regression was your change or a pre-existing fault.
- **Insufficient access (not elevated, missing logs):** report the access gap; do not work around permissions.

## Deliverable contract

Return a report containing:

1. Problem statement and scope.
2. Evidence table: source, query, timestamp, key finding.
3. Ranked hypotheses with the result of each test.
4. Action taken, with approval reference, exact change, and rollback procedure.
5. Verification results against the criteria above, with observation window stated.
6. Residual risks, unverified details, and recommended follow-up.

Do not claim a fix is permanent, complete, or compliant unless the verification evidence supports that specific claim.