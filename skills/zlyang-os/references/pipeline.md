# Pipeline contract

## Before the five publication stages

Discovery is a mandatory task-sufficiency gate, not a sixth evidence stage. Read the task context first, ask one consequential missing question only when needed, then match research priorities to actual use. The purpose contract is required to start NEW formal runs. Historical runs remain readable. See ../../../docs/purpose-research-recall.md.


## Default stage gates

| Stage | Input | Gate to pass | Output |
|---|---|---|---|
| Verify | Raw sources and claims | Material claims have verdicts and traceable evidence | Evidence register |
| Distill | Qualified claims | No hidden contradiction; protected details retained | Decision-ready synthesis |
| Baseline | Approved synthesis | One explicit current rule set with lifecycle metadata | Executable baseline |
| Audit | Baseline plus complete lineage | No open critical finding | Audit report |
| Knowledge | Passed artifact or approved exception | Applicability and maintenance controls present | Reusable knowledge asset |

Each stage writes a checkpoint with `pending`, `pass`, or `blocked`. Audit may record `conditional_pass`, but downstream publication remains blocked until a later audit passes. A later stage cannot pass before every earlier required stage passes. `completed` is valid only after all five checkpoints pass.

## Run controls

The run manifest is the state authority. The coverage matrix, deletion ledger, dependency graph, and review plan are required companions, not optional reports.

- Add one coverage row for every material source item or claim. Update the same row as it moves downstream; never create a second row to hide a gap.
- Add one deletion-ledger entry for every exclusion, merge, compression, or later restoration. `pending_review` load-bearing entries block Distill.
- Rebuild the dependency graph after records change. Unresolved parents, sources, supersession links, and execution prerequisites block the relevant gate.
- Record reviewer identity and independence in the review plan. A required independent review cannot be satisfied by the original author relabeling their own work.

## Risk-based review

| Risk | Typical impact | Minimum review mode |
|---|---|---|
| `low` | Reversible, narrow, low-cost error | `single` |
| `medium` | Material operational, financial, reputational, or broad-scope error | `dual_independent` for material extraction or verification |
| `high` | Safety, legal, irreversible, authoritative, or system-wide impact | `dual_independent` plus `independent_audit` |

Escalate when evidence is strongly conflicted, compression removes load-bearing details, or a baseline changes many dependents. Do not downgrade risk merely to pass a gate.

## Reconstruction gate

Audit must sample the final baseline and reconstruct its material rules backward to protected details, claims, evidence, and raw sources. It must also remove or mutate at least one load-bearing detail and show that the acceptance result changes. A failed reconstruction or insensitive mutation test blocks publication.

## Stop conditions

Stop the full pipeline and report the blocking gate when:

- a material source cannot be identified or accessed;
- evidence cannot distinguish conflicting high-impact claims;
- no authorized rule resolves a baseline conflict;
- a critical audit finding lacks a safe remediation;
- ownership or review responsibility is required but unknown.

Partial outputs remain useful, but label them with their actual stage and status.

## Run trace

Create one run manifest under `workspace/runs/<run-id>/manifest.json`. List every input and output record ID. When a file is not machine-readable, record its path and checksum in the corresponding source record.
