# R-001 — Click option/default source reuse

**Status:** screening envelope draft; written before task prompt and treatment outputs  
**Primary stratum:** S2 — existing-capability reuse  
**Repository:** `pallets/click`  
**Baseline:** `68e7ea7228ca144c52e4d1d282cc09da59f7771f` (8.5.0)

## Repository-grounded premise

At the frozen baseline, Click already owns parameter-value resolution and source tracking.

`Parameter.consume_value` resolves a parameter from command-line input, environment variables, `Context.default_map`, and the parameter default, in precedence order, and returns both the value and a `ParameterSource`.

The baseline tests exercise default-map behavior, callable defaults, type coercion, nested command defaults, and parameter-source introspection.

The benchmark task should therefore not reward an implementation that happens to return the correct final value while creating a second value-resolution path that loses Click's existing precedence or source semantics.

## Candidate behavioral requirement

Introduce a natural application-facing configuration/default input whose supplied option values must participate in Click's existing precedence behavior and remain correctly attributable through the public parameter-source behavior.

The exact user-visible scenario is intentionally not frozen yet. Candidate forms include loading command defaults from a project configuration mapping or adapting an already-parsed configuration object into command defaults. The final prompt must not mention `default_map`, `ParameterSource`, `consume_value`, or the preferred implementation mechanism.

## Architectural envelope

### Required properties

Any acceptable solution must:

1. preserve ordinary command-line option behavior;
2. preserve environment-variable precedence where the option already supports an envvar;
3. allow the new configuration/default input to supply a value when higher-precedence sources do not;
4. preserve parameter type conversion and multi-value behavior through the normal Click contract;
5. preserve correct public source attribution for values supplied through the new/default configuration route;
6. avoid regressions in nested command/default-map behavior relevant to the chosen prompt.

### Acceptable commitments

Acceptable implementations may:

- adapt the new configuration input into the existing context/default mapping machinery;
- extend an existing Click default/source boundary narrowly if the chosen user requirement cannot be represented without doing so;
- add a small helper responsible for translating the external configuration shape into Click's existing resolution contract;
- add tests around source precedence and attribution.

An implementation does **not** have to call a specific private function or preserve a particular internal call graph if it satisfies the public behavior and maintains one coherent source-resolution responsibility.

### Unjustified commitments

Absent new evidence from the final frozen prompt, the following are presumptively unjustified:

- a second independent precedence engine alongside `Parameter.consume_value`;
- a generalized provider/plugin/registry architecture for arbitrary configuration sources;
- new third-party configuration dependencies;
- a parallel option-value store that bypasses context/default semantics;
- changes to unrelated parser, help, completion, or command-registration architecture;
- public extension APIs designed for hypothetical future configuration backends not required by the task.

### Under-build signals

A solution is underbuilt if it:

- makes the new source work only on the happy path but reports the wrong parameter source;
- lets the new source override command-line or environment input contrary to the existing precedence contract;
- bypasses Click's type conversion or multiple/nargs handling;
- works only for a single command shape while the frozen user contract requires nested/default behavior;
- special-cases the benchmark option rather than integrating the behavior at the proper existing responsibility.

### Over-build signals

A solution is overbuilt if it:

- creates new provider/registry abstractions without multiple demonstrated implementations or extension requirements;
- duplicates source-precedence logic already present in the baseline;
- adds broad configuration parsing, file watching, schema systems, dependency injection, or unrelated extensibility;
- touches materially more parser/context architecture than necessary to satisfy the behavioral requirement.

### Responsibility boundary

The baseline indicates that **Click's existing context/parameter value-resolution machinery** owns precedence and source attribution. The external configuration format/parser, if one exists in the final task fixture, may live outside that machinery, but once values enter Click they should not create a competing resolution authority.

## Hidden-test design targets

### CORE

- new configuration/default input supplies the expected typed value when no higher-precedence source exists;
- explicit command-line value wins;
- final command receives the expected value.

### REGRESSION

- environment-variable precedence remains correct;
- ordinary defaults remain correct;
- nested command/default behavior relevant to the fixture remains intact.

### ARCHITECTURAL COMPATIBILITY

Black-box/public API checks should verify:

- `Context.get_parameter_source(...)` reports the correct source class for the value;
- multi-value/type conversion behavior is unchanged;
- the new input does not become an independent higher-precedence source accidentally.

These checks must not assert a private function call or file layout.

## Reference-control requirement

At least two competent reference approaches must pass CORE + REGRESSION without sharing identical internal structure. One may adapt into `default_map`; another may extend an existing context/default entry boundary narrowly if this can be done without creating a second precedence engine.

If only one internal design can satisfy the tests, the task is too implementation-prescriptive and must be revised.

## Anti-reference control

The anti-reference should plausibly set the desired final value through a local/parallel code path while bypassing source attribution or precedence integration. It should pass the simplest happy-path CORE case but fail at least one deterministic source/precedence compatibility check.

## Open gate questions

1. What natural user-facing configuration scenario gives this task enough realism without copying a Click documentation example?
2. Can the scenario be implemented entirely against Click itself, or is a small public/synthetic CLI fixture better for reducing prompt leakage?
3. Can two independently designed solutions satisfy the behavioral contract without forcing `default_map` by name?
4. Does baseline source attribution give enough discriminatory headroom across strong models?
