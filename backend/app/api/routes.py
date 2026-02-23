from app.services.scheduler import post_tweet
from fastapi import APIRouter
from app.models.post import Post
from datetime import datetime, timezone

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to the Post Scheduler API"}

@router.get("/posts/")
async def get_posts():
    posts = await Post.find_all().to_list()
    return posts

@router.post("/posts/")
async def create_post(post: Post):
    await post.insert()

    if post.scheduled_time and post.scheduled_time > datetime.now(timezone.utc):
        schedule_post(str(post.id), post.content, post.platforms, post.scheduled_time)
        return {"message": "Post scheduled", "post_id": str(post.id)}

    # Post immediately
    results = {}
    for platform in post.platforms:
        results[platform] = publish_to_platform(platform, post.content)

    post.status = results
    await post.save()

    return {"message": "Post published", "post_id": str(post.id), "results": results}