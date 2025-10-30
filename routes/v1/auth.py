import jwt
from fastapi import APIRouter, HTTPException, Depends
from schemas.auth.login import UserBase, UserCreate
from sqlalchemy.orm import Session
from core.database import get_db
from crud.user import create_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]  # Swagger'da kategorize eder
)   


@router.post("/login")
def login(login_request: UserBase, db: Session = Depends(get_db)):
    user = login_user(db, login_request)
    if user:
        token = jwt.encode({"email": user.email}, "secret_key", algorithm="HS256")
        print(user)
        return {
            "token": token, 
            "message": "Authentication successful",
            "user": user.to_json(),
            "expires_at": 604800
            }
    raise HTTPException(status_code=401, detail="Passsword veya email hatalı")


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return {"message": f"User {new_user.email} registered successfully."}
