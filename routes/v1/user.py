from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db

from core.security import verify_token
from crud.user import update_user
from models.wishlist import Wishlist
from schemas.user.user_schemas import UserSchema
from schemas.wishlist.wishlist_schemas import WishlistCreate
from services.remote.external_api import RemoteMovieService

movie_service = RemoteMovieService()


router = APIRouter(
    prefix="/users",
    tags=["users"]  # Swagger'da kategorize eder
)

@router.get("/me", dependencies=[Depends(verify_token)])
def get_current_user(db: Session = Depends(get_db), token_data: dict = Depends(verify_token)):
    user_email = token_data.get("email")
    user = db.query(Wishlist).filter(Wishlist.user.has(email=user_email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.user.to_json()

@router.patch("/{user_id}", dependencies=[Depends(verify_token)])
def update_user_details(user_id: int, payload: UserSchema, db: Session = Depends(get_db)):
    print(payload)
    update_user(db, payload)
    return {"message": "User update endpoint called."}

@router.post("/{user_id}/wishlist", dependencies=[Depends(verify_token)])
def add_to_wishlist(user_id: int, payload: WishlistCreate, db: Session = Depends(get_db)):
    new_wishlist_item = Wishlist(
        user_id=user_id,
        movie_id=payload.movie_id,
        note=payload.note,
        added_at=datetime.utcnow()
    )
    db.add(new_wishlist_item)
    db.commit()
    db.refresh(new_wishlist_item)
    return new_wishlist_item

@router.get("/{user_id}/wishlist", dependencies=[Depends(verify_token)])
async def get_wishlist(user_id: int, db: Session = Depends(get_db)):
    movie_detail_list = []
    wishlist_items = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    for item in wishlist_items:
        movie_details = await movie_service.getMovieDetails(item.movie_id)
        movie_detail_list.append(movie_details)
    return movie_detail_list

@router.delete("/{user_id}/wishlist/{movie_id}", dependencies=[Depends(verify_token)])
def remove_from_wishlist(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.movie_id == movie_id
    ).first()
    if not wishlist_item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    db.delete(wishlist_item)
    db.commit()
    return {"message": "Wishlist item removed successfully."}
