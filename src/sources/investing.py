import time
import requests
from bs4 import BeautifulSoup
from src.config import USER_AGENT, INVESTING_BASE
from src.storage.schema import SocialEvent

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}

def search_investing(ticker: str, max_links: int = 10):
    # Lightweight MVP: search page -> pick news/article links
    url = f"{INVESTING_BASE}/search/?q={ticker}"
    html = requests.get(url, headers=HEADERS, timeout=20).text
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        if "/news/" in href or "/equities/" in href:
            if href.startswith("http"):
                links.append(href)
            else:
                links.append(INVESTING_BASE + href)
    # de-dup preserve order
    seen = set()
    out = []
    for x in links:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
        if len(out) >= max_links:
            break
    return out

def fetch_page_text(url: str):
    html = requests.get(url, headers=HEADERS, timeout=20).text
    soup = BeautifulSoup(html, "lxml")
    title = (soup.title.get_text(" ", strip=True) if soup.title else "")[:200]
    text = soup.get_text(" ", strip=True)
    return title, text

def build_events_from_links(ticker: str, urls):
    events = []
    now = int(time.time())
    for u in urls:
        title, text = fetch_page_text(u)
        events.append(SocialEvent(
            event_id=f"inv_{abs(hash(u))}",
            source="investing",
            ticker=ticker,
            created_at=now,  # MVP: use fetch time; upgrade: parse published time
            text=f"{title}\n{text[:6000]}",
            meta={"url": u}
        ))
    return events
