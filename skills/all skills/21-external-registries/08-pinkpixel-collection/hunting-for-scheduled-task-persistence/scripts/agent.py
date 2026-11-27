#!/usr/bin/env python3
# Adapted by Luo Kai on 2026-11-19 from the PinkPixel Skills Collection.
# Original upstream author: mahipal. Licensed under Apache-2.0; see the
# collection LICENSE and NOTICE.md. This helper performs read-only collection.
"""Hunt for Windows scheduled-task persistence indicators (MITRE ATT&CK T1053.005)."""

import argparse
import csv
import json
import re
import subprocess
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

SUSPICIOUS_TASK_PATTERNS = [
    r"powershell.*-enc", r"powershell.*downloadstring", r"powershell.*iex",
    r"cmd\.exe\s+/c", r"mshta\.exe", r"rundll32\.exe", r"regsvr32\.exe",
    r"certutil.*-decode", r"bitsadmin.*transfer",
    r"wscript\.exe", r"cscript\.exe",
    r"\\temp\\", r"\\tmp\\", r"\\appdata\\local\\temp",
    r"\\users\\public\\", r"\\programdata\\",
    r"base64", r"http://", r"https://.*\.exe",
]

LEGITIMATE_TASK_PREFIXES = [
    r"\\Microsoft\\", r"\\Adobe\\", r"\\Google\\", r"\\Apple\\",
    r"\\Mozilla\\", r"\\Intel\\", r"\\NVIDIA\\",
]


def enumerate_tasks():
    """Enumerate scheduled tasks and score indicators without changing task state."""
    try:
        proc = subprocess.run(
            ["schtasks", "/query", "/fo", "CSV", "/v"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"error": "schtasks enumeration timed out"}
    except FileNotFoundError:
        return {"error": "schtasks is available only on Windows"}
    except OSError as exc:
        return {"error": f"could not start schtasks: {exc}"}

    if proc.returncode != 0:
        return {
            "error": "schtasks returned a non-zero exit code",
            "returncode": proc.returncode,
            "stderr": proc.stderr.strip()[:500],
        }
    if not proc.stdout.strip():
        return {"error": "schtasks returned no CSV output"}

    reader = csv.DictReader(StringIO(proc.stdout))
    required_headers = {"TaskName", "Task To Run"}
    if not reader.fieldnames or not required_headers.issubset(set(reader.fieldnames)):
        return {"error": "unexpected schtasks CSV headers", "headers": reader.fieldnames}

    findings = []
    for row in reader:
        task_name = row.get("TaskName", "")
        action = row.get("Task To Run", "")
        author = row.get("Author", "")
        schedule = row.get("Schedule Type", "")
        status = row.get("Status", "")
        is_legit = any(re.search(pattern, task_name, re.I) for pattern in LEGITIMATE_TASK_PREFIXES)
        matches = [pattern for pattern in SUSPICIOUS_TASK_PATTERNS if re.search(pattern, action, re.I)]
        is_suspicious = bool(matches)
        risk = "high" if is_suspicious else ("low" if is_legit else "medium")
        findings.append({
            "task_name": task_name,
            "action": action[:500],
            "author": author,
            "schedule": schedule,
            "status": status,
            "last_run": row.get("Last Run Time", ""),
            "next_run": row.get("Next Run Time", ""),
            "run_as_user": row.get("Run As User", ""),
            "risk": risk,
            "suspicious_match": is_suspicious,
            "matched_indicators": matches,
        })

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_tasks": len(findings),
        "high_risk": sum(1 for item in findings if item["risk"] == "high"),
        "medium_risk": sum(1 for item in findings if item["risk"] == "medium"),
        "suspicious_tasks": [item for item in findings if item["suspicious_match"]],
        "non_vendor_tasks": [item for item in findings if item["risk"] == "medium"],
        "collection_mode": "read-only",
    }


def scan_event_log_4698(evtx_file):
    """Parse Security EVTX for Event ID 4698 (Scheduled Task Created)."""
    path = Path(evtx_file).expanduser()
    if not path.is_file():
        return {"error": f"EVTX file not found: {path}"}
    try:
        import Evtx.Evtx as evtx_lib
    except ImportError:
        return {"error": "python-evtx is not installed"}

    findings = []
    try:
        with evtx_lib.Evtx(str(path)) as log:
            for record in log.records():
                xml = record.xml()
                if "<EventID>4698</EventID>" not in xml:
                    continue
                matched = [pattern for pattern in SUSPICIOUS_TASK_PATTERNS if re.search(pattern, xml, re.I)]
                findings.append({
                    "record_id": record.record_num(),
                    "suspicious": bool(matched),
                    "matched_indicators": matched,
                    "xml_snippet": xml[:1000],
                })
    except Exception as exc:
        return {"error": f"could not parse EVTX file: {exc}"}

    return {
        "file": str(path.resolve()),
        "task_creation_events": len(findings),
        "suspicious_events": sum(1 for item in findings if item["suspicious"]),
        "findings": findings[:200],
    }


def export_task_xml(task_name):
    """Export one scheduled task's XML using a fixed argument list and no shell."""
    if not isinstance(task_name, str) or not task_name.strip():
        return {"error": "task name must be a non-empty string"}
    if len(task_name) > 260 or any(ord(char) < 32 for char in task_name):
        return {"error": "task name contains invalid control characters or exceeds 260 characters"}

    try:
        proc = subprocess.run(
            ["schtasks", "/query", "/tn", task_name, "/xml"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"error": "task XML export timed out"}
    except FileNotFoundError:
        return {"error": "schtasks is available only on Windows"}
    except OSError as exc:
        return {"error": f"could not start schtasks: {exc}"}

    if proc.returncode == 0:
        return {"task_name": task_name, "xml": proc.stdout}
    return {"error": proc.stderr.strip()[:500], "returncode": proc.returncode}


def main():
    parser = argparse.ArgumentParser(description="Hunt for scheduled-task persistence indicators")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("enumerate", help="Enumerate and risk-score scheduled tasks (read-only)")
    events = sub.add_parser("events", help="Scan Security EVTX for task creation events")
    events.add_argument("--evtx-file", required=True)
    export = sub.add_parser("export", help="Export task XML for analysis (read-only)")
    export.add_argument("--task-name", required=True)
    args = parser.parse_args()

    if args.command == "enumerate":
        result = enumerate_tasks()
    elif args.command == "events":
        result = scan_event_log_4698(args.evtx_file)
    elif args.command == "export":
        result = export_task_xml(args.task_name)
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
