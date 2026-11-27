---
name: "Windows Development, Source Control, and Virtualization: Discover Current State"
description: "Inspect developer toolchains, SDKs and runtimes, Git repositories and branches, WSL distributions, virtual machines, and container tooling while preserving secrets and uncommitted work."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0009"
  version: "1.2.0"
---

# Windows Development, Source Control, and Virtualization: Discover Current State

## Objective

Establish a verified baseline of a Windows developer workstation, installed editors and SDKs, project-local configuration, Git repository state, WSL distributions, virtual machines, and container tooling. Preserve environment secrets, uncommitted work, VM disks, container volumes, and host/guest boundaries. This is read-only discovery: do not edit PATH, install tools, modify Git history, delete distributions, or change VM/container state without a separate request and explicit approval.

## When to use

Use for:
- Editors, SDKs, compilers, runtimes, environment variables, and local development setup.
- Repository discovery, status, branches, diffs, commits, remotes, and conflict resolution.
- WSL distributions, Hyper-V/virtualization status, VM lifecycle, and container tooling.

Applies to Windows 10 and Windows 11 developer workstations, including managed devices.

## Required operating discipline

1. Identify the exact device, user/session, project, executable, repository, branch, WSL distribution, VM, or container.
2. Observe before acting. Record current tool versions, executable paths, Git status, distribution/VM identity, and resource/network context only as relevant.
3. Prefer read-only tool discovery and native application surfaces. Use project-local environments where possible.
4. Never expose environment secrets, access tokens, credentials, private remotes, or command lines that may contain secrets.
5. Inspect Git status and uncommitted work before any repository mutation. Never force-push, rewrite shared history, or discard work.
6. Obtain explicit approval before installs, PATH-wide edits, history rewrites, destructive VM/container actions, or changes that affect shared repositories.
7. Keep discovery read-only. Do not turn a status request into an unrequested repair.

## Environment and target identification

Confirm Windows edition/build, architecture, current user/session, and whether the device is local, remote, virtual, or organization-managed.

For developer tools, confirm executable path, version, architecture, and project-local configuration. For Git, confirm repository root, current branch, remote identity, and working-tree state. For WSL and virtualization, distinguish host from guest, distribution from VM, and container from persistent volume. Never infer target identity from a display name alone.

## Domain profiles

### A. Developer workstation and toolchain

**Scope:** Editors, SDKs, compilers, runtimes, environment variables, and local development setup.

**Preferred tools:** Get-Command, where.exe, dotnet --info, python --version, node --version, code --version.

**Inspection:** Check executable path, version, architecture, project-local configuration, and reproducible build result where a build has already been run. Distinguish global tools from project-local versions.

**Safety:** Avoid PATH-wide edits, untrusted extensions, arbitrary install scripts, and exposing environment secrets. Do not print entire environment variables or configuration files that may contain credentials.

**Verification:** Check executable path, version, architecture, project-local configuration, and existing build output.

**Recovery:** Prefer project-local environments and reversible settings; capture exact toolchain diagnostics.

**Read-only examples:**
```powershell
Get-Command python, node, dotnet, git -ErrorAction SilentlyContinue | Select-Object Name, Source
python --version
node --version
dotnet --info
```

### B. Git and source control

**Scope:** Repository discovery, status, branches, diffs, commits, remotes, and conflict resolution.

**Preferred tools:** git status, git remote -v, git diff --check, git log --oneline, and Git GUI.

**Inspection:** Verify repository root, branch, working-tree state, staged/unstaged changes, recent commits, remotes, and whether changes have been pushed. Redact private remote URLs and credentials.

**Safety:** Never force-push, rewrite shared history, discard work, or expose tokens. Inspect status before every mutation. Do not assume a clean working tree from a branch name.

**Verification:** Verify branch, clean/expected diff, commit hash, remote identity, and pushed state when applicable.

**Recovery:** Stash or back up only with approval; preserve uncommitted changes and resolve conflicts explicitly.

**Read-only examples:**
```powershell
git status --short --branch
git diff --check
git log -5 --oneline
git remote -v
```

### C. WSL, virtual machines, and containers

**Scope:** WSL distributions, Hyper-V/virtualization status, VM lifecycle, and container tooling.

**Preferred tools:** wsl --status, wsl --list --verbose, systeminfo, virtualization settings, and Docker/Podman UI.

**Inspection:** Verify distribution/VM identity, resource allocation, network mode, host/guest paths, container identity, and persistent volume relationships. Distinguish the Windows host from each guest environment.

**Safety:** Do not delete distributions, VM disks, containers, or volumes without explicit confirmation and a verified backup. Do not alter networking or virtualization settings during discovery.

**Verification:** Verify distro/VM identity, resource allocation, network mode, and guest health. Check persistent volume identity before considering any future cleanup.

**Recovery:** Export or snapshot before approved destructive maintenance; distinguish host and guest paths.

**Read-only examples:**
```powershell
wsl --status
wsl --list --verbose
systeminfo
```

## Unified discovery workflow

1. **Bind the request.** Select relevant profile(s). Confirm device/session, project/repository, toolchain executable, branch, WSL distro, VM, or container identity.
2. **Capture a baseline.** Observe native UI and use bounded read-only commands. Record only relevant versions, paths, Git state, or guest configuration.
3. **Inspect narrowly.** Do not dump environment secrets, entire config files, private remote URLs, or unrelated repository contents.
4. **Resolve ambiguity.** If multiple tool versions, repositories, branches, distributions, VMs, or volumes match, stop and ask for clarification.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, impact, dependencies, backup/rollback plan, and approval requirements.
6. **Verify independently.** Recheck executable path/version, Git status/diff, or guest identity/resource state in a second native surface when practical.
7. **Close the loop.** Report findings, uncommitted changes, unavailable tools, blocked checks, and remaining risk. Do not claim a build, push, or VM change succeeded unless verified.

## Stop conditions and recovery

Stop if tool identity is ambiguous, a secret may be exposed, the repository contains uncommitted work, a remote is private and not approved for disclosure, a VM/container target is unclear, or a destructive operation is proposed without backup.

Preserve the last known-good state. Retry at most once through a lower-risk read-only route. Never edit PATH, execute arbitrary install scripts, force-push, discard work, delete VM disks/volumes, or remove WSL distributions as an improvised workaround.

## Privacy-safe evidence and handoff

Report tool name/version/path, repository and branch using redacted remotes, Git working-tree state, distribution/VM identity, and relevant resource/network state. Do not include environment secrets, tokens, credentials, private remote URLs, private file contents, or unnecessary VM identifiers.

## Completion checklist

- [ ] Device/session and exact project/tool/repository/guest identity were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection stayed read-only and used least privilege.
- [ ] Tool versions and executable paths were verified.
- [ ] Git status and uncommitted work were preserved.
- [ ] Host/guest, distro/VM, and container/volume identities were distinguished.
- [ ] No PATH, Git history, VM, distribution, container, or volume changes were made.
- [ ] Findings and limitations were independently verified and accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows development tools and environments.
