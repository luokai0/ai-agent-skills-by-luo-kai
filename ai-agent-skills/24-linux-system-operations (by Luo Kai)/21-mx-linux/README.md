# MX Linux agent operations

This folder contains 50 independently addressable AI-agent skills for operating **MX Linux** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apt`
- Service manager: `systemd or SysVinit` (verify at runtime)
- Typical desktop: Xfce/KDE/Fluxbox
- Operating constraint: MX offers multiple init choices and MX Tools; detect the active init before service operations.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
