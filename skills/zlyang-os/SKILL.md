---
name: zlyang-os
description: Run mixed, contradictory, versioned material through gated verification, distillation, baseline creation, audit, and knowledge capture with coverage, deletion, dependency, checkpoint, and risk-based independent review controls.
---

# ZLYang OS

## Precondition: ZLYang Discovery

Before Verify, invoke zlyang-discovery. Extract the downstream task and success conditions from the user's already supplied context. When purpose, selection rules, boundaries and output pattern are clear, immediately research and distill; otherwise ask only the most consequential missing question. A knowledge base is a storage format, not a complete use case. Never force an inferred commercial objective on a clear writing-analysis task.

For full managed runs, prepare and inspect templates/purpose-contract.json with scripts/purpose_gate.py, then pass --purpose-file to scripts/manage_run.py start. Purpose shapes what Verify researches, Distill retains, Audit checks, and Knowledge indexes.

Use scripts/build_capability_index.py and scripts/recall.py to retrieve task-matched atomic capability cards rather than reread all files. Baseline is for stable execution workflows; candidate creative methods may be analyzed without claiming fully validated production readiness. Read ../../docs/purpose-research-recall.md.

Convert uncertain inputs into a traceable decision chain. Preserve source material; never make an unverified claim look settled.

## Route the task

- Use `zlyang-verify` to establish source identity, freshness, support, and confidence.
- Use `zlyang-distill` to deduplicate and compress verified material while preserving conditions, exceptions, numbers, and disagreements.
- Use `zlyang-baseline` to resolve versions and produce the one current execution baseline.
- Use `zlyang-audit` to challenge completeness, lineage, contradictions, and closure.
- Use `zlyang-knowledge` to publish durable, reusable knowledge with review and retirement rules.

Run only the modules the request needs. For a full pipeline, use the order above and stop at a gate when evidence is insufficient.

## Managed capability route

Use the project-local `generate-openings` Skill for Chinese short-video opening generation, rewriting, diagnosis, or scoring. It is a governed execution capability, not a sixth governance stage: ZLYang verifies and versions the method, while `generate-openings` performs the content task. For material method changes, route the revision through the five ZLYang stages before treating the new version as active.

For a new multi-stage run, start with `python3 scripts/manage_run.py start`. Use the generated manifest as the state authority. Advance a stage only with `python3 scripts/manage_run.py checkpoint`; never edit a checkpoint to manufacture a pass.

## Control layer

Every full run maintains four controls under `workspace/runs/<run-id>/`:

- `coverage-matrix.json`: every material input and claim through its downstream destination;
- `deletion-ledger.json`: every exclusion, merge, compression, and restoration decision;
- `dependency-graph.json`: record and execution dependencies plus unresolved edges;
- `review-plan.json`: risk level, required independence, assigned reviewers, and disagreements.

Classify risk before extraction. Low risk may use one processing path. Medium risk requires two independent extraction or verification passes for material claims. High risk requires independent extraction plus an auditor who did not author the baseline. Independence means reviewers do not see the other draft before submitting their own result. Read [the pipeline contract](references/pipeline.md) for thresholds and checkpoint rules.

## Operating invariants

1. Raw inputs are immutable evidence, not conclusions.
2. Every material claim has a source reference or is labeled `unverified`.
3. Conflicts stay visible until a named decision resolves them.
4. Compression must not erase load-bearing details: scope, preconditions, exceptions, thresholds, dates, owners, or failure modes.
5. A baseline must identify what it supersedes and when it becomes effective.
6. Knowledge publication requires passed audit or an explicit exception with owner and review date.
7. Every derived record links backward through `parent_refs` and `source_refs`.

Read [the pipeline contract](references/pipeline.md) for multi-module runs. Read [the unified data model](../../docs/data-model.md) whenever creating or updating machine-readable records.

## Deliverable

Return the requested artifact plus a compact traceability note: run ID, inputs used, coverage gaps, deletions requiring review, unresolved uncertainties, current checkpoint, review mode, and next gate. Do not imply completion when a downstream gate has not passed.
