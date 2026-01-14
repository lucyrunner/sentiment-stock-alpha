import pandas as pd

def align_features_prices(feat: pd.DataFrame, px: pd.DataFrame, bucket_seconds: int = 3600) -> pd.DataFrame:
    # -------------------------
    # Feature side: make 'ts'
    # -------------------------
    feat = feat.copy()
    feat["ts"] = pd.to_datetime(feat["bucket_ts"], unit="s", utc=True)
    feat = feat.sort_values("ts").reset_index(drop=True)

    # -------------------------
    # Price side: flatten MultiIndex from yfinance
    # -------------------------
    px = px.copy()

    # yfinance sometimes returns MultiIndex columns like ('Close','OKLO')
    if isinstance(px.columns, pd.MultiIndex):
        # Keep only the first level name: Open/High/Low/Close/Adj Close/Volume
        px.columns = [str(c[0]).strip() for c in px.columns]

    # Ensure ts column exists (yfinance often uses DatetimeIndex)
    if "ts" not in px.columns:
        px = px.reset_index()

    # Normalize common timestamp column names
    if "Datetime" in px.columns:
        px = px.rename(columns={"Datetime": "ts"})
    if "Date" in px.columns:
        px = px.rename(columns={"Date": "ts"})

    # Make sure ts is datetime
    px["ts"] = pd.to_datetime(px["ts"], utc=True)

    # Choose a close-like column robustly
    close_candidates = ["Close", "Adj Close", "close", "adj close", "adj_close"]
    close_col = next((c for c in close_candidates if c in px.columns), None)
    if close_col is None:
        raise ValueError(f"Could not find a close column. px.columns={list(px.columns)}")

    px = px[["ts", close_col]].rename(columns={close_col: "close"})
    px = px.sort_values("ts").reset_index(drop=True)

    # -------------------------
    # Merge: align each feature bucket to the most recent price point
    # -------------------------
    merged = pd.merge_asof(
        feat,
        px,
        on="ts",
        direction="backward",
        allow_exact_matches=True,
    )

    # Forward return next bucket (1-step)
    merged["close_fwd"] = merged["close"].shift(-1)
    merged["ret_fwd"] = (merged["close_fwd"] / merged["close"]) - 1.0

    return merged

