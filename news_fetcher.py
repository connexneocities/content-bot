import feedparser
import requests
import json
from datetime import datetime

# Free RSS feeds - no API key needed
RSS_FEEDS = {
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "http://feeds.reuters.com/Reuters/worldNews",
    ],
    "sports": [
        "https://feeds.bbci.co.uk/sport/football/rss.xml",
        "https://www.espn.com/espn/rss/news",
    ],
    "technology": [
        "https://feeds.feedburner.com/TechCrunch",
        "https://www.theverge.com/rss/index.xml",
    ],
    "business": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "http://feeds.reuters.com/reuters/businessNews",
    ]
}

def fetch_top_stories(max_per_feed=3):
    """Fetch top stories from all RSS feeds"""
    all_stories = []

    for category, feeds in RSS_FEEDS.items():
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:max_per_feed]:
                    story = {
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", entry.get("description", "")),
                        "link": entry.get("link", ""),
                        "category": category,
                        "source": feed.feed.get("title", feed_url),
                        "published": entry.get("published", str(datetime.now()))
                    }
                    if story["title"]:
                        all_stories.append(story)
            except Exception as e:
                print(f"Error fetching {feed_url}: {e}")

    print(f"✅ Fetched {len(all_stories)} stories")
    return all_stories


def get_best_story(stories):
    """Pick the most engaging story based on keywords"""
    priority_keywords = [
        "breaking", "world cup", "war", "earthquake", "crisis",
        "historic", "first ever", "shocking", "massive", "urgent",
        "election", "explosion", "attack", "summit", "record"
    ]

    scored = []
    for story in stories:
        score = 0
        text = (story["title"] + story["summary"]).lower()
        for kw in priority_keywords:
            if kw in text:
                score += 1
        scored.append((score, story))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[0][1] if scored else stories[0]


if __name__ == "__main__":
    stories = fetch_top_stories()
    best = get_best_story(stories)
    print(f"\n🔥 Best story: {best['title']}")
    print(f"📂 Category: {best['category']}")
    print(f"📰 Source: {best['source']}")
