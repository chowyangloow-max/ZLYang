# Unified data model

ZLYang OS uses a common record envelope so every artifact can be traced and governed consistently. The normative machine schema is [`schemas/zlyang-record.schema.json`](../schemas/zlyang-record.schema.json).

Record schema `1.0.0` remains compatible in ZLYang OS v1.1. The run control plane uses schema `1.1.0`; see [`run-controls.md`](run-controls.md).

## Record types

| Type | Meaning | Typical module |
|---|---|---|
| `source` | Immutable description of an original input | Verify |
| `evidence` | Evidence for or against one or more claims | Verify |
| `claim` | An atomic assertion with verdict and confidence | Verify |
| `distillation` | Decision-ready synthesis with merge/exclusion trace | Distill |
| `baseline` | Versioned, executable current rule set | Baseline |
| `audit` | Checks, findings, and release verdict | Audit |
| `knowledge` | Reusable published knowledge asset | Knowledge |
| `run` | One processing run and its inputs/outputs | Entry pipeline |

## Run control plane

A full run adds a manifest, five ordered checkpoints, a coverage matrix, deletion ledger, dependency graph, and review plan under `workspace/runs/<run-id>/`. These controls govern movement between records; they do not replace the record envelope. The manifest is authoritative for stage state, while the four companion artifacts make loss, broken links, and reviewer independence inspectable.

## Common envelope

Every JSON record contains:

- `schema_version`: currently `1.0.0`.
- `record_id`: stable ID in the form `zly-<type>-<YYYYMMDD>-<slug>-<nn>`.
- `record_type`, `title`, `status`.
- `created_at`, `updated_at`, and `owner`.
- `source_refs`: raw sources used directly.
- `parent_refs`: derived records used to create this record.
- `tags` and optional `scope`.
- `claims`, `decisions`, and `outputs` as applicable.
- `provenance`: run ID, generator, and optional checksum.

References use record IDs, never only filenames. Paths may accompany IDs for convenience.

## Claim model

A claim has an atomic `statement`, a `verdict`, numeric `confidence`, evidence references, scope, validity window, and optional supersession links. If a sentence contains independently disputable assertions, split it into multiple claims.

Verdict and confidence are separate: a claim can be verified for a narrow scope with moderate confidence, or conflicted with high confidence that the conflict is real.

## Lineage rules

1. `source_refs` point to original `source` records.
2. `parent_refs` point to derived records directly consumed.
3. A derived record must not cite itself or a future stage as a parent.
4. Supersession is explicit and bidirectional at the document level: the old asset names the replacement, and the new asset names what it supersedes.
5. Material changes create a new record or version rather than rewriting historical evidence.

## Status vocabulary

The schema allows a shared controlled vocabulary. Each module narrows it further. `active` and `published` are release states; `draft` or `candidate` content must not be presented as current truth.

## Human and machine artifacts

Markdown templates capture reasoning for people. Each released artifact should also have a JSON record under `workspace/records/` using the unified schema. The JSON record may point to a longer Markdown output in its `outputs` field.
