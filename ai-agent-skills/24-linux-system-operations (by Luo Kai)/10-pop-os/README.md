# Pop!_OS agent operations

This folder contains 25 independently addressable AI-agent skills for operating **Pop!_OS** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `apt`
- Service manager: `systemd` (verify at runtime)
- Typical desktop: COSMIC or GNOME
- Operating constraint: Identify Pop release and graphics variant; NVIDIA and System76 power features may change available options.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `LICENSE_SCOPE.md`.
