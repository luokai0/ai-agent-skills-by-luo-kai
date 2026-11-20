# Skill Consolidation Audit

**Repository:** `luokai0/ai-agent-skills-by-luo-kai`  
**Branch:** `main`  
**Audit date:** 2026-11-20  
**Status:** Structural and representative-content audit completed; twelve Windows consolidation pilots committed to `main`; the first workflow has now been consolidated across all 40 Windows domains. Remaining workflow batches are still pending.

## Findings

### Collection 23: Windows Computer Operations

- 40 domain folders were checked.
- Every domain contains the same 30 workflow names, from `01-discover-current-state` through `30-hand-off-a-verified-outcome`.
- The current structure contains 1,200 files arranged as 40 repetitions of 30 generic workflow patterns.
- Representative comparison across all 40 domains found extensive repeated operating discipline, workflow, execution-contract, evidence, and recovery text.
- Domain-specific information still matters: target surfaces, preferred tools, safety boundaries, diagnostic commands, and verification criteria differ. These must become explicit domain profiles in consolidated skills.

### Collection 24: Linux System Operations

- All 25 distribution folders were checked.
- Every distribution contains the same 50 workflow names.
- The current structure contains 1,250 files arranged as 25 repetitions of 50 task patterns.
- Representative package-install comparison across 25 distributions showed approximately 97.9% textual similarity between the Ubuntu and Garuda variants.
- The meaningful differences are distribution-specific package managers, release models, repository rules, init systems, and exceptional operating models such as NixOS, Tails, Qubes OS, and SteamOS. Those distinctions must remain explicit and must never be flattened into one generic command path.

## Recommended consolidation architecture

The objective is to reduce repeated files while preserving every useful capability, example, safety rule, diagnostic, and recovery path.

### Windows

Organize the 40 domains into eight related groups of up to five domains. Each consolidated workflow will include:
- One shared task procedure.
- A domain selector and explicit domain profiles.
- The preferred native UI, accessibility, and PowerShell tools for each profile.
- Profile-specific safety boundaries, verification, and recovery.
- A migration map for every retired skill ID.

Target after full validation: approximately 240 consolidated workflows instead of 1,200 repeated variants.

### Linux

Organize the 25 distributions into five related groups of up to five distributions. Each consolidated workflow will include:
- One shared task procedure.
- A strict distribution and execution-environment detector.
- A native package/init/tooling profile for each supported distribution.
- Explicit special-case handling for immutable, declarative, amnesic, isolated, and non-systemd systems.
- A migration map for every retired skill ID.

Target after full validation: approximately 250 consolidated workflows instead of 1,250 repeated variants.

These are structural targets, not permission to remove useful distinctions. If a task cannot be combined safely, it remains separate.

## Required migration gates

No original skill is deleted until all of the following pass:

1. Every old skill has been assigned to a specific consolidated replacement or explicitly retained as unique.
2. All unique task instructions, commands, examples, preconditions, warnings, and recovery details are represented in the replacement.
3. The replacement has valid YAML frontmatter, a unique stable ID, and an accurate author field.
4. Commands are checked for platform validity, privilege assumptions, destructive effects, and policy bypasses.
5. Distribution and domain profiles are checked against the actual target systems.
6. The consolidated skill is tested for ambiguity, missing branches, unsafe defaults, and false success claims.
7. Catalogs, installation references, collection counts, README content, and validation workflows are updated.
8. The final diff is reviewed before any redundant files are removed.

## Repository-wide scope

The Windows and Linux findings are confirmed. The same duplicate and authorship audit must be run across the remaining collections before making repository-wide ownership or consolidation claims.

## Authorship and rights boundary

Newly authored and independently rewritten material may identify Luo Kai as its author. An author field must not be changed on material that Luo Kai did not independently author or does not have the right to relicense. Required notices and third-party rights must not be erased. A missing license is not permission to copy, modify, or redistribute.

A repository-wide claim that every skill is exclusively owned by Luo Kai is valid only after the remaining material has been independently authored or its rights have been lawfully resolved.


