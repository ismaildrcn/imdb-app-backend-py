from sqlalchemy.orm import Session
from models.user import User
from schemas.auth.login import UserBase, UserCreate
from argon2 import PasswordHasher
from datetime import datetime


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        password=hash_password(user.password),
        created_at=datetime.now()  # Şu anki tarih ve saat
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, user: UserBase):
    login_user = db.query(User).filter(User.email == user.email).first()
    if login_user and verify_password(login_user.password, user.password):
        return login_user
    return None

def get_users(db: Session):
    return db.query(User).all()


def hash_password(password: str) -> str:
    return PasswordHasher().hash(password)

def verify_password(stored_password: str, provided_password: str) -> bool:
    try:
        PasswordHasher().verify(stored_password, provided_password)
        return True
    except:
        return False