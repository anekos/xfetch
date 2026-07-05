import re

from dictlib import dig
from diskcache import Cache
from zyte_api import ZyteAPI

from xfetch.models import Fetched, Product
from xfetch.paths import ZYTE_CACHE_PATH
from xfetch.secrets import ZYTE_API_KEY

ZYTE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
_cache = Cache(str(ZYTE_CACHE_PATH))


def fetch(url: str) -> Fetched:
    if url in _cache:
        response = _cache.get(url)
    else:
        client = ZyteAPI(api_key=ZYTE_API_KEY)
        response = client.get(
            {
                "url": url,
                "product": True,
            }
        )
        _cache.set(url, response)

    p = response["product"]

    return Product(
        name=p["name"],
        url=cleanup_url(p["canonicalUrl"]),
        thumbnail_url=dig(p, "mainImage.url"),
        price=p.get("regularPrice"),
        currency=p.get("currency"),
        raw=response,
    )


def cleanup_url(url: str) -> str:
    if match := re.search(r"^https://www\.amazon\.co\.jp/[^/]+/dp/([A-Z0-9]+)", url):
        asin = match.group(1)
        return f"https://www.amazon.co.jp/dp/{asin}"
    return url
