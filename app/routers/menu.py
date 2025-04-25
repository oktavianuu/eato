# ---------------------------------------------------
# app/routers/menu.py
# ---------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
from app.database import get_db

# APIRouter groups all /menu endpoints together
router = APIRouter(
    prefix="/menu",
    tags=["Menu"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/", response_model=schemas.MenuItem, status_code=201)
async def create_menu_item(
    item: schemas.MenuItemCreate, 
    db: Session = Depends(get_db),
    ):
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