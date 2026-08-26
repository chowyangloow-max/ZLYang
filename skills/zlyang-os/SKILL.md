---
name: zlyang-os
description: Route mixed, contradictory, versioned source material through verification, distillation, baseline creation, audit, and knowledge capture. Use when a task must turn messy information into trustworthy, executable, and traceable records rather than merely summarize it.
---

# ZLYang OS

Convert uncertain inputs into a traceable decision chain. Preserve source material; never make an unverified claim look settled.

## Route the task

- Use `zlyang-verify` to establish source identity, freshness, support, and confidence.
- Use `zlyang-distill` to deduplicate and compress verified material while preserving conditions, exceptions, numbers, and disagreements.
- Use `zlyang-baseline` to resolve versions and produce the one current execution baseline.
- Use `zlyang-audit` to challenge completeness, lineage, contradictions, and closure.
- Use `zlyang-knowledge` to publish durable, reusable knowledge with review and retirement rules.

Run only the modules the request needs. For a full pipeline, use the order above and stop at a gate when evidence is insufficient.

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

Return the requested artifact plus a compact traceability note: inputs used, unresolved uncertainties, current status, and next gate. Do not imply completion when a downstream gate has not passed.
