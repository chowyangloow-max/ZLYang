#!/usr/bin/env python3
"""Build a run's record-lineage dependency graph and report unresolved links."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_records(root: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    records: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted((root / "workspace" / "records").rglob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        record_id = data.get("record_id") if isinstance(data, dict) else None
        if isinstance(record_id, str):
            records[record_id] = (path, data)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    records = load_records(root)
    selected = {
        record_id: item for record_id, item in records.items()
        if item[1].get("provenance", {}).get("run_id") == args.run_id
    }
    nodes = [
        {"record_id": record_id, "record_type": data.get("record_type"), "status": data.get("status"), "path": str(path.relative_to(root))}
        for record_id, (path, data) in selected.items()
    ]
    edges: list[dict[str, str]] = []
    unresolved: list[dict[str, str]] = []
    for record_id, (_, data) in selected.items():
        for field in ("source_refs", "parent_refs", "supersedes", "superseded_by"):
            for ref in data.get(field, []):
                target = ref.get("record_id") if isinstance(ref, dict) else None
                if not target:
                    continue
                edge = {"from": record_id, "to": target, "relation": field}
                (edges if target in records else unresolved).append(edge)
        for dep in data.get("extensions", {}).get("dependencies", []):
            target = dep.get("record_id") if isinstance(dep, dict) else dep
            if isinstance(target, str):
                edge = {"from": record_id, "to": target, "relation": "execution_dependency"}
                (edges if target in records else unresolved).append(edge)
    output = {
        "schema_version": "1.1.0",
        "run_id": args.run_id,
        "updated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "nodes": nodes,
        "edges": edges,
        "unresolved_edges": unresolved,
    }
    path = root / "workspace" / "runs" / args.run_id / "dependency-graph.json"
    if not path.parent.is_dir():
        raise SystemExit(f"Run does not exist: {args.run_id}")
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Dependency graph: {len(nodes)} nodes, {len(edges)} edges, {len(unresolved)} unresolved")
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
