
# Post4U: Schedule Social Media Posts

A self-hosted and cloud-ready open source platform to schedule, compose, and analyze posts for X (Twitter), LinkedIn, and Reddit.

## Business Model Recommendation

**Open-Core + Cloud Hosted SaaS**

| Tier         | Price      | What You Get                                                      |
|--------------|------------|-------------------------------------------------------------------|
| Self-Host    | $0         | Full code on GitHub, run it yourself                              |
| Starter      | $9/month   | 3 accounts, 50 posts/month, basic scheduling                      |
| Creator      | $19/month  | 10 accounts, unlimited posts, AI suggestions                     |
| Pro          | $49/month  | Unlimited accounts, analytics, team seats, priority support       |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REFLEX FRONTEND (Python)                  │
│   Dashboard | Compose | Schedule | Suggestions | Analytics   │
│              Runs as a compiled React app under the hood      │
└────────────────────────┬────────────────────────────────────┘
						 │ HTTP / WebSocket (Reflex State)
┌────────────────────────▼────────────────────────────────────┐
│               FastAPI Backend  (uvicorn)                     │
│                                                              │
│  /api/auth      → OAuth flows (X, LinkedIn, Reddit)         │
│  /api/posts     → Create, read, update, delete posts        │
│  /api/publish   → Immediate publish to platforms            │
│  /api/schedule  → Queue posts with time/date                │
│  /api/suggest   → AI content suggestions endpoint           │
│  /api/analytics → Engagement data per post                  │
└───┬──────────────────────────────────┬───────────────────────┘
	│                                  │
┌───▼───────┐                ┌─────────▼──────────────────────┐
│PostgreSQL │                │    Celery Workers + Redis       │
│           │                │                                 │
│ users     │                │  publish_task(post_id)          │
│ posts     │                │  scheduled_beat (every 1 min)   │
│ schedules │                │  fetch_trends_task (daily)      │
│ analytics │                │  ai_suggest_task                │
└───────────┘                └─────────┬──────────────────────┘
									   │
			  ┌────────────────────────┼───────────────────┐
			  │                        │                   │
	┌─────────▼──────┐    ┌────────────▼──────┐  ┌────────▼──────┐
	│ Tweepy (X v2)  │    │  LinkedIn REST API │  │  PRAW (Reddit)│
	│  post tweet    │    │  post ugcPost      │  │  fetch trends │
	│  get metrics   │    │  get impressions   │  │  top comments │
	└────────────────┘    └───────────────────┘  └───────────────┘
									   │
							 ┌─────────▼──────────┐
							 │    Claude / OpenAI  │
							 │  - Suggest posts    │
							 │  - Rewrite tone     │
							 │  - Generate threads │
							 └────────────────────┘
```

---

## Key Features
- Schedule and publish posts to X (Twitter), LinkedIn, and Reddit
- AI-powered content suggestions and rewriting
- Analytics dashboard for engagement tracking
- Multi-account and team support (cloud tiers)
- Self-hosted and SaaS options

## Quick Start
See `backend/README.md` and `frontend/README.md` for setup instructions.

## License
MIT License

## Maintainers
- ShadowSlayer03 (admin)
