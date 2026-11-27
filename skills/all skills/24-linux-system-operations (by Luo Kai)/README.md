<!-- Copyright (c) 2026 Luo Kai. All rights reserved for original work. -->
# Linux System Operations

**300 consolidated skills · 6 distribution groups · 25 Linux distributions**

A profile-based operating library for AI agents. The 1,250 distribution-specific workflows are consolidated into 300 task skills. Each skill contains three to five exact distribution profiles, preserving the complete procedures, native commands, safety controls, verification, and recovery guidance.

## Six distribution groups

| Group | Distribution profiles | Workflows |
|---|---|---:|
| Debian-family desktops | Ubuntu, Debian, Linux Mint, Pop!_OS, elementary OS | 50 |
| Debian security and specialist derivatives | Kali Linux, Zorin OS, Parrot OS, MX Linux, Tails | 50 |
| RPM-based enterprise and community systems | Fedora, Red Hat Enterprise Linux, Rocky Linux, AlmaLinux | 50 |
| Arch-family rolling systems | Arch Linux, Manjaro, Garuda Linux | 50 |
| Independent and source-based systems | Gentoo, Alpine Linux, Slackware, Void Linux | 50 |
| Specialized and immutable systems | openSUSE, NixOS, Qubes OS, SteamOS | 50 |
| **Total** | **25 distributions** | **300 skills** |

## Profile selection

1. Confirm the actual distribution and release from local system evidence, including /etc/os-release.
2. Identify architecture, kernel, PID 1, package manager, filesystem model, and host, VM, container, qube, live, or remote context.
3. Open the consolidated task skill and select only the matching distribution profile.
4. Follow that profile's complete execution contract. Never transfer package, service, boot, security, or recovery assumptions from another distribution.
5. Start read-only, use least privilege, obtain approval for consequential changes, and independently verify the outcome.

## Safety and reliability

- Preserve Tails amnesia and Tor protections, Qubes isolation, NixOS declarative configuration, and SteamOS immutable-system behavior.
- Do not assume apt, systemd, sudo, mutable root filesystems, or a common release model.
- Do not disable security controls or execute opaque remote installers to bypass a problem.
- Protect remote access, user data, encryption, backups, credentials, and recovery material.
- Stop when the exact target or matching profile cannot be confirmed.

## Repository structure

The consolidated skills live under 00-consolidated-linux-operations, arranged by distribution family and task. The original distribution folders and their README references remain as supporting documentation; standalone task skills are consolidated into the 300 profile-based entries.

## Quality and operating references

- [Linux Skill Quality Standard](SKILL_QUALITY_STANDARD.md)
- [Linux AI Agent Operating Playbook](LINUX_AGENT_OPERATING_PLAYBOOK.md)
- [Collection copyright notice](COPYRIGHT.md)
- [Repository-wide skill merge map](../../docs/SKILL_MERGE_MAP.md)
- [Consolidation audit](../../docs/SKILL_CONSOLIDATION_AUDIT.md)

## Copyright

Copyright (c) 2026 Luo Kai. All rights reserved for original instructional material and workflow design in this collection. No license is granted for original material. Third-party tools, distributions, software, trademarks, and independently owned material retain their respective rights and notices.
