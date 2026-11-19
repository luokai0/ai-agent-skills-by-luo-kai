# openSUSE agent operations

This folder contains 50 independently addressable AI-agent skills for operating **openSUSE** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `zypper`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: KDE Plasma or GNOME
- Operating constraint: Distinguish Leap from Tumbleweed; Tumbleweed uses rolling snapshots and should be updated as a coherent transaction.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
