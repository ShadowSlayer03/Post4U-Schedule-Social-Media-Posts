from __future__ import annotations
from datetime import datetime, timedelta
import asyncio
import logging
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
from app.config import settings
from datetime import datetime, timezone

logger = logging.getLogger("uvicorn.error")

# -- Module-level scheduler instance, configured in init_scheduler() --
scheduler: AsyncIOScheduler | None = None


def init_scheduler() -> AsyncIOScheduler:
    """
    Build and return a configured AsyncIOScheduler with a MongoDB job store.
    Call this once during app startup AFTER the DB connection is established.
    APScheduler's MongoDBJobStore requires a synchronous PyMongo client.
    """
    global scheduler
    mongo_client = MongoClient(settings.MONGO_URI)
    jobstores = {
        "default": MongoDBJobStore(
            database=settings.DATABASE_NAME,
            collection="scheduled_jobs",
            client=mongo_client,
        )
    }
    executors = {
        "default": AsyncIOExecutor(),  # runs async jobs on the event loop
    }
    # Whole point of jobstore is that APScheduler will automatically check for due jobs on startup and run them, no need to handle it ourselves
    scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors)
    return scheduler


# ---------------------------------------------------------------------------
# Job function — must be top-level so APScheduler can re-import it by name
# ---------------------------------------------------------------------------

async def publish_with_retry(post_id: str, attempt: int = 1, retry_platforms: list[str] | None = None) -> None:
    """
    Fetch the post from MongoDB and publish to specified platforms.
    On failure, reschedule ONLY the failed platforms (passed as arg, not re-read from DB).
    retry_platforms=None means first attempt → use all platforms from the post.
    """
    from app.models.post import Post
    from app.services.publisher import publish_to_platform

    post = await Post.get(post_id)
    if post is None:
        logger.warning("publish_with_retry: post %s not found, skipping.", post_id)
        return

    platforms_to_post = retry_platforms if retry_platforms is not None else post.platforms

    results: dict = {}
    failed_platforms: list[str] = []

    for platform in platforms_to_post:
        try:
            result = await publish_to_platform(platform, post.content)
            results[platform] = result
            if result.get("status") == "error":
                failed_platforms.append(platform)
        except Exception as exc:
            logger.error("Platform %s failed on attempt %d: %s", platform, attempt, exc)
            results[platform] = {"status": "error", "message": str(exc)}
            failed_platforms.append(platform)

    post.status = {**post.status, **results}
    await post.save()

    if failed_platforms and attempt < 3:
        delay_minutes = 3 * attempt
        run_at = datetime.now(timezone.utc) + timedelta(minutes=delay_minutes)
        logger.info(
            "Retrying post %s (attempt %d→%d) for platforms %s in %d min",
            post_id, attempt, attempt + 1, failed_platforms, delay_minutes,
        )
        if scheduler:
            scheduler.add_job(
                publish_with_retry,
                "date",
                run_date=run_at,
                args=[post_id, attempt + 1, failed_platforms],
            )


# ---------------------------------------------------------------------------
# Service abstraction — routes call this, never APScheduler directly
# ---------------------------------------------------------------------------

class SchedulerService:
    async def schedule_post(self, post_id: str, run_at: datetime) -> str:
        """Add a one-shot job; returns the APScheduler job id."""
        
        job = scheduler.add_job(
            publish_with_retry,
            "date",
            run_date=run_at,
            args=[post_id],
            id=post_id,
            replace_existing=True,
        )
        return job.id

    async def unschedule_post(self, job_id: str) -> bool:
        """Remove a scheduled job by its ID. Returns True if removed, False if not found."""
        if scheduler is None:
            logger.error("Scheduler not initialized; cannot unschedule post %s", job_id)
            return False
        
        try:
            scheduler.remove_job(job_id)
            return True
        except Exception as e:
            logger.error("Failed to unschedule post %s, error: %s", job_id, e)
            return False


scheduler_service = SchedulerService()