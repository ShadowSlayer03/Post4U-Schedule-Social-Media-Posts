from datetime import datetime
import os
import re
import reflex as rx
import httpx
import pytz
from bs4 import BeautifulSoup
from tzlocal import get_localzone
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class PlatformStatus(BaseModel):
    status: str = "unknown"
    platform_post_id: Optional[str | int] = None
    error: Optional[str] = None
    message: Optional[str] = None


class PostRecord(BaseModel):
    id: str
    content: str
    platforms: list[str]
    status: dict[str, PlatformStatus]
    created_at: str
    scheduled_time: Optional[str] = None
    media_paths: Optional[list[str]] = None

class CharLimits(BaseModel):
    platform: str
    is_over: bool


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
    delete_post_content: str = ""

    og_title: str = ""
    og_image: str = ""
    og_description: str = ""
    og_url: str = ""
    is_fetching_og: bool = False

    # Edit Post tab
    edit_post_id: str = ""
    edit_post_content: str = ""
    edit_post_platforms: list[str] = []
    edit_post_scheduled_time: str | None = None

    # History tab filters
    history_filter_platform: str = ""   # "" = all platforms
    history_filter_status: str = ""     # "" = all, "success", "error"

    # Constant but can be changed acc to platform capabilities
    limits = {"x": 500, "reddit": 40000, "telegram": 4096, "discord": 2000, "bluesky": 300}

    _MAX_RESPONSE_BYTES = 512_000

    @rx.var
    def preview_content(self) -> str:
        if self.active_tab == "edit_post":
            return self.edit_post_content
        return self.content

    @rx.var
    def preview_platforms(self) -> list[str]:
        if self.active_tab == "edit_post":
            return self.edit_post_platforms
        return self.platforms

    @rx.var
    def post_select_options(self) -> list[str]:
        """Returns formatted strings for the select dropdown: 'content[:40] | scheduled_time'"""
        return [
            f"{p.id} | {p.content[:40]}"
            for p in self.posts
                if p.status == {} and p.scheduled_time!=None and p.scheduled_time > datetime.now(pytz.utc).isoformat()
        ]
    
    @rx.var
    def char_limits(self) -> list[CharLimits]:
        results = []
        content_len = len(self.content)
        for p in self.platforms:
            limit = self.limits.get(p, 2000)
            results.append(CharLimits(platform=p, is_over=content_len > limit))
        return results
    
    @rx.var
    def max_characters(self) -> int:
        if not self.platforms:
            return 2000
        return min([self.limits.get(p, 2000) for p in self.platforms])

    @rx.var
    def posts_that_can_be_edited(self) -> list[PostRecord]:
        editable_posts = []
        if self.posts:
            for p in self.posts:
                current_time_utc = datetime.now(pytz.utc)
                if p.status == {} and p.scheduled_time!=None and p.scheduled_time > current_time_utc.isoformat():
                    editable_posts.append(p)
        return editable_posts

    @rx.var
    def filtered_posts(self) -> list[PostRecord]:
        result = []
        for p in self.posts:
            if self.history_filter_platform:
                if self.history_filter_platform not in p.platforms:
                    continue
                if self.history_filter_status:
                    plat_status = p.status.get(self.history_filter_platform)
                    if plat_status is None:
                        continue
                    if plat_status.status != self.history_filter_status:
                        continue
            elif self.history_filter_status:
                matched = any(
                    ps.status == self.history_filter_status
                    for ps in p.status.values()
                )
                if not matched:
                    continue
            result.append(p)
        return result

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def set_history_filter_platform(self, platform: str):
        if self.history_filter_platform == platform:
            self.history_filter_platform = ""
        else:
            self.history_filter_platform = platform

    @rx.event
    def set_history_filter_status(self, status: str):
        if self.history_filter_status == status:
            self.history_filter_status = ""
        else:
            self.history_filter_status = status

    @rx.event
    def clear_history_filters(self):
        self.history_filter_platform = ""
        self.history_filter_status = ""

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
        
        urls = re.findall(r'https?://[^\s{}()<>]+(?:[^\s{}()<>\[\]]|\([^\s{}()<>\[\]]*\))', val)
        if urls:
            first_url = urls[0].rstrip('.,!?;:')
            if first_url != self.og_url:
                return DashboardState.fetch_og_preview(first_url)
        elif self.og_url:
            self.og_title = ""
            self.og_image = ""
            self.og_description = ""
            self.og_url = ""
        return

    def _is_safe_url(self, url: str) -> tuple[bool, str]:
        try:
            from urllib.parse import urlparse
            stripped_url = url.strip()
            parsed = urlparse(stripped_url)

            if parsed.scheme != "https":
                return False, "Only HTTPS URLs are allowed."

            hostname = parsed.hostname
            if not hostname:
                return False, "URL has no hostname."

            return True, ""
        except Exception as e:
            return False, f"URL validation error: {e}"

    @rx.event(background=True)
    async def fetch_og_preview(self, url: str):
        async with self as state:
            state.og_url = url
            state.is_fetching_og = True
            state.og_title = ""
            state.og_image = ""
            state.og_description = ""

        try:
            cleaned_url = url.strip()

            is_safe, reason = self._is_safe_url(cleaned_url)
            if not is_safe:
                yield rx.toast.warning(f"Blocked link preview: {reason}", duration=5000)
                return

            async with httpx.AsyncClient(
                timeout=5.0,
                follow_redirects=False,
            ) as client:
                response = await client.get(
                    cleaned_url,
                    headers={"User-Agent": "Mozilla/5.0 (compatible; Post4U/1.0; +https://post4u.app)"},
                )

                if response.status_code in (301, 302, 303, 307, 308):
                    redirect_url = response.headers.get("location", "")
                    if redirect_url:
                        is_safe, reason = self._is_safe_url(redirect_url)
                        if not is_safe:
                            yield rx.toast.warning(f"Blocked redirect to unsafe URL ({reason}): {redirect_url}", duration=5000)
                            return
                        response = await client.get(
                            redirect_url,
                            headers={"User-Agent": "Mozilla/5.0 (compatible; Post4U/1.0; +https://post4u.app)"},
                        )

                if response.status_code != 200:
                    return

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    yield rx.toast.warning(f"Skipping non-HTML response: {content_type}", duration=5000)
                    return

                raw_bytes = b""
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    raw_bytes += chunk
                    if len(raw_bytes) >= self._MAX_RESPONSE_BYTES:
                        break

                soup = BeautifulSoup(raw_bytes, "html.parser")

                og_title_tag = soup.find("meta", property="og:title")
                og_image_tag = soup.find("meta", property="og:image")
                og_description_tag = soup.find("meta", property="og:description")

                title = soup.title.string.strip() if soup.title and soup.title.string else ""
                description_tag = soup.find("meta", attrs={"name": "description"})

                async with self as state:
                    state.og_title = og_title_tag["content"] if og_title_tag else (title or "")
                    state.og_image = og_image_tag["content"] if og_image_tag else ""
                    state.og_description = og_description_tag["content"] if og_description_tag else (description_tag["content"] if description_tag else "")

        except Exception as e:
            yield rx.toast.warning(f"Error fetching link preview: {e}", duration=5000)
        finally:
            async with self as state:
                state.is_fetching_og = False

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
        self.delete_post_content = val.split(" | ")[1] if " | " in val else ""

    @rx.event
    def select_post_for_edit(self, post_id: str):
        """Populate the edit form by finding the post in self.posts."""
        for post in self.posts:
            if post.id == post_id:
                self.edit_post_id = post.id
                self.edit_post_content = post.content
                self.edit_post_platforms = list(post.platforms)
                self.edit_post_scheduled_time = post.scheduled_time
        return

    @rx.event
    def clear_edit_selection(self):
        self.edit_post_id = ""
        self.edit_post_content = ""
        self.edit_post_platforms = []
        self.edit_post_scheduled_time = None

    @rx.event
    def set_edit_content(self, val: str):
        self.edit_post_content = val

    @rx.event
    def toggle_edit_platform(self, platform: str):
        if platform in self.edit_post_platforms:
            self.edit_post_platforms = [p for p in self.edit_post_platforms if p != platform]
        else:
            self.edit_post_platforms = self.edit_post_platforms + [platform]

    @rx.event
    def set_edit_scheduled_time(self, val: str):
        self.edit_post_scheduled_time = val

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
            # Handle any ISO 8601 string that already carries timezone info (Z or +HH:MM)
            if "T" in raw_time and (raw_time.endswith("Z") or "+" in raw_time[10:] or raw_time.count("-") > 2):
                clean = raw_time.replace("Z", "+00:00")
                utc_dt = datetime.fromisoformat(clean).astimezone(pytz.utc)
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
        is_edit = self.active_tab == "edit_post"

        content = self.edit_post_content if is_edit else self.content
        platforms = self.edit_post_platforms if is_edit else self.platforms
        scheduled_time = self.edit_post_scheduled_time if is_edit else self.scheduled_time

        if not content:
            yield rx.toast.warning("Content cannot be empty.", duration=5000)
            return

        if not platforms:
            yield rx.toast.warning("Pick at least one platform.", duration=5000)
            return

        content_len = len(content)
        for p in platforms:
            limit = self.limits.get(p, 2000)
            if content_len > limit:
                yield rx.toast.warning(f"Content exceeds character limit for {p.capitalize()}.", duration=5000)
                return

        utc_iso = None
        if scheduled_time:
            utc_iso = self._parse_to_utc(scheduled_time)
            if utc_iso is None:
                yield rx.toast.error("Invalid scheduled time format.", duration=5000)
                return
            print(f"[Submit] Final UTC ISO: {utc_iso}")

        self.is_posting = True
        yield

        try:
            data = {
                "content": content,
                "platforms": ",".join(platforms),
            }

            if utc_iso:
                data["scheduled_time"] = utc_iso

            files = None
            if self.media_files:
                files = [("media", (f[0], f[1], f[2])) for f in self.media_files]

            api_key = os.getenv("POST4U_API_KEY")

            async with httpx.AsyncClient() as client:
                backend_url = os.getenv("BACKEND_URL")

                if is_edit:
                    url = f"{backend_url}/posts/{self.edit_post_id}/"
                else:
                    url = f"{backend_url}/posts/"
                
                if is_edit:
                    r = await client.put(
                    url,
                    data=data,
                    files=files,
                    headers={"X-API-Key": api_key},
                    timeout=10
                    )
                else:
                    r = await client.post(
                    url,
                    data=data,
                    files=files,
                    headers={"X-API-Key": api_key},
                    timeout=10
                )
                if r.status_code == 200:
                    body = r.json()
                    results = body.get("results", {})

                    any_error = False
                    for plat, plat_result in results.items():
                        if isinstance(plat_result, dict) and plat_result.get("status") == "error":
                            any_error = True
                            msg = plat_result.get("message", "Unknown error")
                            yield rx.toast.error(f"{plat.capitalize()}: {msg}", duration=7000)

                    if is_edit:
                        if not any_error:
                            yield rx.toast.success("Post updated successfully!", duration=5000)
                        self.clear_edit_selection()
                        self.media_files = []
                        yield DashboardState.load_posts
                    elif self.active_tab == "schedule":
                        if not any_error:
                            yield rx.toast.success("Scheduled successfully!", duration=5000)
                        self.clear_form()
                    else:
                        if not any_error:
                            yield rx.toast.success("Posted successfully!", duration=5000)
                        elif results and all(
                            isinstance(v, dict) and v.get("status") == "error"
                            for v in results.values()
                        ):
                            pass
                        else:
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
                backend_url = os.getenv("BACKEND_URL")

                r = await client.get(f"{backend_url}/posts/", timeout=10,
                                     headers={
                                         "X-API-Key": api_key
                                     })
                if r.status_code == 200:
                    raw_posts = r.json().get("posts", [])
                    self.posts = [PostRecord(**p)
                                  for p in raw_posts]
                    yield rx.toast.success(f"Successfully loaded {len(self.posts)} posts.", duration=5000)
                else:
                    yield rx.toast.error(f"Failed to load posts (HTTP {r.status_code})", duration=5000)

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
                backend_url = os.getenv("BACKEND_URL")

                r = await client.post(
                    f"{backend_url}/posts/{self.delete_post_id}/unschedule/",
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
                    yield rx.toast.error(f"Error: {r.text}", duration=5000)

        except Exception as e:
            yield rx.toast.error(f"Connection error: {str(e)}", duration=5000)

        self.is_posting = False
        self.delete_post_content = ""
