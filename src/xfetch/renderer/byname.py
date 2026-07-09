from typing import Literal

from xfetch.models import Fetched
from xfetch.renderer.base import BaseRenderer
from xfetch.renderer.basic import JsonRenderer
from xfetch.renderer.markdown import (
    MarkdownDefinitionListRenderer,
    MarkdownHeadingContentRenderer,
    MarkdownHeadingRenderer,
    MarkdownLinkRenderer,
    MarkdownListDetailRenderer,
    MarkdownListRenderer,
)

Name = Literal[
    "markdown-heading",
    "markdown-heading-content",
    "markdown-link",
    "markdown-definition-list",
    "markdown-list",
    "markdown-list-detail",
    "json",
]


def render(fetched: Fetched, name: Name) -> str:
    return get_renderer(name)().render(fetched)


def get_renderer(name: Name) -> type[BaseRenderer]:
    match name:
        case "json":
            return JsonRenderer
        case "markdown-heading":
            return MarkdownHeadingRenderer
        case "markdown-heading-content":
            return MarkdownHeadingContentRenderer
        case "markdown-link":
            return MarkdownLinkRenderer
        case "markdown-definition-list":
            return MarkdownDefinitionListRenderer
        case "markdown-list":
            return MarkdownListRenderer
        case "markdown-list-detail":
            return MarkdownListDetailRenderer
    raise ValueError(f"Unknown renderer name: {name}")
