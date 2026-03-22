from app.services.bluesky_client import get_bluesky_client

def post_to_bluesky(content, media_paths=None):
    client = get_bluesky_client()
    
    try:
        if media_paths:
            image_blobs = []
            for path in media_paths[:4]:
                with open(path, "rb") as f:
                    image_blobs.append(f.read())
            
            response = client.send_images(
                text=content,
                images=image_blobs
            )
        else:
            response = client.send_post(text=content)
            
        return {"status": "success", "platform_post_id": response.uri}
    except Exception as e:
        return {"status": "error", "message": f"Failed to post to Bluesky: {str(e)}"}
