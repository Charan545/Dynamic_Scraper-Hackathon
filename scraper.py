import requests
from bs4 import BeautifulSoup
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (compatible; HackathonScraper/1.0; +https://example.com)"
HEADERS = {"User-Agent": USER_AGENT}

def scrape_bbc_headlines(limit=15):
    url = "https://www.bbc.com/news"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    items = []
    # BBC uses anchors with class 'gs-c-promo-heading' for headlines; be tolerant
    for a in soup.select("a.gs-c-promo-heading"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if not title:
            continue
        if href and href.startswith("/"):
            href = "https://www.bbc.com" + href
        items.append({
            "title": title,
            "url": href,
            "source": "BBC",
            "fetched_at": datetime.utcnow(),
            "summary": None
        })
        if len(items) >= limit:
            break
    return items
