# EGCA Tracker Schema

A tracker implementation may use multiple sheets/tables/files, but it should preserve the following conceptual records.

## Overview

Recommended fields:

- Program name
- Target repository/system
- Objective
- Current phase
- Owner
- State backend
- Baseline reference
- EGCA feature/integration branch
- Final integration PR
- Last reviewed
- Notes

The EGCA feature/integration branch is the cumulative candidate-release branch for the program. Experiment/adaptation branches should target it rather than `main`. The final integration PR remains empty/unset until the complete program is ready for the program-level evidence gate.

## Candidate backlog

| Field | Purpose |
|---|---|
| Candidate ID | Stable identifier for the candidate |
| Capability | Short name |
| Problem / opportunity | Why this is being considered |
| Source / inspiration | Where the idea came from |
| Expected value | Why it may help |
| Status | Proposed / Investigating / Experimenting / Decided |
| Priority | Relative attention, independent of IDs |
| Notes | Open context |

## Source investigation

| Field | Purpose |
|---|---|
| Investigation ID | Stable identifier |
| Candidate ID | Candidate being investigated |
| Source | Repository, article, system, package, etc. |
| Source behavior | What the source actually does |
| Transferable principle | General idea worth testing |
| Source-specific details | Details that should not be copied blindly |
| Risks / constraints | Known concerns |
| Counterevidence | Reasons the idea may not transfer |
| References | Durable links or citations |
| Status | Pending / Complete |

## Experiments

| Field | Purpose |
|---|---|
| Experiment ID | Stable historical ID such as E-001 |
| Candidate ID | Candidate being tested |
| Title | Short experiment name |
| Hypothesis | Falsifiable expected outcome |
| Scope | Bounded implementation |
| Success evidence | What would support adoption |
| Rejection evidence | What would falsify or weaken the hypothesis |
| Depends on | Other experiment IDs or prerequisites |
| Execution priority | Scheduling independent of ID |
| Status | Planned / Approved / Running / Validating / Complete / Blocked |
| Base feature branch | EGCA cumulative integration branch used as experiment baseline |
| Experiment branch / PR | Repository evidence for this bounded experiment |
| Integration result | Not integrated / Integrated to feature branch / Superseded by adaptation |
| Validation | Tests, measurements, UX, runtime observations |
| Observed evidence | What actually happened |
| Decision | Adopt / Adapt / Reject / Repeat |
| Decision record | Reference to rationale |
| Follow-up | Resulting work or next experiment |

## Decision log

| Field | Purpose |
|---|---|
| Decision ID | Stable identifier |
| Date | When decision was made |
| Candidate ID | Related capability |
| Experiment ID(s) | Evidence-producing experiments |
| Decision | Adopt / Adapt / Reject / Repeat |
| Evidence summary | Relevant observations |
| Rationale | Why the gate resulted in this decision |
| Architectural consequence | What changes, if anything |
| Feature-branch consequence | What was or was not integrated into the cumulative branch |
| Follow-up | Remaining work/questions |
| References | PRs, tests, benchmarks, docs |

## Program finalization

Recommended fields or a dedicated final-gate record:

- Final gate ID/date
- EGCA feature branch
- Target production branch
- Feature-to-main PR
- Integrated experiment/adaptation IDs
- Full validation evidence
- Baseline reconciliation result
- Known residual risks
- Final release decision

The feature-to-main PR is a program-level artifact. It should not be used as the target for individual experiments.

## Rules

1. Never use row order as experiment identity.
2. Never silently convert candidate status into approved implementation.
3. Keep repository state out of the tracker when a link/reference is sufficient.
4. Preserve negative experiments; failed hypotheses are useful evidence.
5. Re-check repository reality before executing stale planned work.
6. One EGCA tracker/program uses one cumulative feature/integration branch.
7. Experiment and adaptation branches are based on and merge into that feature branch, not directly into `main`.
8. Rejected experiments are not merged into the feature branch merely to preserve history; preserve branch/PR/evidence references instead.
9. The feature branch merges to `main` only after the program-level final evidence gate passes and host-repository approval requirements are satisfied.
