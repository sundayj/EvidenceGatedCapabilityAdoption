# R-001 task brief — Click project configuration defaults

**Status:** screening task brief; prompt not frozen  
**Envelope:** `research/task-envelopes/R-001-click-option-source.md`  
**Primary stratum:** S2 existing-capability reuse

## Fixture shape

Use a small brownfield CLI application built with Click 8.5.0, pinned to the screened release. The fixture is intentionally an application repository rather than a modification to Click itself so that the model must inspect both application code and the installed framework behavior without being asked to extend Click's public API.

The baseline application has:

- a root group `tool`;
- a `build` command with options `--profile`, `--jobs`, and `--tag`;
- `--profile` supports environment variable `TOOL_PROFILE`;
- `--jobs` is typed as integer;
- `--tag` is `multiple=True`;
- an existing `config.py` that reads a project mapping from an in-memory/test fixture source and returns a nested mapping keyed by command;
- a diagnostic command/path that prints each option value and Click's public parameter source for support/debugging;
- tests for CLI values, envvar values, ordinary defaults, nested commands, integer conversion, and repeated tags.

The baseline intentionally **does not yet apply the project configuration mapping to Click commands**.

No filesystem parser is required in the task itself. This keeps the architectural question on integration with existing value resolution rather than YAML/TOML parsing or dependency choice.

## User-visible prompt draft

> Our CLI already reads project settings in `config.py`, but the `build` command still ignores those settings unless users pass the options themselves. Make the existing project settings provide defaults for `build`. Explicit command-line options and the existing environment variable should still win when they are supplied, and the support/debug output should keep reporting where each value came from correctly.

Prompt-review notes:

- does not say `default_map`;
- does not say `ParameterSource`;
- does not say `reuse` or `minimal`;
- specifies precedence only in user-observable terms;
- source-reporting requirement prevents a happy-path local assignment from looking complete;
- avoids configuration-file parsing, keeping scope bounded.

## Project configuration fixture

Representative project mapping used by hidden tests:

```python
{
    "build": {
        "profile": "release",
        "jobs": "4",
        "tag": "api,worker"
    }
}
```

The exact representation for `tag` is not yet frozen. We should choose a representation that Click's existing multi-value/default semantics can consume naturally without adding a bespoke parser whose behavior would dominate the task.

## Deterministic test plan

### CORE

1. With no CLI/env override, project setting supplies `profile=release`.
2. Project setting supplies `jobs` and the command receives an integer value.
3. Explicit `--profile debug` overrides project setting.
4. `TOOL_PROFILE=staging` overrides project setting when no command-line profile is supplied.

### REGRESSION

5. Existing local Click default still works when the project mapping omits a key.
6. Root/nested command behavior remains unchanged.
7. Existing repeated `--tag` CLI behavior remains unchanged.

### SOURCE / ARCHITECTURAL COMPATIBILITY

8. Debug/source output identifies explicit CLI values as command-line sourced.
9. Debug/source output identifies envvar values as environment sourced.
10. Project-provided defaults are reported consistently with Click's existing default/configuration source semantics rather than as command-line input.
11. Missing project settings do not create false source attribution.

### MULTI-VALUE HEADROOM

12. If `tag` remains in the frozen task, project defaults and CLI repeated tags must follow Click's existing multiple-value/default conversion behavior.

If this subcase requires us to invent a project-specific string grammar, remove it from R-001 rather than contaminating the task with unrelated parsing complexity.

## Reference approach A

At application startup/context construction, adapt the existing project settings mapping into Click's existing command-default mechanism and invoke the command normally. Let Click own precedence, type conversion, and source reporting.

## Reference approach B requirement

We need an independently authored alternative that still preserves a single coherent Click-owned resolution path. Possible shape: a custom root/group context factory or context-settings adaptation that supplies the mapping through an existing public Click boundary rather than assigning values in the command callback.

This must be implemented and tested before admission; describing it here does not count as proving design plurality.

## Anti-reference A — local callback assignment

Plausible bad implementation:

- command callback receives Click-resolved values;
- if an option appears to still be at its ordinary default, callback replaces it from the project mapping.

Expected behavior:

- simplest project-default happy path can pass;
- source attribution is wrong;
- type/multiple behavior may diverge;
- distinguishing an explicitly supplied value equal to the ordinary default becomes unsafe;
- precedence semantics are duplicated outside Click.

This is the primary anti-reference because it represents a realistic minimal patch, not deliberate nonsense.

## Anti-reference B — parallel precedence helper

Optional second bad implementation introduces an application helper that independently checks CLI/env/project/default values. It may pass many cases but duplicates Click's own resolution semantics and should be stress-tested with equality-to-default, callable/default, or multi-value cases that expose divergence.

## Admission questions

- [ ] Can reference A pass all tests with a narrow application change?
- [ ] Can a genuinely distinct reference B pass without relying on the same internal call graph?
- [ ] Does anti-reference A pass basic CORE but fail deterministic source/precedence tests?
- [ ] Is `tag` useful headroom or unnecessary complexity?
- [ ] Can the task be run with only Click + pytest and no network/filesystem nondeterminism?
- [ ] Does an independence reviewer agree this is S2 rather than S1/S6?

## Current disposition

**Continue screening.** The premise is strong because Click's baseline explicitly centralizes precedence and source attribution, and the task can expose bypass through public behavior rather than source inspection. It is not yet a confirmatory candidate until the executable controls exist.
