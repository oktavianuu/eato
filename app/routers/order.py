# eato/app/routers/order.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Health-check for Orders router")
async def orders_root():
    return {"message": "Orders router is live!"}
