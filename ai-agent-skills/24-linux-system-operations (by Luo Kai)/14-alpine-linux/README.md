# Alpine Linux agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Alpine Linux** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apk`
- Service manager: `OpenRC` (verify at runtime)
- Typical desktop: Xfce or minimal
- Operating constraint: Alpine uses musl and BusyBox; do not assume GNU utilities or systemd are installed.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
