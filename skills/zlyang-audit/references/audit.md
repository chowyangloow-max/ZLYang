# Audit rules

## Finding severity

- `critical`: can cause unsafe action, wrong authoritative rule, irreversible loss, or fabricated closure; blocks pass.
- `major`: materially impairs evidence, execution, or traceability; blocks unconditional pass.
- `minor`: local clarity or maintainability defect with low outcome risk.
- `observation`: improvement opportunity without a current defect.

## Verdict

- `pass`: no open critical or major findings.
- `conditional_pass`: no open critical findings; named major findings have bounded mitigations, owners, and deadlines.
- `fail`: any critical finding, broken core lineage, or non-executable baseline.

## Mandatory adversarial checks

Trace a conclusion backward to raw source, replay one representative action forward, inspect at least one excluded item, test an exception or boundary case, and verify supersession in both directions.

## Reconstruction and mutation

For representative high-impact baseline rules, reconstruct: baseline step -> distilled conclusion -> protected detail -> claim -> evidence -> raw source. Record every missing or ambiguous hop.

Then remove or alter one scope, prerequisite, exception, threshold, date, owner, permission, rollback, or failure path. The expected decision or acceptance result must change. If it does not, the baseline or its test is not sensitive to a load-bearing detail and cannot pass unconditionally.

## Independence check

For medium and high-risk runs, compare reviewer identities and submission order with the review plan. High-risk audit authors must not be baseline authors. Undocumented or self-certified independence is a major finding; fabricated independence is critical.
