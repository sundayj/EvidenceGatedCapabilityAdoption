# EGCA Migration Notes

## 0.1.x -> 0.2.0

The methodology's experiment lifecycle and branch topology are backward-compatible. The main change is lifecycle/version governance for the EGCA skill itself.

### Existing installed skills

Reinstall or update to 0.2.0 once. Afterward, the installed skill contains `scripts/egca_update.py` and `manifest.json` and can check for later updates itself.

### Active EGCA programs

Do **not** reinterpret prior experiments under a newer methodology version merely because the globally installed skill changed.

Until the canonical tracker/schema gains an explicit methodology-version field, record the governing EGCA version in the program's decision log or equivalent durable notes. If a material EGCA upgrade is adopted during an active program, record that as an explicit methodology migration decision and state which subsequent experiments use the newer contract.

### Update approval

An agent may run the update checker without separate approval because it is read-only. Before applying an update, it must show the user the current version, proposed version, exact source commit, relevant changelog/migration information, and then obtain explicit approval for that update. Approval for one commit does not authorize a different commit if the source branch moves.
