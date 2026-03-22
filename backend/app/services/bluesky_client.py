from atproto import Client
from app.config import settings

def get_bluesky_client():
    client = Client()

    if not settings.BLUESKY_APP_ID or not settings.BLUESKY_APP_PASSWORD:
        raise RuntimeError("Bluesky credentials not set in .env")
    bsClient = client.login(settings.BLUESKY_APP_ID, settings.BLUESKY_APP_PASSWORD)

    if not bsClient.did:
        raise RuntimeError("Failed to authenticate with Bluesky")
    return client
