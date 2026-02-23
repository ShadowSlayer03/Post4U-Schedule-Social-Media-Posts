from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "post_scheduler"

    # X / Twitter
    TWITTER_API_KEY_MAIN: str = ""
    TWITTER_API_SECRET_MAIN: str = ""
    TWITTER_API_BEARER_TOKEN_MAIN: str = ""
    TWITTER_API_ACCESS_TOKEN_MAIN: str = ""
    TWITTER_API_ACCESS_TOKEN_SECRET_MAIN: str = ""

    # Reddit
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USERNAME: str = ""
    REDDIT_PASSWORD: str = ""
    REDDIT_SUBREDDIT: str = "test"

    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHANNEL_ID: str = ""

    # Discord
    DISCORD_WEBHOOK_URL: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()