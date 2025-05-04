from fastapi import Depends
from sqlalchemy.orm import Session
from database.database import get_db
from .user_service import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
