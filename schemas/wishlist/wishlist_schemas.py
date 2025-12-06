from pydantic import BaseModel

class WishlistCreate(BaseModel):
    movie_id: int
    note: str | None = None

