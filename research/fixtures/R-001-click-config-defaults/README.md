# R-001 executable fixture — Click project defaults

Status: authored, **execution not yet verified in this chat mode**.

## Purpose

S2 existing-capability-reuse probe. The task asks an agent to make an existing project settings mapping provide defaults to a Click command while preserving Click precedence, conversion, repeated-value behavior, and source diagnostics.

## Layout

- `baseline/app.py` — brownfield starting point; project config exists but is ignored.
- `fixture_config.py` — deterministic nested project settings.
- `prompt.txt` — current neutral prompt draft; not confirmatory-frozen yet.
- `controls/reference-a/app.py` — supplies the nested mapping through Click's public `default_map` context setting.
- `controls/reference-b/app.py` — independently supplies the same mapping through a custom `Group.make_context` boundary.
- `controls/anti-reference/app.py` — plausible callback-local patch which produces correct values but leaves source attribution on Click's ordinary `DEFAULT` path.
- `tests/test_hidden.py` — deterministic CORE, REGRESSION, and SOURCE checks.

## Expected control behavior (to verify by execution)

```bash
python -m pip install 'click==8.5.0' 'pytest>=8,<10'

BENCH_APP=controls/reference-a/app.py pytest -q
BENCH_APP=controls/reference-b/app.py pytest -q
BENCH_APP=controls/anti-reference/app.py pytest -q
```

Expected after validation:

- reference A: all tests pass;
- reference B: all tests pass;
- anti-reference: CORE and REGRESSION pass; `test_source_project_values_are_click_default_map_values` fails because project values are still attributed to `DEFAULT`.

The anti-reference must not be declared calibrated until those expectations have actually been executed.
