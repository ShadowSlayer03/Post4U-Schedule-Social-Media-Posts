
import logging

from app.services.x_client import get_X_client, get_X_v1_api

logger = logging.getLogger("uvicorn.error")

def post_tweet(content: str, media_paths: list[str] = None):
    client = get_X_client()
    api_v1 = get_X_v1_api()

    try:
        media_ids = []

        if media_paths:
            for path in media_paths[:4]:
                logger.info(f"Uploading media from path: {path}")
                media = api_v1.media_upload(path)
                media_ids.append(media.media_id)
                logger.info(f"Media uploaded, media_id: {media.media_id}")

        response = client.create_tweet(
            text=content,
            media_ids=media_ids if media_ids else None
        )

        logger.info(f"Tweet ID: {response.data['id']}")
        return {"status": "success", "platform_post_id": response.data['id']}

    except Exception as e:
        logger.error(f"Error posting to X: {e}")
        return {"status": "error", "message": str(e)}
