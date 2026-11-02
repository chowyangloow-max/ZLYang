#!/usr/bin/env python3
"""Conservative purpose-aware retrieval; never executes returned capabilities."""
from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def relevant(phrase:str, task:str)->bool:
    a="".join(phrase.lower().split())
    b="".join(task.lower().split())
    if not a or not b: return False
    return a in b or (len(a)>=4 and any(a[i:i+4] in b for i in range(len(a)-3)))

def recall(cards:list[dict], purpose:str, task:str, stage:str="", mode:str="idea", limit:int=5, allow_candidate:bool=False)->list[dict]:
    results=[]
    for c in cards:
        lifecycle=c.get("lifecycle_status")
        evidence=c.get("evidence_status")
        if lifecycle in ("retired","superseded","stale"):continue
        if mode=="execute" and not (lifecycle=="active" and evidence=="verified"):continue
        if mode=="idea" and not (lifecycle=="active" or allow_candidate and lifecycle=="candidate"):continue
        purposes=c.get("purposes",[])
        if purpose not in purposes:continue
        if stage and stage not in c.get("stages",[]):continue
        if any(relevant(x,task) for x in c.get("not_for",[])):continue
        matched=[x for x in c.get("trigger_phrases",[])+c.get("tags",[]) if relevant(x,task)]
        if not matched:continue
        score=10+5*len(matched)+(2 if stage else 0)+(1 if evidence=="verified" else 0)
        results.append({"id":c["id"],"title":c["title"],"score":score,"matched":matched,"path":c["path"],"evidence_status":evidence,"lifecycle_status":lifecycle,"preconditions":c.get("preconditions",[]),"warning": "候选/未验证，仅供参考，不能自动执行" if lifecycle!="active" or evidence!="verified" else None})
    return sorted(results,key=lambda x:(-x["score"],x["id"]))[:max(0,limit)]

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--purpose",required=True)
    parser.add_argument("--task",required=True)
    parser.add_argument("--stage",default="")
    parser.add_argument("--mode",choices=("idea","execute"),default="idea")
    parser.add_argument("--allow-candidate",action="store_true")
    parser.add_argument("--limit",type=int,default=5)
    parser.add_argument("--index",type=Path,default=ROOT/"workspace"/"capabilities"/"index.jsonl")
    args=parser.parse_args()
    if not args.index.is_file():
        parser.error(f"Missing index: {args.index}. Run build_capability_index.py")
    cards=[json.loads(line) for line in args.index.read_text(encoding="utf-8").splitlines() if line.strip()]
    result=recall(cards,args.purpose,args.task,args.stage,args.mode,args.limit,args.allow_candidate)
    print(json.dumps({"purpose":args.purpose,"task":args.task,"mode":args.mode,"results":result},ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
