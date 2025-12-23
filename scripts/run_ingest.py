import argparse
from src.storage.redis_client import get_redis
from src.storage.writer import write_event
from src.sources.stocktwits import fetch_stocktwits_messages, parse_stocktwits
from src.sources.investing import search_investing, build_events_from_links
from src.nlp.sentiment import simple_lexicon_score, label_from_score

def enrich_sentiment(events):
    for e in events:
        if e.label in ("bull", "bear"):
            e.score = 0.6 if e.label == "bull" else -0.6
        else:
            s = simple_lexicon_score(e.text)
            e.score = s
            e.label = label_from_score(s)
    return events

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--hours", type=int, default=72)
    args = ap.parse_args()

    r = get_redis()
    ticker = args.ticker.upper()

    st_json = fetch_stocktwits_messages(ticker)
    st_events = parse_stocktwits(st_json, ticker)

    inv_urls = search_investing(ticker)
    inv_events = build_events_from_links(ticker, inv_urls)

    events = enrich_sentiment(st_events + inv_events)
    for e in events:
        write_event(r, e)

    print(f"Wrote {len(events)} events for {ticker}")

if __name__ == "__main__":
    main()
