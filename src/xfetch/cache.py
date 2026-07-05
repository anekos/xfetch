from diskcache import Cache as DiskCache

from xfetch.paths import ZYTE_CACHE_PATH

ZYTE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
ZyteCache = DiskCache(str(ZYTE_CACHE_PATH))
