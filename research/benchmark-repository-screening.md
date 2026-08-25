# EGCA × Ponytail benchmark repository-family screening

**Status:** pre-confirmatory screening; no task admitted yet  
**Canonical tracker:** issue #9  
**Candidate ledger:** `research/benchmark-task-candidate-ledger.md`

## Purpose

This document records the first destructive screening pass over candidate repository families. The objective is not to find prestigious repositories; it is to find reproducible brownfield systems that can support hundreds of isolated agent trials without hiding the architectural question behind setup cost, external infrastructure, or flaky integration tests.

A family can be useful for some strata and still be unsuitable for others. A `keep` decision below means only that the family is worth deeper task construction; it is not confirmatory admission.

## Screening criteria

Each repository family is screened on:

1. deterministic local setup;
2. narrow test execution without external services;
3. runtime/dependency cost compatible with repeated trials;
4. enough existing structure that repository investigation can matter;
5. realistic opportunities for both reuse and new implementation;
6. ability to derive black-box or public-contract hidden tests;
7. license suitability for reproducible public fixtures;
8. public-solution/memorization risk;
9. overlap with Ponytail or EGCA prior benchmark/case-study tasks;
10. language/runtime balance across the eventual corpus.

Released commits are preferred over arbitrary development heads when they preserve the required architecture.

## Selected core families

### F1 — Pallets Click

**Disposition:** KEEP — primary low-cost Python family  
**Repository:** `pallets/click`  
**Frozen screening baseline:** `68e7ea7228ca144c52e4d1d282cc09da59f7771f` — Click 8.5.0 release  
**License:** BSD-3-Clause  
**Runtime:** Python >= 3.10  
**Ordinary test dependency:** `pytest`  
**Default pytest behavior:** stress tests explicitly excluded by marker

Why it survives:

- small repository and minimal ordinary test dependency surface;
- mature internal concepts around parameter sources, defaults, environment variables, parsing, conversion, callbacks, and context;
- narrow tests can exercise behavior without network, database, browser, or subprocess services;
- existing value-source precedence is explicit enough to support reuse/compatibility tasks without requiring a preferred implementation name in the prompt.

Concrete repository evidence useful for task construction:

`Parameter.consume_value` already defines the precedence path command line -> environment -> `default_map` -> local default and records a `ParameterSource`. This gives us a strong basis for a future S2 reuse task where a new configuration/default input must enter through the existing resolution machinery rather than creating a parallel precedence path.

Potential strata:

- S1 over-build: avoid a second configuration subsystem when current context/default machinery suffices;
- S2 reuse: route new option/default behavior through existing source-resolution semantics;
- S3 irreducible: concrete parser/validation behavior with little architecture leverage;
- S4 reject/defer: avoid a plugin/provider architecture for one new option source or output behavior.

Cautions:

- Click is widely known, so exact historical bug/PR recreation has elevated solution-leakage risk;
- prefer derived-real tasks against the frozen baseline rather than copying famous historical patches;
- keep task prompts at user behavior level and grade observable precedence/compatibility.

## F2 — Pallets Flask

**Disposition:** KEEP — Python web/application family  
**Repository:** `pallets/flask`  
**Frozen screening baseline:** `f00ad424ee3b050d382cc5b4aabb18afbb5e4ae7` — Flask 3.1.3 release  
**License:** BSD-3-Clause  
**Runtime:** Python >= 3.10

Why it survives:

- tests are pytest-based and require only a small test group (`asgiref`, `pytest`, `python-dotenv`) beyond Flask's normal dependencies;
- mature extension and responsibility boundaries make repository fit measurable;
- behavior can often be tested through Flask's test client without external services;
- supports tasks where a correct local patch can still be architecturally wrong because Flask already owns the relevant extension point.

Concrete repository evidence useful for task construction:

