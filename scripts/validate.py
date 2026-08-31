#!/usr/bin/env python3
"""Validate ZLYang OS structure, Skills, schema, and optional JSON records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "zlyang-os",
    "zlyang-verify",
    "zlyang-distill",
    "zlyang-baseline",
    "zlyang-audit",
    "zlyang-knowledge",
    "generate-openings",
)
WORKSPACE_DIRS = ("inbox", "evidence", "records", "baselines", "audits", "knowledge", "runs", "archive")
REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "docs/data-model.md",
    "docs/run-controls.md",
    "schemas/zlyang-record.schema.json",
    "templates/record.json",
    "templates/intake.md",
    "templates/evidence.yaml",
    "templates/distillation.md",
    "templates/baseline.md",
    "templates/audit.md",
    "templates/knowledge.md",
    "templates/run-manifest.json",
    "templates/checkpoint.json",
    "templates/coverage-matrix.json",
    "templates/deletion-ledger.json",
    "templates/dependency-graph.json",
    "templates/review-plan.json",
    "scripts/manage_run.py",
    "scripts/build_dependency_graph.py",
)
RECORD_ID = re.compile(r"^zly-(source|evidence|claim|distillation|baseline|audit|knowledge|run)-\d{8}-[a-z0-9][a-z0-9-]*-\d{2}$")
STATUSES = {
    "draft", "verified", "partially_verified", "conflicted", "unverified", "rejected",
    "approved", "active", "superseded", "retired", "candidate", "published", "stale",
    "pass", "conditional_pass", "fail", "completed", "blocked",
}


def validate_skill_without_yaml(skill_dir: Path, expected_name: str, errors: list[str]) -> None:
    """Apply the official validator's structural invariants when PyYAML is unavailable."""
    skill_md = skill_dir / "SKILL.md"
    agent_yaml = skill_dir / "agents" / "openai.yaml"
    if not skill_md.is_file():
        errors.append(f"skill {expected_name}: missing SKILL.md")
        return
    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        errors.append(f"skill {expected_name}: invalid YAML frontmatter delimiters")
        return
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip('"').strip("'")
    if fields.get("name") != expected_name:
        errors.append(f"skill {expected_name}: frontmatter name does not match directory")
    if not fields.get("description") or fields["description"].startswith("[TODO:"):
        errors.append(f"skill {expected_name}: missing or unfinished description")
    if re.search(r"(?m)^[ ]{0,3}\[TODO:[^\n]*\][ \t]*$", content[match.end():]):
        errors.append(f"skill {expected_name}: unfinished TODO placeholder")
    if not agent_yaml.is_file():
        errors.append(f"skill {expected_name}: missing agents/openai.yaml")


def load_json(path: Path, errors: list[str]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def validate_iso(value: Any, field: str, path: Path, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{path}: {field} must be an ISO 8601 string")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: {field} is not a valid ISO 8601 timestamp")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_record(root: Path, path: Path, data: Any, errors: list[str]) -> None:
    if not isinstance(data, dict):
        errors.append(f"{path}: record must be a JSON object")
        return
    required = {
        "schema_version", "record_id", "record_type", "title", "status", "created_at", "updated_at",
        "owner", "source_refs", "parent_refs", "tags", "claims", "decisions", "outputs", "provenance",
    }
    missing = sorted(required - data.keys())
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")
    record_id = data.get("record_id")
    if not isinstance(record_id, str) or not RECORD_ID.fullmatch(record_id):
        errors.append(f"{path}: invalid record_id")
    elif data.get("record_type") != record_id.split("-")[1]:
        errors.append(f"{path}: record_type does not match record_id")
    if data.get("schema_version") != "1.0.0":
        errors.append(f"{path}: schema_version must be 1.0.0")
    if data.get("status") not in STATUSES:
        errors.append(f"{path}: unsupported status {data.get('status')!r}")
    for field in ("created_at", "updated_at"):
        validate_iso(data.get(field), field, path, errors)
    if data.get("status") == "active" and not data.get("effective_at"):
        errors.append(f"{path}: active records require effective_at")
    if data.get("status") == "superseded" and not data.get("superseded_by"):
        errors.append(f"{path}: superseded records require superseded_by")
    for field in ("source_refs", "parent_refs", "tags", "claims", "decisions", "outputs"):
        if not isinstance(data.get(field), list):
            errors.append(f"{path}: {field} must be an array")
    provenance = data.get("provenance")
    if not isinstance(provenance, dict) or not provenance.get("run_id") or not provenance.get("generator"):
        errors.append(f"{path}: provenance requires run_id and generator")
    for claim in data.get("claims", []) if isinstance(data.get("claims"), list) else []:
        if not isinstance(claim, dict):
            errors.append(f"{path}: each claim must be an object")
            continue
        confidence = claim.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            errors.append(f"{path}: claim confidence must be between 0 and 1")
        if claim.get("verdict") not in {"verified", "partially_verified", "conflicted", "unverified", "rejected"}:
            errors.append(f"{path}: claim has invalid verdict")
    for output in data.get("outputs", []) if isinstance(data.get("outputs"), list) else []:
        if not isinstance(output, dict) or not isinstance(output.get("path"), str):
            errors.append(f"{path}: each output requires a path")
            continue
        output_path = Path(output["path"])
        if output_path.is_absolute():
            errors.append(f"{path}: output path must be repository-relative: {output_path}")
            continue
        resolved = (root / output_path).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f"{path}: output path escapes repository: {output_path}")
            continue
        if not resolved.is_file():
            errors.append(f"{path}: output does not exist: {output_path}")
            continue
        expected_checksum = output.get("checksum_sha256")
        if expected_checksum and file_sha256(resolved) != expected_checksum:
            errors.append(f"{path}: output checksum mismatch: {output_path}")


