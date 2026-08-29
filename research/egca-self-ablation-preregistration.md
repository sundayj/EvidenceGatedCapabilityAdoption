# EGCA self-ablation and minimum-process study — preregistration

**Protocol version:** 1.0  
**Preregistered:** 2026-08-29  
**Status:** confirmatory design frozen before treatment execution; exact run manifest must be frozen before pilot execution  
**Branch:** `research/egca-self-ablation`  
**Canonical tracker:** issue #21

## 1. Purpose

This study uses Evidence-Gated Capability Adoption (EGCA) to evaluate the necessity of EGCA's own process complexity.

The governing question is:

> **What is the smallest EGCA process that preserves measurable architectural/decision benefit, and which mechanisms fail to justify their incremental process cost?**

The study is not intended to validate the current methodology. It must be capable of concluding that:

1. full EGCA materially outperforms simpler variants and earns its additional ceremony;
2. EGCA-Lite preserves the benefit and full EGCA is unnecessarily heavy for the tested task class;
3. a concise evidence-gating instruction preserves the benefit and even EGCA-Lite is unnecessarily heavy;
4. ordinary agent behavior is practically equivalent to all EGCA variants for the tested task class;
5. different process intensities are justified for different task strata;
6. one or more current EGCA mechanisms are harmful, redundant, or useful only longitudinally;
7. evidence is inconclusive and no methodology change is justified yet.

A null, redundancy, simplification, negative, or inconclusive result is valid.

This protocol is intentionally separate from the EGCA × Ponytail factorial. No Ponytail treatment is active in this study.

## 2. Scope and claims

### 2.1 Phase I — immediate decision process

The confirmatory experiment in this protocol evaluates the incremental value of EGCA process intensity on isolated brownfield coding/architecture tasks.

It can support claims about:

- repository investigation;
- explicit uncertainty/hypothesis framing;
- predeclared evidence gates;
- smallest useful experiments;
- contrary-evidence search;
- explicit adoption decisions;
- immediate decision records;
- immediate process cost.

### 2.2 Out of scope for Phase I

Phase I **cannot** establish the value of:

- long-horizon durable state;
- rediscovery prevention across weeks/sessions;
- structured trackers versus concise durable records;
- stable experiment IDs across a program;
- cumulative integration branches;
- program-level final adoption gates;
- continuity across agents/models/sessions.

Those mechanisms require the separately specified longitudinal Phase II protocol in section 19.

A Phase-I result against full EGCA may justify simplifying **single-task/default activation**, but it must not be rewritten as evidence that longitudinal governance has no value.

## 3. Primary research questions

### RQ1 — minimum sufficient process

Is EGCA-Lite practically equivalent to full EGCA on blinded architectural appropriateness and hard task outcomes while materially reducing process cost?

### RQ2 — concise-gate sufficiency

Is a concise evidence-gating instruction practically equivalent to EGCA-Lite and/or full EGCA while materially reducing process cost?

### RQ3 — value over ordinary agent behavior

Do any EGCA variants materially improve architectural appropriateness over an otherwise identical agent without unacceptable correctness, safety, or robustness harm?

### RQ4 — workload dependence

Does the minimum sufficient process differ across the six preregistered architectural task strata?

### RQ5 — cost frontier

Where is the empirical process-efficiency frontier: the point beyond which additional EGCA machinery adds cost without a practically important quality gain?

## 4. Experimental design

Phase I uses a **four-arm randomized blocked design**. Every confirmatory task is run under every arm unless a cross-study reuse cell satisfies section 17.

| Arm | Name | Process intensity |
| --- | --- | --- |
| A | Control | ordinary agent behavior |
| B | Concise evidence gate | one frozen evidence-gating instruction |
| C | EGCA-Lite | frozen six-step lightweight process |
| D | Full EGCA | actual frozen EGCA skill/methodology |

Task is the primary blocking/repeated factor. All arms receive the same task prompt bytes, repository snapshot, repository instructions, model, reasoning effort, tools, permissions, timeout policy, and deterministic acceptance harness.

The primary comparison is **C versus D**. The study is specifically designed so that full EGCA must demonstrate incremental value over EGCA-Lite, not merely outperform control.

Secondary ordered contrasts are **A→B** and **B→C**. The A→D contrast estimates the total effect of current full EGCA versus ordinary agent behavior.

## 5. Frozen treatments

