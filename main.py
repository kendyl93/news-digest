import sys
import feedparser
from src.feeds import load_feeds

def main() -> None:
    print("Python:", sys.version.split()[0])
    print("feedparser:", feedparser.__version__)
    print("OK ✅")

if __name__ == "__main__":
    feeds = load_feeds()
    print(f"Loaded {len(feeds)} feeds")
    for f in feeds:
        print(f"- {f['source']}: {f['url']}")
