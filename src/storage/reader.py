import json
from typing import List
from src.storage.schema import SocialEvent

def read_events(r, ticker: str, start_ts: int, end_ts: int) -> List[SocialEvent]:
    zset_key = f"zset:events:{ticker}:ts"
    ids = r.zrangebyscore(zset_key, start_ts, end_ts)
    out: List[SocialEvent] = []
    for eid in ids:
        h = r.hgetall(f"hash:event:{eid}")
        if not h:
            continue
        out.append(SocialEvent(
            event_id=h.get("event_id",""),
            source=h.get("source",""),
            ticker=h.get("ticker", ticker),
            created_at=int(float(h.get("created_at","0") or 0)),
            text=h.get("text",""),
            meta=json.loads(h.get("meta") or "{}"),
            label=(h.get("label") or None),
            score=(float(h["score"]) if h.get("score") not in ("", None) else None),
        ))
    return out
