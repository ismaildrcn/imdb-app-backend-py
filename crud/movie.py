from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import Optional

from models.movies.movie import Movie
from models.movies.genre import Genre
from models.movies.belongs_to_collection import Collection
from models.movies.production_company import ProductionCompany
from models.movies.production_country import ProductionCountry
from models.movies.spoken_language import SpokenLanguage


def movie_to_dict(movie: Movie) -> dict:
    """Movie objesini dict'e çevirir (API response formatında)"""
    if not movie:
        return None
    
    # origin_country string'ini listeye çevir
    origin_country = []
    if movie.origin_country:
        origin_country = movie.origin_country.split(",")
    return {
        "id": movie.id,
        "adult": movie.adult,
        "backdrop_path": movie.backdrop_path,
        "budget": movie.budget,
        "homepage": movie.homepage,
        "imdb_id": movie.imdb_id,
        "origin_country": origin_country,
        "original_language": movie.original_language,
        "original_title": movie.original_title,
        "overview": movie.overview,
        "popularity": movie.popularity,
        "poster_path": movie.poster_path,
        "release_date": movie.release_date.strftime("%Y-%m-%d") if movie.release_date else None,
        "revenue": movie.revenue,
        "runtime": movie.runtime,
        "status": movie.status,
        "tagline": movie.tagline,
        "title": movie.title,
        "video": movie.video,
        "vote_average": movie.vote_average,
        "vote_count": movie.vote_count,
        "genres": [{"id": g.id, "name": g.name} for g in movie.genres],
        "belongs_to_collection": {
                "id": movie.belongs_to_collection[0].id,
                "name": movie.belongs_to_collection[0].name,
                "poster_path": movie.belongs_to_collection[0].poster_path,
                "backdrop_path": movie.belongs_to_collection[0].backdrop_path
            } if movie.belongs_to_collection else None,
        "production_companies": [
            {
                "id": pc.id,
                "name": pc.name,
                "logo_path": pc.logo_path,
                "origin_country": pc.origin_country
            } for pc in movie.production_companies
        ],
        "production_countries": [
            {
                "iso_3166_1": pc.iso_3166_1,
                "name": pc.name
            } for pc in movie.production_countries
        ],
        "spoken_languages": [
            {
                "iso_639_1": sl.iso_639_1,
                "english_name": sl.english_name,
                "name": sl.name
            } for sl in movie.spoken_languages
        ]
    }


def get_or_create_genre(db: Session, genre_data: dict) -> Genre:
    """Genre varsa getir, yoksa oluştur"""
    # Önce ID ile kontrol et
    genre = db.query(Genre).filter(Genre.id == genre_data["id"]).first()
    if genre:
        return genre
    
    # ID yoksa, name ile kontrol et (unique constraint için)
    genre = db.query(Genre).filter(Genre.name == genre_data["name"]).first()
    if genre:
        return genre
    
    # Hiçbiri yoksa yeni oluştur
    genre = Genre(id=genre_data["id"], name=genre_data["name"])
    db.add(genre)
    db.flush()
    return genre


def get_or_create_collection(db: Session, collection_data: dict) -> Collection:
    """Collection varsa getir, yoksa oluştur"""
    collection = db.query(Collection).filter(Collection.id == collection_data["id"]).first()
    if not collection:
        collection = Collection(
            id=collection_data["id"],
            name=collection_data["name"],
            poster_path=collection_data.get("poster_path"),
            backdrop_path=collection_data.get("backdrop_path")
        )
        db.add(collection)
        db.flush()
    return collection


def get_or_create_production_company(db: Session, company_data: dict) -> ProductionCompany:
    """ProductionCompany varsa getir, yoksa oluştur"""
    company = db.query(ProductionCompany).filter(ProductionCompany.id == company_data["id"]).first()

    company = db.query(ProductionCompany).filter(ProductionCompany.id == company_data["id"]).first()
    if company:
        return company
    
    company = db.query(ProductionCompany).filter(ProductionCompany.name == company_data["name"]).first()
    if company:
        return company
    
    company = ProductionCompany(
        id=company_data["id"],
        name=company_data["name"],
        logo_path=company_data.get("logo_path"),
        origin_country=company_data.get("origin_country")
    )
    db.add(company)
    db.flush()
    return company


def get_or_create_production_country(db: Session, country_data: dict) -> ProductionCountry:
    """ProductionCountry varsa getir, yoksa oluştur"""
    country = db.query(ProductionCountry).filter(
        ProductionCountry.iso_3166_1 == country_data["iso_3166_1"]
    ).first()
    if country:
        return country
    
    country = db.query(ProductionCountry).filter(
        ProductionCountry.iso_3166_1 == country_data["name"]
    ).first()

    if country:
        return country

    country = ProductionCountry(
        iso_3166_1=country_data["iso_3166_1"],
        name=country_data["name"]
    )
    db.add(country)
    db.flush()
    return country


