---
name: evidence-gated-capability-adoption
description: Evaluate and productionize substantial software capabilities, architectural patterns, dependencies, integrations, or design ideas using source investigation, falsifiable hypotheses, bounded experiments, explicit evidence gates, durable decision records, cumulative integration isolation, and lightweight execution telemetry. Use for non-trivial capability adoption and for materially different production implementations derived from adopted prototypes or experiments; do not use for trivial fixes or implementation already proven within the same artifact, environment, data, and integration boundary.
---

# Evidence-Gated Capability Adoption

Use this skill when evaluating whether a substantial capability, architectural pattern, dependency, integration, or design idea should be adopted into an existing software system, and when carrying accepted experimental evidence into a materially different production implementation.

Do **not** repeat discovery for trivial fixes, obvious dependency bumps, or implementation already proven within the same evidence boundary. Continue using the productionization and final-gate controls when admitted implementation introduces material variables that the experiment did not test.

## Objective

Turn promising ideas into evidence-backed architectural decisions without allowing research findings, agent suggestions, or source-project features to silently become implementation commitments.

## Autonomous-governance invariant

EGCA is actor-neutral. Humans, agents, services, and hybrid teams may all investigate, propose, execute, validate, recommend, amend, integrate, release, and observe outcomes. A role label must not suppress reasoning or make an assertion authoritative.

Use **open capability, gated commitment**:

- any authorized actor may propose the next lifecycle action;
- an authoritative state transition occurs only when a versioned evidence gate admits the exact action for the exact object revision;
- self-validation is useful evidence with provenance, but it does not satisfy an independent-evidence requirement by itself;
- independence is established by evidence provenance and materially distinct failure domains, not by counting agents or votes;
- missing derived evidence or authority produces Adapt or Repeat; contrary evidence produces Reject; an authority enforced by an unavailable external system is recorded as `ExternalBlock`, not converted into a synthetic request for human approval;
- a human is required only when an external policy or system actually reserves authority to one, not merely because EGCA traditionally placed a person between two agent steps.

For consequential or autonomous work, derive a versioned **transition mandate** from authoritative sources. Preserve at least the objective, governing methodology and policy versions, object and criteria revisions, requested action and scope, authority references, evidence requirements, expiry or re-evaluation conditions, stop/rollback conditions, and provenance of the synthesizer and audits.

A candidate methodology or policy may never govern its own adoption. Version N evaluates N+1 under version N's pinned criteria. Do not apply amended criteria retroactively to evidence collected under an earlier revision.

## Evidence scope and productionization invariant

An EGCA decision applies only to the artifact, environment, data shapes and scale, integration path, and operational conditions actually tested.

- Adopting a static prototype, fixture, documentation contract, isolated module, or mocked integration does **not** establish that a materially different live implementation is production-ready.
- Carry accepted evidence forward; do not repeat resolved discovery. Isolate and test the **productionization delta**: the untested difference between the validated artifact and the intended production implementation.
- When that delta introduces material uncertainty, create a linked productionization experiment or adaptation with a stable ID, explicit evidence boundary, adversarial cases, and its own evidence gate.
- Material variables commonly include real data and relationship cardinality, shared-component defaults, authorization, failure and degraded states, responsive behavior, accessibility semantics, performance/scale, deployment topology, and operational recovery.
- A green test suite proves only the behavior it exercises. Trace each accepted criterion to production code, adversarial automated evidence, and branch-matched runtime evidence when that behavior is testable before merge.
- Post-merge or production validation confirms release behavior; it must not be the first evidence for behavior that could have been tested safely before merge.

Do not mark a program production-ready while a required productionization delta is unvalidated, deferred without an explicit residual boundary, or represented only by prototype evidence.

## Required lifecycle

1. **Establish baseline**
   - Inspect the current repository/system before proposing change.
   - Identify the relevant architecture, constraints, existing behavior, tests, and known pain points.
   - Treat live code and measured behavior as authoritative over stale tracker notes.

2. **Create the EGCA feature branch**
   - Create one long-lived feature/integration branch for the entire EGCA program from the repository's authoritative baseline branch, normally `main`.
   - Record this branch in durable EGCA state before executing experiments.
   - Treat this branch as the integration target for all accepted/adapted experiment work in the program.
   - Do **not** merge experiment or intermediate EGCA work directly into `main`.

3. **Capture candidate**
   - Record the capability as a candidate, not committed work.
   - State the problem/opportunity and why the candidate may help.

4. **Investigate**
   - Study the source implementation, documentation, comparable systems, or prior art.
   - Separate transferable principles from source-specific implementation details.
   - Record risks, assumptions, dependencies, and counterevidence.

5. **Hypothesize**
   - Write a falsifiable statement describing what should improve in the target system.
   - Define evidence that would support the hypothesis and evidence that would falsify or weaken it.

