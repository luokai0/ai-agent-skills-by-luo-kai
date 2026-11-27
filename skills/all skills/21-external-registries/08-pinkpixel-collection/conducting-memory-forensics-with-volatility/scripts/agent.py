#!/usr/bin/env python3
# Adapted by Luo Kai on 2026-11-19 from the PinkPixel Skills Collection.
# Original upstream author: mahipal. Licensed under Apache-2.0; see the
# collection LICENSE and NOTICE.md. This file is a read-only analysis helper.
"""Memory Forensics Agent - Automates Volatility 3 analysis of memory dumps."""

import argparse
import json
import logging
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PLUGIN_NAME = re.compile(r"^[A-Za-z0-9_.]+$")
MAX_PLUGIN_TIMEOUT = 600


def run_volatility(memory_file, plugin, extra_args=None):
    """Run one Volatility plugin without a shell and return parsed tabular output."""
    try:
        memory_path = Path(memory_file).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        logger.error("Memory image cannot be resolved: %s", exc)
        return []

    if not memory_path.is_file():
        logger.error("Memory image is not a regular file: %s", memory_path)
        return []
    if not isinstance(plugin, str) or not PLUGIN_NAME.fullmatch(plugin):
        logger.error("Rejected invalid Volatility plugin name")
        return []
    if extra_args is not None:
        if not isinstance(extra_args, (list, tuple)) or any(
            not isinstance(arg, str) or "\x00" in arg for arg in extra_args
        ):
            logger.error("Volatility extra arguments must be a list of safe strings")
            return []

    cmd = ["vol", "-f", str(memory_path), plugin]
    if extra_args:
        cmd.extend(extra_args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=MAX_PLUGIN_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logger.error("Volatility plugin %s exceeded %d seconds", plugin, MAX_PLUGIN_TIMEOUT)
        return []
    except FileNotFoundError:
        logger.error("Volatility 3 executable 'vol' was not found on PATH")
        return []
    except OSError as exc:
        logger.error("Could not start Volatility plugin %s: %s", plugin, exc)
        return []

    if result.returncode != 0:
        logger.error("Volatility plugin %s failed (exit %d): %s", plugin, result.returncode, result.stderr[:300])
        return []

    lines = result.stdout.strip().splitlines()
    if len(lines) < 2:
        return []
    headers = [header.strip() for header in lines[0].split("\t")]
    rows = []
    for line in lines[1:]:
        if line.strip() and not line.startswith("*"):
            fields = [field.strip() for field in line.split("\t")]
            if len(fields) == len(headers):
                rows.append(dict(zip(headers, fields)))
    logger.info("Plugin %s returned %d rows", plugin, len(rows))
    return rows


def analyze_processes(memory_file):
    """List running processes and identify suspicious ones."""
    processes = run_volatility(memory_file, "windows.pslist")
    suspicious = []
    suspicious_names = [
        "mimikatz", "procdump", "psexec", "cobalt", "beacon", "meterpreter",
        "nc.exe", "ncat", "powershell", "cmd.exe", "wscript", "cscript",
        "certutil", "bitsadmin", "mshta", "regsvr32",
    ]
    for proc in processes:
        name = proc.get("ImageFileName", "").lower()
        if any(indicator in name for indicator in suspicious_names):
            proc["suspicious_reason"] = "Known offensive-tool name; validate in context"
            suspicious.append(proc)
    logger.info("Processes: %d total, %d suspicious", len(processes), len(suspicious))
    return processes, suspicious


def analyze_network_connections(memory_file):
    """Extract network connections and identify possible command-and-control activity."""
    connections = run_volatility(memory_file, "windows.netscan")
    established = [connection for connection in connections if connection.get("State") == "ESTABLISHED"]
    logger.info("Network connections: %d total, %d established", len(connections), len(established))
    return connections, established


def detect_process_injection(memory_file):
    """Detect possible process injection using the Volatility malfind plugin."""
    results = run_volatility(memory_file, "windows.malfind")
    injected = []
    for entry in results:
        injected.append({
            "pid": entry.get("PID", ""),
            "process": entry.get("Process", ""),
            "start": entry.get("Start VPN", ""),
            "protection": entry.get("Protection", ""),
            "tag": entry.get("Tag", ""),
        })
    logger.info("Malfind: %d potential injection regions detected", len(injected))
    return injected


def analyze_dlls(memory_file, pid=None):
    """List loaded DLLs for a process or all processes."""
    args = ["--pid", str(pid)] if pid is not None else None
    return run_volatility(memory_file, "windows.dlllist", args)


def extract_command_history(memory_file):
    """Extract command-line history and flag suspicious indicators for review."""
    cmdline = run_volatility(memory_file, "windows.cmdline")
    suspicious_cmds = []
    indicators = [
        "powershell -enc", "invoke-expression", "downloadstring", "net user",
        "mimikatz", "sekurlsa", "lsadump", "reg save", "vssadmin",
        "certutil -urlcache", "bitsadmin /transfer",
    ]
    for entry in cmdline:
        args = entry.get("Args", "").lower()
        if any(indicator in args for indicator in indicators):
            entry["suspicious_reason"] = "Suspicious command indicator; verify surrounding evidence"
            suspicious_cmds.append(entry)
    logger.info("Command lines: %d total, %d suspicious", len(cmdline), len(suspicious_cmds))
    return cmdline, suspicious_cmds


def extract_registry_hives(memory_file):
    """List registry hives in memory."""
    hives = run_volatility(memory_file, "windows.registry.hivelist")
    logger.info("Registry hives: %d found", len(hives))
    return hives


def check_kernel_modules(memory_file):
    """List kernel modules and detect drivers absent from the active module list."""
    modules = run_volatility(memory_file, "windows.modules")
    drivers = run_volatility(memory_file, "windows.driverscan")
    module_names = {module.get("Name", "").lower() for module in modules}
    hidden = []
    for driver in drivers:
        if driver.get("Name", "").lower() not in module_names:
            hidden.append(driver)
            logger.warning("Driver absent from active module list: %s", driver.get("Name"))
    return modules, hidden


def generate_forensics_report(memory_file, processes, suspicious_procs, connections,
                               injections, suspicious_cmds, hidden_drivers):
    """Generate a structured memory-forensics report."""
    report = {
        "memory_image": str(Path(memory_file).expanduser()),
        "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
        "process_summary": {
            "total": len(processes),
            "suspicious": len(suspicious_procs),
            "details": suspicious_procs[:20],
        },
        "network_connections": {
            "established": len(connections),
            "details": connections[:20],
        },
        "process_injection": {
            "count": len(injections),
            "details": injections[:20],
        },
        "suspicious_commands": suspicious_cmds[:20],
        "hidden_drivers": hidden_drivers,
    }
    total_findings = len(suspicious_procs) + len(injections) + len(suspicious_cmds) + len(hidden_drivers)
    print(f"MEMORY FORENSICS REPORT - {total_findings} findings")
    return report


def main():
    parser = argparse.ArgumentParser(description="Memory Forensics Agent (Volatility 3)")
    parser.add_argument("--memory-file", required=True, type=Path, help="Path to an authorized memory dump")
    parser.add_argument("--output", type=Path, default=Path("memory_forensics_report.json"))
    args = parser.parse_args()

    memory_path = args.memory_file.expanduser().resolve()
    if not memory_path.is_file():
        parser.error(f"memory image does not exist or is not a file: {memory_path}")

    output_path = args.output.expanduser().resolve()
    if output_path == memory_path:
        parser.error("report output must not overwrite the source memory image")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    processes, suspicious = analyze_processes(memory_path)
    connections, established = analyze_network_connections(memory_path)
    injections = detect_process_injection(memory_path)
    _, suspicious_cmds = extract_command_history(memory_path)
    _, hidden = check_kernel_modules(memory_path)

    report = generate_forensics_report(
        memory_path, processes, suspicious, established,
        injections, suspicious_cmds, hidden,
    )
    with output_path.open("w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=2, ensure_ascii=False)
        report_file.write("\n")
    logger.info("Report saved to %s", output_path)


if __name__ == "__main__":
    main()
