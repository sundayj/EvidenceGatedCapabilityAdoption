# EGCA × Ponytail benchmark preregistration

**Protocol version:** 1.0  
**Preregistered:** 2026-08-25  
**Status:** Confirmatory protocol frozen before benchmark execution  
**Branch:** `research/ponytail-related-work`

## 1. Purpose

This benchmark is designed to test, rather than assume, the empirical relationship between Evidence-Gated Capability Adoption (EGCA) and Ponytail.

The benchmark must be capable of producing any of these conclusions:

1. EGCA provides a meaningful benefit over an otherwise identical coding agent.
2. Ponytail provides a meaningful benefit over an otherwise identical coding agent.
3. EGCA and Ponytail are complementary and their combination produces a positive interaction.
4. EGCA and Ponytail are substantially redundant.
5. Combining EGCA and Ponytail produces a negative interaction, including excessive conservatism or suppression of justified architecture.
6. EGCA does not outperform a simpler workflow enough to justify its additional process cost.
7. Results are task-, model-, or workload-dependent and do not justify a general superiority claim.

The experiment is not intended to validate EGCA. A null, negative, or redundancy result is a valid outcome.

## 2. Primary research questions

### RQ1 — EGCA main effect

Does adding EGCA improve architectural decision quality across brownfield coding tasks where the correct decision may be reuse, bounded new implementation, rejection of a proposed capability, or introduction of genuinely justified architecture?

### RQ2 — Ponytail main effect

Does adding Ponytail reduce unnecessary implementation surface without materially reducing correctness, robustness, safety, or justified architectural expansion?

### RQ3 — EGCA × Ponytail interaction

Does combining EGCA and Ponytail outperform the expected additive behavior of either intervention alone, or do the interventions interact redundantly or negatively?

### RQ4 — process cost

What additional or reduced agent process cost does each treatment produce in tokens, tool calls, elapsed time, and monetary cost?

## 3. Experimental design

The confirmatory experiment is a **2 × 2 factorial randomized blocked design**.

| Arm | EGCA | Ponytail |
| --- | --- | --- |
| A — control | off | off |
| B — Ponytail | off | on |
| C — EGCA | on | off |
| D — EGCA + Ponytail | on | on |

The same task, repository snapshot, agent harness, model, reasoning configuration, tool permissions, timeout policy, and acceptance harness are used across all four arms.

The factorial analysis estimates:

- EGCA main effect;
- Ponytail main effect;
- EGCA × Ponytail interaction.

The interaction term is the formal test of the complementarity hypothesis.

## 4. Treatments

### 4.1 Control

The coding agent receives only the benchmark task, repository instructions required by the target repository, and normal harness/system instructions. It receives no EGCA or Ponytail material.

### 4.2 Ponytail

Ponytail is installed and activated using the project's actual supported integration mechanism, not pasted approximately into the task prompt. The exact Ponytail commit, plugin version, activation mode, and intensity level are frozen in the run manifest.

The default confirmatory Ponytail level is **Full**, because it is the project's normal shipped default. Other levels may be studied later as exploratory or replication work but are not mixed into this factorial experiment.

### 4.3 EGCA

EGCA is installed and invoked using its actual skill package from the frozen EGCA commit. The arm must follow the normal methodology rather than a benchmark-specific abridgment designed to improve scores.

For a single benchmark task, the minimum required EGCA behavior is:

1. inspect the current repository/system baseline;
2. keep the proposed architectural/capability change in candidate state until investigated;
3. state a falsifiable hypothesis when meaningful architectural uncertainty exists;
4. identify supporting and contrary evidence before implementation;
5. choose the smallest experiment or implementation capable of answering the architectural question;
6. collect repository-grounded evidence;
7. make an explicit Adopt / Adapt / Reject / Repeat decision when the task contains an adoption decision;
8. preserve a concise machine-readable decision artifact for scoring process fidelity.

The benchmark must not reward the EGCA arm merely for producing that artifact.

### 4.4 EGCA + Ponytail

