import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.base import Base
from main import app

settings = get_settings()

# Create async test engine
test_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=True,
)

# Create async session for testing
async_session = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db():
    """Create test database."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def db_session():
    """Get async session for each test function."""
    async with async_session() as session:
        yield session
        await session.rollback()
        await session.close()

@pytest.fixture(scope="module")
def test_client():
    """Create a test client for API testing."""
    with TestClient(app) as client:
        yield client 