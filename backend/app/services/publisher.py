import asyncio
from app.controllers.post_reddit import post_to_reddit
from app.controllers.post_discord import post_to_discord
from app.controllers.post_telegram import post_to_telegram
from app.controllers.post_x import post_tweet
from app.controllers.post_bluesky import post_to_bluesky
from app.config import settings

def _publish_sync(platform: str, content: str, media_paths: list[str] = None) -> dict:
    """Synchronous publish — runs in a thread pool executor."""
    platform = platform.lower()
    if platform == "x":
        if not settings.TWITTER_API_KEY_MAIN:
            return {"status": "error", "message": "X credentials not configured in .env"}
        return post_tweet(content, media_paths)
    elif platform == "reddit":
        if not settings.REDDIT_CLIENT_ID:
            return {"status": "error", "message": "Reddit credentials not configured in .env"}
        return post_to_reddit(content, subreddit=settings.REDDIT_SUBREDDIT, media_paths=media_paths)
    elif platform == "telegram":
        if not settings.TELEGRAM_BOT_TOKEN:
            return {"status": "error", "message": "Telegram credentials not configured in .env"}
        return post_to_telegram(content, media_paths=media_paths)
    elif platform == "discord":
        if not settings.DISCORD_WEBHOOK_URL:
            return {"status": "error", "message": "Discord credentials not configured in .env"}
        return post_to_discord(content, media_paths=media_paths)
    elif platform == "bluesky":
        if not settings.BLUESKY_APP_ID:
            return {"status": "error", "message": "Bluesky credentials not configured in .env"}
        
        return post_to_bluesky(content, media_paths=media_paths)
    else:
        return {"status": "error", "message": f"Unsupported platform: {platform}"}

async def publish_to_platform(platform: str, content: str, media_paths: list[str] = None) -> dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _publish_sync, platform, content, media_paths)