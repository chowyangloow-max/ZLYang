#!/usr/bin/env python3
"""Initialize the local ZLYang OS workspace without overwriting user data."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_DIRS = (
    "inbox",
    "evidence",
    "records",
    "baselines",
    "audits",
    "knowledge",
    "runs",
    "archive",
)


def initialize(root: Path) -> tuple[list[Path], list[Path]]:
    workspace = root / "workspace"
    created: list[Path] = []
    existing: list[Path] = []
    for name in WORKSPACE_DIRS:
        path = workspace / name
        if path.exists():
            existing.append(path)
        else:
            path.mkdir(parents=True, exist_ok=False)
            created.append(path)

        keep = path / ".gitkeep"
        if not keep.exists():
            keep.touch()

    metadata = workspace / ".zlyang.json"
    if metadata.exists():
        existing.append(metadata)
    else:
        metadata.write_text(
            json.dumps(
                {
                    "schema_version": "1.1.0",
                    "project": "ZLYang OS",
                    "initialized_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        created.append(metadata)
    return created, existing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Project root (defaults to repository root)")
    args = parser.parse_args()
    root = args.root.resolve()
    created, existing = initialize(root)
    print(f"ZLYang workspace ready: {root / 'workspace'}")
    print(f"Created: {len(created)}; preserved existing: {len(existing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
