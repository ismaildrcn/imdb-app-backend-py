from fastapi import APIRouter, Depends, HTTPException

from services.remote.external_api import RemoteMovieService

movie_service = RemoteMovieService()

router = APIRouter(
    prefix="/remote",
    tags=["remote"]  # Swagger'da kategorize eder
)


@router.get("/movie/{movie_id}")
async def get_movie(movie_id):
    movie_details = await movie_service.getMovieDetails(movie_id)
    if not movie_details:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie_details

@router.get("/movie/{movie_id}/credits")
async def get_movie_credits(movie_id: int):
    movie_credits = await movie_service.getMovieCredits(movie_id)
    if not movie_credits:
        raise HTTPException(status_code=404, detail="Movie credits not found")
    return movie_credits

@router.get("/movie/{movie_id}/reviews")
async def get_movie_reviews(movie_id: int):
    movie_reviews = await movie_service.getMovieReviews(movie_id)
    if not movie_reviews:
        raise HTTPException(status_code=404, detail="Movie reviews not found")
    return movie_reviews

@router.get("/movie/{movie_id}/videos")
async def get_movie_videos(movie_id: int):
    movie_videos = await movie_service.getMovieVideos(movie_id)
    if not movie_videos:
        raise HTTPException(status_code=404, detail="Movie videos not found")
    return movie_videos

@router.get("/person/{person_id}")
async def get_person_details(person_id: int):
    person_details = await movie_service.getPersonDetails(person_id)
    if not person_details:
        raise HTTPException(status_code=404, detail="Person not found")
    return person_details

@router.get("/genre/movie/list")
async def get_genres():
    genres = await movie_service.getGenres()
    if not genres:
        raise HTTPException(status_code=404, detail="Genres not found")
    return genres