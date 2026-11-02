# Run controls

## Purpose discovery prerequisite

New runs require a confirmed purpose contract checked using scripts/purpose_gate.py inspect --file PATH. Supply --purpose-file PATH to manage_run.py start. The controller copies the contract into the run directory; missing purpose, future task, rules, boundaries, acceptance or output paradigm blocks run creation. An already clear task is sufficient; do not delay it by adding redundant questions. Older run manifests without the purpose gate are preserved for backward compatibility.


ZLYang OS v1.1 uses one manifest, five checkpoints, and four control artifacts per full run. Create them with `scripts/manage_run.py start`; do not copy them by hand.

## Coverage matrix

Each `items` entry represents one material source item or claim and uses these fields as applicable:

- `material_id`, `source_refs`, `claim_ref`, `material`;
- `verdict`, `disposition` (`retained`, `excluded`, `merged`, or `compressed`);
- `distillation_ref` or `ledger_entry_id`;
- `baseline_ref`, `audit_ref`, and `knowledge_ref` as the item advances.

The row remains stable across stages. A material item must have a destination or a reviewed deletion-ledger decision.

## Deletion ledger

Each `entries` item records `ledger_id`, `item_refs`, `action`, `original_meaning`, `reason`, `replacement_ref`, `load_bearing`, `reviewer_id`, and `review_status`. Allowed review states are `pending_review`, `approved`, and `rejected`. A load-bearing entry blocks Distill until approved.

## Dependency graph

Run `python3 scripts/build_dependency_graph.py --run-id <run-id>` after record changes. Record-lineage links are generated from `source_refs`, `parent_refs`, `supersedes`, and `superseded_by`. Optional execution dependencies live in `extensions.dependencies`. Any unresolved edge blocks Baseline and later gates.

## Review plan

`reviewers` entries contain `reviewer_id`, `roles`, `independent`, and `submitted_at`. Medium and high-risk runs require two independent Verify reviewers. High-risk runs additionally require an Audit reviewer who is not listed in `baseline_author_ids`. Record comparisons in `disagreements` with `status` set to `open` or `resolved`.

## Checkpoint commands

Start a run:

```bash
python3 scripts/manage_run.py start --slug policy-refresh --owner owner-id --objective "Compile the current policy" --risk medium
```

Pass the current gate only after its controls are populated:

```bash
python3 scripts/manage_run.py checkpoint --run-id run-YYYYMMDD-policy-refresh-01 --stage verify --result pass --reviewer reviewer-a --reviewer reviewer-b
```

Audit additionally requires `--reconstruction pass --mutation pass`. Use `--result conditional_pass --unresolved <condition>` when bounded conditions remain; it records the verdict but blocks publication until re-audit. Use `--result blocked` for an ordinary failed gate.
