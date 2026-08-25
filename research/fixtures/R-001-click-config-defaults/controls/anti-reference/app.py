import json

import click
from click.core import ParameterSource

from fixture_config import load_project_settings


@click.group()
def tool():
    """CLI with a plausible but parallel project-default patch."""


@tool.command()
@click.option("--profile", default="dev", envvar="TOOL_PROFILE", show_default=True)
@click.option("--jobs", default=1, type=int, show_default=True)
@click.option("--tag", multiple=True)
@click.option("--diagnostics", is_flag=True)
@click.pass_context
def build(ctx, profile, jobs, tag, diagnostics):
    project = load_project_settings().get("build", {})

    if ctx.get_parameter_source("profile") is ParameterSource.DEFAULT:
        profile = project.get("profile", profile)
    if ctx.get_parameter_source("jobs") is ParameterSource.DEFAULT and "jobs" in project:
        jobs = int(project["jobs"])
    if ctx.get_parameter_source("tag") is ParameterSource.DEFAULT and "tag" in project:
        tag = tuple(project["tag"])

    payload = {"profile": profile, "jobs": jobs, "tag": list(tag)}
    if diagnostics:
        payload["sources"] = {
            name: ctx.get_parameter_source(name).name
            for name in ("profile", "jobs", "tag")
        }
    click.echo(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    tool()
