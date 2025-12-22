import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını yükle

class Settings:
    PROJECT_NAME = "IMDB Python"
    BASE_URL: str = os.getenv("BASE_URL")
    API_TOKEN: str = os.getenv("API_TOKEN")
    LOCAL_URL: str = os.getenv("LOCAL_URL")
    LOCAL_PORT: int = int(os.getenv("LOCAL_PORT", 8000))
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    # Database Settings
    # Render DATABASE_URL'i varsa onu kullan, yoksa ayrı değişkenlerden oluştur
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_DATABASE: str = os.getenv("DB_DATABASE")
    DB_DIALECT: str = os.getenv("DB_DIALECT", "postgresql")

settings = Settings()
