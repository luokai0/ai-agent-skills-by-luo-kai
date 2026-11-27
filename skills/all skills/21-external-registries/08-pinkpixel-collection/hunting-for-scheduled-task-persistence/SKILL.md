---
name: hunting-for-scheduled-task-persistence
description: >
  Hunts for Windows scheduled-task persistence by reviewing task creation events,
  suspicious task actions, and unusual scheduling patterns. Use during authorized
  threat hunting, incident response, and investigation of MITRE ATT&CK T1053.005.
domain: cybersecurity
subdomain: threat-hunting
tags: [threat-hunting, MITRE-ATT&CK, scheduled-tasks, persistence, T1053]
version: "1.0"
author: mahipal
license: Apache-2.0
metadata:
  original_author: mahipal
  adapted_by: Luo Kai
  modified: "2026-11-19"
  source: https://github.com/pinkpixel-dev/skills-collection-1
---

# Hunting for Scheduled Task Persistence

## When to Use

- Threat intelligence indicates scheduled tasks are being used for persistence.
- EDR or SIEM alerts identify suspicious task creation or execution.
- An incident investigation needs to scope task-based persistence.
- A periodic hunt is reviewing task actions and creation events.

## Authorization and safety

Only inspect systems and event logs you own or are explicitly authorized to investigate. The included helper performs read-only enumeration, event-log parsing, and task XML export. It does not create, delete, disable, or execute scheduled tasks.

Task actions and exported XML may contain usernames, internal paths, command-line arguments, or secrets. Store results as sensitive incident evidence and redact before sharing. Never execute a suspicious task action to test it.

## Prerequisites

- Authorized Windows endpoint access or exported Security EVTX logs.
- EDR or SIEM telemetry where available.
- Sysmon and Windows Security event forwarding configured where appropriate.
- Threat-intelligence indicators for correlation.
- Python 3.8+; install python-evtx only when parsing EVTX files.

## Workflow

1. **Form a hypothesis:** define the persistence behavior and expected evidence from threat intelligence or an ATT&CK gap analysis.
2. **Identify data sources:** determine which endpoint events, task metadata, and telemetry are needed.
3. **Collect read-only evidence:** enumerate tasks or parse an authorized EVTX export.
4. **Analyze indicators:** review task actions, task paths, authors, run-as identities, schedules, and creation events.
5. **Validate findings:** distinguish suspicious indicators from legitimate vendor tasks and administrative automation.
6. **Correlate activity:** connect task creation to process, network, authentication, and endpoint events.
7. **Document and report:** preserve evidence, confidence, limitations, and recommended response actions.

## Detection indicators

Review task actions for encoded PowerShell, download-and-execute patterns, script hosts, LOLBins, unusual temporary or public directories, unexpected external URLs, and commands that do not match the task's stated purpose.

A non-vendor task is not automatically malicious. Use the host baseline, task author, run-as identity, creation time, parent process, and change-management record to establish context.

## Included helper

The scripts/agent.py helper supports:

- enumerate: read-only task enumeration and risk indicators.
- events: read-only parsing of Security EVTX Event ID 4698.
- export: read-only export of one task's XML definition.

Examples:

    python scripts/agent.py enumerate
    python scripts/agent.py events --evtx-file Security.evtx
    python scripts/agent.py export --task-name "\Microsoft\Windows\UpdateOrchestrator\Schedule Scan"

The helper validates inputs, uses fixed argument arrays without a shell, applies command timeouts, and reports command failures instead of treating empty output as a clean result.

## Key concepts

| Concept | Description |
|---|---|
| T1053.005 | MITRE ATT&CK Scheduled Task/Job: Scheduled Task |
| Event ID 4698 | Windows Security event for scheduled task creation |
| Task action | Program or command launched by a scheduled task |
| Task principal | User or security context under which a task runs |
| Persistence | Mechanism that allows activity to survive logoff or reboot |

## Tools and systems

- Microsoft Defender for Endpoint: endpoint telemetry and hunting.
- Sysmon: detailed process and task-related event collection.
- Splunk, Elastic, and Microsoft Sentinel: event correlation and investigation.
- Sigma: portable detection-rule format.
- Windows Task Scheduler and schtasks: native read-only task inspection.

## Common scenarios

- A task repeatedly launches an encoded PowerShell command.
- A task recreates a payload after reboot.
- A task copies sensitive files on a recurring schedule.
- A task action launches a script host from an unexpected directory.

## Output format

Record hunt ID, technique, host, user context, evidence sources, task name and action, creation time, risk level, confidence, indicators, correlation references, recommended containment, and unresolved questions.
