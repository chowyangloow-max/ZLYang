---
name: zlyang-discovery
description: Discover the intended downstream task before researching, distilling, indexing or publishing source material. Ask only the highest-impact missing question; if purpose, rules, boundaries and output pattern are already clear, proceed without another questionnaire.
---

# ZLYang Discovery | Purpose Gate

## Objective
Use the user's future task to select what to investigate, retain, verify, distill and eventually retrieve. A knowledge base is a storage form, not a sufficient use case by itself.

## Decision procedure
1. Read the current message, nearby task context, project instructions and any existing purpose contract. Do not ask the user again for information already supplied.
2. Identify the downstream job, who/what will consume the output, success criterion, selection rules, preservation boundaries and output pattern.
3. Run scripts/purpose_gate.py inspect --file <contract-path>. An absent or incomplete contract is an intake state, not permission to distill.
4. If ready: start targeted research and the requested work immediately. An optional question about commercial objectives must never block a clearly bounded writing-analysis task.
5. If blocked: ask exactly one question with the highest expected effect on research or output, update the contract on answer, and reassess. Do not present a long form by default.
6. Distinguish observed needs from inferred deep needs. Hypotheses require evidence or user confirmation and do not silently change the task.
7. Select a research route according to references/use-case-routing.md. Do not fabricate search results, data, platform statistics or authorship.
8. Create an execution/retrieval plan, not a document-shaped end product by default.

## Gate fields
- purpose: actual future use, e.g. write spoken-video drafts or audit SOPs (not just "make a knowledge base")
- expected_task: concrete example of a later request
- success_criteria: observable output/quality tests, not guaranteed business outcomes
- selection_rules: what counts as a relevant source or candidate
- preservation_boundaries: what must not be lost or wrongly copied
- output_paradigm: reusable card, prompt, Skill, SOP or evidence brief

Consumer, datasets and research gaps improve the plan but are not mandatory to enter; do not block when the core fields are clear.

## Downstream
Only then use Verify → Distill → Baseline (when an actionable baseline is required) → Audit → Knowledge. A content-creation extraction may generate candidate cards, with unverified performance claims clearly marked. Use scripts/recall.py to select a small relevant set of cards for a future task.

Read references/use-case-routing.md and ../../docs/purpose-research-recall.md when executing a full research or retrieval task.
