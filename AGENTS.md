# ZLYang OS operating contract

This repository turns mixed, contradictory, and versioned information into trustworthy, executable, and traceable knowledge and action systems.

## Start here

Use `skills/zlyang-os/SKILL.md` as the router. Load only the module Skill needed for the current stage. For multi-stage work, follow Verify to Distill to Baseline to Audit to Knowledge and respect each gate.

## Non-negotiable rules

- Preserve raw inputs. Never overwrite evidence to match a conclusion.
- Label uncertainty. Unsupported statements remain `unverified`.
- Maintain lineage with `source_refs`, `parent_refs`, and a run manifest.
- Preserve scope, conditions, exceptions, numbers, dates, ownership, and failure paths during compression.
- Never silently resolve conflicting authoritative sources.
- Never call a draft baseline active or a candidate asset published.
- Material changes create a new version and explicit supersession links.
- Stop and report the blocking gate when trustworthy closure is impossible.

## File placement

- Raw inputs: `workspace/inbox/`
- Source snapshots and evidence: `workspace/evidence/`
- Schema-valid machine records: `workspace/records/`
- Human-readable baseline outputs: `workspace/baselines/`
- Audit reports: `workspace/audits/`
- Published or candidate knowledge: `workspace/knowledge/`
- Run manifests and logs: `workspace/runs/<run-id>/`
- Historical superseded material: `workspace/archive/`

Do not edit files in `workspace/archive/` except to repair metadata with an explicit audit trail.

## Definition of done

The requested stage artifact exists, required lineage resolves, uncertainty and open conflicts are visible, status matches the actual gate, and `python3 scripts/validate.py` passes. A full pipeline is done only when audit passes and the knowledge asset has lifecycle metadata.
