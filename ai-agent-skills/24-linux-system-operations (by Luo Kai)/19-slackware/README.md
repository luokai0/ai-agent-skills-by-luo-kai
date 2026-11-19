# Slackware agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Slackware** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `slackpkg/pkgtools`
- Service manager: `SysV-style BSD scripts` (verify at runtime)
- Typical desktop: KDE/Xfce
- Operating constraint: Slackware package tools and init scripts differ from systemd distributions; confirm current release and mirror.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
