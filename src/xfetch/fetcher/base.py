from abc import ABC, abstractmethod

from xfetch.models import Fetched


class BaseFetcher(ABC):
    @abstractmethod
    def fetch(self, url: str) -> Fetched:
        pass