def validate_record_links(records: dict[str, tuple[Path, dict[str, Any]]], errors: list[str]) -> None:
    rank = {"source": 0, "evidence": 0, "claim": 0, "distillation": 1, "baseline": 2, "audit": 3, "knowledge": 4, "run": 5}
    for record_id, (path, data) in records.items():
        for field in ("source_refs", "parent_refs", "supersedes", "superseded_by"):
            for ref in data.get(field, []):
                target_id = ref.get("record_id") if isinstance(ref, dict) else None
                if not target_id or target_id not in records:
                    errors.append(f"{path}: unresolved {field} reference {target_id!r}")
                    continue
                if field == "parent_refs":
                    target_type = records[target_id][1].get("record_type")
                    if rank.get(target_type, -1) >= rank.get(data.get("record_type"), -1):
                        errors.append(f"{path}: parent {target_id} is not from an earlier stage")

        for ref in data.get("supersedes", []):
            target_id = ref.get("record_id") if isinstance(ref, dict) else None
            if target_id in records:
                reverse = {item.get("record_id") for item in records[target_id][1].get("superseded_by", []) if isinstance(item, dict)}
                if record_id not in reverse:
                    errors.append(f"{path}: supersedes link to {target_id} is not reciprocal")
        for ref in data.get("superseded_by", []):
            target_id = ref.get("record_id") if isinstance(ref, dict) else None
            if target_id in records:
                reverse = {item.get("record_id") for item in records[target_id][1].get("supersedes", []) if isinstance(item, dict)}
                if record_id not in reverse:
                    errors.append(f"{path}: superseded_by link to {target_id} is not reciprocal")

        if data.get("record_type") == "baseline" and data.get("status") == "active":
            audits = [
                candidate for _, candidate in records.values()
                if candidate.get("record_type") == "audit"
                and candidate.get("status") == "pass"
                and record_id in {item.get("record_id") for item in candidate.get("parent_refs", []) if isinstance(item, dict)}
            ]
            if not audits:
                errors.append(f"{path}: active baseline has no passing audit that references it")
        if data.get("record_type") == "knowledge" and data.get("status") == "published":
            parents = [records[item.get("record_id")][1] for item in data.get("parent_refs", []) if isinstance(item, dict) and item.get("record_id") in records]
            if not any(item.get("record_type") == "audit" and item.get("status") == "pass" for item in parents):
                errors.append(f"{path}: published knowledge requires a passing audit parent")
            if not any(item.get("record_type") == "baseline" and item.get("status") == "active" for item in parents):
                errors.append(f"{path}: published knowledge requires an active baseline parent")


