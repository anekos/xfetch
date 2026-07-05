from abc import ABC
from typing import Any

from pydantic import BaseModel


class Fetched(ABC):
    url: str
    raw: Any | None


class Product(Fetched, BaseModel):
    url: str
    name: str
    price: float | None = None
    currency: str = "JPY"
    description: str | None = None
    thumbnail_url: str | None = None
    raw: Any | None = None
