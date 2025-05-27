from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings

settings = get_settings()

# PostgreSQL configuration
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MongoDB configuration
mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
mongodb = mongo_client[settings.MONGODB_DB]


def get_db() -> Generator:
    """
    Get SQLAlchemy database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mongodb() -> AsyncIOMotorClient:
    """
    Get MongoDB client.
    
    Returns:
        AsyncIOMotorClient: MongoDB client
    """
    return mongodb 