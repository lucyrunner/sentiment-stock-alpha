from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class SocialEvent:
    event_id: str
    source: str            # "stocktwits" | "investing"
    ticker: str
    created_at: int        # epoch seconds
    text: str
    meta: Dict[str, Any]   # likes/replies/url/raw, etc.
    label: Optional[str] = None   # bull/bear/neutral
    score: Optional[float] = None # [-1,1]
