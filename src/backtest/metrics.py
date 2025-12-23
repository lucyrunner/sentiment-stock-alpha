import numpy as np

def max_drawdown(curve):
    peak = -1e18
    mdd = 0.0
    for x in curve:
        peak = max(peak, x)
        dd = (peak - x) / max(peak, 1e-12)
        mdd = max(mdd, dd)
    return float(mdd)

def summarize(curve):
    arr = np.array(curve, dtype=float)
    if len(arr) < 3:
        return {"max_drawdown": 0.0, "sharpe_like": 0.0}
    rets = np.diff(arr) / (arr[:-1] + 1e-12)
    sharpe = float(np.mean(rets) / (np.std(rets) + 1e-9) * np.sqrt(252)) if len(rets) > 5 else 0.0
    return {"max_drawdown": max_drawdown(curve), "sharpe_like": sharpe}