Treatment text/mechanics may not be rewritten after pilot or confirmatory treatment outputs are observed. Mechanical corrections that do not change treatment meaning require a protocol deviation record and a fresh pilot before confirmatory execution.

### 5.1 Arm A — Control

The agent receives:

- the benchmark task;
- the frozen repository instructions required by that repository;
- normal benchmark harness/system instructions.

It receives no EGCA skill, evidence-gating prompt, Ponytail instruction, KISS/YAGNI/minimalism treatment, prior solution artifact, or treatment-specific durable state.

### 5.2 Arm B — Concise evidence gate

In addition to the same material as Arm A, the agent receives exactly:

> Inspect the existing system first. Do not add architectural complexity unless repository-grounded evidence shows existing capabilities are insufficient. Test the smallest change that can falsify the proposed architecture, and explicitly reject it if the evidence does not justify adoption.

No tracker, decision schema, required hypothesis artifact, branch topology, or EGCA skill is provided.

### 5.3 Arm C — EGCA-Lite

In addition to the same material as Arm A, the agent receives exactly:

> Use this lightweight evidence-gating process when the task contains a meaningful capability or architectural decision. If the task has no such decision, implement it normally and do not manufacture an experiment.
>
> 1. Inspect the existing repository capability and constraints before committing to a design.
> 2. State the architectural decision question or a falsifiable hypothesis.
> 3. State, before implementation, what observable evidence would justify the proposed architectural commitment and what evidence would count against it.
> 4. Make the smallest bounded change or experiment that can answer that question while still satisfying the actual task.
> 5. Based on observed repository/test/runtime evidence, decide Adopt, Adapt, Reject, or Repeat. Do not treat implementation completion as evidence by itself.
> 6. Record the decision and the evidence in one concise durable note. Do not create additional trackers, branch hierarchies, or process artifacts unless the task itself requires them.

Arm C does **not** require:

- explicit candidate-state bookkeeping;
- a separate mandatory contrary-evidence section beyond step 3's evidence-against criterion;
- stable experiment IDs;
- a structured tracker schema;
- a separate execution log;
- an EGCA feature/integration branch;
- experiment/adaptation branch topology;
- a program-level final gate.

### 5.4 Arm D — Full EGCA

Arm D uses the actual `evidence-gated-capability-adoption` skill package, not a paraphrased benchmark prompt.

The initial treatment source is frozen to the EGCA repository state containing:

- source commit: `20718957c333dcde9ddf0dbdb0dd36d7c73c9072`;
- skill path: `skills/evidence-gated-capability-adoption/SKILL.md`;
- skill blob observed at preregistration: `eb142dedb09e7aece5eac6ced05ff54d5b43b08e`.

If the cross-study run manifest freezes a different EGCA commit before **any** pilot treatment output is generated, both studies must freeze the same commit and this protocol must record that administrative manifest substitution before execution. Once pilot treatment output exists, the treatment commit is immutable for the study.

The agent is instructed:

> Use the installed Evidence-Gated Capability Adoption skill according to its own applicability rules. Do not force the full process onto work the skill explicitly says is trivial or already-approved implementation. When it applies, follow the frozen skill without benchmark-specific abridgment.

This intentionally evaluates the real methodology, including its ability to decline unnecessary activation. Process artifacts are not quality outcomes.

## 6. Treatment-intensity interpretation

The arms are ordered by intended process intensity, but Arm D may legitimately decline full activation on a task outside the skill's applicability criteria. That is treated as methodology behavior, not noncompliance.

Treatment activation/fidelity is recorded out of band. A run is not scored better for producing hypotheses, trackers, branches, or decision records; those are only treatment-fidelity/process-cost observations.

## 7. Task sampling frame

The confirmatory corpus uses the existing six-stratum architecture taxonomy:

1. S1 — over-build opportunity;
2. S2 — existing-capability reuse;
3. S3 — irreducible implementation;
4. S4 — reject/defer architecture;
5. S5 — justified new architecture;
6. S6 — ambiguous/evolving brownfield.

The corpus must contain at least **24 confirmatory tasks**, with at least **4 tasks per stratum**, at least **3 repository families**, no more than **25%** of tasks from one repository family, and no more than **50%** from one language/runtime.

At least 25% of tasks must carry a frozen security, robustness, data-integrity, accessibility, performance, concurrency, API-compatibility, or cross-boundary risk axis.

S5 is mandatory so that simplification pressure can be penalized when current evidence genuinely requires new architecture.

### 7.1 Reuse of the EGCA × Ponytail corpus

