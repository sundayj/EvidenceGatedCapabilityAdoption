# Experiment Template

## Experiment ID

`E-XXX`

Stable historical ID. Do not renumber if execution priority changes.

## Candidate ID

`C-XXX`

## Title

Short experiment name.

## Hypothesis

State a falsifiable prediction about what should improve in the target system.

## Scope

Describe the smallest bounded repository change capable of answering the question.

## Out of scope

Explicitly list production rollout, unrelated refactors, or adjacent work that should not be absorbed into the experiment.

## Success evidence

What observable evidence would support adoption?

- tests
- benchmark thresholds
- UX behavior
- operational metrics
- failure reduction
- review findings
- maintenance complexity

## Rejection evidence

What evidence would falsify or materially weaken the hypothesis?

## Dependencies

Other experiment IDs or prerequisites.

## Execution priority

Scheduling field independent of the experiment ID.

## Validation plan

How will evidence be collected?

## Repository references

- branch:
- commit(s):
- PR:
- tests/benchmarks:

## Execution telemetry

Keep this compact. Use a separate execution ledger for detailed events or subagent delegations.

- executor: `Human | ChatGPT | Codex | Other agent | Hybrid | Unknown`
- started at:
- completed at:
- wall-clock elapsed:
- agent-reported elapsed:
- human active time:
- human interventions:
- primary model / tier:
- reasoning level:
- agent runs:
- corrective / rework runs:
- delegation count:
- usage / quota consumed:
- execution ledger reference:
- measurement provenance / confidence:

Do not invent unavailable values. Distinguish runtime-reported duration, repository activity windows, and human estimates.

## Observed evidence

Record what actually happened, including negative and unexpected findings.

## Evidence gate

`Adopt | Adapt | Reject | Repeat`

## Rationale

Why does the evidence justify this decision?

## Follow-up

Resulting implementation work, another experiment, or no action.
