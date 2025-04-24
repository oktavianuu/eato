from fastapi import FastAPI
from app.database import engine, Base
import app.models # ensure ORM classes are loaded

app = FastAPI(title="EATO")

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

from app.routers import menu, order, inventory

# Include routers
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(order.router, prefix="/orders", tags=["Orders"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])