Reuse is permitted only if all of the following are true before the first self-ablation treatment run:

- the task prompt, baseline SHA, hidden tests, architectural envelope, and stratum are already frozen;
- no self-ablation treatment output was used to select, modify, or reject the task;
- no known EGCA or Ponytail case-study task is promoted from pilot-only status;
- independent classification/independence review requirements are satisfied;
- treatment-specific reference or anti-reference implementations are never exposed to benchmark agents;
- the self-ablation study does not change task membership after seeing another study's outcomes.

A task designed after the self-ablation hypothesis became known may be used for pilot/instrumentation, but not as sole evidence for a confirmatory claim unless an independent review establishes that its contract and envelope do not encode a preferred treatment.

## 8. Pilot and sample-size rule

Use a separate pilot set of at least **8 tasks**. Pilot tasks are excluded from confirmatory estimates.

The pilot is used only to:

- verify treatment isolation and activation;
- validate hidden-test and review instruments;
- estimate within-task stochastic variance;
- estimate token/time cost;
- validate de-identification/blinding;
- run prospective power/equivalence simulations.

### 8.1 Repetitions

The confirmatory repetition count is selected prospectively from pilot variance, with a minimum of **5 independent runs per task × arm cell**.

Simulation must show at least 80% power for both:

1. detecting a true C–D architectural-quality difference of **0.25 points** on the 1–5 primary composite; and
2. establishing C–D equivalence within **±0.25 points** when the true difference is 0.

If this cannot be achieved with at most 20 repetitions per cell, increase the number/diversity of tasks or declare the proposed confirmatory design underpowered before execution. Do not inspect confirmatory outputs and then change sample size.

The repetition count and simulation code are committed before confirmatory execution.

## 9. Runtime isolation and contamination controls

Every trial receives:

- a fresh checkout/worktree at the frozen repository SHA;
- a fresh agent process/context;
- only the treatment assigned to that arm;
- no user-global skills/hooks/memories that implement EGCA, Ponytail, KISS/YAGNI, or another architectural treatment;
- identical tools, permissions, network policy, timeout, and retry rules;
- identical task prompt bytes;
- no artifacts or durable state from another arm/repetition.

A treatment canary verifies which treatment is active without exposing the treatment label to the grader.

Trial order is randomized or balanced within task.

## 10. Run manifest freeze

Before pilot execution, commit a run manifest containing:

- task-manifest commit/SHA;
- task prompt and hidden-test hashes;
- exact EGCA treatment commit/blob;
- exact Arm B and Arm C text hashes;
- agent product/CLI/harness version;
- exact model identifier/snapshot where available;
- reasoning effort/configuration;
- temperature/sampling settings where configurable;
- tools and permissions;
- OS/container/runtime versions;
- dependency lockfiles;
- network policy;
- timeout/retry policy;
- pricing metadata used for cost calculation;
- randomization procedure;
- execution dates/window.

Model or materially relevant harness changes stop the block. Changed configurations are separate replications, not silently pooled.

## 11. Hard outcomes

Every solution is first evaluated on task-appropriate deterministic hard outcomes:

- functional correctness;
- completeness;
- build/type/lint/test health;
- security/safety canaries where relevant;
- robustness/edge cases where relevant;
- data-integrity or compatibility checks where relevant.

A smaller, faster, or more elegant solution that fails required behavior is not an efficiency win.

### 11.1 Hard-outcome noninferiority margin

For overall task success/completeness rate, a simpler treatment is considered noninferior only if the lower bound of the prespecified 95% interval for the success-rate difference is greater than **−5 percentage points** relative to the stronger treatment being simplified.

Critical security/safety/data-loss failures are also reported as veto outcomes. A simpler treatment cannot be declared sufficient if it introduces a treatment-attributable critical failure that is deterministic or reproduced in at least two independent repetitions of the same task and is absent from the stronger comparator's corresponding runs.

Rare-event uncertainty is reported; absence of observed critical failures is not claimed as proof of safety.

## 12. Primary architectural outcome

### 12.1 Blinded architectural appropriateness

At least two human reviewers, blinded to treatment arm, independently score each valid solution on six dimensions:

1. **Requirement fit**;
2. **Repository fit and reuse**;
3. **Architectural proportionality**;
4. **Justified expansion**;
5. **Unjustified commitment**;
6. **Future-change coherence**.

Each dimension uses this frozen 1–5 ordinal anchor framework:

