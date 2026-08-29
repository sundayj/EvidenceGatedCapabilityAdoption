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
- Execution ledger reference
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
| Executor | Human / ChatGPT / Codex / other agent / hybrid / unknown |
| Execution start / end | Timing markers when known |
| Elapsed time | Wall-clock, agent-reported, or repository-window duration with type identified |
| Human intervention | Active time or intervention count when defensible |
| Model / reasoning | Primary model/tier and reasoning level when exposed |
| Agent runs / rework | Number of execution and corrective passes when known |
| Delegation summary | Count or compact summary; detailed delegations belong in the execution ledger |
| Usage / quota | Token/context/credit/allocation usage with the runtime's original unit |
| Telemetry confidence | High / Medium / Low, with provenance when needed |
| Execution ledger reference | Pointer to detailed forensic events when applicable |
| Decision | Adopt / Adapt / Reject / Repeat |
| Decision record | Reference to rationale |
| Follow-up | Resulting work or next experiment |

Execution telemetry is process evidence. It must not substitute for capability validation evidence. Unknown telemetry values should remain unknown rather than being guessed.

## Execution ledger

Use a separate append-only execution ledger for non-trivial, delegated, or case-study-worthy programs. It may be a tracker tab, a Git-tracked Markdown/YAML/JSON file beside the tracker, or another durable backend.

Recommended event fields:

| Field | Purpose |
|---|---|
| Timestamp | When the event occurred |
| Experiment / adaptation ID | Work item being executed |
| Executor | Human or agent responsible |
| Task / delegation | Bounded activity performed |
| Model / tier | Model used when configurable or observable |
| Reasoning level | Reasoning effort when configurable or observable |
| Delegation rationale | Why this task was delegated |
| Result | Outcome of the event |
| Used? | Whether a delegated result contributed to final work |
| Elapsed | Runtime or bounded event duration when known |
| Human intervention | Whether a human decision/correction was required |
| Repository reference | Branch, commit, PR, test, CI, or evidence document |
| Measurement source | Runtime report, usage UI, commit chronology, chat timestamp, human recollection, etc. |
| Confidence | High / Medium / Low |

The ledger is evidence provenance, not a transcript. Do not store full chain-of-thought, full chat logs, secrets, or unnecessary private data.

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
- Program execution summary
- Execution ledger reference
- Known telemetry gaps

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
10. Record execution telemetry when it is available and materially useful, especially for delegated or autonomous agent runs.
11. Distinguish agent runtime, wall-clock time, repository activity windows, and human estimates rather than collapsing them into one duration.
12. Preserve the unit and provenance of token/context/credit/quota measurements.
13. Keep detailed forensic execution events in the execution ledger; keep experiment rows concise.
