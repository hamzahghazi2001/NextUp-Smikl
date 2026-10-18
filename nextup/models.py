from pydantic import BaseModel
from typing import List

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