- **1 — materially inappropriate:** consequential mismatch, architectural harm, unjustified commitment, or underbuilding relative to current evidence;
- **2 — materially weak:** notable architectural defect that a competent reviewer would require changing;
- **3 — acceptable:** satisfies the present architectural requirement with no material defect, though improvement is possible;
- **4 — strong:** well-fitted, proportionate, evidence-consistent design with only minor/non-material weaknesses;
- **5 — exceptionally strong:** unusually clear repository/evidence fit with no meaningful architectural weakness visible under the frozen task contract.

Dimension-specific examples/anchors may be added using pilot-only artifacts before confirmatory scoring, but the direction and semantic meaning of the scale may not change.

The primary composite is the **unweighted mean of all six dimension ratings across all blinded reviewers** for that solution.

Raw reviewer ratings are retained. Inter-rater agreement is reported using weighted agreement per ordinal dimension and an intraclass-correlation measure for the composite. Confirmatory scoring does not discard disagreement through post-hoc adjudication.

### 12.2 Architecture-suppression outcome

For S5 tasks, reviewers additionally flag whether the solution avoids/suppresses architectural commitment that current evidence requires. This is a prespecified safety outcome against over-minimalism.

## 13. Practical-equivalence and superiority margins

The minimum practically important difference on the 1–5 architectural composite is frozen at **0.25 points**.

### 13.1 Equivalence

Two arms are considered architecturally equivalent only when the prespecified **90% confidence/credible interval** for their mean difference lies entirely within **−0.25 to +0.25** points, with hard outcomes also satisfying section 11.

Failure to establish superiority is **not** evidence of equivalence.

### 13.2 Material superiority

A stronger process is declared materially superior only when the prespecified 95% interval supports an improvement and the estimated improvement is at least 0.25 points. The analysis report distinguishes statistical evidence from whether the practical threshold is crossed.

If neither equivalence nor material superiority is established, the result is **inconclusive** for that contrast.

## 14. Process cost

Primary process-cost measures are reported separately rather than collapsed into an arbitrary weighted score:

1. total agent tokens (input + reasoning + output; cached tokens reported separately when available);
2. elapsed wall-clock time.

Secondary measures:

- monetary cost from frozen pricing metadata;
- turns;
- tool calls;
- repository reads/searches;
- test/build invocations;
- retries/timeouts;
- artifacts created;
- branch/PR operations;
- human interventions required;
- durable-state records created/updated.

### 14.1 Material process-cost reduction

A simpler arm has a **material process-cost advantage** over a stronger arm when:

- its geometric-mean total tokens **or** elapsed time is at least **20% lower**; and
- the other primary cost measure does not increase by more than **10%**.

If both primary measures fall by at least 20%, report strong cost dominance.

Artifact count, documentation volume, or LOC are not converted into quality points.

## 15. Confirmatory hypotheses and decision rules

### H1 — EGCA-Lite sufficiency (primary)

Arm C is practically equivalent to Arm D on architectural appropriateness and hard outcomes, with a material process-cost advantage.

**If supported:** the additional full-EGCA machinery tested in Phase I fails its gate for mandatory/default use on the tested task class. The evidence supports adapting EGCA toward EGCA-Lite for immediate single-task decisions, while longitudinal mechanisms remain unresolved pending Phase II.

**If D is materially superior to C:** retain the stronger immediate-decision process pending component ablation identifying which additional mechanism causes the gain.

**If neither equivalence nor material superiority is established:** classify C versus D as inconclusive; do not claim simplification from this contrast.

### H2 — concise-gate sufficiency

Arm B is practically equivalent to C and D on architectural appropriateness and hard outcomes and has a material process-cost advantage over both.

**If supported:** even EGCA-Lite has not earned mandatory status for the tested task class; narrow EGCA's immediate value proposition toward a compact evidence-gating discipline plus separately justified longitudinal/governance tooling.

### H3 — EGCA value over ordinary behavior

At least one of B/C/D materially improves architectural appropriateness over A without material hard-outcome degradation.

**If A is equivalent to all EGCA variants:** EGCA's incremental value is unsupported for the tested task class. This does not imply that all longitudinal mechanisms lack value.

### H4 — no architecture-suppression harm

Increasing simplification must not materially increase S5 architecture-suppression or critical correctness/security/robustness failures.

A cheaper arm cannot be declared the minimum sufficient process if its savings arise from omitting currently justified architecture or required behavior.

### H5 — task-stratum dependence

