---
name: hardware-kernel-diagnostics
description: Use when investigating Linux hardware faults, kernel log errors, device driver failures, PCIe/NVMe/storage/network/GPU anomalies, thermal or power events, or machine check errors on a Linux host and a root cause or safe mitigation is needed.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Hardware Kernel Diagnostics

## Purpose and boundaries

This skill guides read-first diagnosis of hardware-related faults visible to the Linux kernel: kernel log (dmesg/journal) errors, device enumeration problems, driver resets, storage and filesystem I/O errors, PCIe link and AER events, memory error reports (EDAC/MCE), thermal throttling, and power or firmware-correlated anomalies.

In scope: collecting evidence, classifying fault domains, correlating events with time and hardware identity, recommending reversible mitigations, and producing a diagnostic report with confidence levels.

Out of scope: physical component replacement decisions without evidence, firmware flashing, BIOS/UEFI setting changes, kernel rebuilds, driver source patching, RAID or filesystem repair writes, and vendor warranty claims. These require the approval gates below.

## Inputs and assumptions

Required before starting:
- Host identity, kernel version (`uname -r`), distribution, and whether the host is production.
- Symptom statement with approximate start time and timezone.
- Access level: confirm whether you have read-only, sudo, or console access.
- Recent changes: kernel updates, firmware updates, hardware moves, driver installs, workload changes.

Assumptions to verify rather than accept: clock sync (NTP state), log retention (journal may be volatile), and whether the host runs a hypervisor (faults may belong to the host, not the guest).

## Operating workflow

1. **Freeze context.** Record kernel version, uptime, boot ID, and the current time. Note whether logs persist across boots (`journalctl --list-boots` shows availability).
2. **Capture kernel errors.** Pull warnings and errors for the relevant window, e.g. `journalctl -k -p warning --since "<start>"`, and for the previous boot if a reboot occurred (`-b -1`). Save raw output before filtering.
3. **Inventory hardware.** Use `lspci -nnk`, `lsblk -o NAME,MODEL,SERIAL,TRAN,HCTL`, and `lscpu`. Map each error-reporting device to a bus address or block device.
4. **Classify the fault domain.** Assign each event to one of: storage, PCIe/link, memory, CPU/machine check, thermal/power, network, GPU/accelerator, firmware/ACPI, or software-induced (driver bug, misconfiguration).
5. **Check counters and health.** Read device-native health data where a read-only tool exists: SMART/NVMe log pages (`smartctl -a` or `nvme smart-log`), EDAC counters under `/sys/devices/system/edac/`, AER counters under `/sys/bus/pci/devices/*/aer_dev_*`, and thermal zones under `/sys/class/thermal/`. Record values with timestamps; a single snapshot is weak evidence.
6. **Correlate.** Align kernel events, workload spikes, and maintenance windows on one timeline. A fault that starts at the same second as a firmware update or a cooling change is a lead, not a conclusion.
7. **Reproduce only when safe.** Repeat a read-only trigger (e.g., `fio` read-only job against a non-critical device) only after approval.
8. **Rank hypotheses** and state the discriminating test for each.

## Decision gates

- **Gate A (scope):** If the host is production and the symptom is data-affecting (I/O errors, corruption, unexpected reset), stop non-read actions until the owner approves.
- **Gate B (writes):** Any command that modifies state requires explicit approval: driver unload/reload, device reset (`echo 1 > .../reset`), PCI remove/rescan, `nvme format`, `smartctl -t` self-tests (they add load), filesystem check with repair, sysctl changes, module parameter changes, reboot, firmware update.
- **Gate C (external impact):** Opening vendor tickets, sending logs or serial numbers outside the organization, or contacting the hardware vendor requires approval and data-minimization review (strip hostnames, IPs, user data).
- **Gate D (sensitive data):** Kernel logs can contain usernames, IPs, and file paths. Redact before sharing.
- **Escalate to hardware replacement** only when at least two independent indicators agree (e.g., rising SMART media errors plus repeated AER correctable errors on the same slot) and the failure reproduces across a boot or a re-seat-free check.

Decision criteria examples:
- Corrected memory errors rising on one DIMM across days: replacement candidate after confirmation via EDAC per-DIMM counters.
- Single `AER: Corrected error` with no recurrence over a week: monitor, do not act.
- `nvme nvme0: I/O ... timeout` followed by controller reset with clean SMART: investigate driver, firmware level, and power states before blaming media.
- `mce: [Hardware Error]` with CPU temperature events: correlate with cooling and load before concluding CPU fault.

## Verification and evidence

Quality checks for a completed diagnosis:
- Every claim cites a log line or counter with timestamp and boot ID.
- Each hypothesis lists one confirming and one refuting observation.
- At least two independent data sources support any hardware-fault conclusion.
- Counters were sampled at least twice with an interval, and deltas are reported.
- Tool versions and output formats are recorded. Smartctl, nvme-cli, and kernel EDAC/AER interfaces change across releases; confirm flag names and output fields against the current official man pages and kernel documentation before relying on them.
- Benchmark or throughput numbers are reported only as measured in this environment, never as expected vendor figures.

## Failure handling

- **No logs available:** State that the window is unobservable; recommend enabling persistent journaling as a proposed change requiring approval.
- **Tool missing or restricted:** Fall back to sysfs and procfs reads; do not install packages without approval.
- **Contradictory evidence:** Keep both hypotheses open, identify the single test that separates them, and request approval if that test is a write.
- **Error storm hides signal:** Rate-limit by device and time bucket before counting.
- **Host becomes unstable during diagnosis:** Stop active tests, preserve logs, and escalate to the owner immediately.

## Deliverable contract

Produce a report containing:
1. Summary: symptom, affected components, current status, and confidence (high, medium, low).
2. Timeline: ordered events with timestamps, boot IDs, and sources.
3. Evidence table: observation, source command or path, value, delta over time.
4. Fault domain classification and ranked hypotheses with discriminating tests.
5. Actions taken, with approval references for any write operation.
6. Recommended next steps: reversible first, each tagged with its gate.
7. Open items and unverified assumptions, including any version-sensitive command details flagged for official-documentation confirmation.

Do not state a root cause without evidence meeting the verification checks. Do not recommend hardware replacement without Gate E-level evidence. Do not run destructive commands, reboot, or alter firmware or BIOS settings on your own initiative, and do not share unredacted logs outside the owning team.