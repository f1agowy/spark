from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from database.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./spark.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Get database session"""
    return SessionLocal()