Both frozen treatments are active simultaneously. Neither treatment is rewritten to make it more compatible with the other after results are observed.

If the treatments conflict in practice, that conflict is an experimental result rather than a reason to silently modify the treatment.

## 5. Task sampling frame

Task selection is a major threat to validity. The confirmatory task set is frozen before any confirmatory runs.

Tasks must be brownfield repository changes with enough context for repository investigation to matter. Toy one-function generation tasks may be used only for instrumentation calibration and are excluded from the primary architectural analysis.

### 5.1 Required task strata

The confirmatory set contains at least **24 tasks**, with at least four tasks in each of six preregistered strata:

1. **Over-build opportunity** — the requirement can be satisfied safely using an existing/native/simple capability and commonly tempts unnecessary custom implementation.
2. **Existing-capability reuse** — the repository already contains an appropriate helper, service, pattern, or subsystem that should normally be reused or extended.
3. **Irreducible implementation** — meaningful new code is required and there is little architectural ambiguity; treatments should not manufacture artificial savings.
4. **Reject/defer architecture** — a proposed abstraction, dependency, service, model, or subsystem is not justified by the repository/task evidence.
5. **Justified new architecture** — existing primitives are demonstrably inadequate and a new abstraction, dependency, shared service, model, interface, or other architectural commitment is the appropriate solution.
6. **Ambiguous/evolving brownfield change** — evidence must be gathered from multiple repository locations and the initially obvious architectural interpretation is incomplete or misleading.

The **justified-new-architecture stratum is mandatory**. A benchmark dominated by simplification opportunities would encode the desired conclusion into the task distribution and is invalid for EGCA.

### 5.2 Task sourcing

Tasks are sourced or adapted from public repositories, public issue/PR histories, benchmark repositories, or synthetic brownfield fixtures constructed before treatment outputs are seen.

For each candidate task, the research ledger records:

- source and repository SHA;
- stratum;
- why the task belongs in that stratum;
- expected evidence an engineer would need to inspect;
- deterministic acceptance criteria where possible;
- known valid architectural alternatives;
- rejection reason if the candidate is excluded.

All materially evaluated task candidates remain in the ledger, including rejected candidates.

### 5.3 Independent task classification

Before confirmatory runs, at least two reviewers classify each task's stratum from the task specification and repository baseline without seeing any treatment output. Disagreements are resolved and recorded before execution.

The classification is not changed after treatment outputs are observed.

## 6. Pilot and sample-size rule

A separate **pilot set of at least 8 tasks** is used to validate the harness and estimate run-to-run variance. Pilot tasks can resemble confirmatory tasks but may not appear in the confirmatory dataset.

The pilot is used only to:

- verify treatment isolation;
- validate scoring instruments;
- estimate within-task stochastic variance;
- estimate runtime/cost;
- perform prospective power simulation for the confirmatory repetition count.

Pilot treatment effects are not reported as confirmatory evidence.

### 6.1 Repetition count

The number of repetitions per task × arm cell is not chosen from convenience alone.

After the pilot, the analysis code performs a prospective simulation using the observed within-task variance. The smallest repetition count that provides at least **80% power** for the preregistered minimum practically important effect on the primary architectural outcome is chosen, subject to a minimum of **5 independent runs per cell**.

The chosen repetition count, simulation code, assumptions, and result are committed before confirmatory execution begins. The repetition count is then frozen and identical across arms except for clearly recorded infrastructure failures.

No confirmatory result may be inspected before the repetition count is frozen.

## 7. Runtime isolation and contamination controls

Every trial receives:

- a fresh checkout/worktree at the exact frozen repository SHA;
- a fresh agent process and conversation/context;
- only the treatment(s) assigned to that arm;
- no user-global skills, hooks, memories, or repository modifications not explicitly part of the treatment;
- identical tool permissions;
- identical network policy;
- identical timeout and retry policy;
- identical task prompt bytes;
- identical repository-level instructions;
- no artifacts from previous arms or repetitions.

Treatment activation is verified out of band and recorded in the trial manifest.

