---
name: services-packages-desktop-workloads
description: Use when installing, removing, upgrading, or auditing Linux system services, software packages, or desktop workloads (login sessions, autostart entries, user units, display-manager-launched apps) on a workstation or server and needing a safe, verifiable change with rollback.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Services Packages Desktop Workloads

## Purpose and boundaries

This skill governs changes to three layers of a Linux system:

1. **Packages**: installation, removal, upgrade, pinning, and inventory via the host's native package manager (for example apt, dnf, zypper, pacman, or a Flatpak/Snap runtime when one is in use).
2. **Services**: systemd system units and user units, including enable/disable state, runtime start/stop, drop-in overrides, and unit ordering.
3. **Desktop workloads**: per-user graphical applications, XDG autostart entries, session-scoped processes, and display-manager-launched components.

In scope: diagnosing why a service or app misbehaves, planning a package change, executing it in a reversible order, and proving the end state.

Out of scope: kernel changes, bootloader edits, disk partitioning, network firewall policy, identity or access policy, and fleet-wide configuration management design. Refer those to the owning procedure.

## Inputs and assumptions

Before acting, collect:

- Distribution, release, and init system (confirm systemd with `systemctl --version`; do not assume).
- Target: host name, role (workstation, server, container host), and whether it is production.
- Requested change in one sentence, plus the business reason.
- Current state snapshot: installed package versions, enabled and active units, autostart entries for affected users.
- Whether a recent backup or VM snapshot exists and its restore path.
- Whether the package source is an official repository, a vendor repository, or a local file.

Assume nothing about flags, unit names, or package names. Verify them on the host with `--help`, `man`, `apt-cache policy`, `systemctl list-unit-files`, or equivalent. Treat any command syntax recalled from memory as unverified until checked against the installed version's documentation.

## Operating workflow

1. **Snapshot.** Record `systemctl list-unit-files --state=enabled`, `systemctl --failed`, the package list for affected names, and the relevant user's `~/.config/autostart/` contents. Save output to a dated file outside the change path.
2. **Identify dependencies.** For packages, query reverse dependencies before removal (apt: `apt-cache rdepends`; rpm-based: `rpm -q --whatprovides` and `dnf repoquery --whatrequires`, verifying syntax locally). For units, check `systemctl list-dependencies` and `Wants=`/`Requires=`/`WantedBy=` relations.
3. **Stage the change.** Prefer a drop-in override (`systemctl edit <unit>`) over editing vendor unit files under `/usr/lib/systemd`. Prefer disabling over masking unless masking is required to block activation.
4. **Dry run where supported.** Use simulation modes the package manager provides, and review the full list of packages to be removed or upgraded, not just the requested one.
5. **Execute one step at a time.** Apply the package change, then reload systemd only if unit files changed (`systemctl daemon-reload`), then restart the affected unit.
6. **Verify** (see the verification section), then record the post-change snapshot.

Desktop workloads follow the same order, but verification occurs inside the user session. Confirm the target user is logged in before testing graphical behavior, and never run session-scoped commands as root on the user's behalf without stating why.

## Decision gates

Stop and request explicit approval before proceeding when any of the following holds:

- The action removes packages, purges configuration, deletes data directories, or disables a unit that other units require.
- The change touches a production host, a shared server, or a host you do not control.
- The action sends data externally, opens network listeners, or changes repository trust (adding keys or sources).
- The package change would upgrade a library that multiple services link against, or the reverse-dependency list is longer than the change's stated scope.
- A service is a security control (audit, endpoint protection, authentication agent, backup agent).
- Restart would interrupt active user sessions or running jobs.
- Any step is irreversible or its rollback path is unknown.

Proceed without a gate only for read-only inspection, reversible enablement of a unit on a non-production host, and installation of an already-approved package in a test environment.

## Verification and evidence

A change is complete only when all of these hold, with evidence captured:

- `systemctl is-active <unit>` and `systemctl is-enabled <unit>` return the intended values; `systemctl --failed` shows no new entries.
- `journalctl -u <unit> --since "<change start>"` contains no new errors or repeated restart loops within a defined observation window (for example, 10 minutes for services, one full login for desktop autostart).
- Package state matches the plan: the package manager reports the expected version, and no unintended removals appear in the transaction log.
- For desktop workloads, the application launches in the target user's session, its autostart entry produces a process owned by that user, and the process is absent when the entry is disabled.
- A reboot test is performed when boot ordering or enablement changed, and the result is recorded.

Evidence means saved command output with timestamps, not a claim of success.

## Failure handling

- **Failed restart:** capture `systemctl status` and the journal, revert the override or re-enable the previous state, and run `systemctl daemon-reload` if unit files changed.
- **Broken dependency during install:** do not force resolution with flags that ignore dependencies. Roll back the transaction using the package manager's history mechanism where available.
- **Desktop app crashes at login:** disable its autostart entry for that user, confirm the session is clean, then diagnose from the user's session journal and application logs.
- **Unknown behavior after upgrade:** restore from the snapshot or VM image rather than patching piecemeal on a production host.

Do not retry a failing action more than twice without new information.

## Deliverable contract

Every completed task returns:

1. Change summary: what was changed, on which host, by which user, and why.
2. Before and after snapshot references.
3. Exact commands executed, with the verified flag syntax noted.
4. Verification results against each criterion above, with pass or fail.
5. Rollback procedure, tested or explicitly marked untested.
6. Open risks and any item that required approval, with the approver's recorded confirmation.
7. Version-sensitive details (package versions, command options, unit behaviors) marked "verify against current official documentation" where they were not confirmed on the host.

## What not to do

- Do not use `rm -rf`, purge flags, or `--force` options to clear obstacles without approval.
- Do not edit files under `/usr/lib/systemd` or other vendor-owned paths.
- Do not mask units or disable security agents on a production host without a gate.
- Do not add third-party repositories or import signing keys without approval.
- Do not restart shared services during active business hours without approval.
- Do not report a change as successful based only on the command exiting zero.
- Do not state compliance, security, or performance outcomes that were not measured.