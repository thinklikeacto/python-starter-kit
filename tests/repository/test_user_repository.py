import pytest
from sqlalchemy import select

from app.models.user import User
from app.repository.user_repository import UserRepository

pytestmark = pytest.mark.asyncio

async def test_create_user(db_session):
    """Test creating a user through repository."""
    repo = UserRepository(db_session)
    user_data = {
        "email": "repo_test@example.com",
        "hashed_password": "hashed_password_here",
        "full_name": "Repository Test User",
        "is_active": True
    }
    
    user = User(**user_data)
    created_user = await repo.create(user)
    
    assert created_user.id is not None
    assert created_user.email == user_data["email"]
    assert created_user.full_name == user_data["full_name"]
    
    # Verify user was actually saved to DB
    result = await db_session.execute(select(User).where(User.id == created_user.id))
    db_user = result.scalar_one()
    assert db_user is not None
    assert db_user.email == user_data["email"]

async def test_get_user_by_email(db_session):
    """Test getting a user by email."""
    repo = UserRepository(db_session)
    user_data = {
        "email": "get_by_email@example.com",
        "hashed_password": "hashed_password_here",
        "full_name": "Get By Email User",
        "is_active": True
    }
    
    # First create a user
    user = User(**user_data)
    await repo.create(user)
    
    # Try to get the user by email
    found_user = await repo.get_by_email(user_data["email"])
    assert found_user is not None
    assert found_user.email == user_data["email"]
    assert found_user.full_name == user_data["full_name"]

async def test_get_user_by_email_not_found(db_session):
    """Test getting a non-existent user by email."""
    repo = UserRepository(db_session)
    user = await repo.get_by_email("nonexistent@example.com")
    assert user is None

async def test_update_user(db_session):
    """Test updating a user."""
    repo = UserRepository(db_session)
    user_data = {
        "email": "update_repo@example.com",
        "hashed_password": "hashed_password_here",
        "full_name": "Update Repo User",
        "is_active": True
    }
    
    # Create user
    user = User(**user_data)
    created_user = await repo.create(user)
    
    # Update user
    created_user.full_name = "Updated Repository Name"
    updated_user = await repo.update(created_user)
    
    assert updated_user.full_name == "Updated Repository Name"
    assert updated_user.email == user_data["email"]  # Should remain unchanged
    
    # Verify changes in DB
    result = await db_session.execute(select(User).where(User.id == created_user.id))
    db_user = result.scalar_one()
    assert db_user.full_name == "Updated Repository Name"

async def test_delete_user(db_session):
    """Test deleting a user."""
    repo = UserRepository(db_session)
    user_data = {
        "email": "delete@example.com",
        "hashed_password": "hashed_password_here",
        "full_name": "Delete Test User",
        "is_active": True
    }
    
    # Create user
    user = User(**user_data)
    created_user = await repo.create(user)
    
    # Delete user
    await repo.delete(created_user.id)
    
    # Verify user was deleted
    result = await db_session.execute(select(User).where(User.id == created_user.id))
    deleted_user = result.scalar_one_or_none()
    assert deleted_user is None

async def test_list_users(db_session):
    """Test listing users with pagination."""
    repo = UserRepository(db_session)
    
    # Create multiple users
    users_data = [
        {
            "email": f"list_test_{i}@example.com",
            "hashed_password": "hashed_password_here",
            "full_name": f"List Test User {i}",
            "is_active": True
        }
        for i in range(5)
    ]
    
    for user_data in users_data:
        user = User(**user_data)
        await repo.create(user)
    
    # Test pagination
    users_page_1 = await repo.list(skip=0, limit=2)
    assert len(users_page_1) == 2
    
    users_page_2 = await repo.list(skip=2, limit=2)
    assert len(users_page_2) == 2
    
    # Verify different users on different pages
    assert users_page_1[0].id != users_page_2[0].id 