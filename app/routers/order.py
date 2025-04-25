# ---------------------------------------------------
# app/routers/order.py
# ---------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import app.crud as crud
import app.schemas as schemas
from app.database import get_db

# Reuse get_db for DB sessions
router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not Found"}},
)

@router.post("/", response_model=schemas.Order, status_code=201)
async def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    ):
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
