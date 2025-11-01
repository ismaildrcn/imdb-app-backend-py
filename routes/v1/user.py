from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db

from core.security import verify_token
from models.wishlist import Wishlist
from schemas.wishlist.wishlist_schemas import WishlistCreate


router = APIRouter(
    prefix="/user",
    tags=["user"]  # Swagger'da kategorize eder
)   


@router.post("/{user_id}/wishlist", dependencies=[Depends(verify_token)])
def add_to_wishlist(user_id: int, payload: WishlistCreate, db: Session = Depends(get_db)):
    new_wishlist_item = Wishlist(
        user_id=user_id,
        imdb_id=payload.imdb_id,
        note=payload.note,
        added_at=datetime.utcnow()
    )
    db.add(new_wishlist_item)
    db.commit()
    db.refresh(new_wishlist_item)
    return new_wishlist_item

@router.get("/{user_id}/wishlist", dependencies=[Depends(verify_token)])
def get_wishlist(user_id: int, db: Session = Depends(get_db)):
    wishlist_items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    return wishlist_items