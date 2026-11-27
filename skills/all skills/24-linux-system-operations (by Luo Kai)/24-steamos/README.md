# SteamOS agent operations

This folder contains 50 independently addressable AI-agent skills for operating **SteamOS** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `read-only base / Flatpak`
- Service manager: `systemd (managed)` (verify at runtime)
- Typical desktop: Gamescope / KDE desktop mode
- Operating constraint: SteamOS is an immutable gaming OS; never disable read-only mode or use generic Arch upgrade instructions. Prefer Steam client updates and Flatpak for desktop apps.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
