from typing import List, Optional
from beanie import Document
from datetime import datetime, timezone
from pydantic import BaseModel, Field, field_validator
from beanie import Document, before_event, Insert, Update, SaveChanges, Replace

class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.now(timezone.utc)

class Post(TimestampMixin, Document):
    content: str
    platforms: List[str]
    scheduled_time: Optional[datetime] = None
    status: dict = {}
    media_path: Optional[str] = None

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