Flask exposes `JSONProvider` / `app.json` as the application-level customization boundary for serialization. The provider contract owns `dumps`, `loads`, file helpers, and JSON responses, and can be replaced per application. A future S2/S6 task can therefore ask for application-wide serialization behavior and test whether the implementation uses the existing application JSON responsibility instead of patching individual endpoints.

Potential strata:

- S1 over-build: use existing Flask/Werkzeug/Python behavior rather than a new dependency;
- S2 reuse: application-wide JSON behavior should use the existing provider boundary;
- S5 justified architecture in a fixture built on Flask: repeated policy across independent routes can require a shared application-level boundary;
- S6 ambiguous brownfield: route-local symptom whose correct owner is application/service configuration.

Cautions:

- do not use the already-public EGCA Jekyll/metadata case as a Flask analogue; keep treatment exposure separate;
- avoid tasks that depend on optional async or external integrations;
- framework internals are public and documented, so historical-PR copies need leakage review.

## F3 — Encode HTTPX

**Disposition:** KEEP WITH CONSTRAINTS — protocol/client family  
**Repository:** `encode/httpx`  
**Frozen screening baseline:** `b5addb64f0161ff6bfe94c124ef76f6a1fba5254`  
**License:** BSD-3-Clause  
**Runtime:** Python >= 3.9

Why it survives:

- repository size is moderate;
- tests are pytest-based and network-requiring tests are explicitly marked, allowing an offline benchmark subset;
- client configuration already contains merging, URL, headers, cookies, query parameters, auth, transports, and sync/async symmetry — useful architectural pressure points;
- protocol-facing behavior has strong public contracts suitable for deterministic tests.

Concrete repository evidence useful for task construction:

The client already centralizes configuration merging (`_merge_url`, `_merge_headers`, `_merge_cookies`, `_merge_queryparams`). This creates a potential S2/S6 task where a new request path must preserve client-level configuration semantics rather than locally reconstructing merge logic.

Potential strata:

- S2 reuse: preserve existing merge/configuration path;
- S3 irreducible: concrete request/response transformation logic;
- S5 justified architecture: sync/async or multiple request paths may require a shared compatibility boundary when a new invariant genuinely spans them;
- S6 ambiguous: symptom appears in one request path but repository evidence shows shared client configuration is the owner.

Cautions:

- optional HTTP/2, SOCKS, compression, CLI, and network paths are excluded from initial task design;
- full-suite execution is unnecessary; tasks must ship narrow deterministic tests;
- current screening SHA is not a release commit; before final admission either resolve a suitable tagged release or explicitly justify this frozen post-release commit.

## F4 — Commander.js

**Disposition:** KEEP — primary JavaScript CLI family  
**Repository:** `tj/commander.js`  
**Frozen screening baseline:** `ba6d13ddb4243e5913367734f8c159089ffe7834`  
**Package version at baseline:** 15.0.0  
**License:** MIT  
**Runtime:** Node >= 22.12  
**Primary test command:** `node --test` plus TypeScript definition checks

Why it survives:

- small repository and no runtime dependencies;
- Node's built-in test runner makes isolated runs cheap;
- mature option/argument parsing and option-value-source APIs create observable compatibility contracts;
- mixed JavaScript implementation + TypeScript declarations give us an opportunity to catch underbuilt behavior that updates runtime but forgets public typing contracts.

Concrete repository evidence useful for task construction:

`Command` has explicit option registration, parsing, value storage, and option-value-source APIs (`setOptionValueWithSource` / `getOptionValueSource` in the baseline). This supports S2/S6 tasks where a new option source or mutation path must preserve the existing source metadata instead of merely setting the final value.

Potential strata:

- S1 over-build: new CLI behavior using existing command/option mechanisms;
- S2 reuse: preserve option-value source machinery;
- S3 irreducible: parser/argument behavior with deterministic input-output semantics;
- S4 reject/defer: avoid a plugin architecture around one new output/option feature;
- S6 ambiguous: runtime behavior and type declaration must evolve together.

