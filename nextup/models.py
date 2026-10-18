from typing import List

from pydantic import BaseModel


class CatalogEntry(BaseModel):
    type: str
    id: str
    name: str


class Manifest(BaseModel):
    id: str
    version: str
    name: str
    description: str
    resources: List[str]
    types: List[str]
    catalogs: List[CatalogEntry]


class MetaPreview(BaseModel):
    id: str
    type: str
    name: str
    poster: str
    posterShape: str | None = None


class CatalogResponse(BaseModel):
    metas: List[MetaPreview] | None
