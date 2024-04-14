# app/core/config.py
# After
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    MONGO_URL: str
    MONGO_DB: str = "music_recommendation_system"  # Default value if not set
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URL: str

    class Config:
        # Tells Pydantic to read the environment variables.
        env_file = ".env"

settings = Settings()
