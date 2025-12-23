import time
import requests
from tenacity import retry, wait_exponential, stop_after_attempt
from src.storage.schema import SocialEvent

@retry(wait=wait_exponential(min=1, max=20), stop=stop_after_attempt(5))
def fetch_stocktwits_messages(ticker: str, limit: int = 200):
    # Public endpoint for symbol stream
    url = f"https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()

def _iso_to_epoch(created_at_iso: str) -> int:
    # Ex: "2025-12-22T10:12:03Z"
    # Keep first 19 chars and parse as UTC-ish; this is MVP-safe
    s = created_at_iso[:19].replace("Z", "")
    return int(time.mktime(time.strptime(s, "%Y-%m-%dT%H:%M:%S")))

def parse_stocktwits(json_obj, ticker: str):
    events = []
    messages = json_obj.get("messages", [])
    for m in messages:
        mid = str(m.get("id"))
        created_at = m.get("created_at") or ""
        ts = _iso_to_epoch(created_at) if created_at else int(time.time())
        body = m.get("body", "") or ""
        sent = (m.get("entities", {}).get("sentiment") or {})
        label = sent.get("basic")  # "Bullish"/"Bearish"
        if label:
            label = "bull" if label.lower().startswith("bull") else "bear"
        meta = {
            "user": (m.get("user") or {}).get("username"),
            "likes": (m.get("likes") or {}).get("total"),
            "reshares": (m.get("reshares") or {}).get("total"),
            "raw": m,
        }
        events.append(SocialEvent(
            event_id=f"st_{mid}",
            source="stocktwits",
            ticker=ticker,
            created_at=ts,
            text=body,
            meta=meta,
            label=label
        ))
    return events
