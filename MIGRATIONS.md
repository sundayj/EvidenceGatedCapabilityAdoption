# EGCA Migration Notes

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
