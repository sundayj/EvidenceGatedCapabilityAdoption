# R-005 task brief — Koa ownership policy across request paths

**Status:** screening task brief; prompt not frozen  
**Envelope:** `research/task-envelopes/R-005-koa-cross-cutting-policy.md`  
**Primary stratum:** S5 justified new architecture  
**Risk axis:** security, cross-boundary

## Fixture shape

Use a small Koa 3.2.1 application fixture pinned to the screened baseline/runtime. Keep all state in memory so every trial is deterministic and requires no database or external service.

The baseline application models projects owned by users:

```text
users:    alice, bob
projects: p1 -> alice, p2 -> bob
```

Authentication is already performed by an upstream fixture middleware that sets `ctx.state.user` from a deterministic test header. The benchmark task is therefore **not** about inventing authentication.

The baseline exposes two existing project mutation paths:

- `POST /projects/:id/archive`
- `POST /projects/:id/rename`

Both are intended by the fixture's user contract to allow only the owning user, but the baseline deliberately contains route-local ownership checks. This historical setup is plausible brownfield debt, not yet the benchmark failure.

The new requested operation is:

- `POST /projects/:id/labels`

Before the benchmark is admitted, the fixture must be calibrated so that route-local patching of only `/labels` leaves a deterministic policy inconsistency or bypass elsewhere, while a shared enforcement boundary covers all three paths.

## Important anti-bias constraint

The fixture may **not** be constructed so that simply moving code into middleware is the only way to pass. Tests grade ownership enforcement across covered operations and side-effect ordering. A shared helper/policy boundary invoked coherently from all covered routes is also acceptable.

The S5 claim is justified only if the requirement and frozen fixture establish that the ownership invariant applies to the operation family as a whole, not merely because three similar checks look aesthetically repetitive.

## User-visible prompt draft

> Add labels to projects. A signed-in user should be able to add a label to one of their own projects, and users must not be able to change projects they do not own. Keep the existing project mutation behavior working consistently.

Prompt-review notes:

- does not mention middleware;
- does not say centralize/shared/refactor;
- does not enumerate the existing archive/rename routes;
- "existing project mutation behavior working consistently" gives the agent a reason to inspect related paths without revealing the intended architecture;
- security requirement is explicit enough that hidden ownership checks are legitimate rather than surprise grading.

A stricter alternate prompt is being held in reserve:

> Add labels to projects. A signed-in user should be able to add a label to one of their own projects. The same ownership rule should apply to project changes throughout the app.

The second version increases contract clarity but may leak that the solution should be cross-cutting. Prompt review must choose one before controls are authored; we should prefer the first if independent reviewers agree the cross-path invariant follows naturally from it.

## Deterministic state and side effects

Each trial receives a clean in-memory project store. Mutation handlers change an object in that store and return a deterministic JSON response.

The hidden harness can therefore assert both:

- response/status behavior;
- whether a forbidden mutation occurred before rejection.

This lets us detect a superficially correct authorization response that happens after the side effect.

## Deterministic test plan

### CORE — named new operation

1. Alice can add a label to `p1`.
2. Bob can add a label to `p2`.
3. Alice cannot add a label to `p2`.
4. Unauthorized label attempt does not mutate `p2`.
5. Missing project follows the fixture's existing not-found behavior.

### REGRESSION — existing operations

6. Owner can still archive own project.
7. Owner can still rename own project.
8. Existing response/error shapes remain compatible.

### SECURITY / S5 UNDERBUILD CANARIES

9. Alice cannot archive Bob's project.
10. Alice cannot rename Bob's project.
11. No forbidden archive/rename side effect occurs before rejection.
12. A project identifier represented in any alternate form supported by the fixture cannot bypass ownership checks.

The crucial calibration question is whether the baseline already passes 9-12. If it does, a local `/labels` patch may be perfectly adequate and the task would **not** justify new shared architecture. In that case R-005 must be redesigned or rejected rather than forcing centralization.

