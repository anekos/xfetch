from io import StringIO

from xfetch.format import format_price
from xfetch.models import Article, Fetched, Product
from xfetch.renderer.base import BaseRenderer


def _is_cjk(ch: str) -> bool:
    cp = ord(ch)
    return (
        0x3000 <= cp <= 0x9FFF
        or 0xF900 <= cp <= 0xFAFF
        or 0xFF00 <= cp <= 0xFFEF
        or 0x20000 <= cp <= 0x2FA1F
    )


def _join_lines(text: str) -> str:
    lines = text.split("\n")
    result = lines[0]
    for line in lines[1:]:
        if result and line and not _is_cjk(result[-1]) and not _is_cjk(line[0]):
            result += " "
        result += line
    return result


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
    if not isinstance(fetched, Article) or fetched.description is None:
        return None
    return _join_lines(fetched.description)


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
            print(f"- {price}", file=buffer)

        if description := _description(fetched):
            print(f"- {description}", file=buffer)

        return buffer.getvalue()


class MarkdownHeadingContentRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        buffer = StringIO()

        print(f"# {_link(fetched)}", file=buffer)
        print("", file=buffer)

        if isinstance(fetched, Article) and fetched.thumbnail_url is not None:
            print(
                f"[![{fetched.thumbnail_url}]({fetched.thumbnail_url})]({fetched.url})",
                file=buffer,
            )

        if isinstance(fetched, Article) and fetched.description is not None:
            print(fetched.description, file=buffer)

        if price := _price(fetched):
            print("", file=buffer)
            print(f"- {price}", file=buffer)

        return buffer.getvalue()


class MarkdownHeadingQuotedRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        buffer = StringIO()

        print(f"# {_link(fetched)}", file=buffer)
        print("", file=buffer)

        if isinstance(fetched, Article) and fetched.thumbnail_url is not None:
            print(
                f"[![{fetched.thumbnail_url}]({fetched.thumbnail_url})]({fetched.url})",
                file=buffer,
            )

        if isinstance(fetched, Article) and fetched.description is not None:
            for line in fetched.description.split("\n"):
                print(f"> {line.strip()}".rstrip(), file=buffer)

        if price := _price(fetched):
            print("", file=buffer)
            print(f"- {price}", file=buffer)

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
        buffer = StringIO()

        print(f"- {_link(fetched)}", file=buffer)

        if price := _price(fetched):
            print(f"- {price}", file=buffer)

        if description := _description(fetched):
            print(f"- {description}", file=buffer)

        return buffer.getvalue()


class MarkdownListDetailRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        buffer = StringIO()

        print(f"- {_link(fetched)}", file=buffer)

        if price := _price(fetched):
            print(f"  - {price}", file=buffer)

        if description := _description(fetched):
            print(f"  - {description}", file=buffer)

        return buffer.getvalue()
