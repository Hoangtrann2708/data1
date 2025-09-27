#!/usr/bin/env python3
"""
Reddit Scraper for r/wallstreetbets
Scrapes all posts from the last 48 hours
"""

import praw
import datetime
import time
import json
from typing import List, Dict

class RedditScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Initialize Reddit API client
        
        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: User agent string for API requests
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
    def get_posts_last_24h(self, subreddit_name: str) -> List[Dict]:
        """
        Get all posts from a subreddit in the last 48 hours
        
        Args:
            subreddit_name: Name of the subreddit (without r/)
            
        Returns:
            List of dictionaries containing post data
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        
        # Calculate timestamp for 48 hours ago (in UTC)
        forty_eight_hours_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=48)
        forty_eight_hours_ago_timestamp = forty_eight_hours_ago.timestamp()
        
        print(f"Fetching posts from r/{subreddit_name} since {forty_eight_hours_ago.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"DEBUG: Current time (UTC): {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"DEBUG: 48 hours ago (UTC): {forty_eight_hours_ago.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"DEBUG: Cutoff timestamp: {forty_eight_hours_ago_timestamp}")
        
        try:
            # Get posts from different time periods to ensure we catch all recent posts
            post_count = 0
            for submission in subreddit.new(limit=1000):  # Get up to 1000 newest posts
                post_count += 1
                post_time = datetime.datetime.fromtimestamp(submission.created_utc, tz=datetime.timezone.utc)
                
                # Debug: Print first few posts to see what we're getting
                if post_count <= 5:
                    print(f"DEBUG: Post {post_count} - Created: {post_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                    print(f"DEBUG: Raw timestamp: {submission.created_utc}, Cutoff: {forty_eight_hours_ago_timestamp}")
                    print(f"DEBUG: Is post newer? {submission.created_utc >= forty_eight_hours_ago_timestamp}")
                    print(f"DEBUG: Time difference: {submission.created_utc - forty_eight_hours_ago_timestamp} seconds")
                
                # Check if post is within last 48 hours
                if submission.created_utc >= forty_eight_hours_ago_timestamp:
                    post_data = {
                        'title': submission.title,
                        'author': str(submission.author) if submission.author else '[deleted]',
                        'score': submission.score,
                        'upvote_ratio': submission.upvote_ratio,
                        'num_comments': submission.num_comments,
                        'url': submission.url,
                        'permalink': f"https://reddit.com{submission.permalink}",
                        'created_utc': submission.created_utc,
                        'created_time': post_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'is_self': submission.is_self,
                        'selftext': submission.selftext if submission.is_self else '',
                        'flair': submission.link_flair_text if submission.link_flair_text else 'No flair'
                    }
                    posts.append(post_data)
                else:
                    # Since posts are sorted by new, we can break once we hit older posts
                    print(f"DEBUG: Breaking at post {post_count} - post is older than 48 hours")
                    break
            
            print(f"DEBUG: Processed {post_count} posts total")
                    
        except Exception as e:
            print(f"Error fetching posts: {e}")
            
        return posts
    
    def save_to_json(self, posts: List[Dict], filename: str = None):
        """
        Save posts to JSON file
        
        Args:
            posts: List of post dictionaries
            filename: Output filename (optional)
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'wallstreetbets_posts_{timestamp}.json'
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(posts)} posts to {filename}")
    
    def print_posts_summary(self, posts: List[Dict]):
        """
        Print a summary of the scraped posts
        
        Args:
            posts: List of post dictionaries
        """
        print(f"\n{'='*80}")
        print(f"SUMMARY: Found {len(posts)} posts from the last 48 hours")
        print(f"{'='*80}")
        
        if not posts:
            print("No posts found in the last 48 hours.")
            return
            
        # Sort by score (highest first)
        sorted_posts = sorted(posts, key=lambda x: x['score'], reverse=True)
        
        print(f"\nTop 10 posts by score:")
        print(f"{'Rank':<4} {'Score':<6} {'Comments':<8} {'Title':<50} {'Author':<15}")
        print(f"{'-'*4} {'-'*6} {'-'*8} {'-'*50} {'-'*15}")
        
        for i, post in enumerate(sorted_posts[:10], 1):
            title = post['title'][:47] + '...' if len(post['title']) > 50 else post['title']
            author = post['author'][:12] + '...' if len(post['author']) > 15 else post['author']
            print(f"{i:<4} {post['score']:<6} {post['num_comments']:<8} {title:<50} {author:<15}")
        
        print(f"\nDetailed post information:")
        print(f"{'='*80}")
        
        for i, post in enumerate(sorted_posts, 1):
            print(f"\n{i}. {post['title']}")
            print(f"   Author: {post['author']}")
            print(f"   Score: {post['score']} (upvote ratio: {post['upvote_ratio']:.2f})")
            print(f"   Comments: {post['num_comments']}")
            print(f"   Posted: {post['created_time']}")
            print(f"   Flair: {post['flair']}")
            print(f"   URL: {post['url']}")
            print(f"   Reddit Link: {post['permalink']}")
            if post['is_self'] and post['selftext']:
                text_preview = post['selftext'][:200] + '...' if len(post['selftext']) > 200 else post['selftext']
                print(f"   Text: {text_preview}")
            print(f"   {'-'*60}")


def main():
    """
    Main function to run the Reddit scraper
    """
    # Reddit API credentials - you need to get these from Reddit
    # Go to https://www.reddit.com/prefs/apps to create a new app
    CLIENT_ID = "4GmDrqKqzYnrgBa1TwV5ew"
    CLIENT_SECRET = "4E4MKJ446Esthw8g9iH-oh51oFOX6w"
    USER_AGENT = "RedditScraper/1.0 by Melodic-Intention-42"
    
    # Check if credentials are set
    if CLIENT_ID == "your_client_id_here" or CLIENT_SECRET == "your_client_secret_here":
        print("ERROR: Please set your Reddit API credentials!")
        print("\nTo get Reddit API credentials:")
        print("1. Go to https://www.reddit.com/prefs/apps")
        print("2. Click 'Create App' or 'Create Another App'")
        print("3. Choose 'script' as the app type")
        print("4. Fill in the required fields")
        print("5. Copy the client ID and client secret")
        print("6. Update the CLIENT_ID and CLIENT_SECRET variables in this script")
        return
    
    # Initialize scraper
    scraper = RedditScraper(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    
    # Scrape posts from r/wallstreetbets
    subreddit_name = "wallstreetbets"
    posts = scraper.get_posts_last_24h(subreddit_name)
    
    # Print summary
    scraper.print_posts_summary(posts)
    
    # Save to JSON file
    if posts:
        scraper.save_to_json(posts)
    
    print(f"\nScraping completed! Found {len(posts)} posts from the last 48 hours.")


if __name__ == "__main__":
    main()