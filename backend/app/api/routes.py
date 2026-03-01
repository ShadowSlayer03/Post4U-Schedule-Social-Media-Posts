from fastapi import APIRouter
from app.models.post import Post
from app.services.publisher import publish_to_platform
from app.services.scheduler import scheduler_service
from datetime import datetime, timezone

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to Post4U - Open Source, Self-Hostable Post Scheduler API"}

@router.get("/posts/")
async def get_posts():
    posts = await Post.find_all().to_list()
    return posts

@router.post("/posts/")
async def create_post(post: Post):
    await post.insert()

    if post.scheduled_time and post.scheduled_time > datetime.now(timezone.utc):
        job_id = await scheduler_service.schedule_post(str(post.id), post.scheduled_time)
        return {"message": "Post scheduled", "post_id": str(post.id), "job_id": job_id}

    results = {}
    for platform in post.platforms:
        results[platform] = await publish_to_platform(platform, post.content)

    post.status = results
    await post.save()
    return {"message": "Post published", "post_id": str(post.id), "results": results}