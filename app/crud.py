from sqlalchemy.orm import Session
from typing import List
import app.models as models
import app.schemas as schemas

# --------------------
# MENU CRUD
# --------------------

def get_menu_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.MenuItem]:
    """Retrieve a list of menu items with pagination."""
    return db.query(models.MenuItem).offset(skip).limit(limit).all()


def get_menu_item(db: Session, item_id: int) -> models.MenuItem:
    """Retrieve a single menu item by ID."""
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()


def create_menu_item(db: Session, item: schemas.MenuItemCreate) -> models.MenuItem:
    """Create a new menu item from a schema."""
    db_item = models.MenuItem(
        name=item.name,
        price=item.price,
        category=item.category,
        available=item.available,
        ingredients=item.ingredients,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # load generated ID
    return db_item


def update_menu_item(db: Session, item_id: int, item: schemas.MenuItemCreate) -> models.MenuItem:
    """Update an existing menu item."""
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not db_item:
        return None
    for field, value in item.dict().items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_menu_item(db: Session, item_id: int) -> bool:
    """Delete a menu item by ID."""
    deleted = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).delete()
    if deleted:
        db.commit()
        return True
    return False

# --------------------
# ORDER CRUD
# --------------------

def create_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """Create a new order with associated order items."""
    db_order = models.Order(
        customer_name=order.customer_name,
        table_number=order.table_number,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # add items
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int) -> models.Order:
    """Retrieve an order by ID, including its items."""
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[models.Order]:
    """Retrieve a list of orders with pagination."""
    return db.query(models.Order).offset(skip).limit(limit).all()


def update_order_status(db: Session, order_id: int, status: str) -> models.Order:
    """Update only the status field of an order."""
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return None
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

# --------------------
# INVENTORY CRUD
# --------------------

def get_inventory_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.InventoryItem]:
    """Retrieve a list of inventory items."""
    return db.query(models.InventoryItem).offset(skip).limit(limit).all()


def get_inventory_item(db: Session, item_id: int) -> models.InventoryItem:
    """Retrieve a single inventory item by ID."""
    return db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()


def create_inventory_item(db: Session, item: schemas.InventoryItemCreate) -> models.InventoryItem:
    """Create a new inventory record."""
    db_item = models.InventoryItem(
        name=item.name,
        quantity=item.quantity,
        unit=item.unit,
        threshold=item.threshold,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_inventory_item(db: Session, item_id: int, item: schemas.InventoryItemCreate) -> models.InventoryItem:
    """Update an existing inventory item."""
    db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if not db_item:
        return None
    for field, value in item.dict().items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_inventory_item(db: Session, item_id: int) -> bool:
    """Delete an inventory record."""
    deleted = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).delete()
    if deleted:
        db.commit()
        return True
    return False
