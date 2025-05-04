from fastapi import APIRouter, Depends, HTTPException
from ..schemas import UserCreate, UserLogin, Token
from ..services.dependencies import get_user_service
from ..services.jwt_services import create_access_token
from ..services.user_service import UserService

router = APIRouter()


@router.post("/signup", response_model=Token)
def signup(user: UserCreate, userservice: UserService = Depends(get_user_service)):
    created_user = userservice.register_user(user)
    token = create_access_token({"sub": created_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, userservice: UserService = Depends(get_user_service)):
    user_authen = userservice.authenticate_user(user.email, user.password)
    if not user_authen:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
