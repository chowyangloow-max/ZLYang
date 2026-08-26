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
