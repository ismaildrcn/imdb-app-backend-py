from fastapi import FastAPI

from routes.v1 import auth, movie, user

app = FastAPI()

# V1 API rotalarını /v1/api prefix'i ile ekle
app.include_router(auth.router, prefix="/v1/api")
app.include_router(movie.router, prefix="/v1/api")
app.include_router(user.router, prefix="/v1/api")


