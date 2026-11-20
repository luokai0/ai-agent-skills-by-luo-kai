<!-- Copyright (c) 2026 Luo Kai. All rights reserved for original work. -->
# Windows Computer Operations (360 consolidated skills)

An original, task-oriented library for AI agents operating Windows 10 and Windows 11 desktops and laptops. The collection consolidates 40 operating domains into 12 cross-domain groups while retaining each domain's procedures, tools, safeguards, examples, verification, and recovery guidance as separate profiles.

Collection size: 360 consolidated SKILL.md files, organized into 12 groups with 30 workflows per group. Each skill combines 2–5 related domain playbooks. Consolidated skills use version 1.2.0 and contain no license field in their frontmatter.

## The 12 consolidated groups

01. Desktop and window management — desktop shell, Windows navigation and settings, window multitasking
02. Workspace and file operations — Start/taskbar, File Explorer, file and folder operations
03. Search, archives, and storage — Windows Search, archive/transfer inspection, storage and volumes
04. Shells, processes, and startup — PowerShell, Command Prompt, processes, services, scheduled tasks
05. Configuration, software, and devices — registry/policy, apps, package managers, updates, drivers
06. Input, output, and peripherals — displays, audio, cameras, clipboard, text entry, printers and scanners
07. Network and secure connectivity — Wi-Fi, Ethernet, DNS, firewall, VPN and secure routes
08. Browser and productivity applications — browser profiles, web apps, documents, mail, calendars
09. Development and virtualization — developer toolchains, Git, WSL, virtual machines, containers
10. Health, security, and privacy — performance, battery/thermal state, event logs, Defender, permissions
11. Accessibility, remote support, and visual automation — assistive technology, remote sessions, UIA, screenshots, OCR
12. Backup, recovery, and provisioning — File History, restore planning, setup, profiles, enrollment

## Consolidation standard

Every replacement contains explicit domain profiles. The full original workflow bodies are retained inside their corresponding profiles, including objectives, operating discipline, procedures, preferred tools, command examples, safety boundaries, execution contracts, verification, recovery, and completion checklists. Shared discovery guidance is added at the consolidated-skill level.

The migration map records every retired skill ID and path. No original workflow is removed unless its replacement and mapping are created in the same change.

## Operating principles

1. Observe before acting. Identify the device, OS build, user session, exact target, and current state.
2. Prefer native Windows interfaces and supported UI Automation for GUI tasks. Use PowerShell for bounded inspection and repeatable checks.
3. Use least privilege. Do not assume administrator rights or bypass UAC, sign-in, MFA, CAPTCHA, consent, or organizational policy.
4. Preserve user data and active work. Do not overwrite, permanently delete, reset, format, or reboot without explicit approval.
5. Treat downloads, archives, scripts, macros, installers, and removable media as untrusted until inspected.
6. Verify the result independently. A click, command completion, or toast notification is not proof of success.
7. Report what changed, what was verified, and what remains uncertain.

## Layout and quality

Each consolidated workflow is stored as a separate SKILL.md under 00-consolidated-desktop-operations. Metadata includes author, platform, stable consolidated ID, and version. Domain profiles preserve former domain/task bindings for traceability; the full mapping is in [docs/SKILL_MERGE_MAP.md](../../docs/SKILL_MERGE_MAP.md).

Quality standard: [SKILL_QUALITY_STANDARD.md](SKILL_QUALITY_STANDARD.md).

## Compatibility

The instructions target Windows 10 and Windows 11, but feature availability varies by edition, build, hardware, policy, and installed applications. Skills instruct agents to check availability rather than assume it.

## Security and rights

Copyright in original instructional material, workflow design, and organization is reserved to Luo Kai. No license is granted for original material. Microsoft, Windows, and third-party product names are used descriptively; their owners retain their respective rights. Third-party material, where separately included in the repository, remains subject to its own rights and notices.
