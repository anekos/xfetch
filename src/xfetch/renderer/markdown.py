from io import StringIO

from xfetch.format import format_price
from xfetch.models import Article, Fetched, Product
from xfetch.renderer.base import BaseRenderer


def _list_item(prefix: str, text: str) -> str:
    indent = " " * len(prefix)
    lines = text.split("\n")
    return prefix + ("\n" + indent).join(lines)


def _link(fetched: Fetched) -> str:
    return f"[{fetched.name}]({fetched.url})"


def _price(fetched: Fetched) -> str | None:
    if not isinstance(fetched, Product) or fetched.price is None:
        return None
    price = f"Price: {format_price(fetched.price)}"
    if fetched.currency is not None:
        price += f" {fetched.currency}"
    return price


def _description(fetched: Fetched) -> str | None:
    if not isinstance(fetched, Article):
        return None
    return fetched.description


class MarkdownHeadingRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        buffer = StringIO()

        print(f"# {_link(fetched)}", file=buffer)
        print("", file=buffer)

        if isinstance(fetched, Article) and fetched.thumbnail_url is not None:
            print(
                f"[![{fetched.thumbnail_url}]({fetched.thumbnail_url})]({fetched.url})",
                file=buffer,
            )

        if price := _price(fetched):
            print(_list_item("- ", price), file=buffer)

        if description := _description(fetched):
            print(_list_item("- ", description), file=buffer)

        return buffer.getvalue()


class MarkdownLinkRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        return _link(fetched)


class MarkdownDefinitionListRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        buffer = StringIO()

        print(_link(fetched), file=buffer)

        if price := _price(fetched):
            print(f": {price}", file=buffer)

        if description := _description(fetched):
            print(f": {description}", file=buffer)

        return buffer.getvalue()


class MarkdownListRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        details = [d for d in (_price(fetched), _description(fetched)) if d]
        text = _link(fetched)
        if details:
            text += " - " + " / ".join(details)
        return _list_item("- ", text)


class MarkdownListDetailRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        buffer = StringIO()

        print(f"- {_link(fetched)}", file=buffer)

        if price := _price(fetched):
            print(_list_item("  - ", price), file=buffer)

        if description := _description(fetched):
            print(_list_item("  - ", description), file=buffer)

        return buffer.getvalue()
