import pytest
from datetime import timedelta

from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    verify_access_token
)

def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    
    # Test hashing
    hashed = get_password_hash(password)
    assert hashed != password
    assert len(hashed) > len(password)
    
    # Test verification
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
    assert verify_password(password, "wronghash") is False

def test_access_token_creation():
    """Test JWT access token creation and verification."""
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    
    token = create_access_token(data, expires_delta)
    assert token is not None
    assert isinstance(token, str)
    
    # Verify token
    decoded_data = verify_access_token(token)
    assert decoded_data["sub"] == data["sub"]
    assert "exp" in decoded_data  # Should have expiration
    assert "iat" in decoded_data  # Should have issued at

def test_access_token_expiration():
    """Test token expiration."""
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=-1)  # Expired token
    
    token = create_access_token(data, expires_delta)
    
    with pytest.raises(Exception) as exc_info:
        verify_access_token(token)
    assert "expired" in str(exc_info.value).lower()

def test_invalid_token():
    """Test invalid token handling."""
    invalid_tokens = [
        "not.a.token",
        "invalid.token.format",
        "",
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid",  # Malformed JWT
    ]
    
    for token in invalid_tokens:
        with pytest.raises(Exception):
            verify_access_token(token) 