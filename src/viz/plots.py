import os
import matplotlib.pyplot as plt
import pandas as pd

def plot_sentiment_attention(feat: pd.DataFrame, ticker: str, outdir="plots"):
    os.makedirs(outdir, exist_ok=True)
    x = feat["bucket_ts"]

    plt.figure()
    plt.plot(x, feat["net_sent"])
    plt.title(f"{ticker} net_sent")
    plt.savefig(f"{outdir}/{ticker}_net_sent.png", dpi=200)
    plt.close()

    plt.figure()
    plt.plot(x, feat["attention_z"])
    plt.title(f"{ticker} attention_z")
    plt.savefig(f"{outdir}/{ticker}_attention_z.png", dpi=200)
    plt.close()

def plot_price_signals(aligned: pd.DataFrame, ticker: str, outdir="plots"):
    os.makedirs(outdir, exist_ok=True)
    x = aligned["bucket_ts"]
    plt.figure()
    plt.plot(x, aligned["close"])
    buys = aligned[aligned["signal"]=="BUY"]
    sells = aligned[aligned["signal"]=="SELL"]
    plt.scatter(buys["bucket_ts"], buys["close"])
    plt.scatter(sells["bucket_ts"], sells["close"])
    plt.title(f"{ticker} Price + Signals")
    plt.savefig(f"{outdir}/{ticker}_signals.png", dpi=200)
    plt.close()
