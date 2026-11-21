---
name: system-state-discovery
description: Use when you need a read-only inventory of a Windows machine's current state (OS, hardware, drivers, services, network, startup, scheduled tasks, installed software, event history, or security configuration) to diagnose a problem, prepare a change, document a baseline, or hand off an unfamiliar host.
author: Luo Kai
provenance: original
version: 1.0.0
---

# System State Discovery

## Purpose and boundaries

This skill produces an accurate, timestamped snapshot of a Windows host's configuration and runtime state using read-only queries. It answers "what is running, configured, and recorded right now," not "what should be changed." Remediation, tuning, and policy decisions belong to other skills or require explicit approval under the gates below.

In scope: OS build and edition, hardware summary, driver inventory, services, scheduled tasks, startup entries, network adapters and routes, installed programs and updates, local accounts and group membership, firewall profile state, recent System and Application event log entries, disk and volume health indicators.

Out of scope: modifying any setting, installing or removing software, collecting secrets (password stores, tokens, private keys, browser data), dumping process memory, and scanning other hosts.

## Inputs and assumptions

Before starting, confirm:

1. Target host name and whether it is the local machine or a remote one. Remote discovery requires approval (see Decision gates).
2. The question being answered. A discovery aimed at a disk-space fault collects different depth than a baseline for audit.
3. Privilege level. Some queries (Security log, certain driver details, BitLocker status, full account enumeration) fail or return partial data without elevation. Record which queries were skipped and why rather than silently omitting them.
4. Time window for event logs (default: last 72 hours unless the incident timeline says otherwise).
5. Output destination. Snapshots may reveal internal topology and usernames; treat them as sensitive.

Assume PowerShell 5.1 is present on Windows client and server builds unless the host is known to differ. Cmdlet availability and property names vary across Windows versions; verify any property you rely on against current Microsoft Learn documentation for that build rather than assuming it.

## Operating workflow

1. Record context: hostname, current user, elevation status, local time and time zone, and the reason for discovery. Write this first so the snapshot is interpretable later.
2. Collect OS and hardware identity using CIM classes such as the operating system, computer system, BIOS, processor, and physical memory classes. Capture build number, not only marketing name.
3. Enumerate services with startup type and current state. Flag services set to automatic that are stopped, and services whose binary path is outside the Windows directory or a known vendor path.
4. Enumerate scheduled tasks, excluding Microsoft-authored tasks in the first pass. Record author, action path, trigger, and last run result.
5. Capture startup entries from the common registry Run keys and the Startup folders for the current and all-users profiles. Read only; do not edit.
6. Capture network state: adapters with link status, IP configuration, DNS server addresses, default routes, and listening TCP ports with owning process ID. Map PIDs to process names.
7. Capture installed software from the uninstall registry hives (both 64-bit and 32-bit views) and installed hotfixes. Note that Win32 product enumeration is slow and can trigger reconfiguration; avoid it unless specifically needed.
8. Capture driver inventory with the signed-driver query and flag unsigned or third-party drivers with dates older than the OS build.
9. Query event logs for Critical and Error levels in System and Application over the time window, grouped by provider and event ID. Do not dump full logs into the snapshot.
10. Capture security posture: firewall profile enabled state, Defender real-time protection status if the module is present, BitLocker volume status, and local Administrators group members.
11. Store results in a single structured file per section, plus a summary index.

## Decision gates

- Stop and request approval before any remote query, any query requiring credentials you were not given, or any action touching other users' profiles.
- Stop before exporting the snapshot outside the originating team or ticket system.
- Stop if a query would require enabling logging, changing a policy, or installing a module. Record the gap instead.
- Proceed without approval only for local, read-only queries within the stated time window.
- If the host is a domain controller, a production database server, or a safety-relevant system, limit to lightweight CIM and event queries and avoid software inventory enumeration that can load the system.

## Verification and evidence

Each section must include the command or query used, the timestamp, the privilege level, and the record count. A section with zero results must say "zero returned" rather than being omitted.

Cross-check at least two independent sources for critical facts: the OS build from CIM and from the registry build key; the service list from the service cmdlets and the service registry hive for any service flagged as anomalous; the listening port owner from the network query and the process list.

Quality checks before handoff:
- Every query in the workflow is either present in the output or listed under "skipped" with a reason.
- No section mixes local and remote data without labeling.
- Timestamps are in one stated time zone.
- Counts in the summary match the detail files.
- No secrets, tokens, or full credential material appear anywhere.

## Failure handling

If a query throws an access error, retry once only if elevation is now available; otherwise record it as skipped. If a CIM query hangs, cancel it, record the timeout, and check the WMI repository health as a separate read-only step. If event log queries return truncated results, state the truncation and narrow the time window rather than assuming absence. If a property is missing on the build, record the missing property and the build number; do not substitute a guessed value.

## Deliverable contract

Deliver:
1. A context header (host, user, elevation, timestamp, time zone, purpose).
2. A summary table of counts per section and any flagged anomalies, each with the evidence reference.
3. Section files for OS and hardware, services, tasks, startup, network, software and updates, drivers, events, and security posture.
4. A skipped-items list with reasons.
5. A sensitivity label on the package and a note on who may receive it.

Do not present inferred root causes as findings. Label interpretations separately as hypotheses requiring follow-up.