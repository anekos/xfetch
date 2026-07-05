import re

from dictlib import dig
from zyte_api import ZyteAPI

from xfetch.cache import ZyteCache
from xfetch.fetcher.base import BaseFetcher
from xfetch.models import Fetched, Product
from xfetch.secrets import ZYTE_API_KEY


class AmazonFetcher(BaseFetcher):
    def fetch(self, url: str) -> Fetched:
        if url in ZyteCache:
            response = ZyteCache.get(url)
        else:
            client = ZyteAPI(api_key=ZYTE_API_KEY)
            response = client.get(
                {
                    "url": url,
                    "product": True,
                }
            )
            ZyteCache.set(url, response)

        p = response["product"]

        return Product(
            name=p["name"],
            url=self.cleanup_url(p["canonicalUrl"]),
            thumbnail_url=dig(p, "mainImage.url"),
            price=p.get("regularPrice"),
            currency=p.get("currency"),
            raw=response,
        )

    def cleanup_url(self, url: str) -> str:
        if match := re.search(
            r"^https://www\.(amazon\.[a-z.]+)/[^/]+/dp/([A-Z0-9]+)", url
        ):
            domain = match.group(1)
            asin = match.group(2)
            return f"https://www.{domain}/dp/{asin}"
        return url
