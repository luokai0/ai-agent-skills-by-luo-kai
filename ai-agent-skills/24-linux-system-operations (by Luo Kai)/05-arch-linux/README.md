# Arch Linux agent operations

This folder contains 25 independently addressable AI-agent skills for operating **Arch Linux** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `pacman`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: User-selected
- Operating constraint: Arch is rolling release; partial upgrades are unsupported. Read Arch news and review the full transaction first.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
