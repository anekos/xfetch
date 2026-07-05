from typing import Literal

from xfetch.models import Fetched
from xfetch.renderer.base import BaseRenderer
from xfetch.renderer.basic import JsonRenderer
from xfetch.renderer.markdown import MarkdownHeadingRenderer

Name = Literal["markdown-heading", "json"]


def render(fetched: Fetched, name: Name) -> str:
    return get_renderer(name)().render(fetched)


def get_renderer(name: Name) -> type[BaseRenderer]:
    match name:
        case "json":
            return JsonRenderer
        case "markdown-heading":
            return MarkdownHeadingRenderer
    raise ValueError(f"Unknown renderer name: {name}")