## Migration progress — 2026-11-20

### Completed pilot: Windows desktop discovery

Three overlapping, independently authored Windows workflows were consolidated into one replacement skill:

- Desktop shell and Explorer — retired ID `windows-0001`.
- Windows navigation and settings — retired ID `windows-0031`.
- Window management and multitasking — retired ID `windows-0061`.

The replacement is `windows-consolidated-0001`, version `1.2.0`, at `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-discover-current-state/SKILL.md`.

The replacement preserves the three domains as explicit profiles, including preferred tools, target identification, unique safety boundaries, verification criteria, and recovery routes. Shared operating discipline and read-only inspection steps are unified. The three retired files were removed in the same atomic commit as the replacement and migration map.

- **Commit:** [c08990c](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/c08990c01e01cfff0b7d320a6ea554da36272585)
- **Windows skill count after pilot:** 1,198 (down from 1,200).
- **Combined Windows + Linux count after pilot:** 2,448 (down from 2,450).
- **Migration map:** [docs/SKILL_MERGE_MAP.md](SKILL_MERGE_MAP.md)

### Next migration work

Continue grouping related Windows domains in batches of two to five skills per replacement. Then apply the same evidence-led process to Linux distribution workflows, preserving package-manager, init-system, release-model, immutable-system, privacy, and isolation differences. Do not delete a group until its replacement and complete ID/path mapping are committed.

### Rights and authorship boundary

This pilot uses only skills already marked as original Luo Kai work. Imported or third-party material is not silently relabeled, stripped of required notices, or claimed as original. Independently rewritten skills may carry Luo Kai authorship only when they are genuinely original and do not reproduce protected expression. The repository's existing third-party notices and applicable rights records remain in force during the audit.


### Second pilot: Windows workspace and file discovery

Three more overlapping, independently authored workflows were consolidated into one replacement:

- Start menu, taskbar, quick settings, and notifications — retired ID `windows-0091`.
- File Explorer navigation and locations — retired ID `windows-0121`.
- File and folder operations — retired ID `windows-0151`.

The replacement is `windows-consolidated-0002`, version `1.2.0`, at `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-discover-workspace-and-files/SKILL.md`.

The replacement retains separate profiles for each surface. It adds explicit local/removable/network/cloud/virtual location detection, file identity and integrity checks, collision planning, and read-only discovery boundaries. The original files were removed in the same commit as the replacement and map update.

- **Commit:** [1140b78](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/1140b78494e869a991e84b5ed02d9d1512f28f35)
- **Windows skill count after two pilots:** 1,196.
- **Combined Windows + Linux count after two pilots:** 2,446.
- **Complete migration map:** [docs/SKILL_MERGE_MAP.md](SKILL_MERGE_MAP.md)


### Third pilot: Windows search, archives, and storage discovery

Three more overlapping, independently authored workflows were consolidated:

- Windows Search and file metadata — retired ID `windows-0181`.
- Archives, downloads, and file transfer — retired ID `windows-0211`.
- Storage, partitions, and volumes — retired ID `windows-0241`.

The replacement is `windows-consolidated-0003`, version `1.2.0`, at `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-discover-search-archives-storage/SKILL.md`.

The replacement keeps separate profiles for search/indexing, archive/transfer inspection, and storage/volume health. It preserves stale-index handling, untrusted-archive safeguards, hash verification, disk identity checks, and the prohibition on destructive storage changes during discovery. The three originals were removed in the same commit as the replacement and map update.

- **Commit:** [9e277b6](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/9e277b6a3f63aa261ec9ad9312290fcbf30fa84c)
- **Windows skill count after three pilots:** 1,194.
- **Combined Windows + Linux count after three pilots:** 2,444.
- **Complete migration map:** [docs/SKILL_MERGE_MAP.md](SKILL_MERGE_MAP.md)


### Fourth pilot: Windows shell, process, and startup discovery

