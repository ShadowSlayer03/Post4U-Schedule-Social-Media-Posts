from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.publisher import publish_to_platform

scheduler = AsyncIOScheduler()

def publish_post(post_id: str, content: str, platforms: list):
    from app.models.post import Post
    import asyncio

    results = {}
    for platform in platforms:
        results[platform] = publish_to_platform(platform, content)

    async def update_status():
        post = await Post.get(post_id)
        if post:
            post.status = results
            await post.save()

    asyncio.create_task(update_status())

def schedule_post(post_id: str, content: str, platforms: list, scheduled_time: datetime):
    scheduler.add_job(
        publish_post,
        "date",
        run_date=scheduled_time,
        args=[post_id, content, platforms],
        id=post_id
    )