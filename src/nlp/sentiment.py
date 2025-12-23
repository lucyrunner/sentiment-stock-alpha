import re
from src.nlp.lexicons import POS_WORDS, NEG_WORDS

def simple_lexicon_score(text: str) -> float:
    tokens = re.findall(r"[a-zA-Z']+", (text or "").lower())
    if not tokens:
        return 0.0
    pos = sum(1 for w in tokens if w in POS_WORDS)
    neg = sum(1 for w in tokens if w in NEG_WORDS)
    score = (pos - neg) / max(1, (pos + neg))
    return max(-1.0, min(1.0, score))

def label_from_score(score: float, th: float = 0.15) -> str:
    if score > th:
        return "bull"
    if score < -th:
        return "bear"
    return "neutral"
