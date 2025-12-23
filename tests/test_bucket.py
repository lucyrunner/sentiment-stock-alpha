from src.features.bucket import bucket_floor, make_bucket

def test_bucket_floor():
    assert bucket_floor(61, 60) == 60

def test_make_bucket():
    b = make_bucket(61, 60)
    assert b.start_ts == 60 and b.end_ts == 120
