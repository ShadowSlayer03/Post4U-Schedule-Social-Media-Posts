
from backend.app.services.x_client import get_X_client

def post_tweet(content: str):
    client = get_X_client()
    try:
        response = client.create_tweet(text=content)
        print(f"Tweet ID: {response.data['id']}")
        return { "status": "success", "tweet_id": response.data['id'] }
    except Exception as e:
        print(f"Error: {e}")
        return { "status": "error", "message": str(e) }