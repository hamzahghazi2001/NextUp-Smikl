from fastapi import FastAPI
from . import contract
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/manifest.json")
def manifest():
    return {
        "id": contract.ADDON_ID,
        "version": contract.ADDON_VERSION,
        "name": contract.ADDON_NAME,
        "description": contract.ADDON_DESCRIPTION,
        "resources": contract.ADDON_RESOURCES,      
        "types": contract.ADDON_TYPES,
        "catalogs": [contract.ADDON_CATALOG]       
    }