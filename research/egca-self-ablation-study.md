# EGCA self-ablation study

**Status:** research design captured; not yet preregistered or executed  
**Branch:** `research/egca-self-ablation`  
**Purpose:** test whether EGCA can simplify itself using its own evidence-gated method

## Research premise

EGCA should apply its governing principle to itself:

> No process complexity gets to remain merely because it sounds useful. It has to earn its place through evidence.

The central question is not merely whether full EGCA can improve architectural decisions. The harder question is:

> **What is the smallest EGCA process that preserves the measurable benefit, and which mechanisms fail to justify their additional process cost?**

This study is intentionally separate from the EGCA × Ponytail comparison. It remains valuable even if no external methodology is used as a comparator.

## Candidate capability under evaluation

The candidate capability is **the current full EGCA process machinery itself**.

### Primary hypothesis

> The current full EGCA process produces meaningfully better architectural decisions and/or longitudinal decision quality than a substantially reduced EGCA process, enough to justify its additional time, token, artifact, and cognitive cost.

### Primary falsification condition

If a reduced EGCA variant produces practically equivalent architectural outcomes while materially reducing process cost, then the additional full-process machinery has not earned mandatory status.

Evidence against full-process necessity may include materially lower:

- tokens;
- agent turns;
- elapsed time;
- tool calls;
- artifacts created;
- human intervention;
- bookkeeping/state-maintenance burden;

without meaningful degradation in:

- correctness;
- completeness;
- security/safety;
- robustness;
- repository fit;
- architectural proportionality;
- justified architectural expansion;
- resistance to unjustified architectural commitment;
- later decision quality where longitudinal state is in scope.

A valid result may therefore be **Adapt EGCA by removing, collapsing, or making optional mechanisms whose incremental value is not demonstrated.**

## Candidate EGCA mechanisms to test

Treat each process mechanism as a capability that must earn its place.

| Mechanism | Candidate question |
| --- | --- |
| Baseline investigation | Does explicitly requiring baseline investigation improve decisions over normal competent agent inspection? |
| Candidate state | Does explicitly labeling an idea as a candidate materially change behavior or merely add bookkeeping? |
| Falsifiable hypothesis | Does formal hypothesis-writing improve architectural discrimination enough to justify its cost? |
| Contrary-evidence search | Does requiring contrary evidence materially reduce confirmation bias or speculative adoption? |
| Smallest useful experiment | Does explicit experiment bounding improve outcomes beyond ordinary incremental implementation? |
| Predeclared evidence criteria | Does defining the gate before implementation reduce motivated reasoning or post-hoc justification? |
| Adopt / Adapt / Reject / Repeat taxonomy | Does the four-way decision vocabulary preserve useful distinctions, or can it be collapsed? |
| Durable decision record | Does retained rationale prevent rediscovery, repeated debate, or inconsistent later decisions? |
| Structured experiment tracker | Does structured project state outperform a short durable Markdown record enough to justify the overhead? |
| Experiment branches | Does branch isolation materially improve evidence integrity or rollback enough to justify workflow cost? |
| Cumulative integration branch | Is a dedicated feature/integration branch necessary for multi-experiment programs? |
| Program-level final gate | Does a final adoption gate catch consequential errors or unjustified accumulation that ordinary review misses? |

No mechanism is presumed necessary because it currently exists in EGCA.

## Proposed primary comparison

Use progressively simpler variants rather than only full-EGCA versus no-EGCA.

| Arm | Process |
| --- | --- |
| A | Agent normally, with benchmark task and ordinary repository instructions only |
| B | Agent + concise evidence-gating instruction |
| C | EGCA-Lite |
| D | Full EGCA |

The central estimand is not simply `D > A`. It is the **marginal value of each increase in process intensity relative to its additional cost**.

## Candidate concise evidence-gating instruction

