import requests
from app.config import settings

def post_to_telegram(content: str):
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": settings.TELEGRAM_CHANNEL_ID,
            "text": content
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return {"status": "success", "message_id": response.json()["result"]["message_id"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}