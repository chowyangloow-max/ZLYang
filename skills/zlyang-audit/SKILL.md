---
name: zlyang-audit
description: Audit ZLYang records and baselines for missing evidence, broken lineage, unresolved conflicts, unsafe compression, non-executable steps, and false closure.
---

# ZLYang Audit

Try to disprove completeness and executability before declaring closure.

## Workflow

1. Check every material conclusion has resolvable evidence and lineage.
2. Reconcile totals, versions, dates, owners, scopes, and statuses across artifacts.
3. Look for details lost during merging or compression.
4. Walk the baseline as an executor: inputs, permissions, branching, outputs, acceptance, and rollback.
5. Search for unresolved conflicts disguised as wording choices.
6. Classify findings by severity and name the owner and remediation gate.
7. Issue `pass`, `conditional_pass`, or `fail`; never use pass when a critical finding remains open.

Read [audit rules](references/audit.md) for severity and gate criteria. Use [the unified model](../../docs/data-model.md) and `templates/audit.md`.

## Output

Produce scope, checks performed, findings, counterexamples, verdict, remediation owners, and re-audit conditions.
