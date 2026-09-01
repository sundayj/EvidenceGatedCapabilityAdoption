# Changelog

All notable changes to EGCA are recorded here. EGCA remains experimental; version numbers describe methodology/package compatibility and do not imply production maturity.

## 0.3.0 - 2026-09-01

### Added

- An evidence-scope invariant: Adopt applies only to the artifact, environment, data shapes/scale, integration path, and operational conditions actually tested.
- A linked productionization experiment/adaptation requirement when the intended live implementation differs materially from the validated prototype, fixture, isolated module, or mocked integration.
- Criterion-to-production traceability across code paths, adversarial fixtures, automated assertions, and branch-matched runtime evidence.
- Explicit lifecycle states for production readiness, merge, deployment, and operational validation.
- Productionization fields in the experiment, decision, tracker, goal-prompt, and JSON-schema contracts.
- A sanitized case-study learning describing the prototype-to-production evidence gap that motivated the change.

### Changed

- Replaced the broad exclusion for "already-approved implementation" with a narrower rule: do not repeat resolved discovery, but continue EGCA productionization controls for material untested deltas.
- Clarified that post-merge validation confirms release behavior and should not be the first evidence for behavior safely testable before merge.
- Restored the installable skill package's parity with already-merged execution-telemetry guidance in the repository root.

### Compatibility

- Backward-compatible with historical trackers and decisions. Existing evidence remains valid within the boundary actually tested.
- Active programs should add evidence-boundary and productionization records prospectively; they should not rewrite historical verdicts.

## 0.2.0 - 2026-08-28

### Added

- Explicit skill version metadata.
- A roadmap for plugin distribution, reproducible methodology pinning, and EGCA-governed methodology evolution.
- `scripts/egca_update.py` for checking the canonical repository for updates and applying an approved update.
- An explicit approval boundary: update checks may be run proactively, but an installed skill may not replace itself until the user has approved the exact proposed repository commit.
- Migration notes for active EGCA programs.

### Security and governance

- Updates are pinned to the exact Git commit shown during the check step.
- The updater refuses an approval if the canonical branch head has moved since approval was granted.
- The updater creates a local backup before replacing managed skill-package files.
- Silent/background self-updates are explicitly prohibited by the skill contract.

## 0.1.0

- Initial public experimental methodology and Agent Skill package.
- Evidence-gated lifecycle, Adopt/Adapt/Reject/Repeat decisions, durable-state requirements, and cumulative EGCA feature-branch isolation.
