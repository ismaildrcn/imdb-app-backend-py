from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base

class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    imdb_id = Column(String(20), nullable=False)
    note = Column(String(255), nullable=True)
    added_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="wishlist")

    __table_args__ = (UniqueConstraint("user_id", "imdb_id", name="unique_user_movie"),)


    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "added_at": self.added_at.isoformat()
        }