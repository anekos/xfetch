from abc import ABC
from typing import Any

from pydantic import BaseModel


class Fetched(BaseModel, ABC):
    url: str
    name: str | None = None
    raw: Any | None


class Article(Fetched):
    url: str
    name: str | None = None
    content: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    raw: Any | None = None


class Product(Article):
    url: str
    name: str | None = None
    price: float | None = None
    currency: str | None = "JPY"
    description: str | None = None
    thumbnail_url: str | None = None
    raw: Any | None = None


class Book(Product):
    url: str
    name: str | None = None
    price: float | None = None
    currency: str | None = "JPY"
    description: str | None = None
    thumbnail_url: str | None = None
    pages: int | None = None
    raw: Any | None = None