Five independently authored workflows were consolidated into `windows-consolidated-0004`:

- PowerShell fundamentals — `windows-0271`.
- Advanced PowerShell administration — `windows-0301`.
- Command Prompt and Windows Terminal — `windows-0331`.
- Processes, services, and applications — `windows-0361`.
- Startup, scheduled tasks, and background execution — `windows-0391`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-discover-shells-processes-and-startup/SKILL.md`.

The replacement keeps five distinct profiles, shell-specific command examples, process/service identity checks, startup-task ownership checks, and each domain's stop/recovery rules.

- **Commit:** [4c38cda](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/4c38cda9970dcb9c845de9a8ffc55938e9b872a7)

### Fifth pilot: Windows configuration, software, updates, and drivers

Five independently authored workflows were consolidated into `windows-consolidated-0005`:

- Registry and Group Policy inspection — `windows-0421`.
- Application installation and compatibility — `windows-0451`.
- Package managers and dependencies — `windows-0481`.
- Windows Update and servicing — `windows-0511`.
- Devices and signed drivers — `windows-0541`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-discover-configuration-software-and-devices/SKILL.md`.

The replacement retains separate profiles for policy, apps, packages, servicing, and hardware, including publisher/source checks, managed-policy boundaries, update/restart safety, and signed-driver checks.

- **Commit:** [6cac159](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/6cac1590a87ddd5fbae46fbaa37f02f66bfac9a6)
- **Windows skill count after five pilots:** 1,186.
- **Combined Windows + Linux count after five pilots:** 2,436.
- **Complete migration map:** [docs/SKILL_MERGE_MAP.md](SKILL_MERGE_MAP.md)


### Sixth pilot: Windows input, output, and peripheral discovery

Three independently authored workflows were consolidated into `windows-consolidated-0006`:

- Displays, audio, cameras, and input devices — `windows-0571`.
- Clipboard, keyboard layouts, and text entry — `windows-1081`.
- Printers, scanners, docks, and peripherals — `windows-1111`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-discover-input-output-peripherals/SKILL.md`.

The replacement preserves separate profiles for displays/audio/cameras, clipboard/text entry, and peripheral queues. It retains sensor-consent safeguards, clipboard privacy, accessibility preferences, and print-queue preservation.

- **Commit:** [9af0505](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/9af05054d516dcd237f4eacff43d79e2753e2d9d)
- **Windows skill count after six pilots:** 1,184.
- **Combined Windows + Linux count after six pilots:** 2,434.
- **Complete migration map:** [docs/SKILL_MERGE_MAP.md](SKILL_MERGE_MAP.md)


### Seventh pilot: Windows network and secure connectivity discovery

Two independently authored workflows were consolidated into `windows-consolidated-0007`:

- Wi-Fi and Ethernet — `windows-0601`.
- DNS, firewall, and VPN — `windows-0631`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-discover-network-and-secure-connectivity/SKILL.md`.

The replacement preserves layered connectivity diagnosis and the safeguards for unknown networks, private routes, firewall, VPN, TLS, and managed settings.

- **Commit:** [e90f177](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/e90f177977a09c5e05d6f17e13ba7c11e1a0c7d1)

### Eighth pilot: Windows browser and productivity discovery

Two independently authored workflows were consolidated into `windows-consolidated-0008`:

- Browsers and web applications — `windows-0661`.
- Office and productivity applications — `windows-0691`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-discover-browser-and-productivity-apps/SKILL.md`.

The replacement preserves browser-session confidentiality, download and permission checks, unsent-message protection, unsaved-document handling, recipient identity, sharing scope, and version recovery.

- **Commit:** [e1360c3](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/e1360c3eca9bc6b61301b9cc69f5cc6ab41ec7c8)
- **Windows skill count after eight pilots:** 1,182.
- **Combined Windows + Linux count after eight pilots:** 2,432.
- **Complete migration map:** [docs/SKILL_MERGE_MAP.md](SKILL_MERGE_MAP.md)


### Ninth pilot: Windows development, source control, and virtualization discovery

Three independently authored workflows were consolidated into `windows-consolidated-0009`:

- Developer workstation and toolchain — `windows-0721`.
- Git and source control — `windows-0751`.
- WSL, virtual machines, and containers — `windows-0781`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-discover-development-and-virtualization/SKILL.md`.

