from typing import cast, get_args

import click

from xfetch.fetcher.site.amazon import fetch as fetch_amazon
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
    product = fetch_amazon(url)
    rendered = render(product, cast(RendererName, format))
    print(rendered)


if __name__ == "__main__":
    main()
