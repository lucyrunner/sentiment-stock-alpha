from dataclasses import dataclass

@dataclass(frozen=True)
class BucketKey:
    start_ts: int
    end_ts: int

def bucket_floor(ts: int, bucket_seconds: int) -> int:
    return ts - (ts % bucket_seconds)

def make_bucket(ts: int, bucket_seconds: int) -> BucketKey:
    s = bucket_floor(ts, bucket_seconds)
    return BucketKey(start_ts=s, end_ts=s + bucket_seconds)
