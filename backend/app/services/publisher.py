from app.controllers.post_reddit import post_to_reddit
from app.config import settings
from backend.app.controllers.post_discord import post_to_discord
from backend.app.controllers.post_telegram import post_to_telegram
from backend.app.controllers.post_x import post_tweet

def publish_to_platform(platform: str, content: str):
    if platform == "x":
        if not settings.TWITTER_API_KEY_MAIN:
            return {"status": "skipped", "message": "X credentials not set"}
        return post_tweet(content)
    elif platform == "reddit":
        if not settings.REDDIT_CLIENT_ID:
            return {"status": "skipped", "message": "Reddit credentials not set"}
        return post_to_reddit(content, subreddit="test")
    elif platform == "telegram":
        if not settings.TELEGRAM_BOT_TOKEN:
            return {"status": "skipped", "message": "Telegram credentials not set"}
        return post_to_telegram(content)
    elif platform == "discord":
        if not settings.DISCORD_WEBHOOK_URL:
            return {"status": "skipped", "message": "Discord credentials not set"}
        return post_to_discord(content)
    else:
        return {"status": "error", "message": f"Unsupported platform: {platform}"}