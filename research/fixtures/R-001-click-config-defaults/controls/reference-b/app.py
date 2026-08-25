import json

import click

from fixture_config import load_project_settings


class ConfiguredGroup(click.Group):
    """Inject project defaults at the public context-construction boundary."""

    def make_context(self, info_name, args, parent=None, **extra):
        extra.setdefault("default_map", load_project_settings())
        return super().make_context(info_name, args, parent=parent, **extra)


@click.group(cls=ConfiguredGroup)
def tool():
    """CLI whose root context supplies project defaults."""


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
