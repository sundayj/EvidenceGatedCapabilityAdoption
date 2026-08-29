# Case Study: Selective Agent Delegation in a PaySpan EGCA Closeout

## Summary

This case study records a late-stage PaySpan EGCA run in which a Codex parent agent was instructed to execute the remaining evidence-gated work autonomously and to delegate bounded subproblems to subagents using the least expensive model/reasoning tier likely to complete each task reliably.

The run is notable for two reasons:

1. the substantive repository work completed in under 20 minutes by commit chronology, despite a contemporaneous human/ChatGPT planning estimate of roughly 2–5 hours;
2. the fast execution still exposed a process defect: Codex did not fully update the final durable tracker state, requiring a later ChatGPT GitHub-connector repair.

This is a case study, not a controlled benchmark. It supports hypotheses for further testing; it does not establish that selective delegation is universally superior to adversarial multi-agent review.

## Context

The active capability program was PaySpan's daily-reconciliation EGCA tracker. By this point the program had already accumulated multiple experiments, deterministic reconciliation policies, compatibility gates, and real-data dogfood evidence.

The remaining work was cross-cutting rather than greenfield implementation. It included:

- completing exception-queue semantics while preserving independent financial and identity authority;
- integrating an evidence-complete reciprocal-institution transfer frontier without weakening abstention boundaries;
- running focused and cross-cutting regression gates;
- reconciling tracker state with repository reality;
- preparing the cumulative EGCA branch for final review without modifying `main`.

## Execution-policy intervention

PaySpan commit `d1827673267dc42164fed8f3725f84a3bab6334c` added an **EGCA Autonomous Execution Policy** to the repository instructions.

The policy told the agent to:

- treat the active EGCA tracker and evidence documents as the governing plan;
- reconstruct completed state instead of repeating finished experiments;
- work autonomously through unresolved experiments and adaptations;
- prefer bounded regressions and evidence gates before implementation;
- use subagents selectively rather than symmetrically;
- route repository search, test reading, mechanical verification, and similar work to low-cost/lightweight agents;
- route bounded implementation, regression coverage, and localized diagnosis to mid-tier agents;
- reserve high-capability agents for architectural ambiguity, cross-cutting invariants, and difficult failures;
- prefer the least expensive agent that can reliably complete a bounded task;
- avoid spawning multiple agents to investigate substantially the same question;
- avoid parallelizing dependent stages merely to reduce elapsed time;
- preserve explicit abstention rather than weakening deterministic policy to reduce queue size.

This differs materially from a symmetric adversarial loop in which two similarly capable agents repeatedly review one another's entire plan or implementation.

## Repository-observed execution window

The policy commit was recorded at:

- `d182767` — 2026-08-29 13:46:21 UTC

The subsequent substantive EGCA commits were:

- `a3dee1e` — 14:04:04 UTC — adopt E-008 transaction-review queue semantics;
- `7323137` — 14:04:11 UTC — avoid treating institution credit labels as refunds;
- `32decd9` — 14:04:11 UTC — promote reciprocal institution transfer evidence;
- `e44a63d` — 14:05:57 UTC — record reciprocal institution transfer adoption and final deterministic compatibility evidence.

Therefore:

- first substantive completion commit: **17m 43s** after the execution-policy commit;
- final Codex-era evidence commit: **19m 36s** after the execution-policy commit.

The interval is unusually tight and the commits are clustered, so this is a **high-confidence repository activity window** for the run. It is still not identical to an independently measured agent runtime unless the Codex session itself reports the same duration.

Git comparison from `d182767` through `e44a63d` shows:

- **4 commits**;
- **15 files changed**;
- approximately **500 additions and 15 deletions**;
- backend/API behavior, deterministic reconciliation logic, frontend review semantics, regression coverage, evidence documentation, and tracker updates all changed within the bounded run.

## Validation evidence

The E-008 work recorded:

- **4 focused API regressions passed**;
- **65 Transaction Review component regressions passed**;
- read-only local-data validation confirmed that the apparent review queue represented identity-only work rather than unresolved financial decisions.

The reciprocal-institution transfer closeout recorded a final deterministic compatibility gate of:

- **61 passed** across transfer, account-verification, exact-income, ledger-noise, historical bill-payment, provider-return, daily-cycle, and transaction-ledger coverage.

The implementation preserved explicit abstention for generic or partial institution labels rather than broadening the deterministic rule simply to resolve more rows.

## Usage observation

The operator reported that the Codex product's weekly usage/context indicator increased by only approximately **4%** during this execution method.

This is a **user-observed product metric**, not a repository-verifiable token count. It should be retained in the case study because it is directly relevant to agent economics, but future runs should capture the exact unit exposed by the runtime or product UI whenever possible.

## Planning estimate versus observed execution

Before execution, the human/ChatGPT planning estimate for the remaining work was approximately **2–5 hours**.

The repository-observed Codex activity window was **19m 36s** from the autonomous-policy commit to the final substantive evidence commit.

This is a large discrepancy, but it must be interpreted carefully:

- the estimate was not a formal benchmark prediction;
- the repository window may omit pre-commit reasoning that occurred before `d182767`;
- some prior EGCA investigation and implementation had already reduced uncertainty;
- the run benefited from a mature tracker, explicit invariants, regression coverage, and existing evidence documents;
- the delegated workflow itself is one plausible contributor to the low elapsed time, not the only contributor.

