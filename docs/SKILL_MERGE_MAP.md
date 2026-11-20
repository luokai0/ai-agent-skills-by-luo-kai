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


### Windows input, output, and peripheral discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-discover-input-output-peripherals/SKILL.md`
- **Replacement ID:** `windows-consolidated-0006`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Displays, audio, cameras, microphones, keyboard and pointing devices; clipboard, keyboard layouts, IME and text entry; printers, scanners, USB/Bluetooth devices, docks, and queues.
- **Retired IDs:** `windows-0571`, `windows-1081`, `windows-1111`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/01-discover-current-state/SKILL.md`

The replacement preserves sensor-consent safeguards, clipboard privacy, accessibility preferences, print-queue preservation, and distinct verification/recovery routes for displays, text entry, and peripherals.


### Windows network and secure connectivity discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-discover-network-and-secure-connectivity/SKILL.md`
- **Replacement ID:** `windows-consolidated-0007`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Wi-Fi and Ethernet adapter state, connection profiles, signal and IP configuration; DNS resolution, firewall profiles, VPN state, routes, and application reachability.
- **Retired IDs:** `windows-0601`, `windows-0631`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/01-discover-current-state/SKILL.md`

The replacement preserves layered connectivity diagnosis and the distinct safeguards for unknown networks, corporate settings, private routes, firewall, VPN, and TLS.


### Windows browser and productivity application discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-discover-browser-and-productivity-apps/SKILL.md`
- **Replacement ID:** `windows-consolidated-0008`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Browser profiles, tabs, downloads, site permissions, web app sessions; documents, spreadsheets, presentations, mail, calendars, collaboration tools, autosave, version history, and sharing scope.
- **Retired IDs:** `windows-0661`, `windows-0691`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/01-discover-current-state/SKILL.md`

The replacement preserves browser-session confidentiality and productivity safeguards for unsent messages, unsaved documents, recipient identity, sharing scope, and version recovery.


### Windows development, source control, and virtualization discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-discover-development-and-virtualization/SKILL.md`
- **Replacement ID:** `windows-consolidated-0009`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Developer editors, SDKs, compilers, runtimes and project-local setup; Git repository, branch, diff, remote and commit inspection; WSL, Hyper-V/virtualization, VM and container discovery.
- **Retired IDs:** `windows-0721`, `windows-0751`, `windows-0781`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/01-discover-current-state/SKILL.md`

The replacement preserves toolchain and project-local diagnostics, Git worktree safety, token/remote confidentiality, host/guest boundaries, and VM/container backup requirements.


### Windows health, security, and privacy discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-discover-health-security-and-privacy/SKILL.md`
- **Replacement ID:** `windows-consolidated-0010`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Performance/resource monitoring; battery, thermal and power inspection; event/reliability diagnostics; Defender, firewall, SmartScreen and threat status; app permissions, local accounts and privacy controls.
- **Retired IDs:** `windows-0811`, `windows-0841`, `windows-0871`, `windows-0901`, `windows-0931`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/01-discover-current-state/SKILL.md`

The replacement retains separate profiles for performance, physical power/thermal safety, narrow event collection, active security protection, and account/privacy controls. It preserves redaction and escalation requirements.


### Windows accessibility, remote support, UI automation, and visual evidence discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-discover-accessibility-remote-ui-and-visual/SKILL.md`
- **Replacement ID:** `windows-consolidated-0011`
- **Version:** `1.2.0`
- **Consolidated capabilities:** Assistive technology and accessibility modalities; Remote Desktop/Quick Assist and consent; UI Automation trees, selectors, focus and resilient interaction; screenshots, OCR, visual grounding and evidence handling.
- **Retired IDs:** `windows-0961`, `windows-0991`, `windows-1021`, `windows-1051`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/01-discover-current-state/SKILL.md`

The replacement preserves assistive preferences, remote-session consent, no-hidden-click boundaries, stable UIA verification, screenshot minimization, redaction, and OCR uncertainty handling.
