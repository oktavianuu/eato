# ---------------------------------------------------
# app/routers/menu.py
# ---------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
from app.database import SessionLocal

# Dependency: create a DB session per request, then close
# This ensures each API call has its own session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# APIRouter groups all /menu endpoints together
router = APIRouter(
    prefix="/menu",
    tags=["Menu"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/", response_model=schemas.MenuItem, status_code=201)
async def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    """
    Create a new menu item.
    - item: validated payload from MenuItemCreate schema.
    - db: database session injected.
    Returns the created MenuItem with its generated ID.
    """
    return crud.create_menu_item(db, item)

@router.get("/", response_model=List[schemas.MenuItem])
async def read_menu_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List menu items with pagination.
    - skip: number of records to skip
    - limit: max number of records to return
    """
    return crud.get_menu_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.MenuItem)
async def read_menu_item(item_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single menu item by ID.
    Raises 404 if not found.
    """
    db_item = crud.get_menu_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.MenuItem)
async def update_menu_item(item_id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    """
    Update an existing menu item.
    Returns updated item or 404 if not found.
    """
    db_item = crud.update_menu_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_item

@router.delete("/{item_id}", status_code=204)
async def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a menu item by ID.
    Returns 204 No Content on success, or 404 if not found.
    """
    success = crud.delete_menu_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")


# ---------------------------------------------------
# app/routers/order.py
# ---------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
from app.database import SessionLocal

# Reuse get_db for DB sessions
router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/", response_model=schemas.Order, status_code=201)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Place a new order with nested items.
    - Validates items with OrderItemCreate schema.
    - Returns the full Order with items.
    """
    return crud.create_order(db, order)

@router.get("/", response_model=List[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List orders with pagination.
    """
    return crud.get_orders(db, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single order by ID, including its items.
    Raises 404 if not found.
    """
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}/status", response_model=schemas.Order)
async def update_status(order_id: int, status: str, db: Session = Depends(get_db)):
    """
    Update only the status of an existing order.
    """
    db_order = crud.update_order_status(db, order_id, status)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


# ---------------------------------------------------
# app/routers/inventory.py
# ---------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
from app.database import SessionLocal

# Reuse get_db for DB sessions
router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/", response_model=schemas.InventoryItem, status_code=201)
async def create_inventory(item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    """
    Add a new ingredient to inventory.
    """
    return crud.create_inventory_item(db, item)

@router.get("/", response_model=List[schemas.InventoryItem])
async def read_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List inventory items with pagination.
    """
    return crud.get_inventory_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.InventoryItem)
async def read_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single inventory item by ID. 404 if missing.
    """
    db_item = crud.get_inventory_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.InventoryItem)
async def update_inventory(item_id: int, item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    """
    Update an existing inventory record.
    """
    db_item = crud.update_inventory_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_item

@router.delete("/{item_id}", status_code=204)
async def delete_inventory(item_id: int, db: Session = Depends(get_db)):
    """
    Remove an inventory item. Returns 204 on success.
    """
    success = crud.delete_inventory_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory item not found")
