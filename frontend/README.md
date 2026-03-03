
## Post4U Frontend

A self-hosted open source frontend for scheduling and managing posts to LinkedIn and X (Twitter), built with Reflex.

### Features
- User-friendly interface for scheduling posts
- Dashboard to view scheduled and posted content
- Connects to the FastAPI backend
- Easy to self-host and use

### Tech Stack
- Python 3.11+
- Reflex (Pynecone)

### Setup
1. Clone the repository and navigate to the frontend folder:
	```bash
	git clone https://github.com/ShadowSlayer03/Post4U-Schedule-Social-Media-Posts.git
	cd frontend
	```
2. (Recommended) Create and activate a virtual environment:
	```bash
	python -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate
	```
3. Install Reflex:
	```bash
	pip install reflex
	```
4. Install other dependencies (if any):
	```bash
	pip install -r requirements.txt
	```
5. Start the Reflex app:
	```bash
	reflex run
	```

### Usage
- Access the frontend in your browser at `http://localhost:3000`
- Schedule posts and manage your content

### Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, features, or improvements.

### License
MIT License

### Maintainers
- ShadowSlayer03 (admin)

---
For backend setup and full project details, see the main project README.
