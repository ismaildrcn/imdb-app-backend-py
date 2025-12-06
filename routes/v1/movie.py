from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query

from services.remote.external_api import RemoteMovieService
from core.security import verify_token
from core.database import get_db
from sqlalchemy.orm import Session
from crud.user import movie_in_wishlist


movie_service = RemoteMovieService()

router = APIRouter(
    prefix="/remote",
    tags=["remote"]  # Swagger'da kategorize eder
)

categorical_movies_cache = {}

@router.get("/movie/{movie_id}", dependencies=[Depends(verify_token)])
async def get_movie(
    movie_id,
    user_id: int = Query(None),
    db: Session = Depends(get_db)
):
    if not str(movie_id).isnumeric():
        cached_data = check_movie_from_cache(movie_id)
        if cached_data:
            return cached_data
        movie_details = await movie_service.getMovieDetailsByCategory(movie_id)
        if not categorical_movies_cache.get(movie_id):
            categorical_movies_cache[movie_id] = (datetime.now(), movie_details)
    else:
        movie_details = await movie_service.getMovieDetails(movie_id)
    if user_id is not None:
        is_in_wishlist = movie_in_wishlist(db, user_id, movie_id)
        movie_details.update({"is_in_wishlist": is_in_wishlist})
    if not movie_details:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie_details

@router.get("/movie/{movie_id}/without-token")
async def get_movie_without_token(movie_id):
    movie_details = await movie_service.getMovieDetailsByCategory(movie_id)
    if not movie_details:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie_details

@router.get("/movie/{movie_id}/credits", dependencies=[Depends(verify_token)])
async def get_movie_credits(movie_id: int):
    movie_credits = await movie_service.getMovieCredits(movie_id)
    if not movie_credits:
        raise HTTPException(status_code=404, detail="Movie credits not found")
    return movie_credits

@router.get("/movie/{movie_id}/reviews", dependencies=[Depends(verify_token)])
async def get_movie_reviews(movie_id: int):
    movie_reviews = await movie_service.getMovieReviews(movie_id)
    if not movie_reviews:
        raise HTTPException(status_code=404, detail="Movie reviews not found")
    return movie_reviews

@router.get("/movie/{movie_id}/videos", dependencies=[Depends(verify_token)])
async def get_movie_videos(movie_id: int):
    movie_videos = await movie_service.getMovieVideos(movie_id)
    if not movie_videos:
        raise HTTPException(status_code=404, detail="Movie videos not found")
    return movie_videos

@router.get("/person/{person_id}", dependencies=[Depends(verify_token)])
async def get_person_details(person_id: int):
    person_details = await movie_service.getPersonDetails(person_id)
    if not person_details:
        raise HTTPException(status_code=404, detail="Person not found")
    return person_details

@router.get("/genre/movie/list", dependencies=[Depends(verify_token)])
async def get_genres():
    genres = await movie_service.getGenres()
    if not genres:
        raise HTTPException(status_code=404, detail="Genres not found")
    return genres

@router.get("/search/movie", dependencies=[Depends(verify_token)])
async def search_movies(query: str, page: int = 1):
    movies = []
    print(f"Searching movies with query: {query}, page: {page}")
    search_results = await movie_service.searchMovies(query, page)
    for movie in search_results.get("results", []):
        m = await movie_service.getMovieDetails(movie.get("id"))
        movies.append(m)
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found for the given query")
    return {"results": movies, "page": page, "total_results": search_results.get("total_results", 0), "total_pages": search_results.get("total_pages", 0)}

@router.get("/trending/movie", dependencies=[Depends(verify_token)])
async def get_trending_movies(time_window: str = "week", page: int = 1):
    cached_data = check_movie_from_cache("trending")
    if cached_data:
        return cached_data
    trending_movies = await movie_service.getTrendingMovies(time_window, page)
    if not categorical_movies_cache.get(f"trending"):
        categorical_movies_cache[f"trending"] = (datetime.now(), trending_movies)
    if not trending_movies:
        raise HTTPException(status_code=404, detail="No trending movies found")
    return trending_movies


def check_movie_from_cache(movie_id: str):
    if movie_id in categorical_movies_cache:
        cached_time, cached_data = categorical_movies_cache[movie_id]
        if datetime.now() - cached_time < timedelta(hours=1):
            return cached_data
        else:
            del categorical_movies_cache[movie_id]
    print(f"Fetching categorical movie details for ID: {movie_id}")
    return None