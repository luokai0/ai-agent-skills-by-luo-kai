---
name: preference-and-default-configuration
description: Use when changing Windows user preferences, default applications, file associations, environment variables, or shell profiles on a workstation or managed endpoint, and the change must be scoped, reversible, and verified.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Preference And Default Configuration

## Purpose and boundaries

This skill covers changing user-level and machine-level Windows preferences: default apps and file associations, user environment variables, PowerShell profiles, display and input preferences, and similar settings. It produces a recorded, reversible change with evidence that the change took effect.

Out of scope: driver installation, OS feature enablement, domain policy authoring, security baseline changes, and anything that edits system files. Those require their own review path.

## Inputs and assumptions

Before acting, confirm:

- Target scope: current user only, or all users on the machine.
- Windows edition and build number (`winver` or Settings > System > About). Settings paths and registry layout vary by build; verify against current Microsoft documentation before relying on a specific path.
- Whether the device is managed by Intune, Group Policy, or another MDM. Managed settings may be reverted or locked.
- The exact desired value, the application or tool affected, and who requested it.
- Whether a backup of the current state is possible.

Assume nothing about the current value. Read it first.

## Operating workflow

1. **Capture current state.** Record the present value of every setting you will touch, with its location (registry key, environment scope, file path, or Settings page).
2. **Export a backup.** For registry keys, export the specific key to a dated `.reg` file. For environment variables, record the full before-value. For profiles, copy the file.
3. **Check for enforcement.** Look for policy keys under `HKLM\SOFTWARE\Policies` and `HKCU\SOFTWARE\Policies`, or MDM-managed indicators in Settings. If a policy controls the value, stop and report rather than overriding it.
4. **Choose the least-privileged mechanism.** Prefer the Settings UI or the supported application setting over direct registry edits. Use direct edits only when no supported path exists.
5. **Apply the single change.** Change one setting per step so failures are attributable.
6. **Verify** (see the verification section).
7. **Record the result** in the deliverable contract format.

Domain examples:

- Default browser or PDF viewer: use Settings > Apps > Default apps. Do not hand-edit the `UserChoice` registry values; Windows protects them with a hash, and manual edits are unreliable and may be reverted.
- User environment variable `EDITOR`: set at user scope, then open a new process to confirm it is inherited. Existing processes will not see the change.
- PowerShell profile: back up the file, append or edit only the target lines, and test by starting a new shell session with `-NoProfile` absent and confirming no errors.

## Decision gates

Stop and request explicit approval before:

- Deleting any registry key, value, file, or environment variable.
- Changing any setting at machine scope (`HKLM`, system environment variables) or for other users.
- Modifying a setting that is controlled by policy, MDM, or a corporate baseline.
- Any change that alters network, proxy, certificate, firewall, or credential behavior.
- Any change affecting remote systems, shared profiles, or settings synced to a cloud account.
- Any action that will require a restart or sign-out of a user session in use.

Proceed without further approval only when the change is user-scope, reversible from the backup, non-policy, and within the stated request.

## Verification and evidence

- Re-read the setting from its source location and compare to the intended value. Quote the observed value.
- For environment variables, start a new process and confirm the value is visible there.
- For default apps, open a file of the affected type and confirm the handler; record the application name shown.
- For profiles, confirm a new shell starts without error output.
- Confirm the backup file exists and is readable.

A change without a before-value, an after-value, and a confirming read is not complete.

## Failure handling

- If verification fails, restore from the backup immediately and re-verify the restored state.
- If a policy reverts the change, report the policy source; do not attempt to bypass it.
- If an export or backup fails, stop before making the change.
- If a restart is needed to confirm, state that explicitly and ask before restarting.
- Never retry a failing registry write in a loop or with escalated privileges without approval.

## Deliverable contract

Return:

1. Scope and mechanism used (Settings page, registry path, environment scope, or file).
2. Before-value and after-value for each setting.
3. Backup location and filename.
4. Verification performed and its observed result.
5. Any items requiring approval, unresolved policy controls, or build-specific paths still to be checked against current official documentation.

Do not state that a setting is "secure," "compliant," or "fixed" unless a verified check demonstrates it. Do not guess registry paths, cmdlet names, or flags; mark any unverified detail for confirmation.