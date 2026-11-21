---
name: network-time-connectivity
description: Use when a Linux host cannot reach, synchronize with, or stay accurately synced to its configured NTP or time sources, or when clock drift is traced to network path, DNS, firewall, or time-daemon reachability issues.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Network Time Connectivity

## Purpose and boundaries

This skill diagnoses why a Linux host cannot reach its time sources and restores reliable network time synchronization. It covers name resolution of time servers, UDP/123 path reachability, firewall and proxy interference, time-daemon configuration (chrony, ntpd, systemd-timesyncd), and reachability evidence from the daemon itself.

It does not cover hardware clock failure analysis, PTP or precision timing hardware design, leap-second policy, or application-level timestamp logic. Escalate those separately.

## Inputs and assumptions

Collect before acting:

- Distribution, init system, and the active time daemon (determine it from the running service, not from installed packages alone).
- Configured sources: `pool`, `server`, or `peer` entries and any DHCP- or cloud-provided sources.
- Whether the host is on a restricted network, behind an egress proxy, or in a segmented VPC or VLAN.
- Current clock offset and the time of last successful sync.
- Change window and owner approval status for config or firewall changes.

Assume nothing about upstream NTP availability until tested. Assume the host has no network access to public pools unless proven otherwise.

## Operating workflow

1. Record baseline state: current offset, daemon status, last sync time, and the configured source list. Save output to the incident record before changing anything.
2. Confirm the daemon's own view. Query the daemon's source table (for chrony, `chronyc sources -v`; for ntpd, `ntpq -p`; for systemd-timesyncd, check `timedatectl` status output). Note each source's reachability or poll state.
3. Resolve each configured hostname with the system resolver. A name that fails here fails in the daemon. Test with the same resolver path the daemon uses.
4. Test UDP/123 reachability per source. Use a time-aware client query where possible rather than ICMP, since ICMP success does not prove NTP reachability. Check the source's response, stratum, and offset.
5. If DNS and UDP succeed from the host but the daemon shows unreachable, inspect daemon config, bind address, and any AppArmor or SELinux denial in the audit log.
6. If UDP fails, trace the path: local firewall rules, cloud security groups, network ACLs, upstream NAT, and egress proxy policy. Identify the exact hop or policy that drops traffic.
7. Apply the smallest fix that restores reachability to at least two independent sources, then confirm sync.
8. Verify after a full poll cycle, not immediately after restart.

## Decision gates

- Gate A, DNS failure: if names do not resolve, fix resolver configuration first. Do not add raw IP sources as a workaround without approval, because IPs may change or be unauthorized.
- Gate B, firewall or security-group change: requires explicit approval from the network or security owner. State the exact rule, scope, and rollback.
- Gate C, source change: switching to a new or internal time source changes trust boundaries. Requires explicit approval and confirmation the source is authorized.
- Gate D, clock step: stepping a clock with a large offset can break databases, certificates, and Kerberos. Confirm the offset magnitude and get approval for a step before running it. Prefer slewing where the daemon permits.
- Gate E, daemon replacement or config rewrite: obtain approval and keep a backup of the original config.

## Verification and evidence

A fix is complete only when all of the following hold:

- At least two configured sources show reachable state with recent successful polls.
- The daemon reports synchronized status and offset below the threshold defined by the owning team (default assumption: under 100 ms unless the service requires tighter bounds).
- Offset remains stable across three consecutive polls.
- The fix survives a reboot or service restart, confirmed by a second check.

Keep raw command output as evidence. Do not report "fixed" from a single green line.

## Failure handling

- If no source becomes reachable, stop changing rules. Report the failed hops and the evidence.
- If the offset grows during troubleshooting, do not force a step without Gate D approval. Escalate.
- If a firewall rule was added and reachability is still broken, remove the rule after recording it and restore prior state.
- Do not disable time synchronization to silence alerts.

## Deliverable contract

Produce a report with:

1. Summary: host, daemon, root cause category, and final status.
2. Baseline and final offset with timestamps.
3. Source table before and after.
4. Commands run and their key outputs.
5. Changes made, with approvals referenced and rollback steps.
6. Open risks and follow-up owners.

Version-sensitive details (exact daemon subcommands, output formats, and systemd tooling options) must be verified against current official documentation for the installed version before being used in a production runbook.