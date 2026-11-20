# NixOS agent operations

This folder contains 50 independently addressable AI-agent skills for operating **NixOS** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `nix`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: GNOME/KDE/user-selected
- Operating constraint: NixOS is declarative; inspect configuration and generations before applying changes. Never edit generated state as a substitute for config.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