### ARCHITECTURAL COHERENCE FOLLOW-UP

A frozen optional follow-up can add a fourth mutation operation after the primary run. This is exploratory maintainability evidence only and cannot define primary correctness.

## Fixture calibration alternatives

We need to choose one of two scientifically defensible fixture histories before admission.

### Variant A — existing routes are correct but duplicated

Archive and rename each have correct route-local ownership checks.

Implication: adding a third correct local check may be repetitive but is not demonstrably wrong. This variant is **not sufficient for S5** unless another frozen invariant proves that one shared enforcement boundary is required. It may instead become S3 or S4 and should not be mislabeled.

### Variant B — existing duplicated policy has already drifted

Archive correctly checks owner; rename has a subtle but realistic divergence that allows one unauthorized mutation path. The user request's consistency language requires the new feature to preserve/fix the project mutation ownership invariant across the app.

Implication: patching only `/labels` leaves an executed bypass. A coherent shared boundary (middleware or shared policy helper) fixes the demonstrated architectural problem.

**Current preference: Variant B**, but only if the drift is plausible and disclosed by repository evidence available to every arm. We must not hide an unrelated planted vulnerability merely to make centralization win.

Candidate plausible drift:

- archive compares authenticated user to `project.ownerId`;
- rename mistakenly checks only that a user is authenticated due to older copy/paste code;
- existing baseline tests cover owner rename but omit cross-owner rename.

The new task causes a competent agent to inspect project mutations and discover the inconsistency. Hidden tests then grade the explicit ownership contract, not an arbitrary internal structure.

## Reference approach A — request-lifecycle policy

Introduce a shared Koa policy boundary that loads the project, verifies ownership, and exposes the authorized project on context before mutation handlers run. Apply it to all covered project mutation routes.

## Reference approach B — shared domain/policy helper

Introduce or consolidate a narrow `requireOwnedProject(ctx)`-style policy helper used coherently by each project mutation handler before side effects. This is architecturally different from middleware composition but still establishes one source of truth and passes all behavioral checks.

The final tests must accept both.

## Anti-reference A — minimal new-route patch

Add correct ownership checking only to the new `/labels` handler and leave existing mutation paths untouched.

Expected outcome under calibrated Variant B:

- all new-operation CORE tests pass;
- existing owner regression tests pass;
- cross-owner rename bypass remains and fails the security/underbuild canary.

This is the primary anti-reference because it represents the exact failure mode the S5 stratum exists to detect: locally minimal work suppresses a justified shared responsibility.

## Anti-reference B — copy/paste all three checks

Optionally make all paths pass today by duplicating ownership logic independently in each handler. If deterministic behavior is fully correct, this **must not automatically fail primary grading merely for duplication**. It may score worse on architectural appropriateness, but hidden correctness tests cannot manufacture a future bug.

This is important: S5 must not equate "shared abstraction" with correctness by fiat.

If we cannot create observable present-tense evidence that duplicated local checks are insufficient, then a shared abstraction is not yet empirically required and R-005 is not a valid S5 task.

## Admission questions

- [ ] Does the frozen fixture contain present-tense evidence that one local patch is insufficient?
- [ ] Is that evidence visible through repository inspection rather than hidden only in grader tests?
- [ ] Can reference A and reference B both pass all deterministic tests?
- [ ] Does anti-reference A pass new-route CORE but fail a legitimate explicit ownership invariant?
- [ ] Are the hidden canaries directly derivable from the prompt + existing application behavior?
- [ ] Can the whole task run with Node 22, Koa, and in-process testing only?
- [ ] Do independent classifiers agree S5 is justified rather than inferred from our preferred design?

## Current disposition

**Continue screening, with a hard validity warning.** R-005 is valuable precisely because it can expose our own bias: if calibration shows that three local checks satisfy every present requirement, then Ponytail-style minimalism is not wrong and the task must not be labeled "justified architecture." The task earns S5 only if repository-visible evidence makes a shared responsibility necessary to satisfy the current contract.
