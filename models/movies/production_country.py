from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

movie_production_country = Table(
    "movie_production_country",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("production_country_id", Integer, ForeignKey("production_countries.production_country_id"), primary_key=True)
)

class ProductionCountry(Base):
    __tablename__ = "production_countries"

    
    production_country_id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, unique=True, index=True)
    iso_3166_1 = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)

    # Relationship - bu production country'e ait filmler
    movies = relationship("Movie", secondary=movie_production_country, back_populates="production_countries")