The replacement preserves toolchain/project-local diagnostics, Git worktree safety, token/remote confidentiality, host/guest boundaries, and VM/container backup requirements.

- **Commit:** [db726a5](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/db726a57f51870edd8680885810dee31b34dc840)

### Tenth pilot: Windows health, security, and privacy discovery

Five independently authored workflows were consolidated into `windows-consolidated-0010`:

- Performance and resource monitoring — `windows-0811`.
- Battery, thermals, and power — `windows-0841`.
- Event logs and diagnostics — `windows-0871`.
- Windows Security and Defender — `windows-0901`.
- Privacy, permissions, and account access — `windows-0931`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-discover-health-security-and-privacy/SKILL.md`.

The replacement retains repeated-sample performance checks, physical battery/thermal safety, narrow event collection, active security protection, and credential/privacy safeguards.

- **Commit:** [e683770](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/e68377088d1ed519dfdae9c14256b16305531e89)

### Eleventh pilot: Windows accessibility, remote support, UI automation, and visual evidence

Four independently authored workflows were consolidated into `windows-consolidated-0011`:

- Accessibility and assistive technology — `windows-0961`.
- Remote Desktop and support sessions — `windows-0991`.
- UI Automation and resilient interaction — `windows-1021`.
- Screenshots, screen reading, and OCR — `windows-1051`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-discover-accessibility-remote-ui-and-visual/SKILL.md`.

The replacement preserves assistive preferences, remote-session consent, no-hidden-click boundaries, stable UIA verification, screenshot minimization, redaction, and OCR uncertainty handling.

- **Commit:** [5576e31](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/5576e313d403c5f97ed20ad265b57bdef23d00d8)

### Twelfth pilot: Windows backup, recovery, and device provisioning discovery

Two independently authored workflows were consolidated into `windows-consolidated-0012`:

- Backup, restore, and recovery — `windows-1141`.
- Windows provisioning and account lifecycle — `windows-1171`.

Replacement: `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-discover-backup-and-device-provisioning/SKILL.md`.

The replacement preserves backup validation, current-disk protection, restore safeguards, device ownership/enrollment checks, and authorized IT handoff requirements.

- **Commit:** [124c604](https://github.com/luokai0/ai-agent-skills-by-luo-kai/commit/124c6045bd8b2010dd6f43fa56826344d05521a5)
- **Windows skill count after twelve pilots:** 1,172.
- **Combined Windows + Linux count after twelve pilots:** 2,422.
- **Complete migration map:** [docs/SKILL_MERGE_MAP.md](SKILL_MERGE_MAP.md)


## Windows workflow consolidation completed — 2026-11-20

The remaining 29 workflows across all 40 Windows domains have been consolidated into 348 profile-based skills across the same 12 domain groups. The 1,160 original standalone files were replaced by 348 consolidated files; every source body is retained inside its domain profile, with only duplicate frontmatter replaced by stable consolidated metadata.

- Previously completed discovery skills: 12
- New consolidated workflows: 348
- Windows skills after consolidation: 360
- Linux skills unchanged: 1,250
- Combined Windows + Linux workflows: 1,610
- Net reduction from the Windows collection: 812 skill files
- Migration map: docs/SKILL_MERGE_MAP.md


## Windows catalog and security pipeline — 2026-11-20

- Full cross-platform validation passed on Ubuntu and Windows.
- Static security and provenance screening passed on both platforms.
- ClamAV malware scan passed.
- Catalog generated: 11,428 skills.
- Distributable bundle generated: 167.7 MiB.
- Versioned release created: skills-180.
- Original Luo Kai skills will carry no license metadata; third-party licenses and notices remain preserved.
