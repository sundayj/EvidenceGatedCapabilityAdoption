# Evidence-Gated Capability Adoption

Use this skill when evaluating whether a substantial capability, architectural pattern, dependency, integration, or design idea should be adopted into an existing software system.

Do **not** use the full process for trivial fixes, obvious dependency bumps, or work whose implementation is already approved and understood.

## Objective

Turn promising ideas into evidence-backed architectural decisions without allowing research findings, agent suggestions, or source-project features to silently become implementation commitments.

## Required lifecycle

1. **Establish baseline**
   - Inspect the current repository/system before proposing change.
   - Identify the relevant architecture, constraints, existing behavior, tests, and known pain points.
   - Treat live code and measured behavior as authoritative over stale tracker notes.

2. **Capture candidate**
   - Record the capability as a candidate, not approved work.
   - State the problem/opportunity and why the candidate may help.

3. **Investigate**
   - Study the source implementation, documentation, comparable systems, or prior art.
   - Separate transferable principles from source-specific implementation details.
   - Record risks, assumptions, dependencies, and counterevidence.

4. **Hypothesize**
   - Write a falsifiable statement describing what should improve in the target system.
   - Define evidence that would support the hypothesis and evidence that would falsify or weaken it.

5. **Design the smallest useful experiment**
   - Prefer the cheapest bounded repository change capable of answering the architectural question.
   - Do not turn an experiment into a disguised production rollout.
   - Assign a stable experiment ID that is never reused or renumbered.
   - Track dependencies and execution priority separately from the ID.

6. **Execute and validate**
   - Implement only the approved experiment scope.
   - Collect repository-grounded evidence: tests, benchmarks, runtime observations, UX findings, failure cases, maintenance cost, review findings, or other appropriate measurements.
   - An agent saying "this works" is not sufficient evidence.

7. **Apply the evidence gate**
   - Compare observed results with the explicit success/rejection criteria.
   - Classify the decision as exactly one of:
     - **Adopt** — evidence supports incorporating the capability substantially as tested.
     - **Adapt** — evidence supports the principle but requires a materially different implementation or scope.
     - **Reject** — evidence does not justify adoption.
     - **Repeat** — evidence is insufficient or reveals a new question requiring another bounded experiment.

8. **Record the decision**
   - Preserve the experiment ID, hypothesis, evidence, decision, rationale, relevant references, and follow-up implications.
   - Update dependencies and next actions without rewriting historical IDs or decisions.

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
- links or references to relevant repository evidence.

Do not use the tracker as a duplicate of the repository. The repository owns current code reality; EGCA state owns research state, hypotheses, experiment intent, evidence summaries, and architectural decisions.

## Stable identity rule

Experiment IDs identify historical experiments, not execution order.

Never renumber prior experiments merely because priorities or dependencies changed. Use explicit dependency and priority fields for scheduling.

## Approval boundary

EGCA does not override the host repository's governance. Stop before merge, deployment, destructive migration, publication, or other consequential actions whenever the project's own instructions require human approval.

## Output expectations

When starting a new EGCA program:

1. summarize the baseline;
2. create or locate the durable tracker;
3. create initial candidate records;
4. identify research gaps;
5. propose experiments only after investigation;
6. make the next executable experiment and its evidence gate unambiguous.

When completing an experiment:

1. summarize the actual changes;
2. report validation evidence and failures;
3. apply the evidence gate;
4. record the decision;
5. update dependencies and recommend the next experiment only if warranted.

See `references/methodology.md` for rationale and `templates/` for reusable records.