import logging
import requests
from app.config import settings

logger = logging.getLogger("uvicorn.error")

def post_to_telegram(content: str) -> dict:
    """
    Send a message to a Telegram channel.

    Requirements:
    - Bot must be added to the channel as an Administrator
    - TELEGRAM_CHANNEL_ID must be in one of these formats:
        Public channel:  @yourchannel
        Private channel: -100xxxxxxxxxx  (numeric chat ID with -100 prefix)
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    channel_id = settings.TELEGRAM_CHANNEL_ID

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": channel_id,
        "text": content,
        "parse_mode": "HTML",   # supports <b>bold</b>, <i>italic</i>, <a href="">links</a>
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        message_id = data["result"]["message_id"]
        logger.info(f"Telegram message sent, message_id: {message_id}")
        return {"status": "success", "message_id": message_id}
    except requests.exceptions.HTTPError as e:
        try:
            error_description = response.json().get("description", str(e))
        except Exception:
            error_description = str(e)
        logger.error(f"Telegram HTTP error: {error_description}")
        return {"status": "error", "message": error_description}
    except requests.exceptions.Timeout:
        logger.error("Telegram request timed out")
        return {"status": "error", "message": "Request timed out"}
    except Exception as e:
        logger.error(f"Telegram unexpected error: {e}")
        return {"status": "error", "message": str(e)}