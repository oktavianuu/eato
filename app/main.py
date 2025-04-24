from fastapi import FastAPI
from app.routers import menu, order, inventory

app = FastAPI(title="EATO")

# Include routers
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
