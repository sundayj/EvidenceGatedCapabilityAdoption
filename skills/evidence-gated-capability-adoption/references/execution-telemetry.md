# EGCA Execution Telemetry

## Purpose

EGCA records whether a capability earned adoption. For agent-assisted engineering, the method should also preserve enough execution provenance to evaluate the cost of producing that evidence.

Execution telemetry answers questions such as:

- how much wall-clock time did an experiment require?
- how much human attention was required?
- which agent/model/reasoning configuration performed the work?
- did delegation reduce or duplicate reasoning?
- how many retries or corrective passes were required?
- what proportion of the available agent budget was consumed, when the runtime exposes that information?

These measurements are process evidence. They do not replace repository-grounded evidence for the capability hypothesis.

## Storage model

Use two levels of detail.

### Experiment summary

Each experiment or adaptation should carry a compact execution summary beside its normal evidence:

- executor: human, ChatGPT, Codex, other agent, or hybrid;
- start and completion timestamps when known;
- wall-clock elapsed time when meaningful;
- agent-reported elapsed time when available;
- human active time or intervention count when reasonably measurable;
- primary model and reasoning level when exposed;
- number of agent runs / corrective passes;
- delegation count;
- token, context, credit, or allocation usage when the runtime exposes it;
- measurement confidence and provenance.

Do not invent unavailable measurements. Prefer `unknown` plus a provenance note over an unsupported estimate.

### Execution ledger

For non-trivial or delegated runs, maintain a separate append-only execution ledger alongside the program tracker. It should record significant execution events without becoming a transcript.

Recommended event fields:

- timestamp;
- experiment/adaptation ID;
- executor;
- task or bounded delegation;
- model/tier;
- reasoning level;
- why delegation was appropriate;
- result;
- whether the result was used;
- relevant branch/commit/PR;
- elapsed time if known;
- human intervention required;
- verification performed;
- notes and measurement source.

The ledger is the detailed forensic record. The tracker remains the compact research and decision state.

## Delegation telemetry

When subagents are used, record each materially distinct delegation. At minimum preserve:

- task;
- model/tier if configurable or observable;
- reasoning level if configurable or observable;
- delegation rationale;
- result;
- whether the parent agent used the result.

The objective is not to maximize delegation. Excess parallelism can duplicate repository discovery, increase token use, create conflicting partial models of the system, and increase integration work. Record enough information to compare selective delegation with alternative workflows.

## Timing rules

Distinguish these measurements:

- **Wall-clock elapsed:** real time from the defined start marker to completion marker. Breaks and waiting make this an upper bound unless the run was known to be continuous.
- **Agent elapsed:** runtime self-report for a task or goal, when provided.
- **Repository activity window:** time from first relevant implementation commit to last relevant implementation/evidence commit. This is a useful forensic proxy but is not automatically equal to active engineering time.
- **Human active time:** time spent supplying evidence, answering blockers, reviewing, or repairing work. Estimate only when there is a defensible basis.

Always state which measurement is being reported.

## Usage / cost rules

If the runtime exposes token, context, credit, or quota consumption, record it with the unit and source. Do not convert between units unless the conversion is documented.

Examples:

- `weekly_allocation_used_percent: 4` — observed in product usage UI;
- `tokens_used: 128000` — reported by runtime;
- `usage: unknown` — runtime did not expose a defensible value.

These figures are useful for comparing workflows but should not be treated as precise monetary cost unless pricing and model accounting are also recorded.

## Evidence quality

Execution metrics need provenance just like capability evidence.

Use a confidence label:

- **High** — runtime-reported duration, explicit usage meter, or timestamps that tightly bracket a continuous run;
- **Medium** — repository/chat timestamps strongly constrain the interval but may include minor idle time;
- **Low** — reconstructed from broad windows or human recollection.

Keep user-reported or agent-reported metrics explicitly labeled as such when they cannot be independently verified.

## Why this belongs in EGCA

A method intended to reduce speculative complexity should be measurable not only by architectural outcomes but also by the cost of reaching those outcomes. Over multiple case studies, execution telemetry can test hypotheses such as:

- selective model routing reduces duplicate high-cost reasoning;
- bounded subagents outperform symmetric adversarial review loops for some repository-scale work;
- evidence-first experiments reduce rework compared with implementation-first plans;
- stronger reasoning is most valuable at ambiguity and integration boundaries rather than for mechanical tasks;
- EGCA ceremony pays for itself by preventing larger rejected implementations.

A single run cannot establish these claims. The telemetry contract exists so future runs can accumulate comparable evidence.