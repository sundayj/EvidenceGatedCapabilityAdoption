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
- Last reviewed
- Notes

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
| Branch / PR | Repository evidence |
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
| Follow-up | Remaining work/questions |
| References | PRs, tests, benchmarks, docs |

## Rules

1. Never use row order as experiment identity.
2. Never silently convert candidate status into approved implementation.
3. Keep repository state out of the tracker when a link/reference is sufficient.
4. Preserve negative experiments; failed hypotheses are useful evidence.
5. Re-check repository reality before executing stale planned work.
