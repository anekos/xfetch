from xfetch.models import Fetched
from xfetch.renderer.base import BaseRenderer


class JsonRenderer(BaseRenderer):
    def render(self, fetched: Fetched) -> str:
        return fetched.model_dump_json(indent=2, ensure_ascii=False)
