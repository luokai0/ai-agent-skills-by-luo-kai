---
name: security-access-hardening
description: Use when auditing or tightening access controls on Linux hosts, including SSH configuration, local accounts, sudo policy, file permissions, service privileges, and firewall exposure, and a change must be planned, verified, and rolled back safely.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Security Access Hardening

## Purpose and boundaries

This skill covers reducing unnecessary access on Linux systems: authentication paths (SSH, console, PAM), privilege escalation (sudo, setuid, capabilities), account hygiene (users, groups, service accounts, shells, password aging), filesystem permissions on sensitive paths, and network reachability of administrative services.

It does not cover application-level authorization logic, malware removal, kernel exploit remediation, cloud IAM policy, or compliance attestation. Do not claim a host is "compliant" or "secure"; report which checks passed, failed, or were not run.

## Inputs and assumptions

Before changing anything, collect:

- Host inventory: hostname, distribution and release, init system, role, and owner.
- Current access paths: SSH listening ports, `AllowUsers`/`AllowGroups` settings, console access, out-of-band management.
- Business-critical sessions that depend on current access (automation, backups, monitoring agents).
- Change window, rollback owner, and an out-of-band recovery path (console, hypervisor, or IPMI) confirmed working.
- Existing configuration management (Ansible, Puppet, Salt, or none). Changes made outside it will be reverted.

Assume a hardening change can lock out operators. Treat a live session as your only proof of access until a second independent session succeeds.

## Operating workflow

1. **Baseline capture.** Record the current state before editing: `sshd -T` output (effective config, not file contents), `sudo -l` for each relevant account, `getent passwd` and `getent group`, `ss -tlnp` for listeners, `find` for setuid/setgid files and world-writable paths, and `ls -l` on `/etc/sudoers.d`, `/etc/ssh`, and `/root`. Save to a timestamped evidence directory.
2. **Identify exposure.** Rank findings by reachability and privilege: unauthenticated network services first, then password-based remote login, then local privilege paths, then hygiene items.
3. **Draft minimal changes.** One control per change. Prefer dropping files into include directories (`/etc/ssh/sshd_config.d/`, `/etc/sudoers.d/`) over editing vendor files. Validate sudoers drafts with `visudo -cf <file>` and SSH drafts with `sshd -t` before reload.
4. **Stage on a non-production host** when one exists with equivalent configuration.
5. **Apply with a safety net.** Keep an existing root or admin session open. Apply the change, then open a new session from a separate terminal before closing the original.
6. **Verify** (see Verification section).
7. **Record** the final state and the rollback command for each change.

## Decision gates

Stop and obtain explicit written approval before:

- Disabling password authentication, root login, or any login method on a host without a verified key-based admin account.
- Changing sudo policy for any account that performs automation or break-glass access.
- Removing accounts, deleting home directories, or changing UID/GID of existing users or services.
- Modifying firewall rules on a remote host where the management path traverses the rule set.
- Any action affecting shared, production, or externally reachable systems.
- Changing file ownership or permissions on paths used by running services.

Proceed without a gate only for read-only inspection, drafting, and validation in a non-production copy.

Use these criteria when choosing a setting:

- Remove a setuid bit only if the binary is not required by an installed package and the package manager can reinstall it.
- Restrict `AllowUsers` to named accounts only after confirming every automation identity is listed.
- Prefer `PermitRootLogin prohibit-password` over `no` when out-of-band root recovery is the only fallback; choose `no` only when an alternative admin account is verified.

## Verification and evidence

Each change requires:

- Syntax check passed (`sshd -t`, `visudo -c`, or the equivalent for the modified file).
- Effective configuration matches intent (`sshd -T | grep -i <directive>`).
- A new session succeeds with the intended identity and fails with a disallowed one (test with a non-admin account; expect denial).
- Listener set matches the approved list (`ss -tlnp` diff against baseline).
- Permission changes confirmed with `stat -c '%U:%G %a %n' <path>`.
- Service restart or reload succeeded and `systemctl status` shows active.

Evidence package: baseline output, diffs, validation output, test session transcripts (credentials redacted), and rollback commands. Do not include private keys, password hashes, or tokens in evidence.

Mark any command output that depends on distribution or OpenSSH version as "verify against current official documentation" when the exact directive behavior is uncertain.

## Failure handling

- **Validation fails:** do not reload. Revert the draft and fix the syntax.
- **New session fails after reload:** do not close the original session. Revert the change, confirm the original session still works, then investigate.
- **Lockout occurs with no session:** use the pre-confirmed out-of-band path. Do not attempt repeated failed logins, which may trigger lockout or fail2ban bans.
- **Automation breaks after change:** restore the prior configuration, then map which identity or port the job uses before retrying with an explicit allow entry.
- Log every failure with timestamp, command, and observed output.

## Deliverable contract

Deliver a report containing:

1. Scope and host list, with the approval reference for each gated action.
2. Findings table: item, risk level, evidence reference, status (fixed, deferred, accepted with reason).
3. Applied changes: exact file paths, before and after values, and rollback command.
4. Verification results with pass/fail per check.
5. Open items and residual risk, stated plainly.
6. Confirmation that out-of-band access was tested, or an explicit statement that it was not.

Do not state that a host is hardened, secure, or compliant. State only what was changed and what was verified.