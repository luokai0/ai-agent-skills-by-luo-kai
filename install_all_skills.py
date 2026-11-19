#!/usr/bin/env python3
"""Compatibility entry point for the reorganized skills source installer."""
from pathlib import Path
import runpy

installer = Path(__file__).resolve().parent / "scripts" / "installer" / "install_all_skills.py"
runpy.run_path(str(installer), run_name="__main__")
