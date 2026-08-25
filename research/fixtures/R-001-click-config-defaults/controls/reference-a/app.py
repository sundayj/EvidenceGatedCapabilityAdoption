import json

import click

from fixture_config import load_project_settings


@click.group(context_settings={"default_map": load_project_settings()})
def tool():
    """CLI whose project configuration enters through Click's default map."""


@tool.command()
@click.option("--profile", default="dev", envvar="TOOL_PROFILE", show_default=True)
@click.option("--jobs", default=1, type=int, show_default=True)
@click.option("--tag", multiple=True)
@click.option("--diagnostics", is_flag=True)
@click.pass_context
def build(ctx, profile, jobs, tag, diagnostics):
    payload = {"profile": profile, "jobs": jobs, "tag": list(tag)}
    if diagnostics:
        payload["sources"] = {
            name: ctx.get_parameter_source(name).name
            for name in ("profile", "jobs", "tag")
        }
    click.echo(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    tool()