> Inspect the existing system first. Do not add architectural complexity unless repository-grounded evidence shows existing capabilities are insufficient. Test the smallest change that can falsify the proposed architecture, and explicitly reject it if the evidence does not justify adoption.

This is a candidate treatment and must be frozen before confirmatory execution.

## Candidate EGCA-Lite

A deliberately reduced process candidate:

1. Inspect existing capability.
2. State the architectural hypothesis.
3. Define what evidence would justify it.
4. Run the smallest useful test.
5. Adopt, adapt, reject, or repeat.
6. Record the decision and evidence concisely.

EGCA-Lite should not require a large tracker schema, elaborate state vocabulary, or ancillary artifacts unless the task itself makes those necessary.

This exact treatment is provisional until preregistration.

## Process-efficiency objective

The study should seek a **process efficiency frontier**, not maximal ceremony or minimal LOC.

Conceptually:

```text
architectural / decision quality
    ^
    |                    full EGCA
    |                *
    |            * EGCA-Lite
    |         * concise gate
    |     * agent alone
    +------------------------------> process cost
```

The useful target is the **knee of the curve**: the smallest process whose additional simplification would cause meaningful loss.

If full EGCA lies materially to the right of EGCA-Lite without meaningful quality gain, full-process mandatory use should fail its adoption gate.

## Component-ablation program

After identifying a viable reduced core, individual mechanisms can be removed one at a time or in carefully designed factorial subsets.

Examples:

### Contrary-evidence ablation

Compare:

- EGCA-Lite;
- EGCA-Lite without an explicit contrary-evidence requirement.

Question: does explicit counterevidence search materially reduce confirmation bias or unjustified adoption?

### Predeclared-gate ablation

Compare:

- EGCA-Lite;
- EGCA-Lite where evidence criteria are not declared before implementation.

Question: does predeclaration reduce post-hoc rationalization?

### Formal-hypothesis ablation

Compare:

- explicit falsifiable hypothesis;
- concise decision question without formal hypothesis wording.

Question: is hypothesis formalization itself valuable, or is the value actually coming from explicit uncertainty and evidence criteria?

### Decision-taxonomy ablation

Compare the full `Adopt / Adapt / Reject / Repeat` vocabulary with a reduced decision representation.

Question: do `Adapt` and `Repeat` preserve consequential distinctions or primarily increase ceremony?

### Tracker ablation

Compare:

- structured tracker/state schema;
- concise durable Markdown decision record.

Question: when does structure improve continuity enough to justify maintenance cost?

### Branch-workflow ablation

Compare EGCA branch isolation/integration mechanics with ordinary disciplined feature-branch work.

Question: does the extra branch topology materially protect experimental evidence or production integration?

## Important separation: single-task vs longitudinal mechanisms

Some EGCA mechanisms cannot be fairly evaluated with one isolated coding ticket.

### Single-task mechanisms

Potentially testable in ordinary benchmark tasks:

- baseline investigation;
- explicit hypothesis;
- contrary-evidence requirement;
- predeclared evidence criteria;
- smallest useful experiment;
- decision taxonomy;
- concise decision recording;
- immediate process cost.

### Longitudinal mechanisms

Require a separate multi-step / multi-session protocol:

- durable decision records;
- structured tracker state;
- rejected-alternative memory;
- reconsideration conditions;
- cumulative integration branch;
- final program-level gate;
- continuity across agents/models/sessions.

Do not infer the value of durable state from a one-ticket factorial.

## Candidate longitudinal sequence

A later preregistration could use a sequence in which:

1. an early abstraction appears attractive;
2. evidence is initially weak and it is rejected/deferred;
3. the same idea resurfaces in a later task;
4. additional evidence changes the decision boundary;
5. a narrow version eventually becomes justified;
6. prior rationale should influence the later implementation;
7. another agent/session must continue from the project state.

This sequence could compare concise/no durable state against EGCA durable state and measure rediscovery cost, consistency, repeated mistakes, and eventual decision quality.