Process intensity may interact with task stratum. Any claim that a particular EGCA intensity should be activated by task type requires a prespecified interaction/stratum pattern plus replication; isolated subgroup wins remain exploratory unless adequately powered.

## 16. Statistical analysis

Use hierarchical/mixed analysis so repeated runs within a task are not treated as independent tasks.

Primary architectural model:

- treatment as a four-level fixed effect;
- task stratum as a fixed effect;
- treatment × stratum interaction reported;
- random intercept for task;
- repository-family random intercept when estimable;
- trial-level residual variation.

Ordinal dimension scores may additionally use ordinal mixed models, but the preregistered primary outcome is the 1–5 mean composite.

Binary hard outcomes use mixed-effects binomial/logistic analysis or task-clustered estimates as appropriate.

Process cost is analyzed on a log scale where distributionally appropriate, with task blocking/random effects.

Report:

- raw task-level distributions;
- arm means/medians as appropriate;
- effect estimates and intervals;
- C–D equivalence result;
- cost ratios;
- hard outcome/failure rates;
- S5 suppression rates;
- stratum breakdowns;
- all protocol deviations.

Analysis code and transformations must be committed and successfully run on synthetic/placeholder data before confirmatory outputs are inspected.

### 16.1 Confirmatory contrast family

Ordered confirmatory contrasts:

1. C vs D — primary equivalence/superiority contrast;
2. B vs C — secondary simplification contrast;
3. A vs B — incremental concise-gate contrast;
4. A vs D — total full-EGCA contrast.

Superiority tests in this family use a frozen Holm correction. The primary C–D equivalence test uses the frozen ±0.25 TOST/interval criterion and is reported separately from superiority multiplicity.

All other pairwise/subgroup findings are exploratory unless separately preregistered.

## 17. Cross-study cell reuse with EGCA × Ponytail

Because this preregistration is frozen before the EGCA × Ponytail confirmatory study is executed, two cells may be shared prospectively to reduce cost:

- self-ablation Arm A ↔ Ponytail-factorial control arm;
- self-ablation Arm D ↔ Ponytail-factorial EGCA-only arm.

Reuse is permitted only when all of the following are **identical**:

- task corpus and task-manifest hashes;
- task prompt bytes;
- repository baseline SHAs;
- hidden tests/acceptance harness;
- system/repository instructions;
- exact model and reasoning configuration;
- agent/harness version;
- tool permissions/network policy;
- timeout/retry policy;
- exact EGCA treatment commit and invocation;
- runtime/dependency environment;
- randomization block definition;
- repetition count or an explicitly prespecified common subset.

If any material item differs, the cell is rerun for self-ablation and is not silently reused.

No cell may be reused based on whether its observed result is favorable. The reuse decision is configuration-based and made before outcome inspection.

This prospective reuse can reduce the marginal self-ablation experiment to the new B and C arms without weakening the blocked comparison, provided the identity requirements hold.

## 18. Failure, retry, and missing-data handling

Primary analysis is intention-to-treat.

Retries are allowed only for predeclared infrastructure/provider failures such as:

- service/API outage outside agent control;
- harness crash unrelated to generated code;
- checkout/container provisioning failure;
- provider transport error before a usable model response;
- corrupted benchmark fixture proven independent of treatment.

The following remain treatment outcomes rather than retry reasons:

- agent timeout caused by its own deliberation/tool loop;
- refusal to complete;
- bad edit;
- test failure;
- excessive process causing the deadline to expire;
- treatment-created branch/state problems;
- incorrect architectural decision.

No run is excluded because it is unusually slow, expensive, large, small, or inconvenient.

## 19. Longitudinal Phase II — separately executed protocol

Phase II is preregistered here at the design level but must receive its own frozen task sequence/run manifest before execution.

### 19.1 Research question

Does EGCA durable/governance state improve later decision quality and reduce rediscovery/repeated mistakes enough to justify its maintenance and workflow cost?

### 19.2 Required sequence structure

Each longitudinal scenario contains multiple temporally separated tasks/sessions in which:

1. an architectural capability initially appears attractive;
2. current evidence is insufficient and it is rejected/deferred;
3. the same or related idea resurfaces later;
4. new evidence changes or sharpens the boundary;
5. a narrow capability eventually becomes justified or remains rejected;
6. prior rationale should affect later work;
7. at least one later step is performed by a fresh agent/session with no conversational memory of prior steps.

### 19.3 Candidate Phase-II arms

At minimum:

