from pathlib import Path

from platformdirs import user_cache_path

_APP_NAME = "xfetch"
_APP_AUTHOR = "anekos"


CACHE_DIR = Path(user_cache_path(_APP_NAME, _APP_AUTHOR))
ZYTE_CACHE_PATH = CACHE_DIR / "zyte"
