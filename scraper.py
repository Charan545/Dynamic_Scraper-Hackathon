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

    # Look for headline links inside <h2> or <a> tags
    for h in soup.select("h2 a[href^='/news']"):
        title = h.get_text(strip=True)
        href = h.get("href")
        if not title or not href:
            continue
        if href.startswith("/"):
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

    # fallback if structure changes again
    if not items:
        for a in soup.find_all("a", href=True):
            if "/news/" in a["href"] and a.text.strip():
                href = a["href"]
                if href.startswith("/"):
                    href = "https://www.bbc.com" + href
                items.append({
                    "title": a.text.strip(),
                    "url": href,
                    "source": "BBC",
                    "fetched_at": datetime.utcnow(),
                    "summary": None
                })
                if len(items) >= limit:
                    break

    return items
