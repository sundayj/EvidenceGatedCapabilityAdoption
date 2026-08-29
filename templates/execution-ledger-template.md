# EGCA Execution Ledger

Program: `<program name>`

Tracker: `<tracker path / URL>`

Feature branch: `<branch>`

## Measurement conventions

- Wall-clock elapsed includes only a continuous run when known; otherwise label it as an upper bound.
- Agent elapsed is copied from the runtime when available.
- Repository windows are forensic proxies, not assumed active time.
- Usage values retain the unit exposed by the runtime.
- Unknown values remain unknown rather than being inferred without evidence.

## Program execution summary

| Field | Value | Provenance / confidence |
|---|---|---|
| Primary executor |  |  |
| Program start |  |  |
| Program completion |  |  |
| Wall-clock elapsed |  |  |
| Agent-reported elapsed |  |  |
| Human active time |  |  |
| Human interventions |  |  |
| Agent runs |  |  |
| Corrective / rework runs |  |  |
| Delegations |  |  |
| Usage / quota consumed |  |  |
| Final outcome |  |  |

## Experiment / adaptation summaries

| ID | Executor | Model / tier | Reasoning | Start | End | Elapsed | Human interventions | Runs / rework | Usage | Confidence |
|---|---|---|---|---|---|---:|---:|---|---|---|
| E-XXX |  |  |  |  |  |  |  |  |  |  |

## Delegation log

| Timestamp | Parent ID | Task | Model / tier | Reasoning | Why delegated | Result | Used? | Elapsed | Reference |
|---|---|---|---|---|---|---|---|---:|---|
|  | E-XXX |  |  |  |  |  |  |  |  |

## Significant execution events

| Timestamp | ID | Executor | Event | Result / evidence | Human intervention | Repository reference | Measurement source |
|---|---|---|---|---|---|---|---|
|  | E-XXX |  |  |  |  |  |  |

## Forensic reconstruction notes

Use this section only when telemetry is being reconstructed after the fact.

For each reconstructed value record:

- the source (runtime report, chat timestamp, commit, PR, CI, usage UI, human recollection);
- whether the interval is exact, bounded, or estimated;
- known idle periods or confounders;
- why the confidence label is justified.

## Retrospective

### What reduced cost or elapsed time?


### What created duplicate work or rework?


### Where was high-capability reasoning actually necessary?


### Where would a lower-cost agent have been sufficient?


### Methodology changes suggested by this run

