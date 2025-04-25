# eato/app/routers/inventory.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
from app.database import get_db   # our shared dependency

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    responses={404: {"description": "Not Found"}}
)

@router.post("/", response_model=schemas.InventoryItem, status_code=201)
async def create_inventory(
    item: schemas.InventoryItemCreate,
    db: Session = Depends(get_db),
    ):
    """
    Add a new ingredient to inventory.
    """
    return crud.create_inventory_item(db, item)

@router.get("/", response_model=List[schemas.InventoryItem])
async def read_inventory(skip: int = 0, limit: int = 100,
                         db: Session = Depends(get_db)):
    """
    List inventory items with pagination.
    """
    return crud.get_inventory_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.InventoryItem)
async def read_inventory_item(item_id: int,
                              db: Session = Depends(get_db)):
    """
    Fetch one inventory item by ID, 404 if not found.
    """
    db_item = crud.get_inventory_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.InventoryItem)
async def update_inventory(item_id: int,
                           item: schemas.InventoryItemCreate,
                           db: Session = Depends(get_db)):
    """
    Update an existing inventory item.
    """
    db_item = crud.update_inventory_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_item

@router.delete("/{item_id}", status_code=204)
async def delete_inventory(item_id: int,
                           db: Session = Depends(get_db)):
    """
    Delete an inventory item by ID.
    """
    success = crud.delete_inventory_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Inventory item not found")
