# Kali Linux agent operations

This folder contains 25 independently addressable AI-agent skills for operating **Kali Linux** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apt`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: Xfce (default)
- Operating constraint: Kali is a penetration-testing distribution, not a general-purpose shortcut; use only authorized security testing.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
