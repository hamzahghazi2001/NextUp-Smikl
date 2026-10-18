from fastapi import APIRouter

from . import catalog_source, contract
from .models import CatalogResponse, Manifest

router = APIRouter()


@router.get("/manifest.json", response_model=Manifest, response_model_exclude_none=True)
async def manifest():
    return {
        "id": contract.ADDON_ID,
        "version": contract.ADDON_VERSION,
        "name": contract.ADDON_NAME,
        "description": contract.ADDON_DESCRIPTION,
        "resources": contract.ADDON_RESOURCES,
        "types": contract.ADDON_TYPES,
        "catalogs": [contract.ADDON_CATALOG],
    }


@router.get(
    f"/catalog/{contract.CATALOG_TYPE}/{contract.CATALOG_ID}.json",
    response_model=CatalogResponse,
    response_model_exclude_none=True,
)
async def manifest_catlog():
    return {"metas": catalog_source.get_metas()}
