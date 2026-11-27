# Rocky Linux agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Rocky Linux** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `dnf`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: GNOME or server
- Operating constraint: Enterprise-compatible lifecycle; verify minor release, repositories, and supported migration guidance.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
