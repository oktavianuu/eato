from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# ---------------------------------------------------
# MenuItem: represents a dish or drink available to order
# ---------------------------------------------------
class MenuItem(Base):
    __tablename__ = "menu_items"  # Table name in the database

    # Unique identifier for each menu item
    id = Column(Integer, primary_key=True, index=True)
    # Name of the dish or drink (e.g., 'Cappuccino', 'Nasi Goreng')
    name = Column(String, nullable=False, index=True)
    # Price in the local currency
    price = Column(Float, nullable=False)
    # Category grouping (e.g., 'Food', 'Drink', 'Dessert')
    category = Column(String, nullable=False)
    # If False, item is hidden/sold-out on the menu
    available = Column(Boolean, default=True, nullable=False)
    # JSON-encoded string or comma-separated list of ingredients
    ingredients = Column(String, nullable=True)

    # Relationship to OrderItem: one menu item may appear in many orders
    orders = relationship("OrderItem", back_populates="menu_item")


# ---------------------------------------------------
# Order: represents a customer order
# ---------------------------------------------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)  # Unique order ID
    # Optional customer name (dine-in or pickup)
    customer_name = Column(String, nullable=True)
    # Table number for dine-in orders
    table_number = Column(Integer, nullable=True)
    # Order status: Received -> In Kitchen -> Ready
    status = Column(String, default="Received", nullable=False)
    # Timestamp when the order was created (UTC by default)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship to OrderItem: one order can contain multiple items
    items = relationship("OrderItem", back_populates="order")


# ---------------------------------------------------
# OrderItem: junction table linking orders and menu items
# ---------------------------------------------------
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    # Foreign key linking to Order
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    # Foreign key linking to MenuItem
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    # Quantity of this menu item in the order
    quantity = Column(Integer, nullable=False)

    # Relationships for easy ORM navigation
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="orders")


# ---------------------------------------------------
# InventoryItem: tracks raw ingredients or stock
# ---------------------------------------------------
class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)  # Unique ingredient ID
    # Ingredient name (e.g., 'Chicken Breast', 'Espresso Beans')
    name = Column(String, nullable=False, index=True)
    # Current stock quantity
    quantity = Column(Float, nullable=False)
    # Unit of measurement (e.g., 'kg', 'pcs', 'liters')
    unit = Column(String, nullable=False)
    # Threshold to trigger a low-stock alert
    threshold = Column(Float, default=10.0)
