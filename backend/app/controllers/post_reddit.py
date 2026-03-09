import os
import logging
from app.services.reddit_client import get_reddit_client
from app.config import settings

logger = logging.getLogger("uvicorn.error")

_VIDEO_EXTS = {".mp4", ".mov", ".avi"}


def post_to_reddit(content: str, subreddit: str, media_paths: list[str] = None):
    """
    Post to Reddit. Behaviour depends on what media is attached:

    - No media       → self-text post
    - 1 image        → image post  (submit_image)
    - 1 video        → video post  (submit_video)
    - 2+ images      → gallery     (submit_gallery)
    - Mixed or video + image → falls back to self-text (PRAW limitation)
    """
    try:
        reddit = get_reddit_client()
        sub = reddit.subreddit(subreddit)
        title = content[:300]

        if not media_paths:
            submission = sub.submit_selfpost(title=title, selftext=content)

        elif len(media_paths) == 1:
            path = media_paths[0]
            ext = os.path.splitext(path)[1].lower()
            if ext in _VIDEO_EXTS:
                submission = sub.submit_video(title=title, video_path=path)
            else:
                submission = sub.submit_image(title=title, image_path=path)

        else:
            image_paths = [p for p in media_paths if os.path.splitext(p)[1].lower() not in _VIDEO_EXTS]
            if image_paths:
                images = [{"image_path": p, "caption": ""} for p in image_paths]
                submission = sub.submit_gallery(title=title, images=images)
            else:
                logger.warning("Reddit gallery requires images; falling back to self-text post")
                submission = sub.submit_selfpost(title=title, selftext=content)

        logger.info(f"Reddit post successful, submission id: {submission.id}")
        return {"status": "success", "platform_post_id": submission.id}

    except Exception as e:
        logger.error(f"Reddit error: {e}")
        return {"status": "error", "message": str(e)}
