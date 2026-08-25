# R-005 executable fixture — Koa project ownership

Status: authored, **execution not yet verified in this chat mode**.

## Purpose

S5 justified-new-architecture probe. The frozen brownfield baseline makes the ownership drift repository-visible: `archive` checks ownership, while `rename` only checks authentication. The new task adds `labels` and explicitly requires users not to change projects they do not own while keeping project mutations consistent.

The grader does not inspect middleware/helper names. It executes ownership and side-effect invariants.

## Layout

- `baseline/app.js` — deterministic Koa app with in-memory users/projects and the historical `rename` drift.
- `prompt.txt` — neutral prompt draft; not confirmatory-frozen yet.
- `controls/reference-a/app.js` — request-lifecycle authorization middleware shared by all project mutations.
- `controls/reference-b/app.js` — a narrow shared `requireOwnedProject` policy helper invoked by each mutation handler.
- `controls/anti-reference/app.js` — plausible minimal patch that secures only the new labels route and leaves the visible rename drift untouched.
- `tests/hidden.test.js` — CORE, REGRESSION, and SECURITY/S5-underbuild checks using native Node `fetch` against an ephemeral in-process Koa server.

## Expected control behavior (to verify by execution)

```bash
npm install

BENCH_APP=controls/reference-a/app.js npm run test:hidden
BENCH_APP=controls/reference-b/app.js npm run test:hidden
BENCH_APP=controls/anti-reference/app.js npm run test:hidden
```

Expected after validation:

- reference A: all tests pass;
- reference B: all tests pass;
- anti-reference: new-label CORE tests and owner regression tests pass, but the cross-owner rename security/underbuild canary fails because the old route remains authorization-inconsistent.

If the anti-reference fails unrelated CORE behavior, or either reference requires grader-specific structure, R-005 must be repaired or rejected before admission.
