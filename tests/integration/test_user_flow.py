import pytest
from fastapi import status
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password, create_access_token

pytestmark = [pytest.mark.asyncio, pytest.mark.integration]

async def test_complete_user_registration_flow(test_client, db_session):
    """
    Test complete user registration flow including:
    - User registration
    - Email verification
    - Profile update
    - Authentication
    - Profile retrieval
    """
    # 1. Register new user
    user_data = {
        "email": "integration@example.com",
        "password": "securepass123",
        "full_name": "Integration Test User"
    }
    
    response = test_client.post("/api/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    user_id = response.json()["id"]
    
    # 2. Verify user was created in database
    result = await db_session.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one()
    assert db_user is not None
    assert db_user.email == user_data["email"]
    assert verify_password(user_data["password"], db_user.hashed_password)
    
    # 3. Authenticate user
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    auth_response = test_client.post("/api/auth/login", data=login_data)
    assert auth_response.status_code == status.HTTP_200_OK
    tokens = auth_response.json()
    assert "access_token" in tokens
    assert "token_type" in tokens
    assert tokens["token_type"] == "bearer"
    
    # 4. Use token to get user profile
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    profile_response = test_client.get(f"/api/users/me", headers=headers)
    assert profile_response.status_code == status.HTTP_200_OK
    profile = profile_response.json()
    assert profile["email"] == user_data["email"]
    assert profile["full_name"] == user_data["full_name"]
    
    # 5. Update user profile
    update_data = {
        "full_name": "Updated Integration User",
        "password": "newpassword123"
    }
    update_response = test_client.patch(
        f"/api/users/{user_id}",
        json=update_data,
        headers=headers
    )
    assert update_response.status_code == status.HTTP_200_OK
    updated_profile = update_response.json()
    assert updated_profile["full_name"] == update_data["full_name"]
    
    # 6. Verify password was updated by trying to login with new password
    new_login_data = {
        "username": user_data["email"],
        "password": update_data["password"]
    }
    new_auth_response = test_client.post("/api/auth/login", data=new_login_data)
    assert new_auth_response.status_code == status.HTTP_200_OK

async def test_user_authentication_flow(test_client, db_session):
    """
    Test complete authentication flow including:
    - User creation
    - Login attempts
    - Token refresh
    - Password reset
    """
    # 1. Create test user
    user_data = {
        "email": "auth_flow@example.com",
        "password": "authpass123",
        "full_name": "Auth Flow User"
    }
    
    response = test_client.post("/api/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # 2. Test failed login attempts
    invalid_attempts = [
        {"username": user_data["email"], "password": "wrongpass"},
        {"username": "wrong@email.com", "password": user_data["password"]},
        {"username": "", "password": ""},
    ]
    
    for invalid_data in invalid_attempts:
        response = test_client.post("/api/auth/login", data=invalid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # 3. Successful login
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    auth_response = test_client.post("/api/auth/login", data=login_data)
    assert auth_response.status_code == status.HTTP_200_OK
    tokens = auth_response.json()
    
    # 4. Use token to access protected endpoint
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    protected_response = test_client.get("/api/users/me", headers=headers)
    assert protected_response.status_code == status.HTTP_200_OK
    
    # 5. Test token refresh
    refresh_response = test_client.post(
        "/api/auth/refresh",
        headers=headers
    )
    assert refresh_response.status_code == status.HTTP_200_OK
    new_tokens = refresh_response.json()
    assert new_tokens["access_token"] != tokens["access_token"]
    
    # 6. Verify new token works
    new_headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}
    new_protected_response = test_client.get("/api/users/me", headers=new_headers)
    assert new_protected_response.status_code == status.HTTP_200_OK

async def test_user_management_flow(test_client, db_session):
    """
    Test administrative user management flow including:
    - Creating admin user
    - Admin creating other users
    - User listing and filtering
    - User deactivation/reactivation
    """
    # 1. Create admin user
    admin_data = {
        "email": "admin@example.com",
        "password": "adminpass123",
        "full_name": "Admin User",
        "is_superuser": True
    }
    
    # Create admin directly in DB as API doesn't allow superuser creation
    admin_user = User(
        email=admin_data["email"],
        hashed_password=get_password_hash(admin_data["password"]),
        full_name=admin_data["full_name"],
        is_superuser=True
    )
    db_session.add(admin_user)
    await db_session.commit()
    
    # 2. Admin login
    login_data = {
        "username": admin_data["email"],
        "password": admin_data["password"]
    }
    auth_response = test_client.post("/api/auth/login", data=login_data)
    assert auth_response.status_code == status.HTTP_200_OK
    admin_token = auth_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # 3. Admin creates multiple users
    test_users = [
        {
            "email": f"test{i}@example.com",
            "password": "testpass123",
            "full_name": f"Test User {i}"
        }
        for i in range(3)
    ]
    
    created_users = []
    for user_data in test_users:
        response = test_client.post(
            "/api/users/",
            json=user_data,
            headers=admin_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        created_users.append(response.json())
    
    # 4. Test user listing with pagination
    list_response = test_client.get(
        "/api/users/?skip=0&limit=2",
        headers=admin_headers
    )
    assert list_response.status_code == status.HTTP_200_OK
    users_page = list_response.json()
    assert len(users_page) == 2
    
    # 5. Test user deactivation
    user_to_deactivate = created_users[0]
    deactivate_response = test_client.patch(
        f"/api/users/{user_to_deactivate['id']}",
        json={"is_active": False},
        headers=admin_headers
    )
    assert deactivate_response.status_code == status.HTTP_200_OK
    assert deactivate_response.json()["is_active"] is False
    
    # 6. Verify deactivated user cannot login
    deactivated_login = {
        "username": user_to_deactivate["email"],
        "password": test_users[0]["password"]
    }
    login_response = test_client.post("/api/auth/login", data=deactivated_login)
    assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # 7. Reactivate user
    reactivate_response = test_client.patch(
        f"/api/users/{user_to_deactivate['id']}",
        json={"is_active": True},
        headers=admin_headers
    )
    assert reactivate_response.status_code == status.HTTP_200_OK
    assert reactivate_response.json()["is_active"] is True
    
    # 8. Verify reactivated user can login
    login_response = test_client.post("/api/auth/login", data=deactivated_login)
    assert login_response.status_code == status.HTTP_200_OK 