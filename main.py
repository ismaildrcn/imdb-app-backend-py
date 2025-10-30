from fastapi import FastAPI

from routes.v1 import auth, movie

app = FastAPI()

# V1 API rotalarını /v1/api prefix'i ile ekle
app.include_router(auth.router, prefix="/v1/api")
app.include_router(movie.router, prefix="/v1/api")



@app.get("/")
def read_root():
    return {"message": "Hello from API!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "İsmail"}
