from typing import Literal, cast, get_args

from xfetch.models import Fetched
from xfetch.renderer.base import BaseRenderer
from xfetch.renderer.basic import JsonRenderer
from xfetch.renderer.markdown import (
    MarkdownDefinitionListRenderer,
    MarkdownHeadingContentRenderer,
    MarkdownHeadingQuotedRenderer,
    MarkdownHeadingRenderer,
    MarkdownLinkRenderer,
    MarkdownListDetailRenderer,
    MarkdownListRenderer,
)

Name = Literal[
    "markdown-heading",
    "markdown-heading-content",
    "markdown-heading-quoted",
    "markdown-link",
    "markdown-definition-list",
    "markdown-list",
    "markdown-list-detail",
    "json",
]


def _initials(name: str) -> str:
    return "".join(word[0] for word in name.split("-"))


def resolve_name(name: str) -> Name:
    names = get_args(Name)
    if name in names:
        return cast(Name, name)
    matches = [n for n in names if _initials(n) == name]
    if len(matches) == 1:
        return cast(Name, matches[0])
    if matches:
        raise ValueError(f"Ambiguous format name: {name} ({', '.join(matches)})")
    raise ValueError(f"Unknown format name: {name}")


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
        case "markdown-heading-quoted":
            return MarkdownHeadingQuotedRenderer
        case "markdown-link":
            return MarkdownLinkRenderer
        case "markdown-definition-list":
            return MarkdownDefinitionListRenderer
        case "markdown-list":
            return MarkdownListRenderer
        case "markdown-list-detail":
            return MarkdownListDetailRenderer
    raise ValueError(f"Unknown renderer name: {name}")
