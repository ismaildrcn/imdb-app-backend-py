from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db

from core.security import verify_token
from models.wishlist import Wishlist
from schemas.wishlist.wishlist_schemas import WishlistCreate
from services.remote.external_api import RemoteMovieService

movie_service = RemoteMovieService()


router = APIRouter(
    prefix="/user",
    tags=["user"]  # Swagger'da kategorize eder
)   


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