# Post4U - Frontend

Reflex-powered dashboard for composing, scheduling, previewing, and managing social media posts. Connects to the Post4U FastAPI backend.

### ✨ Features
- **Modern UI**: Clean, responsive dashboard built with **Reflex**.
- **Unified Composer**: Create one post, preview it for all 5 platforms instantly.
- **Smart Tabs**:
  - **Schedule Post**: Calendar-based scheduling.
  - **Post Now**: Instant multi-platform blasts.
  - **Edit/Unschedule**: Full control over your pending drafts.
  - **History**: Traceable post status (Success/Failed) with full logs.
- **Rich Media**: Dedicated upload zone for post attachments.
- **Dynamic Previews**: Live X, Reddit, Telegram, Discord, and Bluesky templates.
- **Auto-Scraping**: Fetches OpenGraph (OG) data (Title, Image, Desc) for links.
- **Character Limits**: Visual counters to prevent over-length posts per platform.

### 🛠️ Tech Stack
- **Reflex**: Pure Python-based web framework for building performant web apps.
- **httpx**: Modern async HTTP client for backend communication.
- **BeautifulSoup4**: Robust link metadata scraping.
- **PyTZ**: Precise timezone synchronization for scheduling.

### Local Dev Setup

Requires [uv](https://github.com/astral-sh/uv) and the backend already running.

```bash
cd frontend
uv venv && .venv\Scripts\activate   # Windows
# source .venv/bin/activate          # macOS/Linux
uv pip install -r requirements.txt
cp .env.example .env                 # fill in credentials
uv run reflex run
```

> Dashboard is live at `http://localhost:3000`. Reflex also uses port `8001` internally — keep both free.

### Environment Variables

Create a `.env` file inside the `frontend/` directory:

| Variable | Required | Description |
|---|---|---|
| `POST4U_API_KEY` | ✅ | Must match the key set in the backend `.env`. Sent as `X-API-Key` on every request. |
| `BACKEND_URL` | ✅ | URL of the FastAPI backend. Defaults to `http://localhost:8000`. |

```env
POST4U_API_KEY=your_secret_key_here
BACKEND_URL=http://localhost:8000
```

#### Connecting to a remote / Docker backend

If the backend is running on another machine or inside Docker, just update `BACKEND_URL`:

```env
BACKEND_URL=http://192.168.1.100:8000
# or for Docker on the same machine:
BACKEND_URL=http://host.docker.internal:8000
```

No code changes needed — the state manager reads this at runtime.

### Usage
- Access the frontend in your browser at `http://localhost:3000`
- Make sure the backend is running at `http://localhost:8000` before using the dashboard

### Security
The frontend reads `POST4U_API_KEY` from its own `.env` file via `python-dotenv` and sends it as the `X-API-Key` header on every backend request. Keep your frontend `.env` out of version control (it is already covered by `.gitignore`).

### Contributing
Contributions are welcome! Open an issue first for large changes.

### License
MIT License

---

← [Back to main README](../README.md) | [Backend README →](../backend/README.md)

### Maintainers
- ShadowSlayer03 (admin)

---
For backend setup and full project details, see the main project README.
