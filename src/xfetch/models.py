from abc import ABC
from typing import Any

from pydantic import BaseModel


class Fetched(BaseModel, ABC):
    url: str
    name: str
    raw: Any | None


class Product(Fetched):
    url: str
    name: str
    price: float | None = None
    currency: str = "JPY"
    description: str | None = None
    thumbnail_url: str | None = None
    raw: Any | None = None
