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
