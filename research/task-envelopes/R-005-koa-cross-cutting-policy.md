# R-005 — Koa cross-cutting request policy

**Status:** screening envelope draft; written before task prompt and treatment outputs  
**Primary stratum:** S5 — justified new architecture  
**Repository:** `koajs/koa`  
**Baseline:** `4a191b1fb7bc999ebbe4bc822e4f315bb752006e` (3.2.1)

## Repository-grounded premise

At the frozen baseline, Koa owns request-lifecycle composition through application middleware. `Application.use(fn)` registers middleware in the application stack, and `callback()` composes that stack before creating and dispatching each request context.

This makes Koa suitable for an anti-minimalism task only if the frozen fixture demonstrates a policy that genuinely applies across multiple independent request paths. The task must not simply prefer middleware as a stylistic choice.

## Candidate behavioral requirement

Construct a small Koa application fixture with multiple independently reachable protected operations that already share a user-level request policy, then introduce another operation subject to the same policy.

The policy should be something objectively testable across paths, such as tenant/account authorization, request correlation/identity enforcement, or idempotency preconditions. The final prompt names the desired behavior but must not say `middleware`, `centralize`, `shared policy`, or otherwise reveal the expected architectural level.

The preferred first candidate is **authorization/ownership consistency** because it supports executed bypass canaries and gives underbuilding a concrete failure mode.

## Architectural envelope

### Required properties

Any acceptable solution must:

1. enforce the frozen policy on every operation covered by the user-level requirement, not only the newly named route/path;
2. preserve normal behavior for authorized/valid requests;
3. reject or safely handle unauthorized/invalid requests consistently across covered paths;
4. prevent a deterministic bypass when a caller reaches an alternate covered path;
5. preserve existing Koa request/response/error behavior outside the policy;
6. keep the policy's source of truth coherent rather than letting equivalent checks drift independently.

### Acceptable commitments

Acceptable implementations may:

- introduce application/router-level middleware or another shared request-lifecycle policy boundary;
- introduce a narrowly scoped policy/helper abstraction invoked from all covered paths if it demonstrably prevents drift/bypass;
- attach validated policy state to Koa context for downstream handlers;
- reorganize a small amount of fixture code so one boundary owns the invariant;
- add targeted policy tests and executed bypass canaries.

Middleware is not the only acceptable answer. A non-middleware design is valid if one coherent boundary enforces the invariant across all required paths and cannot be bypassed by a covered route.

### Unjustified commitments

Absent evidence from the final frozen fixture, the following are presumptively unjustified:

- a standalone authentication/authorization service process;
- a generalized policy engine or rule DSL;
- role/permission hierarchies beyond the frozen requirement;
- new persistence or external identity dependencies;
- plugin registries, event buses, or dependency-injection frameworks;
- broad rewrites of Koa application/request internals rather than fixture/application policy code.

### Under-build signals

A solution is underbuilt if it:

- patches only the newly requested route while another covered path remains bypassable;
- copies the same check into multiple handlers with observable divergence or omission;
- validates identity but fails ownership/tenant scope required by the user contract;
- enforces the policy after an externally visible side effect has already occurred;
- uses a route-local minimal patch that passes the named happy path but fails an executed cross-path canary.

### Over-build signals

A solution is overbuilt if it:

- introduces a broad policy framework for a single narrow invariant;
- adds external services/dependencies not required by the fixture;
- creates configuration or extension machinery for hypothetical policy types;
- refactors unrelated request/response architecture;
- exposes public abstractions whose only consumer is speculative future use.

### Responsibility boundary

The policy belongs at a **shared request/application boundary that dominates every covered path**, not necessarily at a specific Koa private function. Koa's middleware composition is the baseline mechanism that makes such domination natural, but graders must accept any architecture that demonstrably enforces one coherent invariant across all paths.

## Hidden-test design targets

### CORE

- authorized user can perform the newly requested operation;
- unauthorized/wrong-owner request to the named operation is rejected;
- expected response/body/status behavior is preserved.

### REGRESSION

- existing protected operations still work for authorized users;
- unprotected behavior outside the policy remains unchanged;
- existing error/response flow remains valid.

### SECURITY / UNDERBUILD CANARIES

Executed behavioral tests must include at least:

- alternate existing protected path cannot be used to bypass the same ownership/authorization invariant;
- user A cannot operate on user B's resource through any covered path;
- policy failure occurs before the protected side effect;
- encoded/alternate identifier shape does not accidentally bypass the invariant if such a representation exists in the fixture.

No source-regex test such as "middleware was added" is allowed.

## Reference-control requirement

At least two competent reference approaches must pass all deterministic tests:

1. a shared Koa middleware/application-policy implementation;
2. a distinct shared policy/helper boundary that is invoked in a way that deterministically covers all protected paths.

If only a middleware implementation can pass because tests assert internal structure, the tests are invalid and must be revised.

## Anti-reference control

The required anti-reference is a plausible **minimal local patch**: add the correct ownership/authorization check only to the newly requested path. It must pass the named route's CORE tests but fail the alternate-path executed bypass canary.

A second optional anti-reference may duplicate checks across handlers but intentionally omit one path, demonstrating why repeated local enforcement is fragile in this frozen fixture.

## Headroom requirement

Before confirmatory admission, the anti-reference must reliably pass the happy path while failing the cross-path policy canary. At least two independently authored competent solutions must converge on some shared-enforcement architecture without being told to centralize.

If strong baseline agents almost always centralize correctly even without EGCA/Ponytail, the task may lack treatment headroom and should be pilot-only or rejected rather than retained for ideological reasons.

## Open gate questions

1. Which policy yields the cleanest executed canary with minimal fixture complexity: ownership authorization, tenant isolation, idempotency, or another request invariant?
2. Should the benchmark edit Koa itself or a frozen small Koa application fixture? Current preference: application fixture, because the architectural question is application policy rather than a Koa framework feature.
3. How many independent paths are needed to make shared enforcement objectively warranted without turning the fixture into a toy built around the answer? Current target: three covered paths, with two existing before the new task.
4. Can side effects be represented deterministically in memory so no database/service is needed?
