import pytest
from typing import AsyncGenerator, Generator
from fastapi import FastAPI
from httpx import AsyncClient

from app.core.config import get_settings
from main import app

settings = get_settings()

@pytest.fixture(scope="module")
def test_app() -> Generator[FastAPI, None, None]:
    """
    Create a fresh database on each test case.
    """
    yield app

@pytest.fixture(scope="module")
async def async_client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async client for testing.
    """
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
async def clean_db(db_session):
    """
    Clean database after each test.
    Ensures test isolation.
    """
    yield db_session
    # Clean up logic here
    tables = ['users']  # Add more tables as needed
    for table in tables:
        await db_session.execute(f'TRUNCATE TABLE {table} CASCADE')
    await db_session.commit() 