A baseline contaminated by Ponytail, EGCA, prior solution artifacts, global instructions, or another arm's durable state invalidates that trial.

Trials are executed in randomized or balanced order within each task so time-of-day or transient provider effects are not confounded with treatment arm.

## 8. Frozen model and harness state

The confirmatory run manifest records and freezes:

- repository and task-fixture SHAs;
- EGCA commit SHA;
- Ponytail commit SHA/version;
- agent product and CLI/harness version;
- exact model identifier or snapshot where available;
- reasoning effort/configuration;
- temperature/sampling settings where configurable;
- system/project instructions;
- tool set and permissions;
- runtime/container/OS details;
- dependency lockfiles;
- timeout and retry policy;
- benchmark code SHA;
- execution dates.

A model/version change during the confirmatory run stops the block. Results from materially different model versions are analyzed as separate replications, not pooled silently.

## 9. Outcomes

No single metric is treated as architectural quality.

### 9.1 Hard gates

Every solution is first evaluated on task-appropriate hard outcomes:

- functional correctness;
- task completeness;
- security/safety canaries where relevant;
- robustness/edge-case checks where relevant;
- build/type/lint/test health where relevant.

A smaller or architecturally elegant solution that fails the task does not receive a quality win.

### 9.2 Primary architectural outcome: blinded architectural appropriateness

Architectural appropriateness is scored by **at least two blinded human reviewers** who do not know the generating arm.

Reviewers receive:

- the frozen task specification;
- relevant repository baseline/context;
- the produced diff/artifact;
- deterministic test/acceptance results.

Treatment-specific artifacts, names, comments, and metadata are removed when practical before review.

The published rubric scores these dimensions independently:

1. **Requirement fit** — does the solution satisfy the actual requirement rather than a broader or narrower imagined problem?
2. **Repository fit and reuse** — does it correctly use existing capabilities and conventions where appropriate?
3. **Architectural proportionality** — is the amount and scope of architectural commitment proportionate to demonstrated need?
4. **Justified expansion** — when new architecture is required, did the solution introduce enough structure to solve the demonstrated problem rather than suppressing it for the sake of minimalism?
5. **Unjustified commitment** — does it add abstractions, dependencies, public APIs, state, configuration, layers, or subsystems whose necessity is unsupported?
6. **Future-change coherence** — does the resulting design leave a plausible next change easier to make without speculative scaffolding for unknown futures?

Each dimension uses a symmetric ordinal scale with explicit anchors. The rubric is finalized and validated on held-out examples before confirmatory scoring.

Inter-rater agreement is reported. Disagreement is not silently resolved into a preferred answer; both raw ratings and the prespecified aggregation are retained.

### 9.3 Architecture-suppression outcome

For tasks in the **justified-new-architecture** stratum, reviewers separately score whether the solution under-builds or avoids an architectural commitment that the evidence actually requires.

This outcome prevents a minimalism-biased treatment from winning merely by adding less architecture.

### 9.4 Unnecessary architectural surface

Deterministic/supporting measurements include, where meaningful:

- production source statements/LOC;
- files added/modified;
- new dependencies;
- new classes/interfaces/services/models/modules;
- public API/configuration surface;
- schema/migration additions;
- duplicated vs reused primitives;
- indirection/delegation layers;
- test surface separately from production surface.

These are descriptive proxies. Lower values are not automatically better.

### 9.5 Process cost

Record per trial when available:

- input, cached, reasoning, and output tokens;
- monetary cost using frozen pricing metadata;
- elapsed wall-clock time;
- agent turns;
- tool calls;
- repository reads/searches;
- test/build invocations;
- retries/timeouts.

Artifact efficiency and process efficiency are reported separately.

### 9.6 Decision/process quality

For EGCA arms only, process fidelity is measured descriptively:

- baseline inspected before commitment;
- hypothesis is falsifiable when required;
- contrary evidence is stated;
- acceptance/rejection criteria exist before implementation;
- decision corresponds to observed evidence;
- negative or ambiguous evidence is retained.

These fidelity measures verify that EGCA actually activated. They are **not** used as primary evidence that EGCA is better.

