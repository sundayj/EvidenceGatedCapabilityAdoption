# EGCA × Ponytail benchmark task taxonomy and curation contract

**Protocol relationship:** subordinate to `research/egca-ponytail-benchmark-preregistration.md`  
**Status:** pre-confirmatory design artifact  
**Canonical tracker:** issue #9  
**Taxonomy review:** issue #11

## Purpose

This document turns the preregistered task strata into an operational curation contract. It exists to reduce task-selection freedom before any confirmatory treatment output is produced.

The corpus must be able to punish both architectural excess and architectural insufficiency. No task is admitted merely because it appears to favor EGCA, Ponytail, minimalism, experimentation, or any other preferred result.

## Core authoring rule

Use the following rule for every user-visible task prompt:

> **Pin the behavioral contract; under-specify the solution.**

The prompt should sound like an ordinary brownfield request. It may state the goal and concrete behaviors a user would naturally care about, but it must not prescribe implementation structure unless that structure is itself part of the user requirement.

Do not use treatment-leaking adjectives such as `simple`, `minimal`, `lightweight`, `robust`, `production-grade`, `extensible`, `future-proof`, `clean architecture`, or `YAGNI` unless the original real-world requirement genuinely contains that constraint and the reason is documented.

The task prompt is byte-identical across all four arms.

## Primary strata

Every confirmatory task has exactly one primary stratum. Strata encode the architectural decision shape, not the technology or risk domain.

### S1 — Over-build opportunity

**Question tested:** Can the agent satisfy the requirement without inventing unnecessary implementation surface?

Admission characteristics:
- a native/platform/standard-library/current-dependency capability can satisfy most or all of the requirement; or
- a narrowly scoped implementation is sufficient and a larger subsystem is a common but unnecessary response.

A valid solution may still add code. The stratum is not a code-golf test.

Primary failure modes:
- bespoke replacement for an adequate native capability;
- unnecessary dependency;
- speculative configuration or extension points;
- additional layers unrelated to the demonstrated requirement.

### S2 — Existing-capability reuse

**Question tested:** Does the agent discover and correctly reuse or extend an existing repository primitive rather than duplicating it?

Admission characteristics:
- the relevant capability exists in the frozen baseline;
- finding it requires non-trivial repository inspection;
- blindly implementing the ticket locally would create duplication or inconsistent behavior.

Primary failure modes:
- duplicate helper/service/model/policy;
- bypass of an existing abstraction or responsibility boundary;
- incompatible second implementation of an established pattern.

### S3 — Irreducible implementation

**Question tested:** Do treatments converge when meaningful new implementation is plainly required and there is little architectural uncertainty?

Admission characteristics:
- no adequate existing/native solution exists;
- required behavior is concrete;
- implementation size cannot plausibly collapse merely through reuse or rejection.

Primary failure modes:
- artificial refusal or excessive deliberation;
- incomplete behavior in pursuit of smallness;
- needless architecture added to straightforward work.

This stratum is an important negative control: a treatment that claims large savings everywhere is suspicious.

### S4 — Reject/defer architecture

**Question tested:** Can the agent avoid committing an abstraction, dependency, subsystem, model, service, or integration whose benefit is unsupported by current evidence?

Admission characteristics:
- the task context makes a larger architectural move plausible;
- frozen repository evidence shows the proposed commitment is unnecessary, premature, or belongs elsewhere;
- the user-visible task remains satisfiable without the proposed commitment.

Primary failure modes:
- architecture added because it sounds reusable rather than because current evidence requires it;
- responsibility moved into the wrong layer/repository;
- speculative generalization around a single case.

### S5 — Justified new architecture

**Question tested:** Can the agent introduce enough architecture when the evidence actually warrants it?

Admission characteristics:
- existing primitives are demonstrably inadequate;
- repeated or cross-cutting behavior creates a real shared responsibility;
- the architectural commitment has observable benefits or correctness requirements that cannot be met cleanly through isolated local edits.

Examples of eligible commitment types include a shared abstraction, middleware/service, dependency, persistence model, interface, schema change, or responsibility boundary.

Primary failure modes:
- duplicated local patches when a shared responsibility is required;
- refusal to introduce a dependency or abstraction despite evidence;
- incomplete implementation caused by over-applied YAGNI/minimalism;
- moving complexity into callers instead of owning it centrally.

This stratum is mandatory and may not be weakened after results are observed.

### S6 — Ambiguous/evolving brownfield change

**Question tested:** Does repository investigation materially change the initially obvious interpretation of the request?

Admission characteristics:
- relevant evidence is distributed across multiple files/modules/tests or repositories;
- at least two plausible initial interpretations exist;
- one interpretation is weakened or redirected by frozen repository evidence.

Primary failure modes:
- solving the textual ticket while missing repository reality;
- choosing the wrong responsibility boundary;
- over-refactoring before understanding the actual flow;
- under-scoping behavior because the first code location inspected was misleading.

## Cross-cutting risk axes

These are tags, not strata. A task may carry zero or more.

- `security`: trust boundaries, authorization, injection, traversal, secrets, or equivalent exploit risk;
- `robustness`: malformed/boundary inputs and non-happy-path behavior;
- `data-integrity`: persistence invariants, idempotency, duplicate prevention, migrations, reconciliation;
- `accessibility`: keyboard, semantic, screen-reader, contrast, or equivalent required behavior;
- `performance`: evidence-backed latency, complexity, allocation, I/O, or scalability constraints;
- `concurrency`: races, locking, idempotency, ordering, retries, distributed coordination;
- `api-compatibility`: backwards compatibility, versioning, public contracts;
- `cross-boundary`: responsibility spans packages/services/repos/layers;
- `dependency-choice`: adding, avoiding, or replacing a third-party dependency is materially at issue.

