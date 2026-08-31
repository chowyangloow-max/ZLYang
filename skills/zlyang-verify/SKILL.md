---
name: zlyang-verify
description: Verify sources and claims for identity, provenance, freshness, consistency, and evidentiary support. Use before relying on uncertain, mixed-quality, conflicting, or time-sensitive information.
---

# ZLYang Verify

Establish what may be trusted, to what degree, and for what scope.

## Workflow

1. Inventory each source without altering it; assign a stable source ID.
2. Separate claims from interpretation and action proposals.
3. Check provenance, authority, date, version, scope, and corroboration.
4. Record evidence for and against each material claim.
5. Assign one verdict: `verified`, `partially_verified`, `conflicted`, `unverified`, or `rejected`.
6. Set confidence separately from verdict and explain the limiting factor.
7. Send only usable claims forward; preserve rejected and unresolved claims for traceability.
8. Add every material source item and claim to the run coverage matrix.
9. When the review plan requires independence, perform separate extraction or verification passes before comparing results; record disagreements and their disposition.

Do not treat repetition as corroboration when sources share the same origin. Do not upgrade absence of contradiction into proof.

Read [verification rules](references/verification.md) for source tiers, verdict gates, and edge cases. Use [the unified model](../../docs/data-model.md) and `templates/evidence.yaml`.

## Output

Produce a source register, claim-evidence matrix, coverage updates, independent-review comparison when required, verdicts, confidence, unresolved conflicts, and the next verification action.
