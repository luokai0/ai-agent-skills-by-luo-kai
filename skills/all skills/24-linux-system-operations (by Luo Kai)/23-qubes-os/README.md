# Qubes OS agent operations

This folder contains 50 independently addressable AI-agent skills for operating **Qubes OS** systems. The workflows are distribution-specific and intentionally do not assume that another Linux family uses the same package manager, init system, repository layout, or security defaults.

- Package tooling: `qubes-dom0-update (dom0 only)`
- Service manager: `systemd in dom0; VM-specific` (verify at runtime)
- Typical desktop: XFCE
- Operating constraint: Qubes isolates workloads into qubes. Distinguish dom0 from TemplateVM/AppVM; never run untrusted commands in dom0.

Each skill checks `/etc/os-release`, active init, and execution context before acting. Changes require explicit approval and must be verified. See the collection-level `LINUX_AGENT_OPERATING_PLAYBOOK.md` and `COPYRIGHT.md`.
