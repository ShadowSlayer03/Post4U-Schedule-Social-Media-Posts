# app/main.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.post import Post
from app.api.routes import router
from app.config import settings
from app.services.scheduler import init_scheduler

app = FastAPI()

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

app.include_router(router)