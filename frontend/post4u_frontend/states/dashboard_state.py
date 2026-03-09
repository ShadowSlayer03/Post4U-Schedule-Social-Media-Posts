from datetime import datetime
import os
import reflex as rx
import httpx
import pytz
from tzlocal import get_localzone
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class PlatformStatus(BaseModel):
    status: str = "unknown"
    platform_post_id: Optional[str] = None
    error: Optional[str] = None
    message: Optional[str] = None


class PostRecord(BaseModel):
    id: str
    content: str
    platforms: list[str]
    status: dict[str, PlatformStatus]
    created_at: str
    scheduled_time: Optional[str] = None


class DashboardState(rx.State):
    active_tab: str = "schedule"
    content: str = ""
    platforms: list[str] = []
    scheduled_time: str | None = None
    media_files: list[tuple[str, bytes, str]] = []
    posts: list[PostRecord] = []
    is_posting: bool = False
    is_refreshing: bool = False
    delete_post_id: str = ""

    @rx.var
    def post_select_options(self) -> list[str]:
        """Returns formatted strings for the select dropdown: 'content[:40] | scheduled_time'"""
        return [
            f"{p.id} | {p.content[:40]}"
            for p in self.posts
        ]

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def set_media_files(self, media_files: list[tuple[str, bytes, str]]):
        self.media_files = media_files

    @rx.event
    def toggle_platform(self, platform: str):
        if platform in self.platforms:
            self.platforms = [p for p in self.platforms if p != platform]
        else:
            self.platforms = self.platforms + [platform]

    @rx.event
    def set_content(self, val: str):
        self.content = val

    @rx.event
    def set_scheduled_time(self, val: str):
        self.scheduled_time = val

    @rx.event
    def set_delete_post_id(self, val: str):
        self.delete_post_id = val

    @rx.event
    def set_delete_post_from_option(self, val: str):
        """Parses 'content[:40] | scheduled_time' and stores just the id."""
        self.delete_post_id = val.split(" | ")[0] if " | " in val else val

    @rx.event
    def clear_form(self):
        self.content = ""
        self.platforms = []
        self.scheduled_time = None
        self.media_files = []

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if len(files) > 4:
            yield rx.toast.warning("You can only upload up to 4 media files per post.", duration=5000)
            return

        new_files = []
        for file in files:
            upload_data = await file.read()
            new_files.append((file.filename, upload_data, file.content_type))
        self.media_files = new_files

    def _parse_to_utc(self, raw_time: str) -> str | None:
        """
        Converts a datetime string to UTC ISO 8601.
        Handles two cases:
          1. ISO string with Z suffix (already UTC): "2026-03-05T20:30:00.000Z"
          2. Naive string from local input: "2026-03-06 02:00"
        """
        try:
            if "T" in raw_time and raw_time.endswith("Z"):
                clean = raw_time.replace("Z", "+00:00")
                utc_dt = datetime.fromisoformat(clean)
                print(f"[Datetime] Already UTC: {utc_dt}")
                return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            if len(raw_time) == 16:
                naive = datetime.strptime(raw_time, "%Y-%m-%d %H:%M")
            elif len(raw_time) == 19:
                naive = datetime.strptime(raw_time, "%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError(f"Unrecognized datetime format: {raw_time}")

            local_tz = get_localzone()
            print(f"[Datetime] Local timezone: {local_tz}")
            local = pytz.timezone(str(local_tz))

            local_dt = local.localize(naive, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            print(f"[Datetime] Local: {local_dt} → UTC: {utc_dt}")
            return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        except Exception as e:
            print(f"[Datetime] Error parsing datetime: {e}")
            return None

    @rx.event
    async def submit_post(self):
        if not self.content:
            yield rx.toast.warning("Content cannot be empty.", duration=5000)
            return

        if not self.platforms:
            yield rx.toast.warning("Pick at least one platform.", duration=5000)
            return

        utc_iso = None
        if self.scheduled_time:
            utc_iso = self._parse_to_utc(self.scheduled_time)
            if utc_iso is None:
                yield rx.toast.error("Invalid scheduled time format.", duration=5000)
                return
            print(f"[Submit] Final UTC ISO: {utc_iso}")

        self.is_posting = True
        yield

        try:
            data = {
                "content": self.content,
                "platforms": ",".join(self.platforms),
            }

            if utc_iso:
                data["scheduled_time"] = utc_iso

            files = None
            if self.media_files:
                files = [("media", (f[0], f[1], f[2])) for f in self.media_files]

            api_key = os.getenv("POST4U_API_KEY")

            async with httpx.AsyncClient() as client:
                r = await client.post(
                    "http://localhost:8000/posts/",
                    data=data,
                    files=files,
                    headers={
                        "X-API-Key": api_key
                    },
                    timeout=10
                )
                if r.status_code == 200:
                    yield rx.toast.success("Posted successfully!", duration=5000)
                    self.clear_form()
                else:
                    yield rx.toast.error(f"Error: {r.text}", duration=5000)

        except Exception as e:
            yield rx.toast.error(f"Connection error: {str(e)}", duration=5000)

        self.is_posting = False

    @rx.event
    async def load_posts(self):
        self.is_refreshing = True
        yield
        try:
            async with httpx.AsyncClient() as client:
                api_key = os.getenv("POST4U_API_KEY")
                r = await client.get("http://localhost:8000/posts/", timeout=10,
                                     headers={
                                         "X-API-Key": api_key
                                     })
                if r.status_code == 200:
                    raw_posts = r.json().get("posts", [])
                    self.posts = [PostRecord(**p)
                                  for p in raw_posts]
                    yield rx.toast.success(f"Successfully loaded {len(self.posts)} posts.", duration=5000)
        # Handle this better
        except Exception as e:
            yield rx.toast.error(f"Could not load posts: {str(e)}", duration=5000)
        finally:
            self.is_refreshing = False

    @rx.event
    async def unschedule_post(self):
        if not self.delete_post_id:
            yield rx.toast.warning("No post selected to unschedule.", duration=5000)
            return

        self.is_posting = True
        yield

        try:
            async with httpx.AsyncClient() as client:
                api_key = os.getenv("POST4U_API_KEY")
                r = await client.post(
                    f"http://localhost:8000/posts/{self.delete_post_id}/unschedule/",
                    timeout=10,
                    headers={
                        "X-API-Key": api_key
                    }
                )
                
                if r.status_code == 200:
                    yield rx.toast.success(r.json().get("message", "Post unscheduled successfully!"), duration=5000)
                    self.delete_post_id = ""
                    yield DashboardState.load_posts
                else:
                    print(r)
                    yield rx.toast.error(f"Error: {r.text}", duration=5000)

        except Exception as e:
            yield rx.toast.error(f"Connection error: {str(e)}", duration=5000)

        self.is_posting = False
