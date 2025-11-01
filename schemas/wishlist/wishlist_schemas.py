from pydantic import BaseModel

class WishlistCreate(BaseModel):
    imdb_id: str
    note: str | None = None