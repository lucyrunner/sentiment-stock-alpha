import pandas as pd

def add_attention_z(df: pd.DataFrame, window: int = 24) -> pd.DataFrame:
    m = df["post_count"].rolling(window=window, min_periods=max(3, window//4)).mean()
    s = df["post_count"].rolling(window=window, min_periods=max(3, window//4)).std()
    df["attention_z"] = (df["post_count"] - m) / (s.replace(0, 1e-9))
    df["attention_z"] = df["attention_z"].fillna(0.0)
    return df