## Possible tiered EGCA architecture — hypothesis only

A possible outcome is that EGCA should become progressive rather than monolithic. This is a hypothesis to test, not a methodology change.

### Core layer

Potential always-on minimum:

```text
Investigate
-> Hypothesis / decision question
-> Evidence gate
-> Smallest useful experiment
-> Adopt / Adapt / Reject
```

### Durable-state layer

Enable when decisions span time, agents, or sessions:

```text
Decision record
-> evidence history
-> rejected alternatives
-> reconsideration conditions
```

### Program / architecture layer

Enable only for larger multi-experiment initiatives:

```text
experiment isolation
-> cumulative integration
-> dependency / state tracking
-> program-level final adoption gate
```

If supported, this would make EGCA risk-adjusted and progressive-disclosure rather than uniformly process-heavy.

## Outcome interpretation

All of the following are valid outcomes.

### Full EGCA materially wins

The additional ceremony earns its place. Preserve the mechanisms whose incremental contribution is supported.

### EGCA-Lite matches full EGCA

Simplify EGCA. Move unsupported mechanisms to optional/advanced use or remove them.

### Concise evidence-gating prompt matches EGCA-Lite and full EGCA

Narrow EGCA's value proposition. EGCA may primarily be a compact reasoning discipline plus optional longitudinal/governance tooling.

### Agent alone matches all EGCA variants

Question whether EGCA adds measurable value for that task class. Do not defend the method by changing the benchmark after seeing the result.

### Different intensities win in different contexts

Prefer a risk-adjusted activation rule: lightweight process for ordinary decisions, heavier process only when uncertainty, architectural commitment, or longitudinal coordination crosses evidence-backed thresholds.

## Anti-bias rules

1. Do not select only tasks already known to benefit from EGCA.
2. Preserve tasks where ordinary agent reasoning is expected to be sufficient.
3. Include tasks where new architecture is actually justified, so simplification pressure can cause measurable underbuilding.
4. Measure process cost explicitly; do not treat extra deliberation as free.
5. Do not use artifact count or process compliance as a quality outcome.
6. A full-EGCA run does not score better merely because it produced better documentation.
7. Freeze treatments, outcomes, exclusions, and analysis before confirmatory execution.
8. If a simpler treatment matches full EGCA, accept redundancy as evidence.
9. If removing a mechanism improves outcomes, treat that as evidence against the mechanism.
10. Do not revise EGCA to preserve every existing component.

## Relationship to the Ponytail benchmark

This study asks a different question from the EGCA × Ponytail factorial.

- **Ponytail comparison:** Does another simpler implementation philosophy reproduce, complement, or outperform EGCA's effects?
- **Self-ablation:** How much EGCA is actually necessary even without an external competitor?

The self-ablation should therefore remain independently interpretable.

A strong eventual research program could combine conclusions without conflating them:

1. calibrate whether EGCA has value over ordinary agent behavior;
2. determine the minimum EGCA process preserving that value;
3. test whether Ponytail independently provides the same or different benefit;
4. test longitudinal state/governance separately.

## Next research gates

Before execution:

- [ ] convert this design into a formal preregistration;
- [ ] define exact treatments for A-D;
- [ ] define primary architecture-quality outcome and ordinal anchors;
- [ ] define practical-equivalence / noninferiority margins;
- [ ] define process-cost metrics and weights/reporting rules;
- [ ] decide whether the existing EGCA × Ponytail task corpus can be reused without contamination;
- [ ] determine pilot sample and prospective power/simulation strategy;
- [ ] freeze model/reasoning/runtime/harness;
- [ ] design separate longitudinal preregistration for durable-state mechanisms;
- [ ] ensure null/redundancy/simplification outcomes are explicitly acceptable.

## Governing principle

The self-ablation study should be allowed to produce the conclusion that EGCA itself is overengineered.

If EGCA cannot accept that outcome, the study is not evidence-gated.
