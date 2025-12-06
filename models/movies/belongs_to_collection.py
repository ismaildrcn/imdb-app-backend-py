from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


# Many-to-Many ilişki için ara tablo
movie_collection = Table(
    "movie_collection",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.movie_id"), primary_key=True),
    Column("collection_id", Integer, ForeignKey("collections.collection_id"), primary_key=True)
)

class Collection(Base):
    __tablename__ = "collections"

    collection_id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    poster_path = Column(String(255), nullable=True)
    backdrop_path = Column(String(255), nullable=True)

    # Relationship - bu collection'a ait filmler
    movies = relationship("Movie", secondary=movie_collection, back_populates="belongs_to_collection")