Cautions:

- freeze Node 22.x even though newer versions may exist during execution;
- TypeScript checks can be used selectively; avoid making every trial pay the full `npm test` cost if a narrower `node --test <file>` plus targeted type check is sufficient.

## F5 — Koa

**Disposition:** KEEP — JavaScript web/middleware family  
**Repository:** `koajs/koa`  
**Frozen screening baseline:** `4a191b1fb7bc999ebbe4bc822e4f315bb752006e`  
**Package version at baseline:** 3.2.1  
**License:** MIT  
**Runtime:** Node >= 18; benchmark container will freeze Node 22.x  
**Primary test command:** `node --test`

Why it survives:

- small repository and built-in Node test runner;
- middleware stack, application callback, context/request/response delegation, async local storage, error handling, and response semantics provide real responsibility boundaries;
- request behavior can be exercised in-process with deterministic local HTTP/supertest-style tests;
- useful counterweight to Commander because it is request-lifecycle architecture rather than CLI parsing.

Concrete repository evidence useful for task construction:

`Application.use` owns middleware registration and `callback()` composes the complete middleware stack before creating per-request context and dispatch. This creates S5/S6 possibilities where behavior required across independent routes or request paths should become middleware/application policy rather than repeated local code — but only when the hidden contract demonstrates that cross-cutting requirement.

Potential strata:

- S2 reuse: use existing context/request/response mechanisms rather than parallel state;
- S3 irreducible: concrete response/request behavior;
- S5 justified architecture: cross-cutting request policy where repeated local patches leave a deterministic bypass;
- S6 ambiguous: local symptom whose correct owner is middleware/application lifecycle.

Cautions:

- avoid tasks whose only desired answer is "write middleware"; the prompt must not reveal the architectural conclusion;
- centralization must be justified through multiple observable paths, otherwise the task collapses into a minimalism/style preference.

## Reserve / rejected families

### Express

**Disposition:** RESERVE, not initial core  
**Screened baseline:** `023767fe9872e029271df1418f73401bff20ff40` — Express 5.2.1

Express is technically viable and has deterministic Mocha/Supertest tests, but its dependency and dev-dependency surface is materially heavier than Koa while occupying a similar Node web-framework niche. Keep it as a replacement family if Koa cannot supply enough independent tasks or if corpus concentration requires another project.

### Django

**Disposition:** REJECT from initial core; possible extracted-fixture source

Reason: repository/test-system scale and setup cost are disproportionate for hundreds of repeated trials. Django concepts can still inspire synthetic-brownfield fixtures, but running the full framework repository as a primary family would spend experimental budget on harness overhead rather than treatment differences.

This rejection replaces the unresolved `django/django` screening concepts in the candidate ledger; they must be remapped to smaller families or synthetic fixtures before further consideration.

### Pydantic

**Disposition:** REJECT from initial core; possible design inspiration only

Reason: modern Pydantic includes a substantially larger repository/build surface and compiled-core concerns. It is poorly matched to our repeated-run cost objective, and the public project is sufficiently prominent that exact historical fixes carry notable solution-leakage risk.

### Zod

**Disposition:** REJECT from initial core

Reason: the repository is materially larger (~25 MB GitHub repository-size signal) and package/workspace complexity does not buy enough additional architectural diversity over Commander/Koa for the first confirmatory corpus.

## Provisional runtime balance

If all five core families survive task construction:

- Python: Click, Flask, HTTPX;
- JavaScript/Node: Commander.js, Koa.

Because the preregistration caps one runtime/language at 50% of the confirmatory corpus, the eventual task allocation cannot simply be equal per family. With 24 tasks, Python must be <=12 tasks. A feasible starting allocation is:

- Click: 4
- Flask: 4
- HTTPX: 4
- Commander.js: 6
- Koa: 6

This is a planning target, not a frozen allocation. Task quality outranks symmetry, and a sixth small non-Python family may be added before corpus freeze if needed.

