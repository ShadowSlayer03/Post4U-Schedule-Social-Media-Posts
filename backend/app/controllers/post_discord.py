import json
import os
import logging
import requests
from app.config import settings

logger = logging.getLogger("uvicorn.error")


def post_to_discord(content: str, media_paths: list[str] = None):
    try:
        if media_paths:
            # Discord webhooks accept files via multipart form data.
            # The JSON payload goes in the "payload_json" field.
            opened_files = []
            files_param = []
            for i, path in enumerate(media_paths):
                f = open(path, "rb")
                opened_files.append(f)
                files_param.append((
                    f"files[{i}]",
                    (os.path.basename(path), f, "application/octet-stream")
                ))
            try:
                response = requests.post(
                    settings.DISCORD_WEBHOOK_URL,
                    data={"payload_json": json.dumps({"content": content})},
                    files=files_param,
                    timeout=30
                )
            finally:
                for f in opened_files:
                    f.close()
        else:
            response = requests.post(
                settings.DISCORD_WEBHOOK_URL,
                json={"content": content},
                timeout=10
            )

        response.raise_for_status()
        logger.info("Discord post successful")
        return {"status": "success", "platform_post_id": None}

    except Exception as e:
        logger.error(f"Discord error: {e}")
        return {"status": "error", "message": str(e)}
