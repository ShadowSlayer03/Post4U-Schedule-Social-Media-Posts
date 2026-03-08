import requests
from app.config import settings


def post_to_discord(content: str):
    try:
        payload = {"content": content}
        response = requests.post(settings.DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        return {"status": "success", "platform_post_id": None}
    except Exception as e:
        return {"status": "error", "message": str(e)}