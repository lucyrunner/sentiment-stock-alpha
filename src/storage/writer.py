import json
from src.storage.schema import SocialEvent

def write_event(r, e: SocialEvent) -> None:
    # Streams + ZSET + Hash
    stream_key = f"stream:events:{e.ticker}"
    zset_key = f"zset:events:{e.ticker}:ts"
    hash_key = f"hash:event:{e.event_id}"

    # dedup
    if r.exists(hash_key):
        return

    payload = {
        "event_id": e.event_id,
        "source": e.source,
        "ticker": e.ticker,
        "created_at": str(e.created_at),
        "text": e.text,
        "meta": json.dumps(e.meta, ensure_ascii=False),
        "label": e.label or "",
        "score": "" if e.score is None else str(e.score),
    }

    r.hset(hash_key, mapping=payload)
    r.zadd(zset_key, {e.event_id: float(e.created_at)})
    r.xadd(stream_key, payload, maxlen=200000, approximate=True)
