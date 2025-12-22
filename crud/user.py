from sqlalchemy.orm import Session
from models.user import User
from schemas.auth.login import UserBase, UserCreate
from argon2 import PasswordHasher
from datetime import datetime

from schemas.user.user_schemas import UserSchema


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        password=hash_password(user.password),
        gender=user.gender,
        birthdate=user.birth_date,
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
    
def movie_in_wishlist(db: Session, user_id: int, movie_id: int) -> bool:
    wishlist_item = db.query(User).filter(
        User.id == user_id,
        User.wishlist.any(movie_id=movie_id)
    ).first()
    return wishlist_item is not None

def update_user(db: Session, data: UserSchema):
    has_changed = False
    user = db.query(User).filter(User.id == data.id).first()
    if not user:
        return None
    if data.full_name is not None:
        user.full_name = data.full_name
        has_changed = True
    if data.phone is not None:
        user.phone = data.phone
        has_changed = True
    if data.email is not None:
        user.email = data.email
        user.is_verified = False  # Email değişirse doğrulama durumu sıfırlanır
        has_changed = True
    if data.gender is not None:
        user.gender = data.gender
        has_changed = True
    if data.birthdate is not None:
        user.birthdate = data.birthdate
        has_changed = True
    if has_changed:
        user.last_update = datetime.utcnow()  # Güncelleme zamanını ayarla
        db.commit()
        db.refresh(user)
    return user