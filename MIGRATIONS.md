# EGCA Migration Notes

## 0.3.1 -> 0.4.0

Version 0.4 changes lifecycle governance from actor-specific approval language to actor-neutral evidence-derived transitions. It does not broaden host permissions or reinterpret historical decisions.

### Historical records

Do not rewrite them. Existing human approvals, agent recommendations, and service attestations remain provenance records within the evidence boundary and policy that governed them. They are not automatically sufficient or insufficient merely because of actor type.

### Active programs

For subsequent transitions:

1. Pin the governing EGCA version and exact source revision.
2. Record the criteria revision and a transition mandate binding objective, policy, scoped authority, exact object revision, and requested state change.
3. Distinguish self-validation from evidence produced in independent provenance/failure domains.
4. Re-evaluate mandate, evidence, criteria, object revision, and authority immediately before each authoritative transition.
5. Record `ExternalBlock` only when an external system or policy actually reserves the action for an unavailable principal. Missing evidence or internally derivable authority normally produces Adapt or Repeat.
6. Keep experiment decisions (`Adopt`, `Adapt`, `Reject`, `Repeat`) distinct from control-plane transition outcomes (`Admit`, `Adapt`, `Repeat`, `Reject`, `ExternalBlock`).

An active program may continue under 0.3.1 until it records an explicit methodology migration decision. A global skill update does not silently change the version governing existing records.

### Methodology and skill updates

The currently active methodology evaluates a candidate update; the candidate cannot define the criteria that admit itself. Bind evidence and authority to the exact candidate revision. If the source revision changes, return to Repeat and evaluate the new revision.

The 0.4 methodology permits autonomous update application when the exact revision passes the current evidence gate, independent evidence and recovery criteria are satisfied, and the host grants the required action. Existing updater mechanics may still require an argument named `--approved-sha`; its name is retained for backward compatibility and does not make a human actor intrinsically required. Updater implementation and release validation remain separate productionization work.

### External authority

Protected branches, deployment platforms, credential issuers, organizational policy, and legal controls remain authoritative. When those controls reserve an action for an unavailable principal, record the precise block and continue all safe independent work. Do not widen credentials, impersonate a principal, or substitute evidence for authority the host has not granted.

## 0.3.0 -> 0.3.1

No tracker, schema, experiment, or decision migration is required. Version 0.3.1 adds only an optional closeout invitation when a completed program produced a durable, reusable EGCA lesson.

Drafting, repository placement, and publication or pull-request creation remain separate permissions. Existing programs do not need a new field or retrospective consent record.

## 0.2.x -> 0.3.0

The decision vocabulary and stable experiment identities are unchanged. The new requirement makes the scope of each decision explicit and prevents prototype/fixture evidence from silently authorizing a materially different production implementation.

### Historical decisions

Do not rewrite them. Treat their evidence as valid within the artifact, environment, data, integration, and operational boundary that was actually tested.

### Active programs

For subsequent work:

1. Add the tested artifact/environment and evidence applicability boundary to active experiment or decision records.
2. Identify any material delta between adopted evidence and the intended production implementation.
3. When a delta remains, create a linked productionization experiment/adaptation with a stable ID instead of reopening resolved discovery.
4. Add criterion-to-production traceability and adversarial evidence before declaring the program production-ready.
5. Track production readiness, merge, deployment, and operational validation separately.

Existing trackers remain readable. The new schema fields are optional for interchange compatibility, but the methodology requires them prospectively when a material productionization delta exists.

## 0.1.x -> 0.2.0

The methodology's experiment lifecycle and branch topology are backward-compatible. The main change is lifecycle/version governance for the EGCA skill itself.

### Existing installed skills

Reinstall or update to 0.2.0 once. Afterward, the installed skill contains `scripts/egca_update.py` and `manifest.json` and can check for later updates itself.

### Active EGCA programs

Do **not** reinterpret prior experiments under a newer methodology version merely because the globally installed skill changed.

Until the canonical tracker/schema gains an explicit methodology-version field, record the governing EGCA version in the program's decision log or equivalent durable notes. If a material EGCA upgrade is adopted during an active program, record that as an explicit methodology migration decision and state which subsequent experiments use the newer contract.

### Update approval

An agent may run the update checker without separate approval because it is read-only. Before applying an update, it must show the user the current version, proposed version, exact source commit, relevant changelog/migration information, and then obtain explicit approval for that update. Approval for one commit does not authorize a different commit if the source branch moves.