## First candidate resolutions

The following ledger concepts now have enough repository evidence to continue to architectural-envelope construction. They remain `screening` until reference/anti-reference and hidden tests exist.

### R-001 — Click option/default source reuse

Maps from: `C-S1-05` / `C-S2-05`  
Likely primary stratum: **S2 existing-capability reuse**  
Baseline: Click 8.5.0 `68e7ea7...`

Behavioral concept: introduce a new way for an application/command to supply a value that must obey Click's established option-source precedence and remain introspectable through parameter-source semantics.

Why promising: a local implementation can make the happy-path value correct while bypassing `default_map`/`ParameterSource`, allowing hidden compatibility tests to detect duplication without checking internal names.

Open question before prompt authoring: choose a user-facing scenario natural enough that the new input is not itself an artificial benchmark invention.

### R-002 — Flask application-wide JSON customization

Maps from: `C-S2-01` concept family, replacing the auth-specific wording  
Likely primary stratum: **S2 existing-capability reuse** or **S6 ambiguous brownfield**  
Baseline: Flask 3.1.3 `f00ad42...`

Behavioral concept: a requirement affects JSON serialization consistently across multiple endpoints. The baseline already has an application-level `JSONProvider` responsibility.

Why promising: patching individual endpoints can pass one visible case but fail cross-endpoint consistency; using an application provider is one valid architecture, but the envelope can accept any alternative that demonstrably owns application-wide serialization without duplicate route logic.

Open question: select a serialization behavior whose desired output is unambiguous and does not simply reproduce a documented Flask tutorial.

### R-003 — HTTPX configuration merge consistency

Maps from: `C-S2-03`/`C-S6-04` design intent, replacing the Pydantic/adjacent-package placeholders  
Likely primary stratum: **S2 reuse** or **S6 ambiguous brownfield**  
Baseline: HTTPX `b5addb6...`

Behavioral concept: a new request-building path must combine client-level and per-request configuration with the same semantics as existing request paths.

Why promising: a local happy-path implementation can be functionally correct for one request while breaking headers/query/cookies/base-URL merge behavior; black-box request construction can expose the divergence.

Open question: identify the smallest new public/request path that creates real architectural ambiguity without duplicating a known historical patch.

### R-004 — Commander option-value source preservation

Maps from: `C-S2-05`  
Likely primary stratum: **S2 existing-capability reuse**  
Baseline: Commander 15.0.0 `ba6d13d...`

Behavioral concept: a new option-value input/mutation path must preserve both the value and its source metadata.

Why promising: an under-integrated implementation can set the correct final value but make `getOptionValueSource` wrong, giving us a deterministic compatibility detector.

Open question: derive a natural user-facing feature around configuration/environment/programmatic defaults rather than exposing the source API in the prompt.

### R-005 — Koa cross-cutting request policy

Maps from: `C-S5-02` / `C-S6-01` design intent  
Likely primary stratum: **S5 justified new architecture**  
Baseline: Koa 3.2.1 `4a191b1...`

Behavioral concept: the frozen fixture has multiple independent request paths and introduces another path subject to the same policy. Repeated route-local checks can leave an executed bypass; a shared request-lifecycle policy is therefore warranted.

Why promising: this is a direct anti-minimalism probe. A tiny patch to the named route can pass its happy path while failing another path governed by the same user-level requirement.

Open question: construct the fixture so the shared requirement is real and observable without writing "use middleware" into the prompt.

## Next gate

Before any of R-001 through R-005 can become confirmatory candidates:

1. inspect the exact baseline files/tests relevant to the scenario;
2. write a task-specific architectural envelope;
3. write a neutral prompt only after the envelope exists;
4. implement black-box CORE + REGRESSION tests;
5. implement a plausible reference and anti-reference;
6. confirm two competent alternative implementations can satisfy CORE without a forced internal design;
7. run independence/leakage review.
