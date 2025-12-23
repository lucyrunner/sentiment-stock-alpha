import pandas as pd

def align_features_prices(feat: pd.DataFrame, px: pd.DataFrame, bucket_seconds: int) -> pd.DataFrame:
    feat = feat.copy()
    feat["exec_ts"] = feat["bucket_ts"] + bucket_seconds  # execute next bucket boundary

    merged = pd.merge_asof(
        feat.sort_values("exec_ts"),
        px.sort_values("ts"),
        left_on="exec_ts",
        right_on="ts",
        direction="forward",
    )
    merged["next_close"] = merged["close"].shift(-1)
    merged["ret_fwd"] = (merged["next_close"] - merged["close"]) / merged["close"]
    merged = merged.dropna(subset=["ret_fwd"]).reset_index(drop=True)
    return merged
