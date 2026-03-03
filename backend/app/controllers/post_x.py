
import logging

from app.services.x_client import get_X_client, get_X_v1_api

logger = logging.getLogger("uvicorn.error")

def post_tweet(content: str, media_path: str = None):
    client = get_X_client()
    api_v1 = get_X_v1_api() 
    
    try:
        media_ids = []
        logger.info(f"Uploading media from path: {media_path}")
        
        if media_path:
            logger.info(f"Uploading media from path: {media_path}")
            media = api_v1.media_upload(media_path)
            logger.info("Media upload response:", media)
            media_ids.append(media.media_id)
            logger.info(f"Media uploaded successfully, media_id: {media.media_id}")
            
        response = client.create_tweet(text=content, media_ids=media_ids if media_ids else None)
        
        logger.info(f"Tweet ID: {response.data['id']}")
        return { "status": "success", "tweet_id": response.data['id'] }
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return { "status": "error", "message": str(e) }