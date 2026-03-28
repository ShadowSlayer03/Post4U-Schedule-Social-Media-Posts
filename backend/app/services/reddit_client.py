import praw
from app.config import settings

def get_reddit_client():
    user_agent = f"python:post4u:v1.0 (by /u/{settings.REDDIT_USERNAME})"
    return praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                username=settings.REDDIT_USERNAME,
                password=settings.REDDIT_PASSWORD,
                user_agent=user_agent,
            )
