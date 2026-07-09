from typing import get_args

import click

from xfetch.fetcher.by_url import fetch
from xfetch.renderer.byname import Name as RendererName
from xfetch.renderer.byname import render, resolve_name
from xfetch.summarizer import summarize_description


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
@click.option(
    "--summary",
    is_flag=True,
    default=False,
    help="Summarize the description using the Anthropic API"
    " (requires XFETCH_ANTHROPIC_API_KEY).",
)
def main_fetch(url: str, format: RendererName, summary: bool) -> None:
    fetched = fetch(url)
    if summary:
        summarize_description(fetched)
    rendered = render(fetched, format)
    print(rendered)


if __name__ == "__main__":
    main()
