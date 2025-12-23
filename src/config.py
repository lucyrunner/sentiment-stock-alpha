import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0")
INVESTING_BASE = os.getenv("INVESTING_BASE", "https://www.investing.com")
