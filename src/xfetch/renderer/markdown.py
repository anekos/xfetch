from io import StringIO

from xfetch.models import Fetched, Product
from xfetch.renderer.base import BaseRenderer


class MarkdownHeadingRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        buffer = StringIO()

        print(f"# [{fetched.name}]({fetched.url})", file=buffer)
        print("", file=buffer)

        if isinstance(fetched, Product):
            if fetched.thumbnail_url is not None:
                print(
                    f"[![{fetched.thumbnail_url}]({fetched.thumbnail_url})]({fetched.url})",
                    file=buffer,
                )
            if fetched.price is not None:
                print(f"- Price: {fetched.price}", end="", file=buffer)
                if fetched.currency is not None:
                    print(f" {fetched.currency}", end="", file=buffer)
                print("", file=buffer)

        return buffer.getvalue()
