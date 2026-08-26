# Baseline rules

## Precedence

Resolve competing rules using explicit authority first, then scope specificity, approval status, effective date, and evidentiary strength. Recency alone is insufficient.

## Executability test

An executor should know: trigger, owner, permissions, required inputs, ordered actions, decision branches, expected output, acceptance criteria, failure escalation, and rollback.

## Lifecycle

- `draft`: being assembled; not authoritative.
- `approved`: accepted but not yet effective.
- `active`: the current execution baseline for its declared scope.
- `superseded`: replaced by named baseline IDs.
- `retired`: intentionally no longer applicable without a replacement.

Each active baseline requires `effective_at`. Each superseded baseline requires a forward link to its replacement. Keep historical files immutable; issue a new version for material changes.
