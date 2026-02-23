from app.services.reddit_client import get_reddit_client

def post_to_reddit(content: str, subreddit: str):
    try:
        reddit = get_reddit_client()
        subreddit = reddit.subreddit(subreddit)
        submission = subreddit.submit_selfpost(title=content[:300], selftext=content)
        return {"status": "success", "post_id": submission.id}
    except Exception as e:
        return {"status": "error", "message": str(e)}