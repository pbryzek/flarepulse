import os
import json
import pandas as pd
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API v2 credentials
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Authenticate using Tweepy Client for v2 API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Constants
LAST_TWEET_FILE = "last_tweet.json"
CSV_FILE = "tweets.csv"


def load_last_tweet_id():
    """Load the last seen tweet ID from file."""
    if os.path.exists(LAST_TWEET_FILE):
        with open(LAST_TWEET_FILE, "r") as file:
            try:
                data = json.load(file)
                return data.get("last_tweet_id")
            except json.JSONDecodeError:
                return None
    return None


def save_last_tweet_id(tweet_id):
    """Save the last seen tweet ID to file."""
    with open(LAST_TWEET_FILE, "w") as file:
        json.dump({"last_tweet_id": tweet_id}, file)


def save_tweets_to_csv(tweets):
    """Save tweets to a CSV file."""
    if not tweets:
        print("No new tweets to save.")
        return

    data_list = []
    for tweet in tweets:
        print("Looping")
        print(tweet)
        print(tweet.public_metrics)
        print(tweet.public_metrics["retweet_count"])
        data_list.append({
            "id": tweet.id,
            "text": tweet.text,
            "created_at": tweet.created_at,
            "lang": tweet.lang,
            "author_id": tweet.author_id,
            "conversation_id": tweet.conversation_id,
            "source": tweet.source,
            "possibly_sensitive": tweet.possibly_sensitive,
            "retweet_count": tweet.public_metrics["retweet_count"],
            "reply_count": tweet.public_metrics["reply_count"],
            "like_count": tweet.public_metrics["like_count"],
            "quote_count": tweet.public_metrics["quote_count"],
            "hashtags": [h["tag"] for h in tweet.entities["hashtags"]] if tweet.entities and "hashtags" in tweet.entities else None,
            "mentions": [m["username"] for m in tweet.entities["mentions"]] if tweet.entities and "mentions" in tweet.entities else None,
            "urls": [u["expanded_url"] for u in tweet.entities["urls"]] if tweet.entities and "urls" in tweet.entities else None
        })

    df = pd.DataFrame(data_list)
    df.to_csv(CSV_FILE, mode="a", index=False,
              header=not os.path.exists(CSV_FILE))
    print(f"Saved {len(df)} tweets to {CSV_FILE}")


def fetch_tweets(query, max_results=1):
    """Fetch recent tweets while avoiding duplicates and save to CSV."""
    last_tweet_id = load_last_tweet_id()
    try:
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=["id", "text", "created_at", "lang", "source",
                          "possibly_sensitive", "conversation_id", "public_metrics"],
            expansions=["author_id", "entities.mentions.username"],
            max_results=max_results,
            since_id=last_tweet_id  # Avoid duplicate tweets
        )

        if response and response.data:
            save_tweets_to_csv(response.data)
            save_last_tweet_id(response.data[0].id)  # Save latest tweet ID
        else:
            print("No new tweets found.")
    except tweepy.TweepyException as e:
        print("Error fetching tweets:", e)


# Define search query
search_query = '(FLR OR #FLR OR "Flare Network" OR $FLR)'

# Fetch tweets
fetch_tweets(search_query, 1)