## Failure / correction: durable-state closeout

The run did **not** fully satisfy EGCA's durable-state requirement on its own.

The operator later discovered that Codex had not updated all final tracker details. A ChatGPT GitHub-connector pass subsequently produced commit:

- `e4bd1482b24527ec3f3d3eba20524fc88f847220` — 2026-08-29 17:08:56 UTC — final adoption/tracker repair and integration state.

This later action should not be counted as part of the sub-20-minute Codex implementation window.

It is important negative evidence: autonomous execution can finish repository work while still failing the methodology if the durable record is incomplete.

A subsequent PaySpan instruction change (`b50f1df`) required a concise delegation log recording each subagent's task, model/tier, reasoning level, delegation rationale, result, and whether its work was used.

This case study motivates extending that idea into a general EGCA execution-telemetry contract.

## Comparison hypothesis: selective delegation versus adversarial review loops

A practitioner discussing EGCA proposed an alternative workflow: have one coding agent produce a plan, send it to a second model for simplicity/KISS review, and repeat the adversarial review loop until both agents converge.

That approach is credible and may be useful. Independent review can expose blind spots, challenge assumptions, and reduce single-agent confirmation bias.

However, it is not operationally equivalent to the workflow tested here.

### Symmetric adversarial loop

Typical shape:

```text
Agent A reasons about the full problem
        -> Agent B independently reasons about much of the same problem
        -> critique
        -> Agent A revises
        -> Agent B re-reviews
        -> repeat until convergence
```

Potential strengths:

- independent challenge;
- useful disagreement signal;
- strong review pressure when agents have genuinely different failure modes.

Potential costs:

- duplicate repository discovery and system modeling;
- repeated high-capability reasoning over the same scope;
- large context/token consumption;
- long convergence time;
- review comments that create churn without improving the evidence boundary;
- two agents can still converge on unnecessary complexity.

### Selective EGCA delegation

Observed shape:

```text
one governing EGCA plan + evidence boundaries
        -> parent agent owns integration and architectural state
        -> bounded subproblem A -> cheapest reliable agent
        -> bounded subproblem B -> appropriate agent
        -> high-capability reasoning only at ambiguity/invariant boundaries
        -> parent integrates evidence
        -> explicit regression and final gates
```

The design goal is **non-overlapping cognition** rather than repeated full-problem critique.

The parent does not ask every agent to rediscover the architecture. It delegates narrow work where parallel or cheaper reasoning has a favorable cost/benefit ratio and keeps dependent stages serialized.

## Prior practitioner experience

The operator reports prior moderate success using two Codex agents in an iterative/adversarial arrangement, but also recurring problems:

- overcomplication remained possible;
- duplicate work occurred;
- small integration bugs still appeared;
- token/context usage was high;
- elapsed time was substantially longer.

These observations are retrospective and not a controlled comparison. They justify a future experiment rather than a causal conclusion.

## What this case study supports

The evidence supports the following bounded conclusions:

1. **A mature EGCA tracker can serve as a high-leverage coordination artifact for autonomous agent execution.** The agent did not need another general workflow engine or second architecture model.
2. **Selective subagent routing is compatible with EGCA's smallest-useful-experiment philosophy.** Delegation itself can be evidence-gated and cost-aware.
3. **Repository-scale work can complete much faster than conservative human/ChatGPT estimates when uncertainty has already been reduced and agent roles are bounded.**
4. **Fast implementation is not sufficient EGCA completion.** Durable state must be explicitly verified at the final gate.
5. **Agent economics should become first-class case-study evidence.** Without execution telemetry, later comparisons depend too heavily on chat reconstruction and recollection.

## What this case study does not prove

It does **not** prove that:

- subagents caused the full speedup;
- the same routing strategy will perform equally well on greenfield or highly ambiguous work;
- 4% usage is directly comparable to token counts or dollar cost;
- adversarial review loops are ineffective;
- one model family reviewing itself is always preferable to independent cross-model review;
- the result would reproduce without the prior EGCA tracker, tests, and evidence base.

## New EGCA methodology hypothesis

**H-Execution-Routing:** For repository-scale EGCA work with a mature tracker and explicit evidence boundaries, a parent agent using selective, non-overlapping model/reasoning delegation will reduce wall-clock time and agent usage without increasing rework or escaped defects compared with a symmetric iterative adversarial review loop.

This hypothesis should be tested prospectively across future EGCA programs.

Recommended measurements:

- elapsed time;
- human active time and interventions;
- model/reasoning configuration;
- delegations and overlap;
- token/context/credit usage;
- number of agent runs and rework passes;
- defects found during final review;
- tracker omissions or process failures;
- number of architectural elements proposed, adopted, adapted, and rejected;
- final validation results.

## Methodology consequence

Adopt execution telemetry as part of EGCA's durable evidence contract, while keeping it separate from the capability evidence gate itself.

The tracker should contain a concise execution summary. Detailed forensic events should live in an append-only execution ledger beside the tracker. Public EGCA case studies should carry only sanitized aggregates and evidence references.
