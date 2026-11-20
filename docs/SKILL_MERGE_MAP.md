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


### Windows backup, recovery, and device provisioning discovery

- **Replacement:** `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-discover-backup-and-device-provisioning/SKILL.md`
- **Replacement ID:** `windows-consolidated-0012`
- **Version:** `1.2.0`
- **Consolidated capabilities:** File History, OneDrive sync, restore points, recovery environment, restore planning; initial setup, local profiles, device naming, enrollment indicators, and handoff readiness.
- **Retired IDs:** `windows-1141`, `windows-1171`
- **Retired paths:**
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/01-discover-current-state/SKILL.md`
  - `ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/01-discover-current-state/SKILL.md`

The replacement preserves backup validation, recovery safeguards, current-disk preservation, device ownership/enrollment checks, and authorized IT handoff requirements.


### windows-consolidated-g01-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0002, windows-0032, windows-0062
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0003, windows-0033, windows-0063
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0004, windows-0034, windows-0064
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0005, windows-0035, windows-0065
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0006, windows-0036, windows-0066
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0007, windows-0037, windows-0067
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0008, windows-0038, windows-0068
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0009, windows-0039, windows-0069
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0010, windows-0040, windows-0070
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0011, windows-0041, windows-0071
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0012, windows-0042, windows-0072
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0013, windows-0043, windows-0073
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0014, windows-0044, windows-0074
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0015, windows-0045, windows-0075
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0016, windows-0046, windows-0076
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0017, windows-0047, windows-0077
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0018, windows-0048, windows-0078
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0019, windows-0049, windows-0079
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0020, windows-0050, windows-0080
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0021, windows-0051, windows-0081
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0022, windows-0052, windows-0082
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0023, windows-0053, windows-0083
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0024, windows-0054, windows-0084
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0025, windows-0055, windows-0085
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0026, windows-0056, windows-0086
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0027, windows-0057, windows-0087
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0028, windows-0058, windows-0088
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0029, windows-0059, windows-0089
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g01-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/01-workspace-and-window/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 01-desktop-shell, 02-windows-navigation, 03-window-multitasking
- Retired IDs: windows-0030, windows-0060, windows-0090
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/01-desktop-shell/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/02-windows-navigation/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/03-window-multitasking/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0092, windows-0122, windows-0152
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0093, windows-0123, windows-0153
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0094, windows-0124, windows-0154
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0095, windows-0125, windows-0155
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0096, windows-0126, windows-0156
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0097, windows-0127, windows-0157
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0098, windows-0128, windows-0158
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0099, windows-0129, windows-0159
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0100, windows-0130, windows-0160
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0101, windows-0131, windows-0161
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0102, windows-0132, windows-0162
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0103, windows-0133, windows-0163
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0104, windows-0134, windows-0164
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0105, windows-0135, windows-0165
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0106, windows-0136, windows-0166
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0107, windows-0137, windows-0167
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0108, windows-0138, windows-0168
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0109, windows-0139, windows-0169
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0110, windows-0140, windows-0170
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0111, windows-0141, windows-0171
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0112, windows-0142, windows-0172
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0113, windows-0143, windows-0173
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0114, windows-0144, windows-0174
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0115, windows-0145, windows-0175
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0116, windows-0146, windows-0176
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0117, windows-0147, windows-0177
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0118, windows-0148, windows-0178
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0119, windows-0149, windows-0179
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g02-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/02-workspace-files/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 04-start-taskbar, 05-file-explorer, 06-file-operations
- Retired IDs: windows-0120, windows-0150, windows-0180
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/04-start-taskbar/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/05-file-explorer/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/06-file-operations/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0182, windows-0212, windows-0242
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0183, windows-0213, windows-0243
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0184, windows-0214, windows-0244
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0185, windows-0215, windows-0245
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0186, windows-0216, windows-0246
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0187, windows-0217, windows-0247
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0188, windows-0218, windows-0248
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0189, windows-0219, windows-0249
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0190, windows-0220, windows-0250
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0191, windows-0221, windows-0251
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0192, windows-0222, windows-0252
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0193, windows-0223, windows-0253
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0194, windows-0224, windows-0254
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0195, windows-0225, windows-0255
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0196, windows-0226, windows-0256
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0197, windows-0227, windows-0257
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0198, windows-0228, windows-0258
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0199, windows-0229, windows-0259
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0200, windows-0230, windows-0260
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0201, windows-0231, windows-0261
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0202, windows-0232, windows-0262
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0203, windows-0233, windows-0263
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0204, windows-0234, windows-0264
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0205, windows-0235, windows-0265
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0206, windows-0236, windows-0266
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0207, windows-0237, windows-0267
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0208, windows-0238, windows-0268
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0209, windows-0239, windows-0269
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g03-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/03-search-archive-storage/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 07-search-metadata, 08-archives-transfer, 09-storage-volumes
- Retired IDs: windows-0210, windows-0240, windows-0270
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/07-search-metadata/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/08-archives-transfer/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/09-storage-volumes/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0272, windows-0302, windows-0332, windows-0362, windows-0392
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0273, windows-0303, windows-0333, windows-0363, windows-0393
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0274, windows-0304, windows-0334, windows-0364, windows-0394
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0275, windows-0305, windows-0335, windows-0365, windows-0395
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0276, windows-0306, windows-0336, windows-0366, windows-0396
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0277, windows-0307, windows-0337, windows-0367, windows-0397
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0278, windows-0308, windows-0338, windows-0368, windows-0398
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0279, windows-0309, windows-0339, windows-0369, windows-0399
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0280, windows-0310, windows-0340, windows-0370, windows-0400
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0281, windows-0311, windows-0341, windows-0371, windows-0401
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0282, windows-0312, windows-0342, windows-0372, windows-0402
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0283, windows-0313, windows-0343, windows-0373, windows-0403
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0284, windows-0314, windows-0344, windows-0374, windows-0404
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0285, windows-0315, windows-0345, windows-0375, windows-0405
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0286, windows-0316, windows-0346, windows-0376, windows-0406
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0287, windows-0317, windows-0347, windows-0377, windows-0407
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0288, windows-0318, windows-0348, windows-0378, windows-0408
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0289, windows-0319, windows-0349, windows-0379, windows-0409
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0290, windows-0320, windows-0350, windows-0380, windows-0410
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0291, windows-0321, windows-0351, windows-0381, windows-0411
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0292, windows-0322, windows-0352, windows-0382, windows-0412
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0293, windows-0323, windows-0353, windows-0383, windows-0413
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0294, windows-0324, windows-0354, windows-0384, windows-0414
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0295, windows-0325, windows-0355, windows-0385, windows-0415
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0296, windows-0326, windows-0356, windows-0386, windows-0416
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0297, windows-0327, windows-0357, windows-0387, windows-0417
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0298, windows-0328, windows-0358, windows-0388, windows-0418
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0299, windows-0329, windows-0359, windows-0389, windows-0419
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g04-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/04-shell-process-startup/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 10-powershell-fundamentals, 11-powershell-advanced, 12-terminal-cmd, 13-process-services, 14-startup-scheduling
- Retired IDs: windows-0300, windows-0330, windows-0360, windows-0390, windows-0420
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/10-powershell-fundamentals/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/11-powershell-advanced/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/12-terminal-cmd/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/13-process-services/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/14-startup-scheduling/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0422, windows-0452, windows-0482, windows-0512, windows-0542
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0423, windows-0453, windows-0483, windows-0513, windows-0543
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0424, windows-0454, windows-0484, windows-0514, windows-0544
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0425, windows-0455, windows-0485, windows-0515, windows-0545
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0426, windows-0456, windows-0486, windows-0516, windows-0546
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0427, windows-0457, windows-0487, windows-0517, windows-0547
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0428, windows-0458, windows-0488, windows-0518, windows-0548
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0429, windows-0459, windows-0489, windows-0519, windows-0549
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0430, windows-0460, windows-0490, windows-0520, windows-0550
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0431, windows-0461, windows-0491, windows-0521, windows-0551
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0432, windows-0462, windows-0492, windows-0522, windows-0552
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0433, windows-0463, windows-0493, windows-0523, windows-0553
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0434, windows-0464, windows-0494, windows-0524, windows-0554
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0435, windows-0465, windows-0495, windows-0525, windows-0555
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0436, windows-0466, windows-0496, windows-0526, windows-0556
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0437, windows-0467, windows-0497, windows-0527, windows-0557
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0438, windows-0468, windows-0498, windows-0528, windows-0558
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0439, windows-0469, windows-0499, windows-0529, windows-0559
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0440, windows-0470, windows-0500, windows-0530, windows-0560
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0441, windows-0471, windows-0501, windows-0531, windows-0561
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0442, windows-0472, windows-0502, windows-0532, windows-0562
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0443, windows-0473, windows-0503, windows-0533, windows-0563
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0444, windows-0474, windows-0504, windows-0534, windows-0564
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0445, windows-0475, windows-0505, windows-0535, windows-0565
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0446, windows-0476, windows-0506, windows-0536, windows-0566
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0447, windows-0477, windows-0507, windows-0537, windows-0567
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0448, windows-0478, windows-0508, windows-0538, windows-0568
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0449, windows-0479, windows-0509, windows-0539, windows-0569
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g05-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/05-configuration-software-devices/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 15-registry-policy, 16-app-installation, 17-package-management, 18-windows-updates, 19-devices-drivers
- Retired IDs: windows-0450, windows-0480, windows-0510, windows-0540, windows-0570
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/15-registry-policy/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/16-app-installation/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/17-package-management/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/18-windows-updates/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/19-devices-drivers/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0572, windows-1082, windows-1112
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0573, windows-1083, windows-1113
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0574, windows-1084, windows-1114
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0575, windows-1085, windows-1115
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0576, windows-1086, windows-1116
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0577, windows-1087, windows-1117
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0578, windows-1088, windows-1118
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0579, windows-1089, windows-1119
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0580, windows-1090, windows-1120
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0581, windows-1091, windows-1121
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0582, windows-1092, windows-1122
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0583, windows-1093, windows-1123
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0584, windows-1094, windows-1124
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0585, windows-1095, windows-1125
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0586, windows-1096, windows-1126
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0587, windows-1097, windows-1127
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0588, windows-1098, windows-1128
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0589, windows-1099, windows-1129
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0590, windows-1100, windows-1130
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0591, windows-1101, windows-1131
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0592, windows-1102, windows-1132
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0593, windows-1103, windows-1133
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0594, windows-1104, windows-1134
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0595, windows-1105, windows-1135
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0596, windows-1106, windows-1136
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0597, windows-1107, windows-1137
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0598, windows-1108, windows-1138
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0599, windows-1109, windows-1139
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g06-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/06-input-output-peripherals/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 20-display-audio-input, 37-clipboard-input, 38-printers-peripherals
- Retired IDs: windows-0600, windows-1110, windows-1140
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/20-display-audio-input/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/37-clipboard-input/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/38-printers-peripherals/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0602, windows-0632
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0603, windows-0633
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0604, windows-0634
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0605, windows-0635
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0606, windows-0636
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0607, windows-0637
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0608, windows-0638
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0609, windows-0639
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0610, windows-0640
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0611, windows-0641
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0612, windows-0642
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0613, windows-0643
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0614, windows-0644
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0615, windows-0645
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0616, windows-0646
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0617, windows-0647
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0618, windows-0648
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0619, windows-0649
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0620, windows-0650
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0621, windows-0651
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0622, windows-0652
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0623, windows-0653
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0624, windows-0654
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0625, windows-0655
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0626, windows-0656
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0627, windows-0657
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0628, windows-0658
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0629, windows-0659
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g07-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/07-network-connectivity/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 21-wifi-ethernet, 22-dns-firewall-vpn
- Retired IDs: windows-0630, windows-0660
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/21-wifi-ethernet/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/22-dns-firewall-vpn/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0662, windows-0692
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0663, windows-0693
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0664, windows-0694
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0665, windows-0695
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0666, windows-0696
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0667, windows-0697
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0668, windows-0698
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0669, windows-0699
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0670, windows-0700
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0671, windows-0701
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0672, windows-0702
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0673, windows-0703
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0674, windows-0704
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0675, windows-0705
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0676, windows-0706
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0677, windows-0707
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0678, windows-0708
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0679, windows-0709
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0680, windows-0710
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0681, windows-0711
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0682, windows-0712
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0683, windows-0713
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0684, windows-0714
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0685, windows-0715
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0686, windows-0716
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0687, windows-0717
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0688, windows-0718
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0689, windows-0719
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g08-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/08-browser-productivity/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 23-browser-webapps, 24-office-productivity
- Retired IDs: windows-0690, windows-0720
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/23-browser-webapps/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/24-office-productivity/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0722, windows-0752, windows-0782
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0723, windows-0753, windows-0783
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0724, windows-0754, windows-0784
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0725, windows-0755, windows-0785
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0726, windows-0756, windows-0786
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0727, windows-0757, windows-0787
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0728, windows-0758, windows-0788
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0729, windows-0759, windows-0789
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0730, windows-0760, windows-0790
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0731, windows-0761, windows-0791
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0732, windows-0762, windows-0792
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0733, windows-0763, windows-0793
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0734, windows-0764, windows-0794
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0735, windows-0765, windows-0795
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0736, windows-0766, windows-0796
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0737, windows-0767, windows-0797
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0738, windows-0768, windows-0798
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0739, windows-0769, windows-0799
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0740, windows-0770, windows-0800
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0741, windows-0771, windows-0801
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0742, windows-0772, windows-0802
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0743, windows-0773, windows-0803
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0744, windows-0774, windows-0804
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0745, windows-0775, windows-0805
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0746, windows-0776, windows-0806
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0747, windows-0777, windows-0807
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0748, windows-0778, windows-0808
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0749, windows-0779, windows-0809
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g09-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/09-development-virtualization/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 25-developer-workstations, 26-git-source-control, 27-wsl-virtualization
- Retired IDs: windows-0750, windows-0780, windows-0810
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/25-developer-workstations/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/26-git-source-control/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/27-wsl-virtualization/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0812, windows-0842, windows-0872, windows-0902, windows-0932
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0813, windows-0843, windows-0873, windows-0903, windows-0933
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0814, windows-0844, windows-0874, windows-0904, windows-0934
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0815, windows-0845, windows-0875, windows-0905, windows-0935
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0816, windows-0846, windows-0876, windows-0906, windows-0936
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0817, windows-0847, windows-0877, windows-0907, windows-0937
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0818, windows-0848, windows-0878, windows-0908, windows-0938
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0819, windows-0849, windows-0879, windows-0909, windows-0939
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0820, windows-0850, windows-0880, windows-0910, windows-0940
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0821, windows-0851, windows-0881, windows-0911, windows-0941
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0822, windows-0852, windows-0882, windows-0912, windows-0942
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0823, windows-0853, windows-0883, windows-0913, windows-0943
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0824, windows-0854, windows-0884, windows-0914, windows-0944
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0825, windows-0855, windows-0885, windows-0915, windows-0945
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0826, windows-0856, windows-0886, windows-0916, windows-0946
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0827, windows-0857, windows-0887, windows-0917, windows-0947
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0828, windows-0858, windows-0888, windows-0918, windows-0948
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0829, windows-0859, windows-0889, windows-0919, windows-0949
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0830, windows-0860, windows-0890, windows-0920, windows-0950
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0831, windows-0861, windows-0891, windows-0921, windows-0951
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0832, windows-0862, windows-0892, windows-0922, windows-0952
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0833, windows-0863, windows-0893, windows-0923, windows-0953
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0834, windows-0864, windows-0894, windows-0924, windows-0954
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0835, windows-0865, windows-0895, windows-0925, windows-0955
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0836, windows-0866, windows-0896, windows-0926, windows-0956
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0837, windows-0867, windows-0897, windows-0927, windows-0957
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0838, windows-0868, windows-0898, windows-0928, windows-0958
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0839, windows-0869, windows-0899, windows-0929, windows-0959
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g10-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/10-health-security-privacy/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 28-performance-monitoring, 29-battery-thermal-power, 30-logs-diagnostics, 31-security-defender, 32-privacy-permissions
- Retired IDs: windows-0840, windows-0870, windows-0900, windows-0930, windows-0960
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/28-performance-monitoring/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/29-battery-thermal-power/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/30-logs-diagnostics/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/31-security-defender/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/32-privacy-permissions/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0962, windows-0992, windows-1022, windows-1052
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0963, windows-0993, windows-1023, windows-1053
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0964, windows-0994, windows-1024, windows-1054
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0965, windows-0995, windows-1025, windows-1055
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0966, windows-0996, windows-1026, windows-1056
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0967, windows-0997, windows-1027, windows-1057
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0968, windows-0998, windows-1028, windows-1058
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0969, windows-0999, windows-1029, windows-1059
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0970, windows-1000, windows-1030, windows-1060
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0971, windows-1001, windows-1031, windows-1061
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0972, windows-1002, windows-1032, windows-1062
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0973, windows-1003, windows-1033, windows-1063
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0974, windows-1004, windows-1034, windows-1064
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0975, windows-1005, windows-1035, windows-1065
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0976, windows-1006, windows-1036, windows-1066
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0977, windows-1007, windows-1037, windows-1067
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0978, windows-1008, windows-1038, windows-1068
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0979, windows-1009, windows-1039, windows-1069
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0980, windows-1010, windows-1040, windows-1070
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0981, windows-1011, windows-1041, windows-1071
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0982, windows-1012, windows-1042, windows-1072
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0983, windows-1013, windows-1043, windows-1073
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0984, windows-1014, windows-1044, windows-1074
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0985, windows-1015, windows-1045, windows-1075
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0986, windows-1016, windows-1046, windows-1076
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0987, windows-1017, windows-1047, windows-1077
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0988, windows-1018, windows-1048, windows-1078
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0989, windows-1019, windows-1049, windows-1079
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g11-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/11-accessibility-remote-visual/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 33-accessibility, 34-remote-desktop, 35-ui-automation, 36-screenshots-ocr
- Retired IDs: windows-0990, windows-1020, windows-1050, windows-1080
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/33-accessibility/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/34-remote-desktop/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/35-ui-automation/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/36-screenshots-ocr/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w02

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/02-inspect-configuration/SKILL.md
- Workflow: 02-inspect-configuration
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1142, windows-1172
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/02-inspect-configuration/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/02-inspect-configuration/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w03

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/03-check-health-and-readiness/SKILL.md
- Workflow: 03-check-health-and-readiness
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1143, windows-1173
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/03-check-health-and-readiness/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/03-check-health-and-readiness/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w04

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/04-open-the-target-surface/SKILL.md
- Workflow: 04-open-the-target-surface
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1144, windows-1174
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/04-open-the-target-surface/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/04-open-the-target-surface/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w05

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/05-close-the-target-safely/SKILL.md
- Workflow: 05-close-the-target-safely
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1145, windows-1175
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/05-close-the-target-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/05-close-the-target-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w06

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/06-switch-context-and-focus/SKILL.md
- Workflow: 06-switch-context-and-focus
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1146, windows-1176
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/06-switch-context-and-focus/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/06-switch-context-and-focus/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w07

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/07-search-for-a-target/SKILL.md
- Workflow: 07-search-for-a-target
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1147, windows-1177
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/07-search-for-a-target/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/07-search-for-a-target/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w08

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/08-filter-and-narrow-results/SKILL.md
- Workflow: 08-filter-and-narrow-results
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1148, windows-1178
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/08-filter-and-narrow-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/08-filter-and-narrow-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w09

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/09-sort-and-prioritize-results/SKILL.md
- Workflow: 09-sort-and-prioritize-results
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1149, windows-1179
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/09-sort-and-prioritize-results/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/09-sort-and-prioritize-results/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w10

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/10-create-a-new-item/SKILL.md
- Workflow: 10-create-a-new-item
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1150, windows-1180
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/10-create-a-new-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/10-create-a-new-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w11

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/11-rename-an-existing-item/SKILL.md
- Workflow: 11-rename-an-existing-item
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1151, windows-1181
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/11-rename-an-existing-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/11-rename-an-existing-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w12

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/12-move-an-item-safely/SKILL.md
- Workflow: 12-move-an-item-safely
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1152, windows-1182
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/12-move-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/12-move-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w13

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/13-copy-an-item-safely/SKILL.md
- Workflow: 13-copy-an-item-safely
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1153, windows-1183
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/13-copy-an-item-safely/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/13-copy-an-item-safely/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w14

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/14-remove-an-item-with-recovery-protection/SKILL.md
- Workflow: 14-remove-an-item-with-recovery-protection
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1154, windows-1184
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/14-remove-an-item-with-recovery-protection/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/14-remove-an-item-with-recovery-protection/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w15

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/15-restore-a-prior-item/SKILL.md
- Workflow: 15-restore-a-prior-item
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1155, windows-1185
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/15-restore-a-prior-item/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/15-restore-a-prior-item/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w16

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/16-configure-a-default-option/SKILL.md
- Workflow: 16-configure-a-default-option
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1156, windows-1186
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/16-configure-a-default-option/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/16-configure-a-default-option/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w17

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/17-change-a-user-preference/SKILL.md
- Workflow: 17-change-a-user-preference
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1157, windows-1187
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/17-change-a-user-preference/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/17-change-a-user-preference/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w18

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/18-inspect-access-and-permissions/SKILL.md
- Workflow: 18-inspect-access-and-permissions
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1158, windows-1188
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/18-inspect-access-and-permissions/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/18-inspect-access-and-permissions/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w19

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/19-inspect-dependencies-and-prerequisites/SKILL.md
- Workflow: 19-inspect-dependencies-and-prerequisites
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1159, windows-1189
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/19-inspect-dependencies-and-prerequisites/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/19-inspect-dependencies-and-prerequisites/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w20

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/20-check-compatibility-and-version-support/SKILL.md
- Workflow: 20-check-compatibility-and-version-support
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1160, windows-1190
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/20-check-compatibility-and-version-support/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/20-check-compatibility-and-version-support/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w21

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/21-diagnose-a-common-failure/SKILL.md
- Workflow: 21-diagnose-a-common-failure
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1161, windows-1191
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/21-diagnose-a-common-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/21-diagnose-a-common-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w22

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/22-collect-minimal-diagnostic-evidence/SKILL.md
- Workflow: 22-collect-minimal-diagnostic-evidence
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1162, windows-1192
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/22-collect-minimal-diagnostic-evidence/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/22-collect-minimal-diagnostic-evidence/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w23

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/23-recover-from-a-reversible-failure/SKILL.md
- Workflow: 23-recover-from-a-reversible-failure
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1163, windows-1193
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/23-recover-from-a-reversible-failure/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/23-recover-from-a-reversible-failure/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w24

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/24-automate-a-repeatable-workflow/SKILL.md
- Workflow: 24-automate-a-repeatable-workflow
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1164, windows-1194
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/24-automate-a-repeatable-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/24-automate-a-repeatable-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w25

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/25-validate-an-automation-workflow/SKILL.md
- Workflow: 25-validate-an-automation-workflow
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1165, windows-1195
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/25-validate-an-automation-workflow/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/25-validate-an-automation-workflow/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w26

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/26-monitor-ongoing-state/SKILL.md
- Workflow: 26-monitor-ongoing-state
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1166, windows-1196
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/26-monitor-ongoing-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/26-monitor-ongoing-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w27

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/27-document-a-configuration-or-action/SKILL.md
- Workflow: 27-document-a-configuration-or-action
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1167, windows-1197
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/27-document-a-configuration-or-action/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/27-document-a-configuration-or-action/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w28

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/28-compare-before-and-after-state/SKILL.md
- Workflow: 28-compare-before-and-after-state
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1168, windows-1198
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/28-compare-before-and-after-state/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/28-compare-before-and-after-state/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w29

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/29-perform-routine-maintenance/SKILL.md
- Workflow: 29-perform-routine-maintenance
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1169, windows-1199
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/29-perform-routine-maintenance/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/29-perform-routine-maintenance/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.


### windows-consolidated-g12-w30

- Replacement: ai-agent-skills/23-windows-computer-operations (by Luo Kai)/00-consolidated-desktop-operations/12-backup-provisioning/30-hand-off-a-verified-outcome/SKILL.md
- Workflow: 30-hand-off-a-verified-outcome
- Domains merged: 39-backup-recovery, 40-provisioning-accounts
- Retired IDs: windows-1170, windows-1200
- Retired paths:
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/39-backup-recovery/30-hand-off-a-verified-outcome/SKILL.md
  - ai-agent-skills/23-windows-computer-operations (by Luo Kai)/40-provisioning-accounts/30-hand-off-a-verified-outcome/SKILL.md
- The replacement retains each full source workflow as a nested domain profile; only repeated frontmatter is replaced by consolidated metadata.
