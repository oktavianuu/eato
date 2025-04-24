from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# MENU ITEM MODEL 🍜
class MenuItem(Base):
    __tablename__ = "menu_items"  # Table name in the DB

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each item
    name = Column(String, index=True)  # Dish name
    price = Column(Float)  # Price of the dish
    category = Column(String)  # "Food", "Drink", etc.
    available = Column(Boolean, default=True)  # Show on menu or not
    ingredients = Column(String)  # Optional: List of ingredients (JSON/text)

    # Relationship to OrderItems (many-to-many via order_items table)
    orders = relationship("OrderItem", back_populates="menu_item")


# ORDER MODEL 📦
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)  # Unique order ID
    customer_name = Column(String, nullable=True)  # Optional customer name
    table_number = Column(Integer, nullable=True)  # For dine-in orders
    status = Column(String, default="Received")  # "Received", "In Kitchen", "Ready"
    timestamp = Column(DateTime, default=datetime.utcnow)  # Order time

    # Relationship to OrderItems
    items = relationship("OrderItem", back_populates="order")


# ORDER ITEM MODEL 📝 (linking orders to menu items, for many-to-many)
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))  # Link to Order
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))  # Link to MenuItem
    quantity = Column(Integer)  # Quantity of this item in the order

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="orders")


# INVENTORY MODEL 🌶️
class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Ingredient name
    quantity = Column(Float)  # Current amount in stock
    unit = Column(String)  # "kg", "pcs", "liters", etc.
    threshold = Column(Float, default=10.0)  # When to trigger low stock alert
