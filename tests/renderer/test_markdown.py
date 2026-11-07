from xfetch.models import Article, Product
from xfetch.renderer.markdown import (
    MarkdownHeadingRenderer,
    MarkdownLinkRenderer,
    MarkdownListRenderer,
)

URL = "https://example.com/foo"


def test_link_falls_back_to_bare_url_when_name_is_missing() -> None:
    article = Article(url=URL)
    assert MarkdownLinkRenderer().render(article) == f"<{URL}>"


def test_link_uses_name_when_present() -> None:
    article = Article(url=URL, name="Title")
    assert MarkdownLinkRenderer().render(article) == f"[Title]({URL})"


def test_heading_renders_without_name() -> None:
    article = Article(url=URL, description="Hello")
    assert MarkdownHeadingRenderer().render(article) == f"# <{URL}>\n\n- Hello\n"


def test_list_renders_without_name() -> None:
    product = Product(url=URL, price=1200)
    assert MarkdownListRenderer().render(product) == f"- <{URL}>\n- Price: 1200 JPY\n"
