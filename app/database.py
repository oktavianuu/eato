from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./eato.db"  # Later: PostgreSQL when scaling
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # SQLite only
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Dependency that provides a SQLAlchemy session and ensures it's closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()