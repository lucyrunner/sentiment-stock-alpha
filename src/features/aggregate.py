import numpy as np
import pandas as pd
from collections import defaultdict
from src.features.bucket import make_bucket

def aggregate_events(events, bucket_minutes: int) -> pd.DataFrame:
    bsec = bucket_minutes * 60
    rows = defaultdict(lambda: {
        "bull": 0, "bear": 0, "neutral": 0,
        "post_count": 0,
        "buy_scores": [], "sell_scores": [],
    })

    for e in events:
        bk = make_bucket(e.created_at, bsec).start_ts
        rows[bk]["post_count"] += 1

        label = e.label or "neutral"
        if label not in ("bull","bear","neutral"):
            label = "neutral"
        rows[bk][label] += 1

        if e.score is not None:
            if e.score > 0:
                rows[bk]["buy_scores"].append(e.score)
            elif e.score < 0:
                rows[bk]["sell_scores"].append(abs(e.score))

    data = []
    for ts, d in rows.items():
        bull, bear, neu = d["bull"], d["bear"], d["neutral"]
        total = bull + bear + neu
        bull_ratio = bull / max(1, (bull + bear))
        net_sent = (bull - bear) / max(1, total)
        avg_buy = float(np.mean(d["buy_scores"])) if d["buy_scores"] else 0.0
        avg_sell = float(np.mean(d["sell_scores"])) if d["sell_scores"] else 0.0
        data.append([ts, bull, bear, neu, d["post_count"], bull_ratio, net_sent, avg_buy, avg_sell])

    df = pd.DataFrame(
        data,
        columns=[
            "bucket_ts","bull","bear","neutral","post_count",
            "bull_ratio","net_sent","avg_buy_intent","avg_sell_intent"
        ]
    ).sort_values("bucket_ts").reset_index(drop=True)
    return df
