import pytest
from httpx import AsyncClient
from fastapi import status

from app.core.config import get_settings

settings = get_settings()

pytestmark = pytest.mark.asyncio

async def test_create_user(test_client):
    """Test creating a new user."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = test_client.post("/api/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "password" not in data  # Password should not be in response

async def test_get_user(test_client, test_db):
    """Test getting a user by ID."""
    # First create a user
    user_data = {
        "email": "get@example.com",
        "password": "testpassword123",
        "full_name": "Get Test User"
    }
    create_response = test_client.post("/api/users/", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]
    
    # Now try to get the user
    response = test_client.get(f"/api/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "password" not in data

async def test_get_user_not_found(test_client):
    """Test getting a non-existent user."""
    response = test_client.get("/api/users/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_update_user(test_client, test_db):
    """Test updating a user."""
    # First create a user
    user_data = {
        "email": "update@example.com",
        "password": "testpassword123",
        "full_name": "Update Test User"
    }
    create_response = test_client.post("/api/users/", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]
    
    # Update the user
    update_data = {
        "full_name": "Updated Name"
    }
    response = test_client.patch(f"/api/users/{user_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["email"] == user_data["email"]  # Email should remain unchanged 