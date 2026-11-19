# Debian agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Debian** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apt`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: GNOME or user-selected
- Operating constraint: Stable releases prioritize conservative updates; check sources and release notes before a major upgrade.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
