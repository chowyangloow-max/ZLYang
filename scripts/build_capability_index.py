#!/usr/bin/env python3
"""Build lightweight structured capability index without rewriting source cards."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ALLOWED_LIFECYCLE={"candidate","active","stale","superseded","retired"}
ALLOWED_EVIDENCE={"unverified","reported","qualified","verified","conflicted"}

def load_cards(directory:Path)->list[dict]:
    cards=[]
    seen=set()
    for path in sorted(directory.glob("*.json")):
        data=json.loads(path.read_text(encoding="utf-8"))
        required=("id","title","purposes","stages","tags","trigger_phrases","source_refs","evidence_status","lifecycle_status")
        missing=[k for k in required if k not in data]
        if missing: raise ValueError(f"{path.name}: missing {missing}")
        if not isinstance(data["id"],str) or not data["id"] or data["id"] in seen:
            raise ValueError(f"{path.name}: missing or duplicate id")
        seen.add(data["id"])
        if data["lifecycle_status"] not in ALLOWED_LIFECYCLE or data["evidence_status"] not in ALLOWED_EVIDENCE:
            raise ValueError(f"{path.name}: unsupported status")
        for key in ("purposes","stages","tags","trigger_phrases","source_refs"):
            if not isinstance(data[key],list) or not all(isinstance(i,str) for i in data[key]):
                raise ValueError(f"{path.name}: {key} must be strings")
        card={k:data[k] for k in required}
        card["path"]=path.name
        card["not_for"]=data.get("not_for",[])
        card["preconditions"]=data.get("preconditions",[])
        card["review_at"]=data.get("review_at")
        cards.append(card)
    return cards

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory",type=Path,default=ROOT/"workspace"/"capabilities")
    args=parser.parse_args()
    args.directory.mkdir(parents=True, exist_ok=True)
    cards=load_cards(args.directory)
    path=args.directory/"index.jsonl"
    path.write_text("".join(json.dumps(card,ensure_ascii=False)+"\n" for card in cards),encoding="utf-8")
    print(f"Indexed {len(cards)} capability cards: {path}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