def get_or_create_spoken_language(db: Session, language_data: dict) -> SpokenLanguage:
    """SpokenLanguage varsa getir, yoksa oluştur"""
    language = db.query(SpokenLanguage).filter(
        SpokenLanguage.iso_639_1 == language_data["iso_639_1"]
    ).first()
    if language:
        return language
    
    language = SpokenLanguage(
        iso_639_1=language_data["iso_639_1"],
        english_name=language_data["english_name"],
        name=language_data["name"]
    )
    db.add(language)
    db.flush()
    return language


def parse_release_date(date_string: Optional[str]) -> Optional[datetime]:
    """Release date string'ini datetime'a çevir"""
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return None
    
def get_movie_by_id(db: Session, movie_id: int) -> Optional[Movie]:
    """ID'ye göre film getir (tüm ilişkili verilerle birlikte)"""
    return db.query(Movie).options(
        joinedload(Movie.genres),
        joinedload(Movie.production_companies),
        joinedload(Movie.belongs_to_collection),
        joinedload(Movie.production_countries),
        joinedload(Movie.spoken_languages)
    ).filter(Movie.id == movie_id).first()


def get_movie_by_id_simple(db: Session, movie_id: int) -> Optional[Movie]:
    """ID'ye göre film getir (sadece film bilgisi, ilişkiler lazy load)"""
    return db.query(Movie).filter(Movie.id == movie_id).first()


def save_movie_from_api(db: Session, movie_data: dict) -> Movie:
    """
    API'den gelen film verisini veritabanına kaydeder.
    Tüm ilişkili tabloları da oluşturur/günceller.
    """
    
    # Film zaten var mı kontrol et
    existing_movie = db.query(Movie).filter(Movie.id == movie_data["id"]).first()
    if existing_movie:
        # Varsa güncelle veya direkt döndür
        print("Movie already exists:", existing_movie.title)
        return existing_movie
    
    # origin_country listesini string'e çevir
    origin_country = None
    if movie_data.get("origin_country"):
        origin_country = ",".join(movie_data["origin_country"])
    
    # Yeni film oluştur
    movie = Movie(
        id=movie_data["id"],
        adult=movie_data.get("adult", False),
        backdrop_path=movie_data.get("backdrop_path"),
        budget=movie_data.get("budget"),
        homepage=movie_data.get("homepage"),
        imdb_id=movie_data.get("imdb_id"),
        origin_country=origin_country,
        original_language=movie_data.get("original_language"),
        original_title=movie_data.get("original_title"),
        overview=movie_data.get("overview"),
        popularity=movie_data.get("popularity"),
        poster_path=movie_data.get("poster_path"),
        release_date=parse_release_date(movie_data.get("release_date")),
        revenue=movie_data.get("revenue"),
        runtime=movie_data.get("runtime"),
        status=movie_data.get("status"),
        tagline=movie_data.get("tagline"),
        title=movie_data["title"],
        video=movie_data.get("video", False),
        vote_average=movie_data.get("vote_average"),
        vote_count=movie_data.get("vote_count")
    )
    print("Movie to be added:", movie.title)
    
    db.add(movie)
    db.flush()  # ID'yi almak için
    
    # Genres ekle
    if movie_data.get("genres"):
        for genre_data in movie_data["genres"]:
            genre = get_or_create_genre(db, genre_data)
            movie.genres.append(genre)
    
    # Collection ekle (belongs_to_collection)
    if movie_data.get("belongs_to_collection"):
        collection = get_or_create_collection(db, movie_data["belongs_to_collection"])
        movie.belongs_to_collection.append(collection)
    
    # Production Companies ekle
    if movie_data.get("production_companies"):
        for company_data in movie_data["production_companies"]:
            company = get_or_create_production_company(db, company_data)
            movie.production_companies.append(company)
    
    # Production Countries ekle
    if movie_data.get("production_countries"):
        for country_data in movie_data["production_countries"]:
            country = get_or_create_production_country(db, country_data)
            movie.production_countries.append(country)
    
    # Spoken Languages ekle
    if movie_data.get("spoken_languages"):
        for language_data in movie_data["spoken_languages"]:
            language = get_or_create_spoken_language(db, language_data)
            movie.spoken_languages.append(language)
    
    db.commit()
    db.refresh(movie)
    
    return movie
