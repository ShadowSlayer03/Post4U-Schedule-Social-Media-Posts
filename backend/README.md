# Post4U - Backend

FastAPI backend powering Post4U. Handles platform routing, MongoDB persistence, job scheduling, media uploads, OG scraping, and retry logic. Can be used standalone with any HTTP client.

### Features
- **Smart Scheduling**: Schedule posts for X, Reddit, Telegram, and Discord.
- **Immediate Posting**: Publish to all platforms instantly.
- **Draft Management**: Edit or Unschedule pending posts.
- **Persistent Jobs**: Scheduled jobs survive server restarts via MongoDB JobStore.
- **Fail-Safe Posting**: Per-platform retry logic (up to 3 attempts); only failed platforms are retried.
- **Rich Media**: Supports image uploads and link metadata scraping (OG data).
- **Security**: API key protection (`X-API-Key`) and Rate Limiting.
- **Real-time Previews**: High-fidelity, platform-specific logic for X, Reddit, Telegram, and Discord.

### Tech Stack
- **FastAPI**: Modern, fast (high-performance) web framework.
- **Beanie**: Async MongoDB ODM.
- **APScheduler**: Advanced Python Scheduler with MongoDB backend.
- **Tweepy & PRAW**: Official clients for X and Reddit.
- **httpx & BeautifulSoup4**: For OG data scraping and SSRF protection.

### Local Dev Setup

Requires [uv](https://github.com/astral-sh/uv) and a running MongoDB instance.

```bash
cd backend
uv venv && .venv\Scripts\activate   # Windows
# source .venv/bin/activate          # macOS/Linux
uv pip install -r requirements.txt
cp .env.example .env                 # fill in credentials
uvicorn app.main:app --reload --log-level debug
```

> API is live at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Docker

The project root `docker-compose.yml` runs both `api` and `mongo` services automatically. APScheduler uses the same MongoDB instance — no Redis, no Celery, no extra containers.

```bash
# from the project root
docker compose up --build -d
docker compose logs api   # look for: ✅ Scheduler started and MongoDB connected
```

### API Usage

All endpoints (except `GET /`) require the `X-API-Key` header.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Healthcheck |
| `GET` | `/posts/` | List all posts with per-platform status |
| `POST` | `/posts/` | Publish immediately or schedule a post |
| `POST` | `/posts/{id}/edit/` | Edit a pending/scheduled post |
| `DELETE` | `/posts/{id}/unschedule/` | Cancel a scheduled post |

#### Post immediately
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello from Post4U!", "platforms": ["x", "telegram", "discord"]}'
```

#### Schedule a post
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"content": "Drops at 9am.", "platforms": ["x"], "scheduled_time": "2026-06-01T09:00:00Z"}'
```

> `scheduled_time` must be a future UTC datetime in ISO 8601 format. If the time has already passed, it falls back to an immediate post.

### Platform Setup

#### X (Twitter)
1. Create an app at [developer.twitter.com](https://developer.twitter.com)
2. Enable **OAuth 1.0a** with Read & Write permissions
3. Generate Access Token + Secret

```env
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_API_ACCESS_TOKEN=...
TWITTER_API_ACCESS_TOKEN_SECRET=...
```

#### Reddit
1. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) → **Create App** → type: **script**
2. Note the client ID (under the app name) and secret

```env
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
REDDIT_SUBREDDIT=test
```

> Use `r/test` for testing. Reddit requires some account karma before posting to most subreddits.

#### Telegram
1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → copy the token
2. Add the bot as **admin** to your channel

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHANNEL_ID=@yourchannel
```

#### Discord
1. Go to your server → **Integrations → Webhooks** → **New Webhook** → copy the URL

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `POST4U_API_KEY` | ✅ | Secret key for `X-API-Key` header auth. Server refuses to start without it. |
| `MONGO_URI` | ✅ | MongoDB connection string (e.g. `mongodb://mongo:27017/post4u`) |
| `TWITTER_API_KEY` | ⬜ | X (Twitter) credentials |
| `TWITTER_API_SECRET` | ⬜ | |
| `TWITTER_API_ACCESS_TOKEN` | ⬜ | |
| `TWITTER_API_ACCESS_TOKEN_SECRET` | ⬜ | |
| `REDDIT_CLIENT_ID` | ⬜ | Reddit app credentials |
| `REDDIT_CLIENT_SECRET` | ⬜ | |
| `REDDIT_USERNAME` | ⬜ | |
| `REDDIT_PASSWORD` | ⬜ | |
| `REDDIT_SUBREDDIT` | ⬜ | Target subreddit (without `r/`) |
| `TELEGRAM_BOT_TOKEN` | ⬜ | Telegram bot token from BotFather |
| `TELEGRAM_CHANNEL_ID` | ⬜ | Channel ID or `@handle` |
| `DISCORD_WEBHOOK_URL` | ⬜ | Full Discord webhook URL |

> Leaving a platform's variables blank skips that platform gracefully — no crash.

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

### Security

All API endpoints (except the healthcheck `GET /`) require a valid `X-API-Key` header.

**Setup:**
1. Generate a key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. Add it to your `.env`:
   ```env
   POST4U_API_KEY=your_generated_key_here
   ```
3. Pass it as a header in every request:
   ```bash
   curl -H "X-API-Key: your_generated_key_here" http://localhost:8000/posts/
   ```

> The server **refuses to start** if `POST4U_API_KEY` is not set — this is intentional.
> Never commit your `.env` file to git.

---

← [Back to main README](../README.md) | [Frontend README →](../frontend/README.md)