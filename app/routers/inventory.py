# eato/app/routers/inventory.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Health-check for Inventory router")
async def inventory_root():
    return {"message": "Inventory router is live!"}
