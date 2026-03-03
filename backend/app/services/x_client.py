import tweepy
from app.config import settings

def get_X_client():
    return tweepy.Client(
        access_token=settings.TWITTER_API_ACCESS_TOKEN_MAIN,
        access_token_secret=settings.TWITTER_API_ACCESS_TOKEN_SECRET_MAIN,
        consumer_key=settings.TWITTER_API_KEY_MAIN,
        consumer_secret=settings.TWITTER_API_SECRET_MAIN,  
    )
    
def get_X_v1_api():
    """Returns Tweepy v1 API — ONLY needed for media uploads."""
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY_MAIN,
        settings.TWITTER_API_SECRET_MAIN,
        settings.TWITTER_API_ACCESS_TOKEN_MAIN,
        settings.TWITTER_API_ACCESS_TOKEN_SECRET_MAIN,
    )
    return tweepy.API(auth)