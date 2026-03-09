import logging

from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.post import Post
from app.api.routes import router
from app.config import settings
from app.services.scheduler import init_scheduler
from app.api.middleware.verify import verify_api_key
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import RateLimiter

logger = logging.getLogger("uvicorn.error")

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to Post4U - Open Source, Self-Hostable Post Scheduler API"}


@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DATABASE_NAME]
    await init_beanie(database=db, document_models=[Post])
    sched = init_scheduler()
    sched.start()


@app.on_event("shutdown")
async def shutdown_event():
    from app.services.scheduler import scheduler
    if scheduler:
        scheduler.shutdown()


app.include_router(router, dependencies=[Depends(verify_api_key), Depends(RateLimiter(limiter=Limiter(Rate(2, Duration.SECOND * 5))))])