# POST4U - Social Media Autopilot

> **Cross-post, schedule, and automate your presence on X, Reddit, Telegram, and Discord — from one place. Self-hosted. Open source. No BS.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Motor%20%2B%20Beanie-47A248?style=flat-square&logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Self Hostable](https://img.shields.io/badge/Self--Hostable-Yes-brightgreen?style=flat-square)

---

## What is this?

Post4U is a **self-hosted social media scheduler** built with Python. Write a post once, publish it to multiple platforms instantly or at a scheduled time. No subscriptions, no data harvesting, no lock-in. Your keys, your server, your data.

**Supported platforms:**
- **X (Twitter)** via Tweepy
- **Reddit** via PRAW
- **Telegram** via Bot API (requests)
- **Discord** via Webhooks

---

## Features

- ✅ Post immediately or schedule for a future time
- ✅ Cross-post to multiple platforms in one request
- ✅ Per-platform success/failure tracking
- ✅ MongoDB-backed post history with timestamps
- ✅ Persistent scheduling — jobs survive server restarts via MongoDB job store
- ✅ Per-platform retry logic — only failed platforms are retried (up to 3 attempts)
- ✅ Platforms with missing credentials are skipped gracefully, not crashed
- ✅ API key authentication — all endpoints protected via X-API-Key header
- ✅ Rate limiting — prevents abuse and DoS attacks
- ✅ Simple REST API — connect any frontend or call it from scripts
- ✅ APScheduler with MongoDBJobStore (no Redis, no Celery — just runs)
- ✅ Docker Compose setup — one command and you're live
- ✅ Reflex web dashboard — compose, schedule, view history and unschedule posts
- 🔜 Image/media attachment support & security
- 🔜 Bluesky and Mastodon integration
- 🔜 OG link preview before scheduling
- 🔜 AI-powered post suggestions

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/)
- API keys for the platforms you want to use (see [Platform Setup](#platform-setup))

### 1. Clone the repo

```bash
git clone https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts.git ./post4u

cd post4u
```

### 2. Set up your environment

```bash
cp .env.example .env
```

Open `.env` and fill in the keys for the platforms you want. You can leave the others blank — the app will simply skip platforms with missing credentials.

### 3. Run it

```bash
docker compose up --build -d
```

> **Note:** The initial build might take a few minutes as it compiles all dependencies.

That's it. 
- **Backend API:** `http://localhost:8000`
- **Interactive API Docs:** `http://localhost:8000/docs`
- **Frontend Dashboard:** `http://localhost:3000` (Once the frontend service is complete)

---

## Testing Your Setup

### 1. Check API Health
```bash
curl http://localhost:8000/
```
Expected: `{"message": "Welcome to Post4U..."}`

### 2. Verify MongoDB & Scheduler
Check the logs to ensure MongoDB connected and the scheduler initialized successfully:
```bash
docker compose logs api
```
Look for: `INFO: ✅ Scheduler started and MongoDB connected`

### 3. Post a Test Message (Immediate)
Replace the platforms with ones you have configured in `.env`:
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Testing Post4U! 🚀",
    "platforms": ["discord", "telegram"]
  }'
```

### 4. Schedule a Post
**Important:** Use a UTC time string. If the time has already passed, the API will fall back to an immediate post.
```bash
# Example for a time in the future
curl -X POST http://localhost:8000/posts/ \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a scheduled message.",
    "platforms": ["x"],
    "scheduled_time": "2026-03-01T15:00:00Z"
  }'
```

---

## Without Docker (Local Dev)

### Backend:

Requires [uv](https://github.com/astral-sh/uv) and a running MongoDB instance.

```bash
# Install dependencies
uv sync

# Run the API
uv run uvicorn app.main:app --reload --port 8000

# Run with all logs enabled
uv run uvicorn app.main:app --reload --log-level debug
```

### Frontend:

```bash
# Run the frontend - requires 2 ports
uv run reflex run

# Run with all logs enabled
uv run reflex run --loglevel debug
```

---

## Security

Post4U uses API key authentication on all endpoints.

### Setup
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
   curl -X POST http://localhost:8000/posts/ \
     -H "X-API-Key: your_generated_key_here" \
     -H "Content-Type: application/json" \
     -d '{"content": "Hello!", "platforms": ["discord"]}'
   ```

> The server will **refuse to start** if `API_KEY` is not set.
> Never commit your `.env` file to git.

---

## Usage

### Post immediately to multiple platforms

```bash
curl -X POST http://localhost:8000/posts/ \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello world from Social Autopilot!",
    "platforms": ["x", "reddit", "telegram", "discord"]
  }'
```

### Schedule a post

```bash
curl -X POST http://localhost:8000/posts/ \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This drops at 9am sharp.",
    "platforms": ["x", "telegram"],
    "scheduled_time": "2025-03-01T09:00:00Z"
  }'
```

### View all posts

```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/posts/
```

### API Docs

FastAPI's interactive docs are available at:
```
http://localhost:8000/docs
```

---

## Platform Setup

### X (Twitter)

1. Go to [developer.twitter.com](https://developer.twitter.com) and create a project + app
2. Under **User Authentication Settings**, enable OAuth 1.0a with Read & Write permissions
3. Generate your Access Token and Secret
4. Add to `.env`:

```env
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_API_ACCESS_TOKEN=...
TWITTER_API_ACCESS_TOKEN_SECRET=...
```

---

### Reddit

1. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **Create App** → choose **script**
3. Add to `.env`:

```env
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_SUBREDDIT=test        # subreddit to post to (without r/)
```

> **Note:** Reddit requires your account to have some karma before posting to most subreddits. Use `r/test` for testing.

---

### Telegram

1. Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`
2. Copy the bot token
3. Add the bot as an **admin** to your channel
4. Your channel ID is `@yourchannel` or a numeric ID like `-1001234567890`
5. Add to `.env`:

```env
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHANNEL_ID=@yourchannel
```

---

### Discord

1. Go to your Discord server → **Server Settings → Integrations → Webhooks**
2. Click **New Webhook**, choose the channel, copy the URL
3. Add to `.env`:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

No OAuth, no bot, no approval needed.

---

## Environment Variables Reference

```env
# MongoDB
MONGO_URI=mongodb://mongo:27017
DATABASE_NAME=post_scheduler

# X / Twitter
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_API_ACCESS_TOKEN=
TWITTER_API_ACCESS_TOKEN_SECRET=

# Reddit
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_PASSWORD=
REDDIT_SUBREDDIT=

# Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHANNEL_ID=

# Discord
DISCORD_WEBHOOK_URL=
```

Leave any value blank to disable that platform. The app won't crash, it'll just skip it.

---

## Docker Compose

The `Dockerfile` lives in `backend/`. The `docker-compose.yml` and `.env` live at the project root.

```yaml
# docker-compose.yml  (project root)
services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - mongo
    restart: unless-stopped

  mongo:
    image: mongo:7
    volumes:
      - mongo_data:/data/db
    restart: unless-stopped

volumes:
  mongo_data:
```

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> The two services are all you need — `api` + `mongo`. APScheduler uses the same MongoDB instance for its job store. No Redis, no Celery, no extra containers.

---

## Contributing

PRs welcome. For big changes, open an issue first so we can discuss.

```bash
git clone https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts.git ./post4u
cd post4u
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload
```

---

## License

MIT — do whatever you want with it.

---

<p align="center">Built with FastAPI · MongoDB · Tweepy · PRAW · APScheduler · Reflex<br>No VC funding. No tracking. Just vibes.</p>