import pandas as pd

def run_backtest(df: pd.DataFrame) -> dict:
    pos = 0  # -1 short, 0 flat, 1 long
    equity = 1.0
    curve = []

    for _, r in df.iterrows():
        sig = r["signal"]
        if sig == "BUY":
            pos = 1
        elif sig == "SELL":
            pos = -1

        equity *= (1.0 + pos * float(r["ret_fwd"]))
        curve.append(float(equity))

    return {"final_equity": float(equity), "curve": curve}
