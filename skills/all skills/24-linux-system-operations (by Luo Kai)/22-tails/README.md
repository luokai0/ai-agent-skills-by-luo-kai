# Tails agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Tails** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apt (restricted)`
- Service manager: `systemd (managed)` (verify at runtime)
- Typical desktop: GNOME
- Operating constraint: Tails is amnesic by design; do not weaken Tor routing, persistence safeguards, or system integrity. Most system modifications are intentionally temporary or unsupported.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
