---
name: conducting-memory-forensics-with-volatility
description: >
  Performs authorized memory forensics with Volatility 3 to investigate process
  execution, injection, network connections, suspicious command history, and
  memory-resident malware during incident response. Use for RAM dump analysis,
  volatile evidence triage, and incident-response investigations.
domain: cybersecurity
subdomain: incident-response
tags: [memory-forensics, volatility, RAM-analysis, process-injection, DFIR]
version: 1.0.0
author: mahipal
license: Apache-2.0
metadata:
  original_author: mahipal
  adapted_by: Luo Kai
  modified: "2026-11-19"
  source: https://github.com/pinkpixel-dev/skills-collection-1
---

# Conducting Memory Forensics with Volatility

## When to Use

- An endpoint has been contained during an active incident and volatile evidence must be preserved.
- EDR alerts suggest process injection or fileless malware that may exist only in memory.
- Investigators need to correlate process trees, network connections, loaded modules, and command history.
- A rootkit or kernel-level compromise is suspected and disk-only analysis is insufficient.

Do not use this workflow for disk images or general file-system artifacts; use dedicated disk-forensics tools for those tasks.

## Authorization and evidence safety

Only analyze systems and memory images you own or are explicitly authorized to investigate. Preserve chain of custody and record who acquired the image, when, how, and with which tool.

The included helper runs Volatility plugins in read-only analysis mode. It does not execute extracted payloads or change the source memory image. Never run commands or binaries recovered from memory. Treat recovered credentials, hashes, tokens, browser data, and personal information as highly sensitive evidence. Record exposure and arrange secure rotation; do not copy secrets into reports or send them to third parties.

## Prerequisites

- A documented memory-acquisition tool and an authorized evidence image.
- Volatility 3 installed with Python 3.8+ and the required symbol tables.
- Storage appropriate for the memory image and derived evidence.
- YARA rules for memory malware detection, where authorized.
- A baseline of normal processes and DLLs for the operating-system version.
- Chain-of-custody documentation for evidence handling.

## Workflow

### Step 1: Acquire and preserve the memory image

Capture RAM using a forensically sound method, such as WinPmem, Magnet RAM Capture, DumpIt, or AVML for Linux. Do not power down or modify the target before acquisition unless containment procedures require it.

Record the host, acquisition tool and version, operator, UTC timestamp, image size, and SHA-256 hash. Preserve the original image as read-only and perform analysis on a verified working copy.

### Step 2: Identify the operating system and profile

Use Volatility 3 to identify the operating system and validate the detected symbols:

    vol -f memory.raw windows.info

Record the OS build, kernel base, DTB, and symbol information. Resolve symbol errors before trusting downstream plugin output.

### Step 3: Analyze processes

Use process-listing and process-scan plugins to identify hidden or unlinked processes:

    vol -f memory.raw windows.pslist
    vol -f memory.raw windows.pstree
    vol -f memory.raw windows.psscan

Compare the active list with the scan results. Investigate unusual parent-child relationships, misspelled process names, unexpected executable paths, and duplicate singleton processes. A suspicious name is an indicator, not proof of compromise.

### Step 4: Investigate network connections

Extract active and recently closed connections:

    vol -f memory.raw windows.netscan

Correlate local and foreign addresses with process IDs, known infrastructure, endpoint telemetry, and the incident timeline. Investigate unexpected external destinations and non-browser processes making outbound connections.

### Step 5: Detect injection and memory-resident malware

Use malfind to identify suspicious executable memory regions:

    vol -f memory.raw windows.malfind

Review protection flags, memory contents, process context, and offsets. Where authorized, scan a working copy with YARA rules and record exact rule names and offsets. Do not execute extracted code.

### Step 6: Review modules, DLLs, and command history

Useful plugins include:

    vol -f memory.raw windows.modules
    vol -f memory.raw windows.driverscan
    vol -f memory.raw windows.dlllist --pid 3847
    vol -f memory.raw windows.cmdline

Compare active modules with scanned drivers. Review command-line indicators such as encoded PowerShell, suspicious download commands, and credential-dumping tool names in context. Treat recovered credentials and hashes as sensitive evidence; do not reproduce their values in a general-purpose report.

### Step 7: Generate a structured report

The included scripts/agent.py helper runs selected Volatility plugins and writes a JSON report. It validates the input image and plugin name, uses an argument list without a shell, applies a timeout, and avoids overwriting the source image.

Run it from an isolated analysis environment:

    python scripts/agent.py --memory-file memory.raw --output reports/memory-forensics.json

Review the generated report manually. Plugin output is evidence to validate, not an automatic incident verdict.

## Key concepts

| Term | Definition |
|---|---|
| Volatile evidence | Data present in RAM that may be lost when a system powers off |
| Process injection | Code placed in another process's memory to evade ordinary execution visibility |
| EPROCESS | Windows kernel structure representing a process |
| VAD | Virtual Address Descriptor describing memory regions allocated to a process |
| PAGE_EXECUTE_READWRITE | Memory protection state that can be suspicious but is not proof of malicious injection |
| Memory-resident malware | Malware operating in RAM without relying on persistent files |

## Tools and systems

- Volatility 3: primary open-source memory-forensics framework.
- WinPmem, DumpIt, and Magnet RAM Capture: Windows acquisition options.
- AVML: Linux memory acquisition.
- YARA: rule-based scanning of memory images and extracted evidence.
- MemProcFS: presents memory images through a virtual file-system interface.

## Common pitfalls

- Analyzing only the process list and skipping process-scan comparisons.
- Failing to preserve the original image and its hash.
- Using outdated Volatility 2 profiles on modern systems.
- Treating every executable memory region as malicious without contextual review.
- Running recovered payloads instead of analyzing them statically.
- Publishing raw credentials, hashes, or private data in a report.

## Output format

Include incident ID, evidence identifier, SHA-256, OS build, Volatility version, plugins executed, findings with PIDs and offsets, network indicators, YARA matches, confidence, limitations, and recommended containment or recovery actions. Store the report under the incident's access controls.
