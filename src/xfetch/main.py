from typing import get_args

import click

from xfetch.fetcher.by_url import fetch
from xfetch.renderer.byname import Name as RendererName
from xfetch.renderer.byname import render, resolve_name


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    # ctx.obj = App()
    pass


def _resolve_format(
    ctx: click.Context, param: click.Parameter, value: str
) -> RendererName:
    try:
        return resolve_name(value)
    except ValueError as e:
        raise click.BadParameter(str(e))


@main.command("fetch")
@click.argument("URL", type=str, required=True)
@click.option(
    "--format",
    "-f",
    type=str,
    default="markdown-heading",
    show_default=True,
    callback=_resolve_format,
    help=f"Output format ({', '.join(get_args(RendererName))});"
    " initials like 'mhq' also work.",
)
def main_fetch(url: str, format: RendererName) -> None:
    fetched = fetch(url)
    rendered = render(fetched, format)
    print(rendered)


if __name__ == "__main__":
    main()
