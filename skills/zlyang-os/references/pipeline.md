# Pipeline contract

## Default stage gates

| Stage | Input | Gate to pass | Output |
|---|---|---|---|
| Verify | Raw sources and claims | Material claims have verdicts and traceable evidence | Evidence register |
| Distill | Qualified claims | No hidden contradiction; protected details retained | Decision-ready synthesis |
| Baseline | Approved synthesis | One explicit current rule set with lifecycle metadata | Executable baseline |
| Audit | Baseline plus complete lineage | No open critical finding | Audit report |
| Knowledge | Passed artifact or approved exception | Applicability and maintenance controls present | Reusable knowledge asset |

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