Risk tags must never be used to infer that more or less code is preferable.

## Provenance classes

Every task records one provenance class:

1. `historical-real`: reconstructed from a public issue/PR at a frozen pre-solution commit;
2. `derived-real`: a newly authored task against a frozen public repository, not copied from a known solution;
3. `synthetic-brownfield`: a deliberately constructed repository fixture with realistic history and competing architectural options;
4. `benchmark-derived`: adapted from an existing benchmark task.

`benchmark-derived` and treatment-authored tasks are presumed **pilot-only** unless the independence review gives a written reason otherwise.

## Architectural envelope

Before treatment outputs exist, every admitted task receives an architectural envelope. It defines a set of acceptable solutions rather than a single gold implementation.

The envelope contains:

### Required properties
Behavioral or architectural properties that any competent solution must provide.

### Acceptable commitments
Architectural elements that are allowed when justified, including multiple alternative designs where appropriate.

### Unjustified commitments
Specific commitments that frozen repository/task evidence does not support. This list must be reasoned from the baseline, not from later treatment output.

### Under-build signals
What would indicate that a solution suppressed architecture or required behavior to stay small.

### Over-build signals
What would indicate unnecessary architecture, duplication, configurability, dependency, or indirection.

### Responsibility boundary
The module/layer/service/repository that owns the behavior, when the baseline makes that boundary materially knowable.

The envelope is reviewer input, not an implementation prescription. Reviewers may accept an unlisted alternative if it satisfies the required properties and does not violate a justified boundary; such departures are recorded.

## Hidden-test contract

Hidden tests must derive from the user-visible goal and frozen repository invariants, not from the reference implementation.

Each task has at least:
- `CORE`: directly required behavior;
- `REGRESSION`: frozen existing behavior that must remain intact;
- optional risk-axis tiers such as `SECURITY`, `ROBUSTNESS`, `DATA_INTEGRITY`, or `ACCESSIBILITY`.

Tests should prefer black-box or public-interface behavior. Internal shape may be inspected only when the architecture itself is the measured construct and the inspection rule was frozen before outputs existed.

## Reference and anti-reference controls

Every confirmatory task must have:

- at least one `reference` solution that passes all required deterministic checks and falls inside the architectural envelope;
- at least one `anti-reference` solution representing the task's intended failure mode.

The anti-reference must be plausible rather than absurd. Depending on stratum it may be:
- correct but unnecessarily overbuilt;
- correct happy-path behavior that under-builds required robustness/security;
- duplicated local implementation that ignores an existing primitive;
- minimal patch that fails a justified shared-architecture requirement;
- broad abstraction that solves the task but violates the responsibility/evidence boundary.

For S5 justified-new-architecture tasks, at least one anti-reference must specifically represent **underbuilding**.

## Curation gate

A task may move from `screening` to `pilot` or `confirmatory-candidate` only if all applicable gates pass:

1. baseline SHA and build/test instructions are frozen and reproducible;
2. prompt contains no treatment cue and is byte-stable;
3. stratum is assigned before treatment output;
4. provenance and exposure risks are recorded;
5. architectural envelope is written before treatment output;
6. reference passes all CORE/REGRESSION and applicable risk checks;
7. anti-reference passes enough CORE behavior to be plausible while failing its declared architectural/risk axis;
8. two independently produced competent solutions can satisfy CORE without being forced into one internal design;
9. hidden tests do not require the reference implementation's names/layout unless explicitly part of the task contract;
10. task runtime is deterministic enough for repeated trials;
11. task has sufficient architectural headroom for its stratum;
12. independence review approves treatment-exposure and public-solution leakage risk;
13. prompt hash, baseline SHA, fixture SHA, test SHA, envelope SHA, and manifest SHA are frozen before confirmatory execution.

Failure at any gate is recorded in the candidate ledger; the candidate is not deleted.

## Corpus balancing constraints

For the confirmatory corpus:

- minimum 24 tasks;
- minimum 4 tasks in each S1-S6 stratum;
- no single repository may contribute more than 25% of confirmatory tasks without a preregistered amendment justified before outputs;
- no single language/runtime may contribute more than 50% of confirmatory tasks;
- at least 3 distinct repository families/projects;
- at least 25% of tasks carry a cross-cutting risk axis;
- at least 4 S5 tasks must have a deterministic or strongly constrained under-build detector;
- benchmark-derived or prior EGCA/Ponytail case-study tasks are excluded from confirmatory analysis by default and are preferred for pilot/calibration.

## Exposure and leakage ratings

Each candidate receives three independent ordinal ratings: `low`, `medium`, `high`.

- **treatment exposure:** was this task or close variant used to develop/evaluate EGCA or Ponytail?
- **author familiarity:** has the EGCA researcher already implemented or deeply analyzed this exact task?
- **public solution leakage:** is an exact historical solution highly visible and likely to be memorized by the model?

Any `high` treatment exposure makes a task pilot-only. A `high` author-familiarity or public-solution-leakage rating requires an explicit independence-review disposition before confirmatory admission.

## Freeze rule

After the first confirmatory run begins, task prompts, strata, architectural envelopes, hidden tests, acceptance thresholds, exclusions, and corpus membership are immutable for the confirmatory analysis. Any discovered defect creates a protocol deviation and, if necessary, a separate replication corpus; it does not permit silent repair of an inconvenient task.