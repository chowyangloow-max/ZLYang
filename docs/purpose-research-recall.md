# Purpose Gate, targeted research and reusable capability retrieval

## Why this layer exists
A neat summary cannot be evaluated without knowing its intended use. Discovery is a **sufficiency gate**, not an interrogation phase. If the user has already supplied purpose, selection criteria, preservation boundaries and output pattern, do not ask again.

## End-to-end sequence
1. Identify future task and success conditions.
2. Persist one purpose contract for the current scope.
3. Choose research sources according to the purpose; distinguish observed data from hypotheses.
4. Perform Verify and purpose-specific Distill, preserving original evidence and load-bearing context.
5. Represent reusable methods as atomic capability cards. A source can yield many cards; a card can cite many sources.
6. Build index and retrieve by intended use, task wording, trigger phrases and tags.
7. Check status, evidence, conditions, exceptions and not-for scope **after** retrieval, before execution.
8. Record real outcomes; re-evaluate failed or stale methods instead of expanding the card archive indefinitely.

## Purpose contract
Source of truth for the declared task. Its six required sufficiency fields are: purpose, expected_task, success_criteria, selection_rules, preservation_boundaries, output_paradigm. An empty consumer or research_focus field is not a reason to hold up work.

Inspect: python3 scripts/purpose_gate.py inspect --file templates/purpose-contract.json

Create a working copy in workspace, fill from what the user already said, and inspect again. Use no invented user goals or undocumented defaults.

## Repository layout
- skills/zlyang-discovery/ — routing and inquiry behavior.
- templates/purpose-contract.json — gate input template.
- templates/capability-card.json — reusable method schema example.
- workspace/capabilities/ — candidate/active method cards, one JSON per card.
- workspace/capabilities/index.jsonl — generated lightweight retrieval index.
- scripts/recall.py — deterministic first-pass retrieval and conservative execution filtering.
- scripts/build_capability_index.py — index builder and structural card validation.
- scripts/test_purpose_recall.py — local regression tests.
- Existing workspace/runs/ controls still govern full gated evidence publication.

## Publishing versus retrieving
A candidate can be read as a creative reference with visible warnings, but is **not** an active validated execution method. Auto-execution is allowed only for active cards with verified evidence and satisfied preconditions; this first-pass CLI does not perform side-effectful execution. An active lifecycle flag by itself does not prove efficacy.

## Retrieval semantics
Two modes: idea and execute. Idea may recall candidate cards if explicitly allowed and labeled. Execute excludes unverified evidence, expired or superseded cards, and unmet scope. Lexical scoring is deliberate minimal functionality, not semantic understanding. For synonym-rich retrieval use Codex to expand query terms, then verify each proposed card's scope; later add embeddings if measurable recall misses persist.

## Example: one video script, three purposes
- Content creation → HOOK and STRUCT cards recording contrast hook, emotion beats, oral expression, minimal edits.
- Knowledge lookup → CLAIM and CONCEPT cards distinguishing subjective claims from evidence.
- SOP extraction → ACTION card with triggers, constraints, exceptions and acceptance; never interpret persuasive rhetoric as an operational rule.
All three retain the raw source link. None may invent creator metrics.
