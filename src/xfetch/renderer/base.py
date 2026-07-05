from abc import ABC, abstractmethod

from xfetch.models import Fetched


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, fetched: Fetched) -> str:
        pass
