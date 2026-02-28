# Scheduling Architecture — Dev Notes

## The Problem with Default APScheduler

APScheduler runs as a background thread **inside the FastAPI process**. Jobs are held in memory by default. If the container restarts or crashes, all pending scheduled jobs are lost silently — posts never publish, no error thrown.

---

## The Fix — MongoDB Job Store (No New Infrastructure)

Use APScheduler's built-in MongoDB job store. You already have Mongo running. This makes jobs **persistent across restarts** with zero new containers.

```python
from apscheduler.jobstores.mongodb import MongoDBJobStore

jobstores = {
    'default': MongoDBJobStore(
        database='post_scheduler',
        collection='scheduled_jobs',
        client=mongo_client
    )
}
```

Docker Compose stays the same — just `api` + `mongo`. No Redis, no extra service.

---

## Retry on Publish Failure

If a platform API is down or rate-limited, catch the exception inside `publisher.py` and reschedule with a delay + attempt counter. Keep it self-contained.

```python
async def publish_with_retry(post_id: str, attempt: int = 1):
    try:
        await publish(post_id)
    except Exception:
        if attempt < 3:
            scheduler.add_job(
                publish_with_retry,
                'date',
                run_date=datetime.utcnow() + timedelta(minutes=5 * attempt),
                args=[post_id, attempt + 1]
            )
```

---

## SchedulerService Abstraction — Do This Now

Don't call APScheduler directly in routes. Wrap it behind a service class so you can swap the backend later without touching routes.

```python
# services/scheduler.py
class SchedulerService:
    async def schedule_post(self, post_id: str, run_at: datetime):
        scheduler.add_job(
            publish_with_retry,
            'date',
            run_date=run_at,
            args=[post_id]
        )

    async def cancel_post(self, job_id: str):
        scheduler.remove_job(job_id)
```

One interface = one place to change when/if you ever swap APScheduler out.

---

## What About the Cron Project?

The separate cron visualization + hosting tool is **not a dependency of Post4U**. They are independent projects.

- Post4U handles its own scheduling internally (via the above)
- The cron tool is a standalone generic scheduler for any use case
- Power users *can* optionally replace Post4U's internal scheduler with the cron service, but it's opt-in — not required for self-hosting

**Self-hosting story stays clean:**
```bash
docker compose up -d   # just api + mongo, nothing else needed
```