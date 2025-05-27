from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.repository.user import user_repository
from app.models.user import User
from app.api.v1.schemas.user import UserCreate, UserUpdate
from app.core.errors import NotFoundException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    User service containing business logic for user operations
    """

    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        user = user_repository.get(db=db, id=user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return user_repository.get_by_email(db=db, email=email)

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return user_repository.get_multi(db=db, skip=skip, limit=limit)

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        user = user_repository.get_by_email(db=db, email=user_in.email)
        if user:
            raise ValueError("Email already registered")
        
        hashed_password = self.get_password_hash(user_in.password)
        user_data = user_in.dict()
        del user_data["password"]
        user_data["hashed_password"] = hashed_password
        
        return user_repository.create(db=db, obj_in=UserCreate(**user_data))

    def update_user(self, db: Session, user_id: int, user_in: UserUpdate) -> User:
        user = self.get_user(db=db, user_id=user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        
        if user_in.password:
            hashed_password = self.get_password_hash(user_in.password)
            user_data = user_in.dict()
            del user_data["password"]
            user_data["hashed_password"] = hashed_password
            user_in = UserUpdate(**user_data)
        
        return user_repository.update(db=db, db_obj=user, obj_in=user_in)

    def delete_user(self, db: Session, user_id: int) -> User:
        user = self.get_user(db=db, user_id=user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user_repository.delete(db=db, id=user_id)

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(db=db, email=email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user_repository.is_active(user)

    def is_superuser(self, user: User) -> bool:
        return user_repository.is_superuser(user)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


# Create a singleton instance
user_service = UserService() 