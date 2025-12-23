import time
import argparse
import pandas as pd
from src.storage.redis_client import get_redis
from src.storage.reader import read_events
from src.features.aggregate import aggregate_events
from src.features.attention import add_attention_z

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--bucket-minutes", type=int, default=60)
    ap.add_argument("--lookback-days", type=int, default=90)
    args = ap.parse_args()

    r = get_redis()
    now = int(time.time())
    start = now - args.lookback_days * 86400
    ticker = args.ticker.upper()

    events = read_events(r, ticker, start, now)
    feat = aggregate_events(events, args.bucket_minutes)
    feat = add_attention_z(feat, window=max(12, 24))
    feat.to_csv(f"features_{ticker}.csv", index=False)
    print(f"Saved features_{ticker}.csv rows={len(feat)}")

if __name__ == "__main__":
    main()
