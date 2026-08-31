---
name: zlyang-baseline
description: Resolve competing versions and turn approved conclusions into the single current execution baseline, including owners, conditions, effective dates, superseded rules, and rollback triggers.
---

# ZLYang Baseline

Create one executable current truth without destroying history.

## Workflow

1. Confirm inputs passed verification and distillation gates or document an approved exception.
2. Identify all rules and versions that govern the same action.
3. Resolve conflicts using authority, evidence, scope, and effective date.
4. Write the current procedure with owner, trigger, inputs, steps, outputs, acceptance criteria, and failure path.
5. List superseded rules explicitly; never rely on readers to infer obsolescence.
6. Set effective date, review date, rollback trigger, and change rationale.
7. Mark the baseline `draft`, `approved`, `active`, `superseded`, or `retired`.
8. Update the coverage matrix and dependency graph, including rule prerequisites, decision branches, failure escalation, rollback, and downstream dependents.

No baseline is active merely because it is the newest file. Activation requires an explicit status and effective date.

Read [baseline rules](references/baseline.md) for precedence and lifecycle. Use [the unified model](../../docs/data-model.md) and `templates/baseline.md`.

## Output

Produce the current baseline, supersession map, execution dependency graph, activation metadata, exceptions, and rollback/review conditions.
