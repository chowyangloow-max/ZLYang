#!/usr/bin/env python3
"""Purpose sufficiency gate: only ask when missing facts change the actual task."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

REQUIRED = (
    ("purpose", "你以后拿这份材料具体完成什么任务？"),
    ("expected_task", "以后你会用什么具体问题调用这份成果？"),
    ("success_criteria", "怎样判断这次整理或调用是有用的？"),
    ("selection_rules", "按什么规则筛选需要保留的内容？"),
    ("preservation_boundaries", "有哪些事实、原话、条件或边界绝对不能丢？"),
    ("output_paradigm", "最终要形成能力卡、写作方法、执行 Skill 还是别的可调用形式？"),
)

def read_contract(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot load purpose contract {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Purpose contract must be a JSON object")
    return data

def assess(data: dict) -> dict:
    missing = []
    for key, question in REQUIRED:
        value = data.get(key)
        if isinstance(value, str):
            valid = bool(value.strip())
        elif isinstance(value, list):
            valid = bool(value) and all(isinstance(v, str) and v.strip() for v in value)
        else:
            valid = False
        if not valid:
            missing.append({"field":key, "question":question})
    if not data.get("confirmed", False):
        missing.append({"field":"confirmed","question":"请确认以上用途和规则是否确实来自用户的要求。"})
    return {"status": "ready" if not missing else "needs_clarification", "missing":missing, "next_question": missing[0]["question"] if missing else None}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    inspect=sub.add_parser("inspect")
    inspect.add_argument("--file",type=Path,required=True)
    args=parser.parse_args()
    try:
        decision=assess(read_contract(args.file))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    return 0 if decision["status"]=="ready" else 2

if __name__=="__main__":
    raise SystemExit(main())
