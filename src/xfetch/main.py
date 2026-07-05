import click

from xfetch.fetcher.site.amazon import fetch as fetch_amazon


@click.group()
@click.pass_context
def main(ctx: click.Context) -> None:
    # ctx.obj = App()
    pass


@main.command("fetch")
@click.argument("URL", type=str, required=True)
def main_fetch(url: str) -> None:
    product = fetch_amazon(url)
    print(product.raw)


if __name__ == "__main__":
    main()
