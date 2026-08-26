#!/usr/bin/env python3
"""Validate ZLYang OS structure, Skills, schema, and optional JSON records."""

from __future__ import annotations

import argparse
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
)
WORKSPACE_DIRS = ("inbox", "evidence", "records", "baselines", "audits", "knowledge", "runs", "archive")
REQUIRED_FILES = (
    "AGENTS.md",
    "README.md",
    "docs/data-model.md",
    "schemas/zlyang-record.schema.json",
    "templates/record.json",
    "templates/intake.md",
    "templates/evidence.yaml",
    "templates/distillation.md",
    "templates/baseline.md",
    "templates/audit.md",
    "templates/knowledge.md",
    "templates/run-manifest.json",
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


def validate_record(path: Path, data: Any, errors: list[str]) -> None:
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Project root")
    parser.add_argument("--records", action="store_true", help="Also validate workspace/records/*.json")
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
    load_json(root / "templates/run-manifest.json", errors)

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

    if args.records:
        for path in sorted((root / "workspace" / "records").rglob("*.json")):
            data = load_json(path, errors)
            if data is not None:
                validate_record(path, data, errors)

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