def validate_run(run_dir: Path, records: dict[str, tuple[Path, dict[str, Any]]], errors: list[str]) -> None:
    manifest_path = run_dir / "manifest.json"
    manifest = load_json(manifest_path, errors)
    if not isinstance(manifest, dict):
        return
    run_id = manifest.get("run_id")
    if run_id != run_dir.name:
        errors.append(f"{manifest_path}: run_id does not match directory")
    if manifest.get("schema_version") != "1.1.0":
        errors.append(f"{manifest_path}: schema_version must be 1.1.0")
    stages = manifest.get("stages")
    expected_stages = ("verify", "distill", "baseline", "audit", "knowledge")
    if not isinstance(stages, list) or [stage.get("name") for stage in stages if isinstance(stage, dict)] != list(expected_stages):
        errors.append(f"{manifest_path}: stages must follow the five-stage order")
        stages = []
    seen_noncomplete = False
    for stage in stages:
        status = stage.get("status")
        if status != "completed":
            seen_noncomplete = True
        elif seen_noncomplete:
            errors.append(f"{manifest_path}: a later stage completed before an earlier stage")
        checkpoint_path = run_dir / str(stage.get("checkpoint_path", ""))
        checkpoint = load_json(checkpoint_path, errors) if checkpoint_path.is_file() else None
        if not checkpoint_path.is_file():
            errors.append(f"{manifest_path}: missing checkpoint for {stage.get('name')}")
        elif isinstance(checkpoint, dict):
            if checkpoint.get("run_id") != run_id or checkpoint.get("stage") != stage.get("name"):
                errors.append(f"{checkpoint_path}: identity does not match manifest")
            if stage.get("status") == "completed" and checkpoint.get("gate_status") != "pass":
                errors.append(f"{checkpoint_path}: completed stage requires a passing gate")
            if stage.get("name") == "audit" and checkpoint.get("gate_status") == "pass":
                tests = checkpoint.get("tests", {})
                if tests.get("reconstruction") != "pass" or tests.get("mutation") != "pass":
                    errors.append(f"{checkpoint_path}: audit pass requires reconstruction and mutation passes")

    required_controls = ("coverage-matrix.json", "deletion-ledger.json", "dependency-graph.json", "review-plan.json")
    controls: dict[str, dict[str, Any]] = {}
    for filename in required_controls:
        path = run_dir / filename
        data = load_json(path, errors) if path.is_file() else None
        if not path.is_file():
            errors.append(f"{manifest_path}: missing control artifact {filename}")
        elif isinstance(data, dict):
            controls[filename] = data
            if data.get("run_id") != run_id or data.get("schema_version") != "1.1.0":
                errors.append(f"{path}: identity or schema version does not match run")
    graph = controls.get("dependency-graph.json", {})
    if manifest.get("status") == "completed" and graph.get("unresolved_edges"):
        errors.append(f"{run_dir / 'dependency-graph.json'}: completed run has unresolved edges")
    review = controls.get("review-plan.json", {})
    if review and (review.get("risk_level") != manifest.get("risk_level") or review.get("review_mode") != manifest.get("review_mode")):
        errors.append(f"{run_dir / 'review-plan.json'}: risk settings do not match manifest")
    if manifest.get("status") == "completed" and (not stages or any(stage.get("status") != "completed" for stage in stages)):
        errors.append(f"{manifest_path}: completed run requires all stages completed")
    coverage = controls.get("coverage-matrix.json", {})
    items = coverage.get("items", [])
    claim_ids = {
        claim.get("claim_id")
        for _, record in records.values()
        for claim in record.get("claims", [])
        if isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
    }
    stage_status = {stage.get("name"): stage.get("status") for stage in stages if isinstance(stage, dict)}
    expected_types = {
        "distillation_ref": "distillation",
        "baseline_ref": "baseline",
        "audit_ref": "audit",
        "knowledge_ref": "knowledge",
    }
    required_by_stage = {
        "distillation_ref": stage_status.get("distill") == "completed",
        "baseline_ref": stage_status.get("baseline") == "completed",
        "audit_ref": stage_status.get("audit") in {"completed", "blocked"},
        "knowledge_ref": stage_status.get("knowledge") == "completed",
    }
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict) or not item.get("material", True):
            continue
        material_id = item.get("material_id", "?")
        if item.get("claim_ref") not in claim_ids:
            errors.append(f"{run_dir / 'coverage-matrix.json'}: {material_id} has unresolved claim_ref {item.get('claim_ref')!r}")
        for source_id in item.get("source_refs", []):
            if source_id not in records or records[source_id][1].get("record_type") != "source":
                errors.append(f"{run_dir / 'coverage-matrix.json'}: {material_id} has unresolved source ref {source_id!r}")
        if item.get("disposition", "retained") == "excluded":
            continue
        for field, expected_type in expected_types.items():
            if not required_by_stage[field]:
                continue
            target_id = item.get(field)
            if target_id not in records or records[target_id][1].get("record_type") != expected_type:
                errors.append(f"{run_dir / 'coverage-matrix.json'}: {material_id} has unresolved {field} {target_id!r}")
    if manifest.get("status") == "completed":
        ledger = controls.get("deletion-ledger.json", {})
        if not items:
            errors.append(f"{run_dir / 'coverage-matrix.json'}: completed run has no material coverage")
        ledger_ids = {entry.get("ledger_id") for entry in ledger.get("entries", []) if isinstance(entry, dict)}
        for item in items:
            if not isinstance(item, dict) or not item.get("material", True):
                continue
            if not item.get("distillation_ref") and item.get("ledger_entry_id") not in ledger_ids:
                errors.append(f"{run_dir / 'coverage-matrix.json'}: material item lacks a distillation destination or ledger entry")
            if item.get("disposition", "retained") != "excluded":
                for field in ("baseline_ref", "audit_ref", "knowledge_ref"):
                    if not item.get(field):
                        errors.append(f"{run_dir / 'coverage-matrix.json'}: material item lacks {field}")
        for entry in ledger.get("entries", []):
            if isinstance(entry, dict) and entry.get("load_bearing") and entry.get("review_status") != "approved":
                errors.append(f"{run_dir / 'deletion-ledger.json'}: load-bearing entry is not approved")
        reviewers = [item for item in review.get("reviewers", []) if isinstance(item, dict) and item.get("independent")]
        verify_reviewers = {item.get("reviewer_id") for item in reviewers if "verify" in item.get("roles", [])}
        if manifest.get("risk_level") in {"medium", "high"} and len(verify_reviewers) < 2:
            errors.append(f"{run_dir / 'review-plan.json'}: risk level requires two independent verify reviewers")
        if any(item.get("status") != "resolved" for item in review.get("disagreements", []) if isinstance(item, dict)):
            errors.append(f"{run_dir / 'review-plan.json'}: unresolved reviewer disagreement")
        if manifest.get("risk_level") == "high":
            authors = set(review.get("baseline_author_ids", []))
            auditors = {item.get("reviewer_id") for item in reviewers if "audit" in item.get("roles", [])}
            if not (auditors - authors):
                errors.append(f"{run_dir / 'review-plan.json'}: high risk requires an independent auditor")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Project root")
    parser.add_argument("--records", action="store_true", help="Also validate records and cross-record gates")
    parser.add_argument("--runs", action="store_true", help="Also validate run manifests, checkpoints, and controls")
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    for name in WORKSPACE_DIRS:
        if not (root / "workspace" / name).is_dir():
            errors.append(f"missing workspace directory: workspace/{name}")

    schema = load_json(root / "schemas/zlyang-record.schema.json", errors)
    if isinstance(schema, dict) and schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("schema must declare JSON Schema draft 2020-12")
    load_json(root / "templates/record.json", errors)
    for template in ("run-manifest.json", "checkpoint.json", "coverage-matrix.json", "deletion-ledger.json", "dependency-graph.json", "review-plan.json"):
        load_json(root / "templates" / template, errors)

    quick_validator = Path("/Users/mac/.codex/skills/.system/skill-creator/scripts/quick_validate.py")
    if not quick_validator.is_file():
        errors.append(f"skill validator not found: {quick_validator}")
    else:
        for skill in SKILLS:
            skill_dir = root / "skills" / skill
            result = subprocess.run(
                [sys.executable, str(quick_validator), str(skill_dir)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                detail = (result.stdout + result.stderr).strip()
                if "No module named 'yaml'" in detail:
                    validate_skill_without_yaml(skill_dir, skill, errors)
                else:
                    errors.append(f"skill {skill} failed validation: {detail}")

    records: dict[str, tuple[Path, dict[str, Any]]] = {}
    if args.records or args.runs:
        for path in sorted((root / "workspace" / "records").rglob("*.json")):
            data = load_json(path, errors)
            if data is not None:
                validate_record(root, path, data, errors)
                if isinstance(data, dict) and isinstance(data.get("record_id"), str):
                    if data["record_id"] in records:
                        errors.append(f"{path}: duplicate record_id {data['record_id']}")
                    records[data["record_id"]] = (path, data)
        validate_record_links(records, errors)

    if args.runs:
        for run_dir in sorted((root / "workspace" / "runs").iterdir()):
            if run_dir.is_dir() and not run_dir.name.startswith("."):
                validate_run(run_dir, records, errors)

    if errors:
        print("ZLYang OS validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ZLYang OS validation passed.")
    print(f"Validated {len(SKILLS)} Skills, {len(REQUIRED_FILES)} core files, and {len(WORKSPACE_DIRS)} workspace directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
