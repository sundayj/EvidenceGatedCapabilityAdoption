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

## Tested artifact and environment

State what is actually being tested: prototype, fixture, isolated module, integrated branch implementation, staged runtime, or another concrete artifact/environment.

## Evidence applicability boundary

State the data shapes, scale, integrations, runtime conditions, and behaviors to which this experiment's evidence may legitimately be applied.

## Productionization delta

Describe only the unresolved difference between the tested artifact and the intended production implementation, or record `None`. Link the prior experiment/decision whose evidence is being carried forward.

## Productionization status

`Not required | Required | Planned | Running | Validated | Blocked | Deferred`

Record the current state of the delta separately from its description. Link the productionization experiment/adaptation when one exists, and state the residual boundary for a deferred status.

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

### Adversarial / counterexample cases

List the assumptions and production boundaries most likely to fail, with at least one meaningful counterexample for each consequential assumption.

### Criterion-to-evidence traceability

| Accepted criterion | Production code path | Automated evidence | Branch-matched runtime evidence |
|---|---|---|---|
|  |  |  |  |

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

The decision applies only within the recorded evidence applicability boundary.

## Rationale

Why does the evidence justify this decision?

## Follow-up

Resulting implementation work, a linked productionization experiment/adaptation, another experiment, or no action. Record productionization status explicitly rather than treating Adopt as automatic production readiness.