## 10. Failure and missing-data handling

Treatment-induced failure must not create artificial efficiency wins.

Primary analysis is **intention-to-treat**: every valid launched trial remains assigned to its arm.

A solution that fails correctness/completeness cannot be treated as a successful reduction in architectural surface. Failure rates are reported as outcomes.

Infrastructure failures are distinguished from model/treatment failures using predeclared categories. A retry is allowed only for documented infrastructure/provider failure under the same frozen configuration. Model errors, bad edits, timeouts caused by the agent's behavior, or refusal to complete the task remain treatment outcomes unless the same predefined infrastructure criterion applies.

No trial is excluded because its result is inconvenient or unusually large/small.

## 11. Randomization and blinding

- Trial execution order is randomized or balanced within task.
- Human architectural reviewers are blinded to arm and trial identifiers.
- Pairwise presentation order, when pairwise comparisons are used, is randomized.
- Reviewers do not participate in treatment execution for the solutions they score when avoidable.
- Task authors/classifiers do not see confirmatory treatment outputs before the task manifest is frozen.

## 12. Confirmatory hypotheses

### H1 — EGCA architectural decision quality

Across the confirmatory task set, the EGCA main effect improves blinded architectural appropriateness relative to no EGCA, while not materially reducing the hard correctness/completeness outcomes.

**Falsified/unsupported if:** the EGCA main effect is negligible, negative, or accompanied by meaningful correctness/completeness degradation.

### H2 — Ponytail implementation restraint

Across tasks with reducible implementation surface, Ponytail reduces unnecessary architectural/implementation surface relative to no Ponytail without a material reduction in correctness, safety, robustness, or justified architectural expansion.

**Falsified/unsupported if:** reductions primarily come from omitted required behavior, robustness, safety, or justified architecture, or if the effect does not distinguish itself from baseline variance.

### H3 — Complementarity / interaction

The EGCA × Ponytail interaction is positive on architectural appropriateness and/or unnecessary-surface reduction **without** a corresponding increase in architecture suppression or hard-outcome failures.

**Supported only if:** the interaction term and stratum-level pattern show that the combined arm provides benefit beyond the expected main effects without shifting failures into the justified-new-architecture stratum.

**Redundancy result:** the combined arm is practically indistinguishable from the stronger single-treatment arm and the interaction is approximately zero.

**Negative-interaction result:** the combined arm performs worse than expected from the main effects, including excessive investigation/process cost, incomplete implementation, or suppression of justified architecture.

### H4 — EGCA process overhead

EGCA may impose additional process cost. Cost is reported as a tradeoff, not assumed to be a failure. A claimed efficiency benefit requires measured evidence and may not be inferred from smaller diffs.

## 13. Statistical analysis

The primary analysis treats task as a repeated/blocking factor rather than treating all runs as independent observations.

For continuous/approximately continuous outcomes, use a hierarchical mixed-effects model with:

- fixed effect: EGCA on/off;
- fixed effect: Ponytail on/off;
- fixed interaction: EGCA × Ponytail;
- prespecified task-stratum effects;
- random intercept for task;
- trial-level residual variation.

Ordinal reviewer outcomes use an ordinal mixed model where practical; a prespecified robust alternative is used if model diagnostics fail.

Binary hard outcomes use mixed-effects logistic/binomial analysis or task-clustered estimates as appropriate.

Report:

- effect estimates;
- uncertainty intervals;
- raw task-level distributions;
- interaction estimate;
- task-stratum breakdowns;
- correctness/failure rates beside any size reduction;
- practical effect sizes, not only p-values.

The analysis code and transformations are committed and run on synthetic/placeholder data before confirmatory outputs are inspected.

## 14. Multiplicity and interpretation

The confirmatory family is limited to the preregistered main effects/interactions and hard non-harm outcomes. Multiple-comparison correction is applied to the declared confirmatory family using a frozen procedure chosen before confirmatory execution.

All additional task-, language-, repository-, model-, metric-, or subgroup findings are labeled exploratory.

