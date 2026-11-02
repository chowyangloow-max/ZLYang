#!/usr/bin/env python3
"""Install project skills for Codex discovery using non-destructive symlinks."""
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/".agents"/"skills"
target.mkdir(parents=True,exist_ok=True)
for source in sorted((ROOT/"skills").iterdir()):
    if not (source/"SKILL.md").is_file():continue
    destination=target/source.name
    if destination.exists() or destination.is_symlink():
        print(f"Preserved existing: {destination}")
        continue
    destination.symlink_to(Path("../../skills")/source.name,target_is_directory=True)
    print(f"Installed: {destination}")
