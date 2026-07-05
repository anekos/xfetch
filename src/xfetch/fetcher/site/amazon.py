import re

from dictlib import dig
from zyte_api import ZyteAPI

from xfetch.cache import ZyteCache
from xfetch.fetcher.base import BaseFetcher
from xfetch.models import Book, Fetched, Product
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

        props = p["additionalProperties"]
        pages: int | None = None
        for prop in props:
            if m := re.search(r"([,\d]+)\s*ページ", prop["value"]):
                pages = int(re.sub(",", "", m.group(1)))

        base = dict(
            currency=p.get("currency"),
            description=p.get("description"),
            name=p["name"],
            price=(p.get("price") or p.get("regularPrice")),
            thumbnail_url=dig(p, "mainImage.url"),
            url=cleanup_url(p["canonicalUrl"]),
            raw=response,
        )

        if pages is not None:
            return Book(pages=pages, **base)

        return Product(**base)


def cleanup_url(url: str) -> str:
    if match := re.search(r"^https://www\.(amazon\.[a-z.]+)/[^/]+/dp/([A-Z0-9]+)", url):
        domain = match.group(1)
        asin = match.group(2)
        return f"https://www.{domain}/dp/{asin}"
    return url