A favorable exploratory result may motivate replication but may not be rewritten as a preregistered hypothesis.

## 15. Evaluator-bias protections

Architectural quality is especially vulnerable to encoding the methodology into the rubric.

Therefore:

- reviewers score appropriateness to task/repository evidence, not compliance with EGCA or Ponytail vocabulary;
- "less code", "reuse", "more abstraction", and "new architecture" are not intrinsically positive or negative rubric answers;
- the justified-new-architecture stratum must contain cases where a solution that refuses architecture scores worse;
- the reject/defer stratum must contain cases where speculative architecture scores worse;
- deterministic task outcomes remain visible to reviewers;
- reviewer agreement and arm guesses are measured where practical;
- any LLM judge is secondary/exploratory and cannot be the sole primary architectural evaluator.

## 16. Prompt contamination and learning/carryover

No conversational context, tracker state, generated solution, reviewer feedback, or prior-arm artifact is reused across confirmatory trials.

If the agent product includes memory or global customization, those features are disabled or the run environment uses an isolated benchmark identity/profile.

The same benchmark operator may run multiple cells, but the agent process itself receives no carryover.

## 17. Model/version drift

All cells for a confirmatory block must run under one frozen model/version/configuration. Provider-side unannounced drift is recorded when detectable.

If the provider materially changes the model during collection, stop rather than mixing versions. Restart as a separately labeled replication block if necessary.

The primary benchmark initially targets one model to preserve internal validity. Cross-model generalization requires later replication and is not inferred from the first block.

## 18. Separate EGCA ablation study

The four-arm factorial answers whether the full EGCA treatment has an effect relative to control and Ponytail. It does **not** determine whether EGCA's full process is necessary.

A separate preregistered ablation should therefore compare:

1. agent alone;
2. agent + a concise evidence-gating instruction;
3. agent + full EGCA.

That study must remain separate from the factorial confirmatory family. If a short instruction matches full EGCA on bounded tasks, the result narrows EGCA's plausible value proposition toward longitudinal state, governance, and cumulative decision history rather than single-task architectural judgment.

## 19. Longitudinal follow-up

A single-task benchmark cannot fully test EGCA's durable-state claim.

A later preregistered longitudinal benchmark should use sequential related tasks in which:

- early evidence suggests an abstraction;
- later evidence weakens or changes it;
- a previously rejected architecture can reappear;
- a narrow abstraction may eventually become justified;
- prior decision rationale materially affects later work.

This follow-up tests whether durable hypotheses, negative evidence, dependencies, and decision history improve cumulative architecture across sessions.

It is not part of the primary four-arm confirmatory experiment.

## 20. Freeze rules

Before confirmatory execution, the following are committed and tagged as the frozen preregistration package:

- this protocol;
- task manifest and all rejected-candidate ledger entries;
- repository/task SHAs;
- exact treatment versions;
- model/reasoning/harness configuration;
- scoring rubric;
- deterministic acceptance/safety/robustness harnesses;
- randomization seed-generation procedure;
- pilot-derived repetition count and power simulation;
- statistical analysis code;
- exclusion/retry rules.

After the freeze tag, substantive changes require:

1. a new protocol version;
2. a durable amendment explaining why the change was necessary;
3. a declaration of whether any outcome data had been inspected;
4. affected results to be labeled exploratory unless the confirmatory experiment is restarted cleanly.

Typos and documentation clarifications that cannot change analysis or interpretation may be corrected with a logged non-substantive amendment.

## 21. Reporting commitments

The final report will publish or preserve, subject to repository/license/privacy constraints:

- protocol and amendments;
- complete task ledger, including rejected task candidates;
- frozen manifests and SHAs;
- trial-level metrics;
- failure/exclusion log;
- analysis code;
- aggregate and task-level results;
- inter-rater agreement;
- null and negative findings;
- evidence of treatment contamination or instrumentation failures;
- conclusions that distinguish observation from interpretation.

The report will not describe EGCA and Ponytail as complementary, redundant, or superior to one another unless the observed evidence supports that characterization.
