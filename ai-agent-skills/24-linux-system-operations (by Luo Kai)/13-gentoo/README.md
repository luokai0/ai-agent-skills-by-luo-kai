# Gentoo agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Gentoo** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `emerge`
- Service manager: `OpenRC or systemd` (verify at runtime)
- Typical desktop: User-selected
- Operating constraint: Source-based system; inspect profile, USE flags, package masks, and active init before changing world set.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
