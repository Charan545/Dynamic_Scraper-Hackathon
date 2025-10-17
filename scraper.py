import feedparser
from datetime import datetime

BBC_RSS_URL = "http://feeds.bbci.co.uk/news/rss.xml"

def scrape_bbc_articles(limit=10):
    feed = feedparser.parse(BBC_RSS_URL)
    articles = []
    for entry in feed.entries[:limit]:
        articles.append({
            "title": entry.title,
            "url": entry.link,
            "source": "BBC",
            "fetched_at": datetime.utcnow(),
            "content": getattr(entry, 'summary', '')  # summary if content not available
        })
    print(f"Scraper found {len(articles)} articles")
    return articles
