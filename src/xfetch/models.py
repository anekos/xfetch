from abc import ABC
from typing import Any

from pydantic import BaseModel


class Fetched(BaseModel, ABC):
    url: str
    name: str
    raw: Any | None


class Article(Fetched):
    url: str
    name: str
    content: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    raw: Any | None = None


class Product(Article):
    url: str
    name: str
    price: float | None = None
    currency: str = "JPY"
    description: str | None = None
    thumbnail_url: str | None = None
    raw: Any | None = None
