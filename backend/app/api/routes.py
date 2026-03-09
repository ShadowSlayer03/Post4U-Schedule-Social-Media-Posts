import uuid

from fastapi import APIRouter, UploadFile, File, Form
from werkzeug.utils import secure_filename
from app.models.post import Post
from app.services.publisher import publish_to_platform
from app.services.scheduler import scheduler_service
from datetime import datetime, timezone
import os
import shutil

router = APIRouter()

# Get all posts
@router.get("/posts/")
async def get_posts():
    posts = await Post.find_all().to_list()
    if not posts:
        return {"message": "No posts found", "posts": [], "status_code": 404 }
    
    serialized = []
    for post in posts:
        data = post.model_dump()
        data["id"] = str(post.id)
        serialized.append(data)

    return {"message": f"{len(posts)} posts found", "posts": serialized, "status_code": 200 }

# Create a new post (with optional scheduling)
@router.post("/posts/")
async def create_post(
    content: str = Form(...),
    platforms: str = Form(...),
    scheduled_time: str = Form(None),
    media: UploadFile = File(None)
):
    
    media_path = None
    if media:
        static_dir = "app/static"
        os.makedirs(static_dir, exist_ok=True)
        
        ext = os.path.splitext(media.filename)[1]
        
        unique_name = f"{uuid.uuid4().hex}{ext}"
        safe_name = secure_filename(unique_name)
        
        media_path = os.path.join(static_dir, safe_name)
        with open(media_path, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)

    post = Post(
        content=content,
        platforms=[p.strip().lower() for p in platforms.split(",")],
        scheduled_time=datetime.fromisoformat(scheduled_time) if scheduled_time else None,
        media_path=media_path
    )
    await post.insert()

    if post.scheduled_time and post.scheduled_time > datetime.now(timezone.utc):
        job_id = await scheduler_service.schedule_post(str(post.id), post.scheduled_time)
        return { "message": "Post scheduled", "post_id": str(post.id), "job_id": job_id, "status_code": 200 }

    results = {}
    for platform in post.platforms:
        results[platform] = await publish_to_platform(platform, post.content, post.media_path)

    post.status = results
    await post.save()
    return { "message": "Post published", "post_id": str(post.id), "results": results, "status_code": 200 }

# Unschedule posts
@router.post("/posts/{id}/unschedule/")
async def unschedule_post(id: str):
    post = await Post.get(id)
    if post is None:
        return { "message": "Post not found", "post_id": id, "status_code": 404 }
    await post.delete()
    
    success = await scheduler_service.unschedule_post(id)
    if success:
        return { "message": "Post unscheduled", "post_id": id, "status_code": 200 }
    return { "message": "Post not found or not scheduled", "post_id": id, "status_code": 404 }
