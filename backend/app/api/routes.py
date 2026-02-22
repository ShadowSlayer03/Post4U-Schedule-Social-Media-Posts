from app.services.scheduler import post_tweet
from fastapi import APIRouter
from app.models.post import Post

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to the Post Scheduler API"}

@router.post("/posts/")
async def create_post(post: Post):
    #await post.create()
    result = post_tweet(post.content)
    if result["status"] == "success":
        return {"message": "Post scheduled successfully", "tweet_id": result["tweet_id"]}
    else:
        return {"message": "Failed to schedule post", "error": result["message"]}