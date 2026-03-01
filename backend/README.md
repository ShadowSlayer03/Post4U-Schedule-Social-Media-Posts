## Post4U Backend

A self-hosted open source backend for scheduling and automatically posting content to X (Twitter), Reddit, Telegram, and Discord.

### Features
- Schedule posts for X (Twitter), Reddit, Telegram, and Discord
- Cross-post to multiple platforms in one request
- Automatic posting at specified times (scheduling)
- **Persistent scheduling — scheduled jobs survive server restarts via MongoDB job store**
- **Per-platform retry logic with exponential back-off (up to 3 attempts)**
- **Only failed platforms are retried — successful platforms are never re-posted**
- Per-platform success/failure tracking in MongoDB
- MongoDB database for storing scheduled posts and scheduler jobs
- FastAPI REST API
- Easy to self-host and use

### Tech Stack
- Python 3.11+
- FastAPI
- Beanie (MongoDB ODM) — async MongoDB models
- Motor — async MongoDB driver (app data)
- PyMongo — sync MongoDB driver (APScheduler job store)
- MongoDB
- Tweepy (Twitter/X API)
- PRAW (Reddit API)
- requests (Telegram/Discord webhooks)
- APScheduler 3.x with MongoDBJobStore (persistent scheduling)
- uv (dependency management)

### Setup
1. Clone the repository and navigate to the backend folder:
    ```bash
    git clone https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts.git
    cd backend
    ```
2. Create and activate a virtual environment:
    ```bash
    uv venv
    .venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    uv pip install -r requirements.txt
    ```
4. Configure your `.env` file with MongoDB and platform credentials as provided in the .env.example file.
  
5. Start the backend server:
    ```bash
    uvicorn app.main:app --reload --log-level debug
    ```

### Usage
- Use `/` endpoint for healthcheck
- Use `/posts/` (POST) to immediately publish or schedule a post to any combination of platforms
- Use `/posts/` (GET) to retrieve all posts and their per-platform statuses
- API documentation available at `/docs`

#### Example: Post immediately to multiple platforms
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello world from Post4U!",
    "platforms": ["x", "reddit", "telegram", "discord"]
  }'
```

#### Example: Schedule a post
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This drops at 9am sharp.",
    "platforms": ["x", "telegram"],
    "scheduled_time": "2026-03-01T09:00:00Z"
  }'
```

> **Note:** `scheduled_time` must be a future UTC datetime in ISO 8601 format (e.g. `2026-03-01T09:00:00Z`). If the time has already passed, the post will be published immediately instead.

> **Note:** Multi-line content must use `\n` for line breaks in JSON, not actual newlines.

#### Example: View all posts
```bash
curl http://localhost:8000/posts/
```

### How Scheduling Works
1. When a post with a future `scheduled_time` is received, it is saved to MongoDB and a job is registered with APScheduler.
2. APScheduler persists the job to the `scheduled_jobs` MongoDB collection.
3. At the scheduled time, APScheduler calls `publish_with_retry` which fetches the post from MongoDB and publishes to all specified platforms.
4. If any platform fails, **only the failed platforms** are retried with a back-off delay:
   - Attempt 1 fails → retry in 5 minutes
   - Attempt 2 fails → retry in 10 minutes
   - Attempt 3 fails → marked as error in MongoDB, no further retries
5. On server restart, APScheduler automatically reads all pending jobs from MongoDB and resumes scheduling — **no jobs are lost.**

### MongoDB Collections
| Collection | Purpose |
|---|---|
| `posts` | Stores post content, platforms, scheduled time, and per-platform publish results |
| `scheduled_jobs` | Managed by APScheduler — stores pending job metadata for persistence across restarts |

### Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, features, or improvements.

### License
MIT License

### Maintainers
- ShadowSlayer03 (Admin)

---
For frontend setup and full project details, see the main project README.