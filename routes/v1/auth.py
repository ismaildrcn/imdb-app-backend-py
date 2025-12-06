from datetime import datetime
import jwt
from fastapi import APIRouter, HTTPException, Depends
from schemas.auth.login import UserBase, UserCreate
from sqlalchemy.orm import Session
from core.database import get_db
from crud.user import create_user, login_user
from core.config import settings
from core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]  # Swagger'da kategorize eder
)   


@router.post("/login")
def login(login_request: UserBase, db: Session = Depends(get_db)):
    user = login_user(db, login_request)
    if user:
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        token = create_access_token({"email": user.email})
        return {
            "token": token, 
            "message": "Authentication successful",
            "user": user.to_json()
            }
    raise HTTPException(status_code=401, detail="Passsword veya email hatalı")


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return {"message": f"User {new_user.email} registered successfully."}
