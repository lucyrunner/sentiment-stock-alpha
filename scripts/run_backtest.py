import json
import argparse
import pandas as pd
from src.signals.rules import generate_signals
from src.backtest.prices import load_prices
from src.backtest.align import align_features_prices
from src.backtest.engine import run_backtest
from src.backtest.metrics import summarize
from src.viz.plots import plot_sentiment_attention, plot_price_signals

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--bucket-minutes", type=int, default=60)
    ap.add_argument("--lookback-days", type=int, default=90)
    args = ap.parse_args()

    ticker = args.ticker.upper()
    feat = pd.read_csv(f"features_{ticker}.csv")
    feat = generate_signals(feat)

    # pick yfinance interval closest to bucket
    interval = "1h" if args.bucket_minutes >= 60 else "30m"
    px = load_prices(ticker, period_days=args.lookback_days, interval=interval)

    aligned = align_features_prices(feat, px, bucket_seconds=args.bucket_minutes * 60)
    bt = run_backtest(aligned)
    m = summarize(bt["curve"])
    out = {"ticker": ticker, **bt, **m}

    with open(f"backtest_{ticker}.json", "w") as f:
        json.dump(out, f, indent=2)

    plot_sentiment_attention(feat, ticker)
    plot_price_signals(aligned, ticker)
    print(f"Saved backtest_{ticker}.json and plots/*.png")

if __name__ == "__main__":
    main()