6. **Design the smallest useful experiment**
   - Prefer the cheapest bounded repository change capable of answering the architectural question.
   - Do not turn an experiment into a disguised production rollout.
   - Assign a stable experiment ID that is never reused or renumbered.
   - Track dependencies and execution priority separately from the ID.
   - Declare the tested artifact/environment and the evidence applicability boundary.
   - If this is a productionization experiment, state the delta from the previously validated artifact rather than reopening resolved discovery.

7. **Execute and validate**
   - Branch each experiment from the current EGCA feature branch, not from `main`.
   - Implement only the experiment scope admitted by the governing evidence gate.
   - Bind autonomous execution to the exact transition mandate and record revision; never infer broad authority from repository access, agent identity, or a prior action.
   - Collect repository-grounded evidence: tests, benchmarks, runtime observations, UX findings, failure cases, maintenance cost, review findings, or other appropriate measurements.
   - An agent saying "this works" is not sufficient evidence.
   - Include adversarial or counterexample cases for the assumptions most likely to fail at production boundaries.
   - Preserve self-validation and independent validation separately. When independence is required, record why the evidence sources do not share the same material failure domain.
   - For assigned Work Orders, keep execution and validation identities distinct. The executor claims, starts, records evidence/proposals, and submits a non-authoritative Adopt/Adapt/Reject/Repeat recommendation. Independent review either validates that exact submitted revision or returns it for another fresh claim under the unchanged scope and mandate.
   - Treat execution claims as bounded leases, not durable authority. Long-running executors renew before expiry with the same authenticated principal and claim token, carry the returned revision into the next transition, and fail closed when a lease expires or renewal is refused.
   - Maintain criterion-to-evidence traceability for materially different production implementations.
   - Record lightweight execution telemetry when available and materially useful: executor, timing, model/reasoning configuration, human intervention, agent runs/rework, delegations, and runtime-exposed usage or quota information.
   - For delegated or case-study-worthy runs, maintain a separate execution ledger rather than bloating the experiment record.
   - Do not invent unavailable execution measurements; record provenance and confidence for reconstructed values.

8. **Apply the evidence gate**
   - Compare observed results with the explicit success/rejection criteria.
   - Verify the governing methodology/policy version, criteria revision, object revision, transition mandate, and evidence provenance before committing an authoritative transition.
   - Classify the decision as exactly one of:
     - **Adopt** — evidence supports incorporating the capability substantially as tested, within the recorded evidence boundary.
     - **Adapt** — evidence supports the principle but requires a materially different implementation or scope.
     - **Reject** — evidence does not justify adoption.
     - **Repeat** — evidence is insufficient or reveals a new question requiring another bounded experiment.

9. **Integrate according to the decision**
   - **Adopt:** merge or transplant the accepted experiment work into the EGCA feature branch.
   - **Adapt:** create the bounded production adaptation on a branch based on the EGCA feature branch, validate it, then merge that adaptation into the EGCA feature branch.
   - **Reject:** do not merge rejected implementation into the EGCA feature branch; preserve the experiment branch/PR and evidence as historical artifacts when useful.
   - **Repeat:** keep the feature branch stable and create the next bounded experiment from it after recording the new question.
   - Experimental branches are evidence-producing branches. The EGCA feature branch is the cumulative candidate release branch.
   - If productionization differs materially from the tested artifact, keep it on a linked experiment/adaptation branch until its own gate passes.

10. **Record the decision**
   - Preserve the experiment ID, hypothesis, evidence, decision, rationale, relevant references, and follow-up implications.
   - A decision author may be a human or an authenticated service controller. Actor type is provenance, not approval; the author must hold the exact object-scoped decision capability and must not substitute for required independent validation.
   - Record the tested artifact/environment, evidence applicability boundary, productionization delta/status, and traceability references when applicable.
   - Preserve the compact execution summary and execution-ledger reference when telemetry was collected.
   - Update dependencies and next actions without rewriting historical IDs or decisions.

