# scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser

def scrape_bbc_articles(limit=20):
    """
    Scrapes BBC RSS feed and fetches full article content.
    Returns a list of articles with title, url, source, fetched_at, content.
    """
    feed_url = "http://feeds.bbci.co.uk/news/rss.xml"
    articles = []

    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:limit]:
        title = entry.title
        url = entry.link
        source = "BBC"
        fetched_at = datetime.utcnow()
        
        # Default content from feed summary
        content = entry.get("summary", "")
        
        try:
            # Fetch the full page HTML
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # BBC articles usually have main content inside <article> or specific div
            article_tag = soup.find("article")
            
            if article_tag:
                paragraphs = article_tag.find_all("p")
                if paragraphs:
                    content = " ".join([p.get_text() for p in paragraphs])
            else:
                # fallback for older BBC pages
                div_body = soup.find("div", {"class": "story-body__inner"})
                if div_body:
                    paragraphs = div_body.find_all("p")
                    content = " ".join([p.get_text() for p in paragraphs])
            
        except Exception as e:
            print(f"Failed to fetch full content for {title}: {e}")

        articles.append({
            "title": title,
            "url": url,
            "source": source,
            "fetched_at": fetched_at,
            "content": content
        })

    print(f"Scraper found {len(articles)} articles")
    return articles

# Test run
if __name__ == "__main__":
    scraped = scrape_bbc_articles()
    for a in scraped:
        print(a["title"])
        print(a["content"][:300], "...\n")
