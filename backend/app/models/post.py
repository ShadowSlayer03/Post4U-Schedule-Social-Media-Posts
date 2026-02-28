from typing import List, Optional
from beanie import Document
from datetime import datetime, timezone

class Post(Document):
    content: str
    platforms: List[str]
    scheduled_time: Optional[datetime] = None  # Always send in UTC from frontend/testing platform
    status: dict = {}  # Tracks each platform scheduled post result

    class Settings:
        name = "posts"