11. **Finalize the EGCA program**
   - After all required experiments, adaptations, migrations, tests, documentation, and integration checks are complete, validate the EGCA feature branch as a whole against the current target baseline.
   - Verify that accepted criteria are traced to the cumulative production implementation and that required productionization deltas have branch-matched evidence.
   - Distinguish production readiness, merge, deployment, and operational validation; none is implied by the previous state.
   - Verify that the governing tracker, evidence documents, and execution ledger are internally consistent before declaring the program complete.
   - Only then open or finalize the single feature/integration PR from the EGCA feature branch to `main` (or the repository's equivalent release branch).
   - Merge the EGCA feature branch to `main` only after the program-level final evidence gate passes and the host repository's current authority requirements are satisfied.
   - Until that point, `main` must remain free of partial EGCA adoption work.

## Branch topology invariant

For one EGCA tracker/program, use one cumulative feature/integration branch.

```text
main
  └── feature/<egca-program>
        ├── experiment/e-001-...
        ├── experiment/e-002-...
        ├── adaptation/e-001-...
        ├── productionization/e-002-...
        └── experiment/e-003-...
```

Experiment and adaptation branches merge **into the feature branch**. The feature branch merges **once into main** when the complete EGCA program is release-ready.

Do not use this topology when the host repository explicitly mandates a stricter branching model; in that case, preserve the same logical isolation using the host repository's equivalent integration branch.

## Durable-state requirements

The storage backend may be Google Sheets, Git-tracked Markdown/YAML/JSON, an issue tracker, or a structured database. Regardless of backend, preserve at least:

- candidate identity and status;
- source investigation and transferable principle;
- hypothesis;
- experiment ID, scope, dependencies, and execution priority;
- success/rejection criteria;
- observed evidence;
- Adopt / Adapt / Reject / Repeat decision;
- decision rationale and follow-up;
- tested artifact/environment and evidence applicability boundary;
- productionization delta and status when the intended implementation differs materially;
- criterion-to-evidence traceability references;
- EGCA feature/integration branch identity;
- experiment/adaptation branch and PR references;
- links or references to relevant repository evidence;
- governing EGCA methodology version and exact source revision;
- transition-mandate reference, criteria revision, and authority provenance for autonomous or consequential transitions;
- self-validation and independent-evidence provenance when independence is required;
- a compact execution summary when meaningful execution telemetry is available;
- an execution-ledger reference for delegated, autonomous, or case-study-worthy runs.

Do not use the tracker as a duplicate of the repository. The repository owns current code reality; EGCA state owns research state, hypotheses, experiment intent, evidence summaries, architectural decisions, and compact execution provenance.

## Execution telemetry

Execution telemetry measures the cost and shape of producing EGCA evidence. It is **process evidence**, not a substitute for capability validation.

When available, record:

- executor: human, ChatGPT, Codex, another agent, hybrid, or unknown;
- start/completion markers and the type of elapsed-time measurement;
- agent-reported elapsed time when the runtime exposes it;
- human active time or intervention count when defensible;
- primary model/tier and reasoning level when exposed;
- number of agent runs and corrective/rework passes;
- delegation count and a concise delegation log for materially distinct subagents;
- token/context/credit/quota consumption in the runtime's original unit when exposed;
- measurement provenance and confidence.

For subagent delegation, preserve at least the bounded task, model/tier and reasoning level when known, why delegation was appropriate, result, and whether the result was used.

Distinguish:

- wall-clock elapsed time;
- agent-reported runtime;
- repository activity windows reconstructed from commits/PRs;
- human estimates.

Do not collapse them into one number or infer unavailable token/cost values.

Keep detailed forensic events in a separate execution ledger beside the tracker. The ledger is evidence provenance, not a transcript: do not store full chain-of-thought, unnecessary chat logs, credentials, or private data.

See `references/execution-telemetry.md` and `templates/execution-ledger-template.md`.

## Optional case-study contribution

At program closeout, consider whether the run produced a reusable EGCA lesson supported by durable evidence. When it did, and the user has not already authorized, declined, or prohibited a case study, ask once whether they would like a sanitized case-study draft prepared for possible contribution to the EGCA project.

Keep the invitation non-blocking and make clear that drafting does not authorize repository placement, publication, a push, or a pull request. Treat each of those as a separate permission under the host project's governance.

Do not ask when the work was routine, duplicates an existing case study, lacks durable evidence, or cannot be sanitized without exposing private or materially reconstructable details. Never infer contribution permission from repository access, implementation approval, or a prior contribution.

When inviting, briefly state the reusable lesson and use language such as:

> This program produced a potentially reusable EGCA learning about [brief topic]. Would you like me to prepare a sanitized case-study draft for possible contribution to the EGCA project? Drafting would not authorize publication or opening a pull request.

See `references/case-study-learnings.md` for sanitization and evidence-preservation guidance.

## Stable identity rule

Experiment IDs identify historical experiments, not execution order.

Never renumber prior experiments merely because priorities or dependencies changed. Use explicit dependency and priority fields for scheduling.

## Pull-request hygiene

When EGCA work results in a pull request, follow the host repository's conventions first. Unless the user or repository instructions expressly say otherwise:

- target experiment/adaptation PRs at the EGCA feature branch, never directly at `main`;
- reserve the feature-to-main PR for final program integration after the program-level evidence gate;
- assign the pull request to the current/authenticated GitHub user when that identity can be resolved safely;
- apply all clearly appropriate existing repository labels based on the work performed (for example enhancement, bug, documentation, testing, performance, or repository-specific workflow labels);
- do not invent or create labels merely to satisfy this rule unless the user asks for new labels;
- record the branch/PR reference in durable EGCA state;
- preserve draft/review status and other governance boundaries required by the host repository.

If assignment or labeling cannot be completed because of permissions, unavailable labels, or unresolved identity, record that limitation instead of silently omitting it.

## Skill lifecycle and updates

The installable EGCA package may check its canonical source for updates. Discovery alone does not justify changing the active methodology.

When `manifest.json` and `scripts/egca_update.py` are present beside this installed skill package:

1. Run `python scripts/egca_update.py check` to retrieve the canonical branch head, remote version, changelog, and migration notes.
2. If no newer version exists, report that result and stop.
3. Treat an update as an EGCA candidate governed by the currently installed methodology version. Record at least:
   - installed version;
   - proposed version;
   - exact source commit SHA;
   - relevant changelog/migration information;
   - compatibility and active-program implications;
   - authenticity/integrity evidence;
   - isolated migration and regression evidence;
   - independent audit evidence where required;
   - backup, activation, and rollback plan.
4. Apply an evidence gate under the current pinned methodology. The proposed version and its candidate policy must not participate as governing sources in that gate.
5. When the gate result is Adopt or an accepted Adapt and the host environment grants the exact update action, apply only the exact admitted source revision. No human relay is intrinsically required.
6. If the source revision moves, evidence or compatibility changes, or the mandate expires, Repeat the gate for the new exact revision; never substitute it silently.
7. Activate atomically where possible, retain the prior installation, run post-activation validation, and roll back automatically when declared rollback conditions occur.
8. Record the decision, activation result, active methodology version, and backup/rollback reference.

Never:

- update merely because a newer version exists or a source branch moved;
- treat a scheduled/background check as evidence that the update should be adopted;
- reuse an admitted transition for a different commit, package, criteria revision, or materially different version;
- bypass host/workspace permission or approval controls;
- rewrite the governing methodology of an active EGCA program merely because the globally installed skill changed.

For an active EGCA program, preserve the methodology version that governed historical decisions. A material mid-program methodology upgrade is itself an explicit decision and should be recorded in durable state with the point from which the new version applies.

If this repository's root compatibility copy of `SKILL.md` is being used directly and the packaged updater files are not adjacent to it, treat Git/repository update mechanisms as authoritative rather than attempting to mutate the repository through the installed-skill updater.

## Authority boundary

EGCA does not override the host repository's governance or manufacture credentials. Before merge, deployment, destructive migration, publication, or another consequential action, resolve the host's current policy and authority requirements into the transition mandate and re-evaluate them at action time.

When the host supplies machine-verifiable authority and the evidence gate passes, EGCA does not add a separate human approval step. When an external system or binding policy reserves the action to a person or unavailable principal, record `ExternalBlock` with the exact missing authority and continue every independent action that remains in scope. Never bypass or silently broaden the external control.

Even when intermediate merges are permitted, merge them only into the EGCA feature branch. A merge to `main` is a program-level release action, not an experiment-level action.

## Output expectations

When starting a new EGCA program:

1. summarize the baseline;
2. create or locate the durable tracker;
3. create and record the EGCA feature/integration branch;
4. create initial candidate records;
5. identify research gaps;
6. propose experiments only after investigation;
7. make the next executable experiment and its evidence gate unambiguous;
8. establish an execution-ledger location when the program will use autonomous/delegated agents or is intended as a case study.

When completing an experiment:

1. summarize the actual changes;
2. report validation evidence and failures;
3. report the compact execution summary and delegation log when telemetry was collected;
4. apply the evidence gate;
5. record the decision;
6. state the evidence applicability boundary and whether a productionization delta remains;
7. integrate Adopt/Adapt results into the EGCA feature branch only;
8. create or update a linked productionization experiment when the intended production implementation differs materially;
9. update dependencies and recommend the next experiment only if warranted.

When completing the program:

1. validate the cumulative EGCA feature branch;
2. reconcile it with the current target baseline;
3. reconcile the tracker and execution ledger with actual repository state;
4. verify criterion-to-production evidence traceability and close or explicitly defer every required productionization delta;
5. record the program-level final evidence gate;
6. report known telemetry gaps or reconstructed measurements separately from exact runtime metrics;
7. report production readiness, merge, deployment, and operational validation as distinct states;
8. only then prepare/merge the feature branch into `main` under host-repository governance;
9. when the run produced a defensible reusable lesson and the user's preference is not already known, make one optional, non-blocking case-study invitation after reporting completion.

See `references/methodology.md`, `references/execution-telemetry.md`, and `templates/` for reusable records.
