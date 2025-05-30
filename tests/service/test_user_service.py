import pytest
from fastapi import HTTPException

from app.schemas.user import UserCreate, UserUpdate
from app.service.user_service import UserService
from app.core.security import verify_password

pytestmark = pytest.mark.asyncio

async def test_create_user_service(db_session):
    """Test user creation through service layer."""
    service = UserService(db_session)
    user_in = UserCreate(
        email="service_test@example.com",
        password="testpassword123",
        full_name="Service Test User"
    )
    
    user = await service.create(user_in)
    
    assert user.email == user_in.email
    assert user.full_name == user_in.full_name
    assert hasattr(user, "hashed_password")
    assert verify_password("testpassword123", user.hashed_password)
    assert user.is_active  # Should be True by default

async def test_create_user_duplicate_email(db_session):
    """Test creating user with duplicate email."""
    service = UserService(db_session)
    user_data = UserCreate(
        email="duplicate@example.com",
        password="testpassword123",
        full_name="Original User"
    )
    
    # Create first user
    await service.create(user_data)
    
    # Try to create second user with same email
    with pytest.raises(HTTPException) as exc_info:
        await service.create(user_data)
    assert exc_info.value.status_code == 400
    assert "Email already registered" in str(exc_info.value.detail)

async def test_authenticate_user(db_session):
    """Test user authentication."""
    service = UserService(db_session)
    user_in = UserCreate(
        email="auth_test@example.com",
        password="testpassword123",
        full_name="Auth Test User"
    )
    
    # Create user
    await service.create(user_in)
    
    # Test successful authentication
    authenticated_user = await service.authenticate(
        email="auth_test@example.com",
        password="testpassword123"
    )
    assert authenticated_user is not None
    assert authenticated_user.email == user_in.email
    
    # Test failed authentication - wrong password
    wrong_auth_user = await service.authenticate(
        email="auth_test@example.com",
        password="wrongpassword"
    )
    assert wrong_auth_user is None
    
    # Test failed authentication - wrong email
    nonexistent_auth_user = await service.authenticate(
        email="nonexistent@example.com",
        password="testpassword123"
    )
    assert nonexistent_auth_user is None

async def test_update_user_service(db_session):
    """Test updating user through service layer."""
    service = UserService(db_session)
    
    # Create user
    user_in = UserCreate(
        email="update_service@example.com",
        password="testpassword123",
        full_name="Update Service User"
    )
    user = await service.create(user_in)
    
    # Update user
    user_update = UserUpdate(
        full_name="Updated Service Name",
        password="newpassword123"
    )
    updated_user = await service.update(user.id, user_update)
    
    assert updated_user.full_name == user_update.full_name
    assert verify_password("newpassword123", updated_user.hashed_password)
    assert updated_user.email == user.email  # Should remain unchanged

async def test_get_user_by_id_not_found(db_session):
    """Test getting non-existent user by ID."""
    service = UserService(db_session)
    
    with pytest.raises(HTTPException) as exc_info:
        await service.get(999999)
    assert exc_info.value.status_code == 404
    assert "User not found" in str(exc_info.value.detail)

async def test_deactivate_user(db_session):
    """Test deactivating a user."""
    service = UserService(db_session)
    user_in = UserCreate(
        email="deactivate@example.com",
        password="testpassword123",
        full_name="Deactivate Test User"
    )
    
    # Create user
    user = await service.create(user_in)
    assert user.is_active is True
    
    # Deactivate user
    user_update = UserUpdate(is_active=False)
    updated_user = await service.update(user.id, user_update)
    assert updated_user.is_active is False
    
    # Try to authenticate deactivated user
    auth_result = await service.authenticate(
        email="deactivate@example.com",
        password="testpassword123"
    )
    assert auth_result is None 