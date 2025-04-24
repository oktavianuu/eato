from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ---------------------------------------------------
# MenuItem Schemas
# ---------------------------------------------------
class MenuItemBase(BaseModel):
    # Shared properties for reading and creating menu items
    name: str                   # Name of the dish or drink
    price: float                # Price in the local currency
    category: str               # Category grouping (e.g., 'Food', 'Drink')
    available: Optional[bool] = True  # Whether item is visible/available on menu
    ingredients: Optional[str] = None # Optional list or JSON string of ingredients

class MenuItemCreate(MenuItemBase):
    # Inherits all fields from MenuItemBase for creation
    pass

class MenuItem(MenuItemBase):
    # Response schema includes the database-generated ID
    id: int

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------
# OrderItem Schemas (junction between orders and menu items)
# ---------------------------------------------------
class OrderItemBase(BaseModel):
    menu_item_id: int           # ID of the menu item being ordered
    quantity: int               # Quantity of the item in this order

class OrderItemCreate(OrderItemBase):
    # For creating new OrderItem records
    pass

class OrderItem(OrderItemBase):
    id: int                     # Database-generated ID for each order line

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------
# Order Schemas
# ---------------------------------------------------
class OrderBase(BaseModel):
    # Shared properties for reading and creating orders
    customer_name: Optional[str] = None   # Optional name for dine-in or pickup
    table_number: Optional[int] = None    # Table number if dine-in

class OrderCreate(OrderBase):
    # Creation schema includes list of order items
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int                     # Database-generated order ID
    status: str                 # Current status: Received, In Kitchen, Ready
    timestamp: datetime         # When the order was placed
    items: List[OrderItem]      # Nested list of ordered items

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------
# InventoryItem Schemas
# ---------------------------------------------------
class InventoryItemBase(BaseModel):
    name: str                   # Ingredient or stock item name
    quantity: float             # Current amount in stock
    unit: str                   # Unit of measurement (kg, pcs, liters)
    threshold: Optional[float] = 10.0  # Alert threshold for low stock

class InventoryItemCreate(InventoryItemBase):
    # Schema for creating new inventory records
    pass

class InventoryItem(InventoryItemBase):
    id: int                     # Database-generated ID for each stock item

    model_config = {
        "from_attributes": True
    }
