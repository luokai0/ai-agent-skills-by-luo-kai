#!/usr/bin/env python3
"""Fail if any tracked repository path cannot be checked out on Windows."""

from __future__ import annotations

import subprocess
import sys

INVALID_CHARACTERS = set('<>:"|?*')
RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
    *(f"COM{i}" for i in ("¹", "²", "³")),
    *(f"LPT{i}" for i in ("¹", "²", "³")),
}


def windows_path_problems(path: str) -> list[str]:
    problems: list[str] = []
    for component in path.split("/"):
        if not component:
            problems.append("empty path component")
            continue

        bad = sorted({char for char in component if char in INVALID_CHARACTERS or ord(char) < 32})
        if bad:
            problems.append(f"invalid character(s) {bad!r} in component {component!r}")

        if component.endswith((" ", ".")):
            problems.append(f"component ends in a space or dot: {component!r}")

        device_name = component.split(".", 1)[0].upper()
        if device_name in RESERVED_NAMES:
            problems.append(f"reserved Windows device name: {component!r}")

    return problems


def main() -> int:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    )
    paths = [entry.decode("utf-8", errors="surrogateescape") for entry in result.stdout.split(b"\0") if entry]

    failures: list[tuple[str, list[str]]] = []
    for path in paths:
        problems = windows_path_problems(path)
        if problems:
            failures.append((path, problems))

    print(f"Scanned {len(paths):,} tracked paths.")
    if failures:
        print(f"Found {len(failures):,} Windows-incompatible path(s):", file=sys.stderr)
        for path, problems in failures:
            print(f" - {path!r}", file=sys.stderr)
            for problem in problems:
                print(f"    {problem}", file=sys.stderr)
        return 1

    print("PASS: no tracked path contains Windows-invalid characters, trailing spaces/dots, or reserved device names.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
