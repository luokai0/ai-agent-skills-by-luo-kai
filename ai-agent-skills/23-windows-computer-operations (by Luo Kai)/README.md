<!-- Copyright (c) 2026 Luo Kai. All rights reserved for original work. -->
# Windows Computer Operations (1,200 skills)

An original, task-oriented library for AI agents that operate Windows 10 and Windows 11 desktops and laptops. It is designed for real interactive machines, including older laptops, standard user accounts, multi-monitor setups, and managed workstations.

**Collection size:** 1,200 individual `SKILL.md` files, organized into 40 domains with 30 operational workflows per domain. All skills are upgraded to **v1.1** with a task-bound agent execution contract.

## Operating principles

1. Observe before acting. Identify the device, OS build, user session, exact target, and current state.
2. Prefer native Windows interfaces and supported UI Automation for GUI tasks. Use PowerShell for bounded inspection and repeatable checks.
3. Use least privilege. Do not assume administrator rights or bypass UAC, sign-in, MFA, CAPTCHA, consent, or organizational policy.
4. Preserve user data and active work. Do not overwrite, permanently delete, reset, format, or reboot without explicit approval.
5. Treat downloads, archives, scripts, macros, installers, and removable media as untrusted until inspected.
6. Verify the result independently. A click, command completion, or toast notification is not proof of success.
7. Report what changed, what was verified, and what remains uncertain.

## Domain map

01. **Windows desktop shell** — 30 focused workflows
02. **Windows navigation and settings** — 30 focused workflows
03. **Window management and multitasking** — 30 focused workflows
04. **Start menu, taskbar, and notifications** — 30 focused workflows
05. **File Explorer navigation** — 30 focused workflows
06. **File and folder operations** — 30 focused workflows
07. **Windows search and file metadata** — 30 focused workflows
08. **Archives, downloads, and file transfer** — 30 focused workflows
09. **Storage, partitions, and volumes** — 30 focused workflows
10. **PowerShell fundamentals** — 30 focused workflows
11. **Advanced PowerShell administration** — 30 focused workflows
12. **Command Prompt and Windows Terminal** — 30 focused workflows
13. **Processes, services, and applications** — 30 focused workflows
14. **Startup, scheduled tasks, and background execution** — 30 focused workflows
15. **Registry and Group Policy inspection** — 30 focused workflows
16. **Application installation and removal** — 30 focused workflows
17. **Windows package managers and dependencies** — 30 focused workflows
18. **Windows Update and update servicing** — 30 focused workflows
19. **Device Manager and hardware drivers** — 30 focused workflows
20. **Displays, audio, cameras, and input devices** — 30 focused workflows
21. **Wi-Fi, Ethernet, and network adapters** — 30 focused workflows
22. **DNS, firewall, VPN, and secure connectivity** — 30 focused workflows
23. **Browsers, web apps, and downloads** — 30 focused workflows
24. **Office and productivity applications** — 30 focused workflows
25. **Developer workstation setup** — 30 focused workflows
26. **Git and source-control operations** — 30 focused workflows
27. **WSL, virtual machines, and containers** — 30 focused workflows
28. **Performance and resource monitoring** — 30 focused workflows
29. **Laptop battery, thermals, and power management** — 30 focused workflows
30. **Event logs and Windows troubleshooting** — 30 focused workflows
31. **Windows security and Microsoft Defender** — 30 focused workflows
32. **Privacy, permissions, and account access** — 30 focused workflows
33. **Accessibility and assistive technology** — 30 focused workflows
34. **Remote access and support sessions** — 30 focused workflows
35. **Reliable Windows UI automation** — 30 focused workflows
36. **Screenshots, screen reading, and OCR** — 30 focused workflows
37. **Clipboard, text entry, and input reliability** — 30 focused workflows
38. **Printers, scanners, docks, and peripherals** — 30 focused workflows
39. **Backup, restore, and recovery** — 30 focused workflows
40. **Windows provisioning and account lifecycle** — 30 focused workflows

## v1.1 agent-grade upgrade

Every skill now carries its own execution contract bound to its domain and task. It adds explicit target identification, baseline capture, risk classification, concrete task controls, approval rules, independent success checks, stop conditions, bounded recovery, and a privacy-safe handoff. The original procedures, IDs, command examples, safety rules, and licensing boundaries are preserved. See [`SKILL_QUALITY_STANDARD.md`](SKILL_QUALITY_STANDARD.md) for the maintenance and acceptance criteria.

## Layout

Each workflow is a separate folder containing `SKILL.md`. The skill metadata includes a stable ID (`windows-0001` through `windows-1200`), author, platform, version, and license scope. The maintenance generator is `scripts/maintenance/generate_windows_skill_pack.py`.

## Compatibility

The instructions target Windows 10 and Windows 11, but feature availability varies by edition, build, hardware, policy, and installed applications. Skills instruct agents to check availability rather than assume it. Some PowerShell probes require built-in modules or optional components; use `Get-Command` and fall back to the UI when a command is unavailable.

## Security and rights

These 1,200 skills are original instructional material authored for Luo Kai. Copyright in original text is reserved to Luo Kai. Microsoft, Windows, and third-party product names are used only to identify the relevant platform or tool; their owners retain their respective rights. This collection does not claim ownership of Microsoft software, APIs, trademarks, or third-party tools.
