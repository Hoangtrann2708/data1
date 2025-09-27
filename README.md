# Reddit Scraper for r/wallstreetoasis

This Python script scrapes all posts from r/wallstreetoasis that were posted within the last 24 hours.

## Features

- Fetches posts from the last 24 hours
- Displays post summary with top posts by score
- Shows detailed information for each post
- Saves all posts to a JSON file
- Includes post metadata (score, comments, author, etc.)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Reddit API Credentials

1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Fill in the required fields:
   - Name: Any name you prefer
   - Description: Optional
   - About URL: Optional
   - Redirect URI: `http://localhost:8080` (required but not used for scripts)
5. Click "Create app"
6. Copy the client ID (under the app name) and client secret

### 3. Configure the Script

Edit `reddit_scraper.py` and update these variables:

```python
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
USER_AGENT = "RedditScraper/1.0 by YourUsername"
```

Replace:
- `your_client_id_here` with your actual client ID
- `your_client_secret_here` with your actual client secret
- `YourUsername` with your Reddit username

## Usage

Run the script:

```bash
python reddit_scraper.py
```

The script will:
1. Fetch all posts from r/wallstreetoasis from the last 24 hours
2. Display a summary of the top 10 posts by score
3. Show detailed information for all posts
4. Save all posts to a JSON file with timestamp

## Output

The script provides:
- Console output with post summaries and details
- JSON file with all post data for further analysis

### JSON Output Format

Each post includes:
- `title`: Post title
- `author`: Post author
- `score`: Post score (upvotes - downvotes)
- `upvote_ratio`: Ratio of upvotes to total votes
- `num_comments`: Number of comments
- `url`: Original URL (if link post)
- `permalink`: Reddit permalink
- `created_utc`: Unix timestamp
- `created_time`: Human-readable timestamp
- `is_self`: Whether it's a text post
- `selftext`: Text content (if text post)
- `flair`: Post flair

## Rate Limits

Reddit API has rate limits. The script is designed to be respectful of these limits, but if you encounter rate limiting issues, you may need to add delays between requests.

## Notes

- The script fetches up to 1000 of the newest posts and filters for the last 24 hours
- Posts are sorted by score (highest first) in the summary
- All times are in UTC
- The script handles deleted users gracefully
