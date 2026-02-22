from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "post_scheduler"
    TWITTER_API_KEY_MAIN: str
    TWITTER_API_SECRET_MAIN: str
    TWITTER_API_BEARER_TOKEN_MAIN: str
    TWITTER_API_ACCESS_TOKEN_MAIN: str
    TWITTER_API_ACCESS_TOKEN_SECRET_MAIN: str

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()