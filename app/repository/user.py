from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.repository.base import BaseRepository
from app.api.v1.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    User repository with custom methods for user-specific operations
    """
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


# Create a singleton instance
user_repository = UserRepository(User) 