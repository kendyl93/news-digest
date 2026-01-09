import json
from pathlib import Path

FEEDS_PATH = Path("feeds/feeds.json")

def load_feeds():
    return json.loads(FEEDS_PATH.read_text(encoding="utf-8"))
