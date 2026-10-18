from fastapi import FastAPI
from . import catalog_source, contract
from fastapi.middleware.cors import CORSMiddleware
from .models import Manifest, CatalogResponse 


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/manifest.json", response_model=Manifest, response_model_exclude_none=True)
async def manifest():
    return {
        "id": contract.ADDON_ID,
        "version": contract.ADDON_VERSION,
        "name": contract.ADDON_NAME,
        "description": contract.ADDON_DESCRIPTION,
        "resources": contract.ADDON_RESOURCES,      
        "types": contract.ADDON_TYPES,
        "catalogs": [contract.ADDON_CATALOG]       
    }

@app.get(f"/catalog/{contract.CATALOG_TYPE}/{contract.CATALOG_ID}.json", response_model=CatalogResponse, response_model_exclude_none=True)
async def manifest():
    return {"metas": catalog_source.get_metas()}