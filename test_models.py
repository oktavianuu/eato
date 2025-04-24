# test_models.py

import pytest
from sqlalchemy import create_engine, inspect
from app.database import Base
import app.models   # this loads all your model classes

@pytest.fixture(scope="module")
def engine():
    # in-memory SQLite = zero-configuration, super-fast
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    # create all tables defined on Base
    Base.metadata.create_all(bind=engine)
    return engine

def test_table_names(engine):
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    expected = {"menu_items", "orders", "order_items", "inventory_items"}
    assert tables == expected, f"Tables {tables} != expected {expected}"