- L0 — no durable decision state beyond repository code/history;
- L1 — concise durable Markdown decision record;
- L2 — structured EGCA durable state;
- L3 — structured EGCA state + cumulative integration/final-gate workflow.

### 19.4 Longitudinal outcomes

Measure:

- correct reuse of prior evidence/rationale;
- rediscovery time/tokens/tool calls;
- repeated rejected proposals;
- contradictory later decisions;
- inappropriate persistence of outdated decisions;
- ability to reconsider when new evidence arrives;
- cumulative integration defects/conflicts;
- final architectural appropriateness;
- state-maintenance overhead.

No conclusion about tracker/branch/final-gate necessity is made from Phase I alone.

## 20. Predeclared component-ablation sequence

After Phase I, component ablations are **new confirmatory studies**, not post-hoc rescoring of Phase-I data.

The default investigation order is:

1. predeclared evidence criteria;
2. formal hypothesis wording versus concise decision question;
3. explicit contrary-evidence search;
4. Adopt/Adapt/Reject/Repeat vocabulary versus reduced decision representation;
5. decision-record detail;
6. structured tracker versus concise durable note (Phase II);
7. experiment branch topology (Phase II);
8. cumulative integration branch and program final gate (Phase II).

If Phase I shows D materially superior to C, first run **bridging ablations** that add D-only mechanisms to C in the above order until the incremental benefit is localized. If C matches D, run **removal ablations** from C in the above order to locate the minimum sufficient core.

Changing this order because an observed Phase-I result makes another component look more promising requires a new preregistration and is exploratory until replicated.

## 21. Anti-bias and interpretation rules

1. Current inclusion in EGCA is not evidence that a mechanism is necessary.
2. Process compliance is never a quality outcome.
3. More documentation cannot compensate for worse code/architecture.
4. Less code cannot compensate for correctness, security, robustness, or justified-architecture failure.
5. Failure to prove superiority is not equivalence.
6. Failure to prove equivalence is not superiority.
7. An inconclusive result remains inconclusive; do not rewrite it as support for the preferred methodology.
8. If a simpler treatment is equivalent and materially cheaper, accept redundancy as evidence.
9. If removing process improves quality or safety, treat that as evidence against the removed mechanism's mandatory status.
10. Do not modify tasks, margins, reviewer anchors, exclusions, or treatment text after seeing confirmatory outcomes.
11. Do not infer longitudinal value or lack of value from isolated tickets.
12. Any methodology change motivated by confirmatory results must state exactly which claim the data supports and which claims remain unresolved.

## 22. Methodology decision gate

After confirmatory analysis, apply this evidence gate to EGCA itself:

### Adopt current full immediate process

Supported only if D demonstrates a practically important architectural/hard-outcome advantage over C sufficient to justify its additional process cost.

### Adapt toward EGCA-Lite

Supported if C is architecturally/hard-outcome equivalent to D and materially cheaper.

### Adapt toward concise evidence gate

Supported if B is equivalent to C/D on quality/hard outcomes and materially cheaper.

### Reject mandatory EGCA for the tested task class

Supported if A is equivalent to the EGCA variants on quality/hard outcomes and no EGCA arm demonstrates a practically important benefit.

### Repeat

Required when the key contrast is inconclusive, underpowered, contaminated, or materially model/task-dependent without sufficient replication.

These decisions apply only to the scope supported by the data. Phase-II mechanisms remain candidate capabilities until longitudinal evidence crosses their own gate.

## 23. Freeze and deviation policy

After the first pilot treatment output:

- A/B/C/D treatment meaning is immutable;
- practical-equivalence and cost margins are immutable;
- primary/secondary outcomes are immutable;
- reviewer scale direction and primary composite are immutable.

After the first confirmatory treatment output:

- corpus membership is immutable;
- prompts/tests/envelopes are immutable;
- repetition count is immutable;
- analysis code version is immutable except for documented bug fixes that do not depend on outcome direction.

Every deviation is recorded with timestamp, reason, affected runs, and whether those runs remain confirmatory.

## 24. Governing falsification principle

The strongest result this study can produce is not necessarily evidence that EGCA should remain as written.

If a smaller process preserves the benefit at lower cost, the evidence-gated decision is to simplify.

If ordinary agent behavior preserves the benefit, the evidence-gated decision is to narrow or reject mandatory EGCA for that task class.

If full EGCA earns its additional machinery, retain it because the evidence supports it—not because the methodology authored the experiment.
