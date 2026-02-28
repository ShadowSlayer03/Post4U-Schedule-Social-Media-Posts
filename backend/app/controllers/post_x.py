
import logging

from app.services.x_client import get_X_client

logger = logging.getLogger("uvicorn.error")

def post_tweet(content: str):
    client = get_X_client()
    try:
        response = client.create_tweet(text=content)
        logger.info(f"Tweet ID: {response.data['id']}")
        return { "status": "success", "tweet_id": response.data['id'] }
    except Exception as e:
        logger.error(f"Error: {e}")
        return { "status": "error", "message": str(e) }