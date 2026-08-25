def load_project_settings():
    """Return deterministic project settings used by the fixture.

    BENCH_CONFIG_MODE=empty simulates a project with no stored defaults so the
    hidden regression suite can verify Click's ordinary defaults still work.
    """
    import os

    if os.environ.get("BENCH_CONFIG_MODE") == "empty":
        return {}

    return {
        "build": {
            "profile": "release",
            "jobs": "4",
            "tag": ("api", "worker"),
        }
    }
