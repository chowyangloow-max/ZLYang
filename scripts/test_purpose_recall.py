#!/usr/bin/env python3
"""Regression tests for purpose sufficiency and conservative capability routing."""
import unittest
from purpose_gate import assess
from recall import recall

READY={"purpose":"创作短视频","expected_task":"拆解口播开头","success_criteria":["原文保留","能够复用"],"selection_rules":["只选近期低粉爆文"],"preservation_boundaries":["不改原句事实"],"output_paradigm":"短视频开头能力卡","confirmed":True}

CARDS=[
 {"id":"HOOK-1","title":"开头机制","purposes":["内容创作"],"stages":["开头"],"tags":["五秒"],"trigger_phrases":["前五秒"],"not_for":[],"lifecycle_status":"active","evidence_status":"verified","path":"HOOK-1.json"},
 {"id":"OLD","title":"废弃","purposes":["内容创作"],"stages":["开头"],"tags":["五秒"],"trigger_phrases":["前五秒"],"not_for":[],"lifecycle_status":"superseded","evidence_status":"verified","path":"OLD.json"},
 {"id":"SOP","title":"流程","purposes":["执行SOP"],"stages":["执行"],"tags":["检查"],"trigger_phrases":["审核流程"],"not_for":[],"lifecycle_status":"active","evidence_status":"verified","path":"SOP.json"},
 {"id":"CAND","title":"候选","purposes":["内容创作"],"stages":["开头"],"tags":["五秒"],"trigger_phrases":["前五秒"],"not_for":[],"lifecycle_status":"candidate","evidence_status":"unverified","path":"CAND.json"}
]
class PurposeRecallTests(unittest.TestCase):
 def test_ready_not_pestered(self): self.assertEqual(assess(READY)["status"],"ready")
 def test_missing_purpose_asks_one(self):
  d=dict(READY,purpose="")
  self.assertEqual(assess(d)["status"],"needs_clarification")
  self.assertTrue(assess(d)["next_question"])
 def test_invalid_core_rules(self):
  self.assertEqual(assess(dict(READY,selection_rules=[]))["status"],"needs_clarification")
 def test_purpose_prevents_wrong_sop(self):
  r=recall(CARDS,"内容创作","优化前五秒",stage="开头",mode="execute")
  self.assertEqual([x["id"] for x in r],["HOOK-1"])
 def test_candidate_only_as_labeled_idea(self):
  r=recall(CARDS,"内容创作","优化前五秒",stage="开头",allow_candidate=True)
  self.assertEqual({x["id"] for x in r},{"HOOK-1","CAND"})
  self.assertTrue(next(x for x in r if x["id"]=="CAND")["warning"])
 def test_candidate_not_executable(self):
  r=recall(CARDS,"内容创作","优化前五秒",stage="开头",mode="execute",allow_candidate=True)
  self.assertEqual([x["id"] for x in r],["HOOK-1"])

if __name__=="__main__":unittest.main()
