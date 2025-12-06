from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

movie_spoken_language = Table(
    "movie_spoken_language",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.movie_id"), primary_key=True),
    Column("spoken_language_id", Integer, ForeignKey("spoken_languages.spoken_language_id"), primary_key=True)
)

class SpokenLanguage(Base):
    __tablename__ = "spoken_languages"

    spoken_language_id = Column(Integer, primary_key=True, autoincrement=True)
    english_name = Column(String(100), nullable=False)
    iso_639_1 = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)

    # Relationship - bu spoken language'e ait filmler
    movies = relationship("Movie", secondary=movie_spoken_language, back_populates="spoken_languages")