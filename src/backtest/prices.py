import pandas as pd
import yfinance as yf

def load_prices(ticker: str, period_days: int = 90, interval: str = "1h") -> pd.DataFrame:
    df = yf.download(ticker, period=f"{period_days}d", interval=interval, auto_adjust=True, progress=False)
    if df is None or df.empty:
        raise RuntimeError(f"No price data returned for {ticker}. Try a different interval/period.")
    df = df.reset_index()
    ts_col = "Datetime" if "Datetime" in df.columns else "Date"
    df["ts"] = (pd.to_datetime(df[ts_col]).astype("int64") // 10**9).astype(int)
    df = df.rename(columns={"Close":"close"})
    return df[["ts","close"]].sort_values("ts").reset_index(drop=True)
