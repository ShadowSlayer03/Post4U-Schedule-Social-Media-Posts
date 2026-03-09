import json
import os
import logging
import requests
from app.config import settings

logger = logging.getLogger("uvicorn.error")

_VIDEO_EXTS = {".mp4", ".mov", ".avi"}
_GIF_EXTS = {".gif"}


def _get_media_type(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in _VIDEO_EXTS:
        return "video"
    if ext in _GIF_EXTS:
        return "animation"
    return "photo"


def post_to_telegram(content: str, media_paths: list[str] = None) -> dict:
    """
    Send a message (with optional media) to a Telegram channel.

    - No media      → sendMessage
    - 1 file        → sendPhoto / sendVideo / sendAnimation (with caption)
    - 2–10 files    → sendMediaGroup (caption on first item)

    Requirements:
    - Bot must be added to the channel as an Administrator
    - TELEGRAM_CHANNEL_ID: @yourchannel  OR  -100xxxxxxxxxx
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    channel_id = settings.TELEGRAM_CHANNEL_ID
    base_url = f"https://api.telegram.org/bot{bot_token}"

    try:
        if not media_paths:
            response = requests.post(
                f"{base_url}/sendMessage",
                json={"chat_id": channel_id, "text": content, "parse_mode": "HTML"},
                timeout=10
            )

        elif len(media_paths) == 1:
            path = media_paths[0]
            media_type = _get_media_type(path)
            method_map = {"photo": "sendPhoto", "video": "sendVideo", "animation": "sendAnimation"}
            file_key_map = {"photo": "photo", "video": "video", "animation": "animation"}

            with open(path, "rb") as f:
                response = requests.post(
                    f"{base_url}/{method_map[media_type]}",
                    data={"chat_id": channel_id, "caption": content, "parse_mode": "HTML"},
                    files={file_key_map[media_type]: f},
                    timeout=60
                )

        else:
            capped_paths = media_paths[:10]
            media_group = []
            files_param = {}
            opened_files = []

            for i, path in enumerate(capped_paths):
                attach_name = f"file{i}"
                media_type = _get_media_type(path)
                if media_type == "animation":
                    media_type = "photo"

                f = open(path, "rb")
                opened_files.append(f)
                files_param[attach_name] = f

                item = {"type": media_type, "media": f"attach://{attach_name}"}
                if i == 0:
                    item["caption"] = content
                    item["parse_mode"] = "HTML"
                media_group.append(item)

            try:
                response = requests.post(
                    f"{base_url}/sendMediaGroup",
                    data={"chat_id": channel_id, "media": json.dumps(media_group)},
                    files=files_param,
                    timeout=60
                )
            finally:
                for f in opened_files:
                    f.close()

        response.raise_for_status()
        data = response.json()

        result = data["result"]
        message_id = result[0]["message_id"] if isinstance(result, list) else result["message_id"]
        logger.info(f"Telegram post successful, message_id: {message_id}")
        return {"status": "success", "platform_post_id": message_id}

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