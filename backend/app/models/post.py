from beanie import Document
from pydantic import BaseModel
from datetime import datetime, timezone

class Post(Document):
    content: str
    platform: str  # "LinkedIn" or "X"

    class Settings:
        name = "posts"