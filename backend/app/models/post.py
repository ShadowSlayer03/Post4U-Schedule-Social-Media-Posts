from typing import List, Optional
from beanie import Document
from datetime import datetime, timezone

class Post(Document):
    content: str
    platforms: List[str]  # ["x", "reddit", "telegram", "discord"]
    scheduled_time: Optional[datetime] = None
    status: dict = {}  # per-platform result tracking

    class Settings:
        name = "posts"