# Skill Merge Map

This file records completed consolidations and maps retired skill identifiers to their replacement. A source skill is removed only after its useful task instructions, examples, safety boundaries, diagnostics, verification rules, and recovery guidance are represented in the replacement.

## Completed

### Windows desktop, navigation, and multitasking: discover current state
- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-discover-current-state/SKILL.md`
- **Replacement ID:** `windows-consolidated-0001`
- **Version:** `1.2.0`
- **Consolidated capabilities:** desktop shell and Explorer; desktop icons and notification area; shell-process inspection; Settings and Control Panel navigation; system pages and search; window focus and snapping; virtual desktops and task switching; multi-monitor placement.
- **Retired IDs:** `windows-0001`, `windows-0031`, `windows-0061`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/01-discover-current-state/SKILL.md`

The replacement combines repeated operating discipline while retaining each profile's preferred controls, unique safety boundaries, verification requirements, and recovery routes. This migration covers only independently authored Luo Kai skills.

## Migration rules
1. Merge only skills with materially overlapping task outcomes. Similar wording alone is insufficient.
2. Preserve every unique capability, command example, precondition, warning, approval gate, verification step, and recovery route.
3. Keep separate profiles where tools, commands, safety boundaries, or platform behavior differ.
4. Assign a stable replacement ID and version; record every retired ID and path.
5. Update catalogs, installation references, collection counts, README content, and validation workflows in the same migration batch.
6. Do not remove third-party notices or represent third-party material as original.


### Windows workspace and file discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-discover-workspace-and-files/SKILL.md`
- **Replacement ID:** `windows-consolidated-0002`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Start menu, pinned apps, taskbar controls, quick settings, system tray and notifications; File Explorer windows, address bar, navigation, libraries and views; file/folder identity, metadata, hash checks, and safe operation planning.
- **Retired IDs:** `windows-0091`, `windows-0121`, `windows-0151`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/01-discover-current-state/SKILL.md`

The replacement retains separate profiles for shell/taskbar, Explorer navigation, and file integrity/operation planning. File discovery remains read-only; destructive or externally visible actions require a separate request and approval.


### Windows search, archives, and storage discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-discover-search-archives-storage/SKILL.md`
- **Replacement ID:** `windows-consolidated-0003`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Windows Search, indexing and filters; file metadata and integrity; archive/download inspection and safe transfer verification; disk, volume, removable storage, capacity and health inspection.
- **Retired IDs:** `windows-0181`, `windows-0211`, `windows-0241`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/01-discover-current-state/SKILL.md`

The replacement retains distinct search, archive/transfer, and storage profiles. It preserves stale-index handling, untrusted-archive precautions, hash verification, disk identity checks, and explicit prohibition on destructive storage changes during discovery.


### Windows shell, process, and startup discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-discover-shells-processes-and-startup/SKILL.md`
- **Replacement ID:** `windows-consolidated-0004`
- **Version:** `1.2.0`
- **Consolidated capabilities:** PowerShell fundamentals and advanced/CIM inspection; Command Prompt and Windows Terminal; process, service, and application diagnostics; startup applications, scheduled tasks, and background execution.
- **Retired IDs:** `windows-0271`, `windows-0301`, `windows-0331`, `windows-0361`, `windows-0391`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/01-discover-current-state/SKILL.md`

The replacement retains five distinct profiles, shell-specific command examples, safe inspection tools, process/service identity checks, startup-task ownership checks, and each domain's unique stop and recovery rules. Shared execution discipline is unified; all five source workflows were independently authored Luo Kai material.


### Windows configuration, software, updates, and driver discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-discover-configuration-software-and-devices/SKILL.md`
- **Replacement ID:** `windows-consolidated-0005`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Registry and Group Policy inspection; application and installer inventory; winget and Store package sources; Windows Update history and restart state; Plug-and-Play device and signed-driver inspection.
- **Retired IDs:** `windows-0421`, `windows-0451`, `windows-0481`, `windows-0511`, `windows-0541`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/01-discover-current-state/SKILL.md`

The replacement preserves distinct profiles for policy, apps, packages, servicing, and hardware. It retains publisher/source checks, managed-policy boundaries, update/restart safety, signed-driver checks, and recovery routes.
