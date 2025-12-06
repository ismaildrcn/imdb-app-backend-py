from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from core.database import Base


# Many-to-Many ilişki için ara tablo
movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.movie_id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True)
)

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Bizim primary key
    id = Column(Integer, unique=True, index=True)  # API'den gelen ID
    name = Column(String(100), nullable=False, unique=True, index=True)

    # Relationship - bu genre'a ait filmler
    movies = relationship("Movie", secondary="movie_genre", back_populates="genres")