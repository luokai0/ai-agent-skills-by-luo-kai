<!-- Copyright (c) 2026 Luo Kai. All rights reserved for original work. -->
# Linux System Operations — Collection 24

An original library of **625 Linux operations skills** for AI agents, organized into **25 distribution-specific folders**, with **25 task-focused skills per distribution**. The collection is capped by usefulness, not by a quota: 88,000 is an upper ceiling, not a target. No filler or artificial variants are added merely to inflate the count.

## 25 supported distributions

- [Ubuntu](01-ubuntu/) — 25 focused skills; `apt`; systemd
- [Debian](02-debian/) — 25 focused skills; `apt`; systemd
- [Linux Mint](03-linux-mint/) — 25 focused skills; `apt`; systemd
- [Fedora](04-fedora/) — 25 focused skills; `dnf`; systemd
- [Arch Linux](05-arch-linux/) — 25 focused skills; `pacman`; systemd
- [Kali Linux](06-kali-linux/) — 25 focused skills; `apt`; systemd
- [Red Hat Enterprise Linux](07-red-hat-enterprise-linux/) — 25 focused skills; `dnf`; systemd
- [openSUSE](08-opensuse/) — 25 focused skills; `zypper`; systemd
- [Manjaro](09-manjaro/) — 25 focused skills; `pacman`; systemd
- [Pop!_OS](10-pop-os/) — 25 focused skills; `apt`; systemd
- [Rocky Linux](11-rocky-linux/) — 25 focused skills; `dnf`; systemd
- [AlmaLinux](12-almalinux/) — 25 focused skills; `dnf`; systemd
- [Gentoo](13-gentoo/) — 25 focused skills; `emerge`; OpenRC or systemd
- [Alpine Linux](14-alpine-linux/) — 25 focused skills; `apk`; OpenRC
- [elementary OS](15-elementary-os/) — 25 focused skills; `apt`; systemd
- [Zorin OS](16-zorin-os/) — 25 focused skills; `apt`; systemd
- [Parrot OS](17-parrot-os/) — 25 focused skills; `apt`; systemd
- [NixOS](18-nixos/) — 25 focused skills; `nix`; systemd
- [Slackware](19-slackware/) — 25 focused skills; `slackpkg/pkgtools`; SysV-style BSD scripts
- [Void Linux](20-void-linux/) — 25 focused skills; `xbps`; runit
- [MX Linux](21-mx-linux/) — 25 focused skills; `apt`; systemd or SysVinit
- [Tails](22-tails/) — 25 focused skills; `apt (restricted)`; systemd (managed)
- [Qubes OS](23-qubes-os/) — 25 focused skills; `qubes-dom0-update (dom0 only)`; systemd in dom0; VM-specific
- [SteamOS](24-steamos/) — 25 focused skills; `read-only base / Flatpak`; systemd (managed)
- [Garuda Linux](25-garuda-linux/) — 25 focused skills; `pacman`; systemd

## What each skill contains

Every skill is a separate `SKILL.md` with valid YAML frontmatter, stable ID (`linux-0001` through `linux-0625`), a precise objective, distribution/release detection, prerequisites, read-only diagnostics, approval gates, native commands, independent verification, failure recovery, and a completion checklist.

## Operating model

Read `LINUX_AGENT_OPERATING_PLAYBOOK.md` before running any skill. Agents must detect the actual distribution and execution context, use least privilege, preserve user data, and ask for explicit approval before consequential changes. The workflows do not assume that every Linux system uses systemd, apt, sudo, or a mutable root filesystem.

## Coverage

Package and repository management; release and hardware inventory; service managers; user and privilege review; storage and mounts; networking, DNS, firewall and SSH; boot and kernel inspection; logs and scheduled jobs; developer toolchains; containers; backups and snapshots; desktop sessions; and distribution-specific specialist tools.

## Rights and attribution

Original instructions and collection organization are authored by Luo Kai. Third-party distribution names and tool names are used descriptively; their owners retain all rights in their software, trademarks, and documentation. See `LICENSE_SCOPE.md`.
