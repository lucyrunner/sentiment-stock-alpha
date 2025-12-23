import pandas as pd
from src.signals.rules import generate_signals

def test_generate_signals_runs():
    df = pd.DataFrame({
        "bucket_ts":[1,2,3,4,5,6],
        "net_sent":[0,0.1,0.2,0.3,-0.4,-0.5],
        "attention_z":[0,0,0,3,0,0],
        "post_count":[1,1,1,10,1,1]
    })
    out = generate_signals(df)
    assert "signal" in out.columns
