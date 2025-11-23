import httpx
from core.config import settings
from typing import Optional


class RemoteMovieService:
    BASE_URL = settings.BASE_URL + "/3"
    API_TOKEN = settings.API_TOKEN

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    async def _make_request(self, endpoint: str, query_params: Optional[dict] = None):
        """Ortak HTTP request fonksiyonu"""
        url = f"{self.BASE_URL}{endpoint}"
        print(f"Making request to URL: {url}")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=query_params)
            try:
                response.raise_for_status()  # hata durumunda exception atar
                return response.json()
            except httpx.HTTPError as e:
                return {"error": f"{response.status_code} {response.reason_phrase}"}

    async def getMovieDetails(self, movie_id):
        return await self._make_request(f"/movie/{movie_id}")
            
    async def getMovieCredits(self, movie_id: int):
        return await self._make_request(f"/movie/{movie_id}/credits")
    
    async def getMovieReviews(self, movie_id: int):
        return await self._make_request(f"/movie/{movie_id}/reviews")
    
    async def getMovieVideos(self, movie_id: int):
        return await self._make_request(f"/movie/{movie_id}/videos")
    
    async def getPersonDetails(self, person_id: int):
        return await self._make_request(f"/person/{person_id}")
    
    async def getGenres(self):
        return await self._make_request("/genre/movie/list")
    
    async def searchMovies(self, query: str, page: Optional[int] = 1):
        return await self._make_request("/search/movie", query_params={"query": query, "page": page})