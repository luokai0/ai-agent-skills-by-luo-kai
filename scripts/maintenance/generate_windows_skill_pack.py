#!/usr/bin/env python3
"""Retired legacy generator.

The Windows collection was consolidated on 2026-11-20 into 360 profile-based
skills. This legacy generator must not recreate the retired standalone files.
Use the current consolidated collection and its validation workflow instead.
"""

def main() -> None:
    raise SystemExit(
        "This generator is retired. The Windows workflows are consolidated under "
        "00-consolidated-desktop-operations."
    )

if __name__ == "__main__":
    main()
