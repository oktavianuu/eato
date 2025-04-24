# eato/app/routers/menu.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Health-check for Menu router")
async def menu_root():
    return {"message": "Menu router is live!"}
