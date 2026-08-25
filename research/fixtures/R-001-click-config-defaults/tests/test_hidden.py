import json
import os
from pathlib import Path
import subprocess
import sys

FIXTURE_ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get("BENCH_APP", FIXTURE_ROOT / "baseline" / "app.py"))


def invoke(*args, env=None):
    merged = os.environ.copy()
    merged["PYTHONPATH"] = str(FIXTURE_ROOT)
    if env:
        merged.update(env)
    proc = subprocess.run(
        [sys.executable, str(APP), "build", *args],
        cwd=FIXTURE_ROOT,
        env=merged,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip().splitlines()[-1])


def test_core_project_defaults_flow_through_build():
    result = invoke()
    assert result == {"jobs": 4, "profile": "release", "tag": ["api", "worker"]}


def test_core_explicit_cli_values_win():
    result = invoke("--profile", "debug", "--jobs", "2", "--tag", "cli")
    assert result["profile"] == "debug"
    assert result["jobs"] == 2
    assert result["tag"] == ["cli"]


def test_core_environment_wins_over_project_default():
    result = invoke(env={"TOOL_PROFILE": "staging"})
    assert result["profile"] == "staging"


def test_regression_ordinary_defaults_survive_missing_project_settings():
    result = invoke(env={"BENCH_CONFIG_MODE": "empty", "TOOL_PROFILE": ""})
    assert result == {"jobs": 1, "profile": "dev", "tag": []}


def test_source_project_values_are_click_default_map_values():
    result = invoke("--diagnostics")
    assert result["sources"] == {
        "jobs": "DEFAULT_MAP",
        "profile": "DEFAULT_MAP",
        "tag": "DEFAULT_MAP",
    }


def test_source_cli_and_environment_attribution_remain_correct():
    result = invoke("--jobs", "7", "--tag", "one", "--diagnostics", env={"TOOL_PROFILE": "prod"})
    assert result["sources"] == {
        "jobs": "COMMANDLINE",
        "profile": "ENVIRONMENT",
        "tag": "COMMANDLINE",
    }
    assert result["jobs"] == 7
    assert result["profile"] == "prod"
    assert result["tag"] == ["one"]


def test_source_missing_project_setting_is_not_false_attribution():
    result = invoke("--diagnostics", env={"BENCH_CONFIG_MODE": "empty", "TOOL_PROFILE": ""})
    assert result["sources"] == {
        "jobs": "DEFAULT",
        "profile": "DEFAULT",
        "tag": "DEFAULT",
    }
