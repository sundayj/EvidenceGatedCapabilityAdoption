# EGCA competing-baselines validation

**Status:** research design note; not executed  
**Branch:** `research/cross-model-simplicity-baseline`  
**Created:** 2026-08-30  
**Purpose:** add cross-model iterative simplicity review as a serious competing baseline for empirical EGCA validation

## Context

A Reddit response to the EGCA article proposed a practical alternative workflow: the primary coding agent creates a plan or architectural decision, a second frontier model independently reviews it for KISS/simplicity, and the agents iterate until the result is sufficiently simple.

This should be recorded as **cross-model iterative simplicity review**, not merely KISS prompting. The mechanism is not just telling one model to keep the solution simple. It is an iterative two-model critique loop in which an independent reviewer model applies simplicity pressure to architecture and fine-grained implementation decisions.

The proposal is a serious competing baseline. It could remove unnecessary complexity without EGCA's full tracker, hypothesis, experiment, branch, and decision-record machinery. EGCA must not assume that its durable evidence process produces better outcomes until that claim is measured.

## Baseline definition

### Cross-model iterative simplicity review

A candidate treatment should freeze a workflow approximately as follows:

1. The primary coding agent inspects the repository and produces a plan, capability decision, or implementation proposal.
2. A second capable model, such as Claude or another frontier reviewer, independently reviews the plan for KISS/simplicity, unnecessary architecture, excessive fields, avoidable abstractions, and failure to reuse existing system capabilities.
3. The primary agent revises the plan or implementation in response.
4. The reviewer repeats the simplicity review.
5. The loop stops at a preregistered convergence criterion, budget limit, or unresolved-disagreement state.
6. The final implementation proceeds under the reviewed plan, with the review transcript or structured summary retained only as process evidence.

The treatment should not be scored as EGCA compliance. It should be scored on task outcomes, architectural appropriateness, unnecessary complexity, justified architecture retention, process cost, and downstream rework.

## Economic and operational critique

The main critique is not only that the loop may be more expensive. It may also duplicate context acquisition and add coordination latency.

Potential costs to measure:

- access to a second capable model, which may require a second paid subscription, separate API account, or additional usage allocation;
- inference/reasoning tokens consumed by both the primary agent and reviewer;
- overlapping repository/system context acquisition by both models;
- repeated handoff, review, revision, and convergence latency;
- additional human attention when models disagree or the stop criterion is unclear;
- integration cost when the reviewer optimizes for simplicity in a way that conflicts with hidden requirements, future-change needs, or evidence that actually justifies architecture.

The speed question is empirical. Cross-model review may be slower per task because two models reason and exchange context, or faster overall if it prevents overbuilt implementations and reduces later rework. Both possibilities must remain open until measured.

## EGCA contrast: durable accumulated context

EGCA's competing claim is that durable project state can reduce repeated rediscovery over time. A tracker, research ledger, and decision log may preserve:

- hypotheses and decision questions;
- source investigations and repository/system knowledge;
- evidence criteria and experiment designs;
- observed evidence and validation gaps;
- negative results and rejected alternatives;
- architectural decisions and reconsideration conditions;
- execution telemetry and cost history.

This may let later agents or sessions start from accumulated evidence rather than reacquiring the same repository and decision context from scratch. That is a hypothesis, not a settled advantage. EGCA's durable state also has maintenance cost, can become stale, and may bias later agents if repository reality has moved.

## Minimum comparative experiment

A future preregistered comparison should include at least these arms:

| Arm | Treatment | Primary mechanism under test |
| --- | --- | --- |
| A | Agent alone | ordinary competent coding-agent behavior under repository instructions |
| B | Self-review / KISS | same model reviews its own plan/implementation for simplicity before proceeding |
| C | Cross-model iterative simplicity review | primary coding agent plus independent frontier reviewer loop for KISS/simplicity |
| D | Ponytail | explicit minimum-sufficient-implementation pressure using Ponytail's frozen method |
| E | EGCA | evidence-gated capability adoption using the frozen EGCA skill/methodology |
| F | EGCA + independent reviewer | optional combined treatment: EGCA with a second-model reviewer applied at defined gates |

Arm F is optional because it changes both evidence gating and reviewer topology. It may be useful for testing whether independent review complements EGCA, but it should not be used to rescue EGCA unless preregistered before outcome inspection.

## Validation dimensions

The comparison should measure more than code size or whether a model says the result is simple.

Required dimensions:

- functional correctness and required test/build outcomes;
- architectural appropriateness and repository fit;
- unnecessary architectural surface, including avoidable services, registries, models, fields, dependencies, and configuration;
- reuse of existing capabilities;
- ability to retain justified architecture when the evidence really requires it;
- downstream rework rate and severity;
- wall-clock latency from task start to accepted result;
- total inference/token usage, including reasoning tokens where exposed;
- monetary or allocation cost using frozen pricing/allocation metadata where available;
- repository/context acquisition work duplicated across models or sessions;
- human intervention required for disagreements, ambiguity, or failed convergence;
- durability of the decision when similar questions recur later.

## Threats to validity

- If reviewers know which arm produced a solution, architectural-quality scores may encode method preference.
- If task selection favors overengineering failures, simplicity-review baselines may appear stronger than they are in tasks where architecture is actually justified.
- If task selection favors longitudinal governance, EGCA may appear stronger than it is for one-off implementation tickets.
- If cross-model review uses a stronger or more expensive model than the other arms, results may compare model capacity rather than workflow design.
- If the second model receives too little repository context, the treatment may underperform because of context starvation rather than reviewer-loop weakness.
- If the second model receives full context every round, the treatment may become unrealistically expensive for users with tight subscription/API budgets.
- If prior EGCA notes are supplied only to EGCA arms, context availability becomes part of the treatment and must be measured, not hidden.

## Decision discipline

Valid outcomes include:

- cross-model iterative simplicity review beats EGCA on quality, speed, or total cost;
- EGCA beats cross-model review only in longitudinal or high-uncertainty scenarios;
- self-review/KISS is sufficient for many ordinary tasks;
- Ponytail captures the same simplification benefit at lower cost;
- EGCA plus independent review is best but too expensive for routine use;
- all structured workflows are equivalent to agent-alone behavior for the tested task class;
- results are inconclusive or model/provider dependent.

No conclusion should be generalized beyond the frozen task strata, model/runtime configuration, and budget profile tested.

## Relationship to existing EGCA studies

This note extends, rather than replaces, the EGCA self-ablation and EGCA x Ponytail work. The self-ablation study asks how much EGCA process is necessary. The Ponytail comparison asks whether a separate minimum-sufficient-implementation method reproduces or complements EGCA's effects. Cross-model iterative simplicity review adds a workflow-topology baseline: independent model critique plus iteration.

The shared research question is whether EGCA's extra durable-state and evidence-gating machinery earns its cost compared with cheaper, faster, or more familiar agent-review workflows.
