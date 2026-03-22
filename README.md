# POST4U — Social Media Autopilot

> **Write once. Post everywhere. Schedule anything.**
> Cross-post to X, Reddit, Telegram, Discord, and Bluesky — from a single self-hosted dashboard. No subscriptions. No data harvesting. Your keys, your server, your data.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/Reflex-UI-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/Self--Hostable-Yes-brightgreen?style=flat-square" />
</p>

---

## ✨ What You Get

| | |
|---|---|
| **X (Twitter)** | **Reddit** |
| **Telegram** | **Discord** |
| **Bluesky** | |

Post to all five from one form. Right now, or on a schedule.

---

## 🔥 Features

- **Compose once, post everywhere** - one form, five platforms, zero repetition
- **Schedule with confidence** - jobs persist across server restarts (MongoDB-backed)
- **Smart retry** - only failed platforms are retried; successful ones never re-post
- **Live previews** - see how your post looks on X, Reddit, Telegram, Discord, and Bluesky *before* sending
- **OG link previews** - paste a URL and metadata is auto-fetched (title, image, description)
- **Character counters** - real-time per-platform limits so you never go over
- **Edit & Unschedule** - change your mind before it goes live
- **Media uploads** - attach images directly from the dashboard
- **API-first** - the FastAPI backend works standalone; connect any client you want
- **Rate limited & secure** - API key auth on all endpoints, SSRF protection baked in

---

## 📸 Screenshots

<img src="/screenshots/hero.png" alt="Hero" width="100%" /><br>

<details>
  <summary>Click to view Dashboard</summary>
  <p align="center">
    <br><br>
    <img src="/screenshots/schedule_post.png" width="90%" />
    <img src="/screenshots/post_immediately.png" width="90%" /><br>
    <img src="/screenshots/edit_post.png" width="90%" />
    <img src="/screenshots/unschedule_post.png" width="90%" /><br>
    <img src="/screenshots/post_history.png" width="90%" />
  </p>
</details>

---

## ⚡ Quick Start

```bash
git clone https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts.git ./post4u
cd post4u
cp backend/.env.example backend/.env    # add platform credentials + generate API key
cp frontend/.env.example frontend/.env  # paste the same API key here
docker compose up --build -d
```

> **`POST4U_API_KEY` must be set to the same value in both `backend/.env` and `frontend/.env`.**

| Service | URL |
|---|---|
| 🎨 Dashboard | `http://localhost:3000` |
| 📡 REST API | `http://localhost:8000` |
| 📖 API Docs | `http://localhost:8000/docs` |

> First build takes a few minutes. After that, it's instant.

---

## 🗂️ Docs

| Module | What's inside |
|---|---|
| [📦 Backend](backend/README.md) | FastAPI setup, API usage, platform credentials, env vars, scheduling internals, security |
| [🎨 Frontend](frontend/README.md) | Reflex dashboard setup, env vars, connecting to a remote backend |

---

## 🤝 Contributing

PRs are welcome! Open an issue first for large changes.

## 📄 License

MIT — do whatever you want with it.

---

<p align="center">
  Built with FastAPI · MongoDB · APScheduler · Reflex · Tweepy · PRAW<br>
  <strong>No VC funding. No tracking. Just vibes.</strong>
</p>
