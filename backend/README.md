## Post4U Backend

A self-hosted open source backend for scheduling and automatically posting content to X (Twitter), Reddit, Telegram, and Discord.

### Features
- Schedule posts for X (Twitter), Reddit, Telegram, and Discord
- Cross-post to multiple platforms in one request
- Automatic posting at specified times (scheduling)
- Per-platform success/failure tracking
- MongoDB database for storing scheduled posts
- FastAPI REST API
- OAuth2 user authentication for X (Twitter)
- Easy to self-host and use

### Tech Stack
- Python 3.11+
- FastAPI
- Beanie (MongoDB ODM)
- MongoDB
- Tweepy (Twitter/X API)
- PRAW (Reddit API)
- requests (Telegram/Discord)
- APScheduler (scheduling)
- uv (dependency management)

### Setup
1. Clone the repository and navigate to the backend folder:
	```bash
	git clone https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts.git
	cd backend
	```
2. Create and activate a virtual environment:
	```bash
	uv venv create
	uv venv activate
	```
3. Install dependencies:
	```bash
	uv pip install -r requirements.txt
	```
4. Configure your `.env` file with MongoDB and platform credentials:
	```env
	# MongoDB
	MONGO_URI=mongodb://localhost:27017
	DATABASE_NAME=post_scheduler

	# X / Twitter
	TWITTER_API_KEY=your_api_key
	TWITTER_API_SECRET=your_api_secret
	TWITTER_API_ACCESS_TOKEN=your_access_token
	TWITTER_API_ACCESS_TOKEN_SECRET=your_access_token_secret

	# Reddit
	REDDIT_CLIENT_ID=your_reddit_client_id
	REDDIT_CLIENT_SECRET=your_reddit_client_secret
	REDDIT_USERNAME=your_reddit_username
	REDDIT_PASSWORD=your_reddit_password
	REDDIT_SUBREDDIT=your_subreddit

	# Telegram
	TELEGRAM_BOT_TOKEN=your_telegram_bot_token
	TELEGRAM_CHANNEL_ID=@yourchannel

	# Discord
	DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
	```
5. Start the backend server:
	```bash
	uvicorn app.main:app --reload
	```

### Usage
- Use `/` endpoint for healthcheck
- Use `/posts/` endpoint to schedule and cross-post to any combination of platforms
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
	"scheduled_time": "2025-03-01T09:00:00Z"
  }'
```

#### Example: View all posts
```bash
curl http://localhost:8000/posts/
```

### Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, features, or improvements.

### License
MIT License

### Maintainers
- ShadowSlayer03 (Admin)

---
For frontend setup and full project details, see the main project README.
