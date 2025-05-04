from sqlalchemy.orm import Session
from ..schemas import UserCreate
from passlib.hash import bcrypt
from fastapi import HTTPException, status
from ..repositories import user_repository


# the service implement functions for register a user and authenticate it ,
# we inject Session as depencency to pass it to the data acess layer
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user: UserCreate):
        existing_user = user_repository.get_user_by_email(self.db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )
        return user_repository.create_user(self.db, user)

    def authenticate_user(self, email: str, password: str):
        user = user_repository.get_user_by_email(self.db, email)
        if not user or not bcrypt.verify(password, user.hashed_password):
            return None
        return user
