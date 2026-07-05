from typing import cast, get_args

import click

from xfetch.fetcher.by_url import fetch
from xfetch.renderer.byname import Name as RendererName
from xfetch.renderer.byname import render


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    # ctx.obj = App()
    pass


@main.command("fetch")
@click.argument("URL", type=str, required=True)
@click.option(
    "--format",
    "-f",
    type=click.Choice(get_args(RendererName)),
    default="markdown-heading",
)
def main_fetch(url: str, format: str) -> None:
    fetched = fetch(url)
    rendered = render(fetched, cast(RendererName, format))
    print(rendered)


if __name__ == "__main__":
    main()
