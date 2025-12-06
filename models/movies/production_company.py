from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


# Many-to-Many ilişki için ara tablo
movie_production_company = Table(
    "movie_production_company",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.movie_id"), primary_key=True),
    Column("production_company_id", Integer, ForeignKey("production_companies.production_company_id"), primary_key=True)
)


class ProductionCompany(Base):
    __tablename__ = "production_companies"
    
    production_company_id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, index=True)
    logo_path = Column(String(255), nullable=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    origin_country = Column(String(20), nullable=True)

    # Relationship - bu production'a ait filmler
    movies = relationship("Movie", secondary=movie_production_company, back_populates="production_companies")