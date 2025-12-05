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


@router.get("/movie/{movie_id}", dependencies=[Depends(verify_token)])
async def get_movie(
    movie_id,
    user_id: int = Query(None),
    db: Session = Depends(get_db)
):
    if not str(movie_id).isnumeric():
        movie_details = await movie_service.getMovieDetailsByCategory(movie_id)
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
    print(f"Searching movies with query: {query}, page: {page}")
    search_results = await movie_service.searchMovies(query, page)
    if not search_results:
        raise HTTPException(status_code=404, detail="No movies found for the given query")
    return search_results