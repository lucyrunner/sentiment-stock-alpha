import pandas as pd

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    q_hi = df["net_sent"].rolling(200, min_periods=50).quantile(0.95)
    q_lo = df["net_sent"].rolling(200, min_periods=50).quantile(0.05)
    q_hi = q_hi.fillna(df["net_sent"].quantile(0.95))
    q_lo = q_lo.fillna(df["net_sent"].quantile(0.05))

    sig = []
    for i in range(len(df)):
        ns = float(df.loc[i, "net_sent"])
        az = float(df.loc[i, "attention_z"])
        if ns > float(q_hi.loc[i]) and az > 2:
            sig.append("SELL")
        elif ns < float(q_lo.loc[i]) and az < 2:
            sig.append("BUY")
        else:
            sig.append("HOLD")
    df["signal"] = sig
    return df
