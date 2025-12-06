from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship, validates
from core.database import Base


from models.movies.production_company import movie_production_company
from models.movies.genre import movie_genre
from models.movies.belongs_to_collection import movie_collection
from models.movies.production_country import movie_production_country
from models.movies.spoken_language import movie_spoken_language


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    adult = Column(Boolean, default=False)
    backdrop_path = Column(String(255), nullable=True)
    budget = Column(Integer, nullable=True)
    homepage = Column(String(255), nullable=True)
    id = Column(Integer, unique=True, index=True)
    imdb_id = Column(String(50), unique=True, index=True)
    
    origin_country = Column(String(100), nullable=True)
    
    original_language = Column(String(20), nullable=True)
    original_title = Column(String(200), nullable=True)
    overview = Column(String(1000), nullable=True)
    popularity = Column(Float, nullable=True)
    poster_path = Column(String(255), nullable=True)

    release_date = Column(DateTime, nullable=True)
    revenue = Column(Integer, nullable=True)
    runtime = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)
    tagline = Column(String(255), nullable=True)
    title = Column(String(200), nullable=False)
    video = Column(Boolean, default=False)
    vote_average = Column(Float, nullable=True)
    vote_count = Column(Integer, nullable=True)

    # Relationship - bu filme ait production companies
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    production_companies = relationship("ProductionCompany", secondary=movie_production_company, back_populates="movies")
    belongs_to_collection = relationship("Collection", secondary=movie_collection, back_populates="movies")
    production_countries = relationship("ProductionCountry", secondary=movie_production_country, back_populates="movies")
    spoken_languages = relationship("SpokenLanguage", secondary=movie_spoken_language, back_populates="movies")

    @validates('imdb_id', 'homepage', 'tagline', 'backdrop_path', 'poster_path')
    def convert_empty_to_none(self, key, value):
        """Boş string değerlerini None'a çevir"""
        if value == '' or (isinstance(value, str) and not value.strip()):
            return None
        return value