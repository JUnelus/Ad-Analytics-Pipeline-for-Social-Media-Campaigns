import praw
import json
from google.cloud import storage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Reddit authentication
reddit = praw.Reddit(
    client_id=os.getenv('reddit_client_id'),
    client_secret=os.getenv('reddit_client_secret'),
    user_agent=os.getenv('reddit_user_agent')
)

def fetch_reddit_data(subreddit="technology", limit=100):
    posts = [{"title": submission.title, "score": submission.score, "comments": submission.num_comments}
             for submission in reddit.subreddit(subreddit).top(limit=limit)]

    # Save to Google Cloud Storage (GCS)
    gcs_client = storage.Client()
    bucket = gcs_client.bucket("social-media-campaigns1-bucket")
    blob = bucket.blob("reddit_data.json")
    blob.upload_from_string(json.dumps(posts), content_type="application/json")

if __name__ == "__main__":
    fetch_reddit_data()
