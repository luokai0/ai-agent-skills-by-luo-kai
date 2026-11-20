# Parrot OS agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Parrot OS** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apt`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: MATE or KDE
- Operating constraint: Use Parrot repositories and security tooling only for authorized work; avoid mixing Kali or Debian suites.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
