
## Post4U Frontend

A self-hosted open source frontend for scheduling and managing posts to X (Twitter), Reddit, Telegram, and Discord, built with Reflex.

### Features
- User-friendly dashboard for creating and scheduling posts
- Cross-post to multiple platforms from one form
- View post history and per-platform publish status
- Unschedule pending posts
- Connects to the FastAPI backend

### Tech Stack
- Python 3.11+
- Reflex
- httpx (async HTTP client)
- python-dotenv

### Setup
1. Clone the repository and navigate to the frontend folder:
	```bash
	git clone https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts.git
	cd frontend
	```
2. Create and activate a virtual environment (using uv):
	```bash
	uv venv
	.venv\Scripts\activate  # Windows
	source .venv/bin/activate  # macOS/Linux
	```
3. Install dependencies:
	```bash
	uv pip install -r requirements.txt
	```
4. Create a `.env` file in the `frontend/` directory with your API key:
	```env
	POST4U_API_KEY=your_generated_key_here
	```
	> This must match the `POST4U_API_KEY` set in the backend `.env`. The frontend reads this at runtime and sends it as an `X-API-Key` header with every request to the backend. Without it, all API calls will return `401 Unauthorized`.
5. Start the Reflex app:
	```bash
	uv run reflex run
	```

### Usage
- Access the frontend in your browser at `http://localhost:3000`
- Make sure the backend is running at `http://localhost:8000` before using the dashboard

### Security
The frontend reads `POST4U_API_KEY` from its own `.env` file via `python-dotenv` and sends it as the `X-API-Key` header on every backend request. Keep your frontend `.env` out of version control (it is already covered by `.gitignore`).

### Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, features, or improvements.

### License
MIT License

### Maintainers
- ShadowSlayer03 (admin)

---
For backend setup and full project details, see the main project README.
