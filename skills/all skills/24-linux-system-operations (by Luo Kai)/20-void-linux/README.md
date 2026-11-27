# Void Linux agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Void Linux** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `xbps`
- Service manager: `runit` (verify at runtime)
- Typical desktop: Xfce or user-selected
- Operating constraint: Void uses XBPS and runit; service enablement is symlink-based and should be inspected before edits.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
