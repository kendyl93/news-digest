import json
from datetime import datetime
from pathlib import Path

from src.feeds import load_feeds
from src.fetch import fetch_feed

OUTPUTS_DIR = Path("outputs")

def main():
    OUTPUTS_DIR.mkdir(exist_ok=True)

    feeds = load_feeds()
    all_articles = []

    print("=== Ingest ===")
    for feed in feeds:
        source = feed["source"]
        url = feed["url"]

        items = fetch_feed(url)
        print(f"- {source}: {len(items)}")

        for item in items:
            item["source"] = source
            item["feed_url"] = url
            item["fetched_at"] = datetime.utcnow().isoformat()
            all_articles.append(item)
    print(f"\nTotal: {len(all_articles)}")
    print("\nSample:")
    for article in all_articles[:5]:
        print(f"- {article['source']}: {article['title']}")
        print(f"  {article['link']}")

    out_path = OUTPUTS_DIR / f"raw_{datetime.utcnow().date().isoformat()}.json"
    out_path.write_text(json.dumps(all_articles, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved: {out_path}")

if __name__ == "__main__":
    main()
