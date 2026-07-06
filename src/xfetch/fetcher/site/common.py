from dictlib import dig
from zyte_api import ZyteAPI

from xfetch.cache import ZyteCache
from xfetch.fetcher.base import BaseFetcher
from xfetch.models import Article, Fetched
from xfetch.secrets import ZYTE_API_KEY


class CommonFetcher(BaseFetcher):
    def fetch(self, url: str) -> Fetched:
        if url in ZyteCache:
            response = ZyteCache.get(url)
        else:
            client = ZyteAPI(api_key=ZYTE_API_KEY)
            response = client.get(
                {
                    "url": url,
                    "article": True,
                }
            )
            ZyteCache.set(url, response)

        a = response["article"]

        return Article(
            content=a.get("articleBody"),
            description=a.get("description"),
            name=a["headline"],
            raw=response,
            thumbnail_url=dig(a, "mainImage.url"),
            url=a.get("canonicalUrl", url),
        )
