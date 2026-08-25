---
name: evidence-gated-capability-adoption
description: Evaluate whether a substantial software capability, architectural pattern, dependency, integration, or design idea should be adopted using source investigation, falsifiable hypotheses, bounded experiments, explicit evidence gates, durable decision records, and cumulative integration isolation. Use when a coding agent or engineer needs to research and experimentally validate a non-trivial capability before committing it to a production architecture; do not use for trivial fixes or already-approved implementation work.
---

# Evidence-Gated Capability Adoption

Use this skill when evaluating whether a substantial capability, architectural pattern, dependency, integration, or design idea should be adopted into an existing software system.

Do **not** use the full process for trivial fixes, obvious dependency bumps, or work whose implementation is already approved and understood.

## Objective

Turn promising ideas into evidence-backed architectural decisions without allowing research findings, agent suggestions, or source-project features to silently become implementation commitments.

EGCA is **not** a minimum-code or "always simplify" methodology. Prefer the smallest experiment that can answer the current question, but allow the evidence gate to justify additional models, abstractions, dependencies, or other architecture when the evidence supports them. The target is justified architecture, not minimum lines of code.

Minimal-implementation disciplines such as [Ponytail](references/related-work.md) can complement EGCA by constraining an experiment or accepted implementation after the adoption question and experiment boundary are understood.

## Required lifecycle

1. **Establish baseline**
   - Inspect the current repository/system before proposing change.
   - Identify the relevant architecture, constraints, existing behavior, tests, and known pain points.
   - Treat live code and measured behavior as authoritative over stale tracker notes.

2. **Create the EGCA feature branch**
   - Create one long-lived feature/integration branch for the entire EGCA program from the repository's approved baseline branch, normally `main`.
   - Record this branch in durable EGCA state before executing experiments.
   - Treat this branch as the integration target for all accepted/adapted experiment work in the program.
   - Do **not** merge experiment or intermediate EGCA work directly into `main`.

3. **Capture candidate**
   - Record the capability as a candidate, not approved work.
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
   - When useful, predeclare an implementation boundary such as allowed files, function/interface names and inputs/outputs, or another explicit scope budget. Require the agent to stop and explain why the boundary is insufficient rather than silently widening it.
   - Do not freeze such a boundary before investigation; a premature interface budget can encode the wrong architecture. Treat a justified request to cross the boundary as evidence to review.
   - Assign a stable experiment ID that is never reused or renumbered.
   - Track dependencies and execution priority separately from the ID.

7. **Execute and validate**
   - Branch each experiment from the current EGCA feature branch, not from `main`.
   - Implement only the approved experiment scope.
   - Collect repository-grounded evidence: tests, benchmarks, runtime observations, UX findings, failure cases, maintenance cost, review findings, or other appropriate measurements.
   - An agent saying "this works" is not sufficient evidence.

8. **Apply the evidence gate**
   - Compare observed results with the explicit success/rejection criteria.
   - Classify the decision as exactly one of:
     - **Adopt** — evidence supports incorporating the capability substantially as tested.
     - **Adapt** — evidence supports the principle but requires a materially different implementation or scope.
     - **Reject** — evidence does not justify adoption.
     - **Repeat** — evidence is insufficient or reveals a new question requiring another bounded experiment.

9. **Integrate according to the decision**
   - **Adopt:** merge or transplant the accepted experiment work into the EGCA feature branch.
   - **Adapt:** create the bounded production adaptation on a branch based on the EGCA feature branch, validate it, then merge that adaptation into the EGCA feature branch.
   - **Reject:** do not merge rejected implementation into the EGCA feature branch; preserve the experiment branch/PR and evidence as historical artifacts when useful.
   - **Repeat:** keep the feature branch stable and create the next bounded experiment from it after recording the new question.
   - Experimental branches are evidence-producing branches. The EGCA feature branch is the cumulative candidate release branch.

10. **Record the decision**
   - Preserve the experiment ID, hypothesis, evidence, decision, rationale, relevant references, and follow-up implications.
   - Update dependencies and next actions without rewriting historical IDs or decisions.

11. **Finalize the EGCA program**
   - After all required experiments, adaptations, migrations, tests, documentation, and integration checks are complete, validate the EGCA feature branch as a whole against the current target baseline.
   - Only then open or finalize the single feature/integration PR from the EGCA feature branch to `main` (or the repository's equivalent release branch).
   - Merge the EGCA feature branch to `main` only after the program-level final evidence gate passes and host-repository approval requirements are satisfied.
   - Until that point, `main` must remain free of partial EGCA adoption work.

## Branch topology invariant

For one EGCA tracker/program, use one cumulative feature/integration branch.

```text
main
  └── feature/<egca-program>
        ├── experiment/e-001-...
        ├── experiment/e-002-...
        ├── adaptation/e-001-...
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
- EGCA feature/integration branch identity;
- experiment/adaptation branch and PR references;
- links or references to relevant repository evidence.

Do not use the tracker as a duplicate of the repository. The repository owns current code reality; EGCA state owns research state, hypotheses, experiment intent, evidence summaries, and architectural decisions.

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

## Approval boundary

EGCA does not override the host repository's governance. Stop before merge, deployment, destructive migration, publication, or other consequential actions whenever the project's own instructions require human approval.

Even when intermediate merges are permitted, merge them only into the EGCA feature branch. A merge to `main` is a program-level release action, not an experiment-level action.

## Output expectations

When starting a new EGCA program:

1. summarize the baseline;
2. create or locate the durable tracker;
3. create and record the EGCA feature/integration branch;
4. create initial candidate records;
5. identify research gaps;
6. propose experiments only after investigation;
7. make the next executable experiment and its evidence gate unambiguous.

When completing an experiment:

1. summarize the actual changes;
2. report validation evidence and failures;
3. apply the evidence gate;
4. record the decision;
5. integrate Adopt/Adapt results into the EGCA feature branch only;
6. update dependencies and recommend the next experiment only if warranted.

When completing the program:

1. validate the cumulative EGCA feature branch;
2. reconcile it with the current target baseline;
3. record the program-level final evidence gate;
4. only then prepare/merge the feature branch into `main` under host-repository governance.

See `references/methodology.md` for rationale, `references/related-work.md` for adjacent tools and complementary techniques, and `templates/` for reusable records.
