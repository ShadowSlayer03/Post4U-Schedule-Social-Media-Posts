from typing import List, Optional
from beanie import Document
from datetime import datetime, timezone
from pydantic import field_validator

class Post(Document):
    content: str
    platforms: List[str]
    scheduled_time: Optional[datetime] = None
    status: dict = {}

    @field_validator("platforms", mode="before")
    @classmethod
    def lowercase_platforms(cls, v):
        if isinstance(v, list):
            return [p.lower() for p in v]
        return v

    @field_validator("scheduled_time", mode="before")
    @classmethod
    def ensure_utc(cls, v):
        if v is None:
            return v
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    class Settings:
        name = "posts"