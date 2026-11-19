# Linux Mint agent operations

This folder contains 25 independently addressable AI-agent skills for operating **Linux Mint** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apt`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: Cinnamon (often)
- Operating constraint: Mint editions are based on Ubuntu LTS or Debian; identify the edition and base before changing repositories.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
