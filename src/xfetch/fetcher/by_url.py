from urllib.parse import urlparse

from xfetch.fetcher.base import BaseFetcher
from xfetch.fetcher.site.amazon import AmazonFetcher
from xfetch.fetcher.site.common import CommonFetcher
from xfetch.models import Fetched


def fetch(url: str) -> Fetched:
    return get_fetcher(url)().fetch(url)


def get_fetcher(url: str) -> type[BaseFetcher]:
    hostname = urlparse(url).hostname or ""
    if hostname == "amazon.co.jp" or hostname.endswith(".amazon.co.jp"):
        return AmazonFetcher
    return CommonFetcher
