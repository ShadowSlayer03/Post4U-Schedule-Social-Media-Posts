import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from werkzeug.utils import secure_filename
from app.models.post import Post
from app.services.publisher import publish_to_platform
from app.services.scheduler import scheduler_service
from datetime import datetime, timezone
from app.api.utils.check_files import check_files

router = APIRouter()

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  
MAX_FILES = 4                        
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "video/mp4", "video/quicktime", "video/x-msvideo"}
ALLOWED_PLATFORMS = {"x", "reddit", "telegram", "discord"}

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
    media: list[UploadFile] = File(default=[])
):
    platform_list = [p.strip().lower() for p in platforms.split(",")]
    invalid_platforms = set(platform_list) - ALLOWED_PLATFORMS
    if invalid_platforms:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown platform(s): {', '.join(invalid_platforms)}. Allowed: {', '.join(ALLOWED_PLATFORMS)}"
        )

    media_paths = []

    if media:
        if len(media) > MAX_FILES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You can upload up to {MAX_FILES} media files per post."
            )
        
        validated_results = await check_files(media)

        static_dir = "app/static"
        os.makedirs(static_dir, exist_ok=True)

        for item in validated_results:
            ext = os.path.splitext(item["filename"])[1].lower()
            safe_name = secure_filename(f"{uuid.uuid4().hex}{ext}")
            media_path = os.path.join(static_dir, safe_name)

            def _write_file(path=media_path, data=item["bytes"]):
                with open(path, "wb") as f:
                    f.write(data)

            await run_in_threadpool(_write_file)
            media_paths.append(media_path)

    post = Post(
        content=content,
        platforms=platform_list,
        scheduled_time=datetime.fromisoformat(scheduled_time) if scheduled_time else None,
        media_paths=media_paths
    )
    await post.insert()

    if post.scheduled_time and post.scheduled_time > datetime.now(timezone.utc):
        job_id = await scheduler_service.schedule_post(str(post.id), post.scheduled_time)
        return { "message": "Post scheduled", "post_id": str(post.id), "job_id": job_id, "status_code": 200 }

    results = {}
    for platform in post.platforms:
        results[platform] = await publish_to_platform(platform, post.content, post.media_paths)

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
