# Distillation rules

## Protected details

Never remove a detail that can change the decision or execution result: scope, prerequisites, exceptions, thresholds, units, dates, sequence dependencies, owner, permissions, rollback, and failure modes.

## Merge policy

Merge claims only when their meaning, scope, time window, and evidence are compatible. When wording overlaps but scope differs, keep separate statements and explain their relationship.

## Conflict policy

Preserve both sides, their strongest evidence, and the decision needed. A more recent source wins only when it has authority over the same scope and actually supersedes the older source.

## Deletion ledger

Record every excluded, merged, compressed, or restored item with source or claim IDs, original meaning, action, replacement destination, reason, load-bearing flag, reviewer, and review status. Allowed reasons include duplicate, out of scope, stale, unsupported, superseded, or low relevance. Exclusion is not destruction: the original remains immutable.

A load-bearing item cannot remain `pending_review` when Distill passes. A compressed item must identify where its protected meaning survives.
