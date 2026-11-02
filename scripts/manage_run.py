#!/usr/bin/env python3
"""Create and advance gated ZLYang OS runs without overwriting existing work."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from purpose_gate import assess, read_contract


ROOT = Path(__file__).resolve().parents[1]
STAGES = ("verify", "distill", "baseline", "audit", "knowledge")
CONTROL_TEMPLATES = {
    "coverage-matrix.json": "coverage-matrix.json",
    "deletion-ledger.json": "deletion-ledger.json",
    "dependency-graph.json": "dependency-graph.json",
    "review-plan.json": "review-plan.json",
}


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Expected a JSON object: {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise SystemExit("Slug must contain an ASCII letter or digit")
    return slug


def review_mode(risk: str) -> str:
    return {"low": "single", "medium": "dual_independent", "high": "dual_independent_and_independent_audit"}[risk]


def new_run_id(root: Path, slug: str) -> str:
    prefix = f"run-{datetime.now().astimezone():%Y%m%d}-{slug}-"
    runs = root / "workspace" / "runs"
    for number in range(1, 100):
        candidate = f"{prefix}{number:02d}"
        if not (runs / candidate).exists():
            return candidate
    raise SystemExit(f"No available run number for {prefix}NN")


def start(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    contract = read_contract(args.purpose_file)
    gate = assess(contract)
    if gate["status"] != "ready":
        raise SystemExit("Purpose gate blocked: " + str(gate["next_question"]))
    run_id = new_run_id(root, safe_slug(args.slug))
    run_dir = root / "workspace" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    timestamp = now()
    mode = review_mode(args.risk)

    manifest = read_json(root / "templates" / "run-manifest.json")
    manifest.update({
        "run_id": run_id,
        "started_at": timestamp,
        "owner": args.owner,
        "objective": args.objective,
        "risk_level": args.risk,
        "review_mode": mode,
        "purpose_gate": "pass",
        "purpose_contract_path": "purpose-contract.json",
    })
    write_json(run_dir / "manifest.json", manifest)
    write_json(run_dir / "purpose-contract.json", contract)

    checkpoint_template = read_json(root / "templates" / "checkpoint.json")
    for index, stage in enumerate(STAGES):
        checkpoint = dict(checkpoint_template)
        checkpoint.update({
            "run_id": run_id,
            "stage": stage,
            "status": "in_progress" if index == 0 else "pending",
            "updated_at": timestamp,
        })
        write_json(run_dir / f"checkpoint-{stage}.json", checkpoint)

    for filename, template_name in CONTROL_TEMPLATES.items():
        data = read_json(root / "templates" / template_name)
        data["run_id"] = run_id
        if "updated_at" in data:
            data["updated_at"] = timestamp
        if filename == "review-plan.json":
            data["risk_level"] = args.risk
            data["review_mode"] = mode
        write_json(run_dir / filename, data)

    print(run_id)
    print(f"Run ready: {run_dir}")
    print(f"Risk: {args.risk}; review mode: {mode}; current stage: verify")
    return 0


def control_errors(run_dir: Path, stage: str) -> list[str]:
    errors: list[str] = []
    coverage = read_json(run_dir / "coverage-matrix.json")
    ledger = read_json(run_dir / "deletion-ledger.json")
    graph = read_json(run_dir / "dependency-graph.json")
    review = read_json(run_dir / "review-plan.json")
    items = coverage.get("items", [])
    entries = ledger.get("entries", [])

    if stage == "verify" and not items:
        errors.append("coverage matrix has no material items")
    if stage in {"distill", "baseline", "audit", "knowledge"}:
        ledger_ids = {entry.get("ledger_id") for entry in entries if isinstance(entry, dict)}
        for item in items:
            if not isinstance(item, dict) or not item.get("material", True):
                continue
            if not item.get("distillation_ref") and item.get("ledger_entry_id") not in ledger_ids:
                errors.append(f"coverage item {item.get('material_id', '?')} has no distillation destination or ledger entry")
        for entry in entries:
            if isinstance(entry, dict) and entry.get("load_bearing") and entry.get("review_status") != "approved":
                errors.append(f"load-bearing ledger entry {entry.get('ledger_id', '?')} is not approved")
    if stage in {"baseline", "audit", "knowledge"}:
        if graph.get("unresolved_edges"):
            errors.append("dependency graph contains unresolved edges")
        for item in items:
            if isinstance(item, dict) and item.get("material", True) and item.get("disposition", "retained") != "excluded" and not item.get("baseline_ref"):
                errors.append(f"coverage item {item.get('material_id', '?')} has no baseline destination")
    if stage in {"verify", "distill", "baseline", "audit", "knowledge"}:
        risk = review.get("risk_level")
        reviewers = [r for r in review.get("reviewers", []) if isinstance(r, dict) and r.get("independent")]
        verify_reviewers = {r.get("reviewer_id") for r in reviewers if "verify" in r.get("roles", [])}
        if risk in {"medium", "high"} and len(verify_reviewers) < 2:
            errors.append("risk level requires two independent verify reviewers")
        if review.get("disagreements") and any(d.get("status") != "resolved" for d in review["disagreements"] if isinstance(d, dict)):
            errors.append("independent-review disagreement remains unresolved")
        if risk == "high" and stage in {"audit", "knowledge"}:
            authors = set(review.get("baseline_author_ids", []))
            auditors = {r.get("reviewer_id") for r in reviewers if "audit" in r.get("roles", [])}
            if not (auditors - authors):
                errors.append("high risk requires an independent auditor who is not a baseline author")
    if stage in {"audit", "knowledge"}:
        for item in items:
            if isinstance(item, dict) and item.get("material", True) and item.get("disposition", "retained") != "excluded" and not item.get("audit_ref"):
                errors.append(f"coverage item {item.get('material_id', '?')} has no audit destination")
    if stage == "knowledge":
        for item in items:
            if isinstance(item, dict) and item.get("material", True) and item.get("disposition", "retained") != "excluded" and not item.get("knowledge_ref"):
                errors.append(f"coverage item {item.get('material_id', '?')} has no knowledge destination")
    return errors


def checkpoint(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    run_dir = root / "workspace" / "runs" / args.run_id
    manifest_path = run_dir / "manifest.json"
    manifest = read_json(manifest_path)
    if manifest.get("current_stage") != args.stage:
        raise SystemExit(f"Current stage is {manifest.get('current_stage')!r}, not {args.stage!r}")
    checkpoint_path = run_dir / f"checkpoint-{args.stage}.json"
    existing_checkpoint = read_json(checkpoint_path)
    if args.result == "conditional_pass" and args.stage != "audit":
        raise SystemExit("conditional_pass is only valid for the audit stage")
    if args.result == "conditional_pass" and not args.unresolved:
        raise SystemExit("conditional_pass requires at least one bounded unresolved condition")
    if args.result == "pass":
        errors = control_errors(run_dir, args.stage)
        unresolved = args.unresolved or existing_checkpoint.get("unresolved_critical", [])
        if unresolved:
            errors.append("checkpoint contains unresolved critical items")
        if args.stage == "audit" and (args.reconstruction != "pass" or args.mutation != "pass"):
            errors.append("audit pass requires passing reconstruction and mutation tests")
        if errors:
            raise SystemExit("Gate blocked:\n- " + "\n- ".join(errors))

    timestamp = now()
    data = existing_checkpoint
    data.update({
        "status": "completed" if args.result == "pass" else "blocked",
        "gate_status": args.result,
        "updated_at": timestamp,
        "reviewer_ids": args.reviewer,
        "unresolved_critical": args.unresolved,
        "notes": args.notes,
    })
    if args.stage == "audit":
        data["tests"] = {"reconstruction": args.reconstruction, "mutation": args.mutation}
    write_json(checkpoint_path, data)

    stage_index = STAGES.index(args.stage)
    manifest["stages"][stage_index]["status"] = data["status"]
    if args.result in {"blocked", "conditional_pass"}:
        manifest["status"] = "blocked"
        manifest["blocked_gate"] = args.stage
    elif stage_index == len(STAGES) - 1:
        manifest["status"] = "completed"
        manifest["completed_at"] = timestamp
        manifest["current_stage"] = None
        manifest["blocked_gate"] = None
    else:
        next_stage = STAGES[stage_index + 1]
        manifest["status"] = "in_progress"
        manifest["current_stage"] = next_stage
        manifest["blocked_gate"] = None
        manifest["stages"][stage_index + 1]["status"] = "in_progress"
        next_checkpoint = read_json(run_dir / f"checkpoint-{next_stage}.json")
        next_checkpoint["status"] = "in_progress"
        next_checkpoint["updated_at"] = timestamp
        write_json(run_dir / f"checkpoint-{next_stage}.json", next_checkpoint)
    write_json(manifest_path, manifest)
    print(f"{args.run_id}: {args.stage} -> {args.result}")
    print(f"Run status: {manifest['status']}; next stage: {manifest.get('current_stage')}")
    return 0


def status(args: argparse.Namespace) -> int:
    manifest = read_json(args.root.resolve() / "workspace" / "runs" / args.run_id / "manifest.json")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Project root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Create a new gated run")
    start_parser.add_argument("--slug", required=True)
    start_parser.add_argument("--owner", required=True)
    start_parser.add_argument("--objective", required=True)
    start_parser.add_argument("--purpose-file", type=Path, required=True)
    start_parser.add_argument("--risk", choices=("low", "medium", "high"), default="low")
    start_parser.set_defaults(func=start)

    checkpoint_parser = subparsers.add_parser("checkpoint", help="Pass or block the current stage")
    checkpoint_parser.add_argument("--run-id", required=True)
    checkpoint_parser.add_argument("--stage", choices=STAGES, required=True)
    checkpoint_parser.add_argument("--result", choices=("pass", "conditional_pass", "blocked"), required=True)
    checkpoint_parser.add_argument("--reviewer", action="append", default=[])
    checkpoint_parser.add_argument("--unresolved", action="append", default=[])
    checkpoint_parser.add_argument("--notes", default="")
    checkpoint_parser.add_argument("--reconstruction", choices=("pending", "pass", "fail"), default="pending")
    checkpoint_parser.add_argument("--mutation", choices=("pending", "pass", "fail"), default="pending")
    checkpoint_parser.set_defaults(func=checkpoint)

    status_parser = subparsers.add_parser("status", help="Show run status")
    status_parser.add_argument("--run-id", required=True)
    status_parser.set_defaults(func=status)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
