## Post4U Backend

A self-hosted open source backend for scheduling and automatically posting content to LinkedIn and X (Twitter).

### Features
- Schedule posts for LinkedIn and X (Twitter)
- Automatic posting at specified times
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
4. Configure your `.env` file with MongoDB and Twitter/X credentials:
	```env
	MONGO_URI=mongodb://localhost:27017
	DATABASE_NAME=post_scheduler
	TWITTER_CLIENT_ID=your_client_id
	TWITTER_CLIENT_SECRET=your_client_secret
	TWITTER_CALLBACK_URL=http://localhost:8000/callback
	```
5. Start the backend server:
	```bash
	uvicorn app.main:app --reload
	```

### Usage
- Use `/` endpoint for healthcheck
- Use `/posts/` endpoint to schedule and post tweets
- API documentation available at `/docs`

### Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, features, or improvements.

### License
MIT License

### Maintainers
- ShadowSlayer03 (Admin)

---
For frontend setup and full project details, see the main project README.
