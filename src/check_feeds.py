import json
from pathlib import Path

import feedparser


FEEDS_PATH = Path("feeds/feeds.json")


def main() -> None:
    feeds = json.loads(FEEDS_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(feeds)} feeds\n")

    for feed in feeds:
        url = feed["url"]
        source = feed.get("source", "UNKNOWN")

        print(f"=== {source} ===")
        print(f"URL: {url}")

        parsed = feedparser.parse(url)

        if parsed.bozo:
            # bozo=1 means parser had issues (often still works, but worth knowing)
            print(f"WARNING: bozo=1 (parse issue): {parsed.bozo_exception}")

        entries = parsed.entries or []
        print(f"Entries: {len(entries)}")

        # Print first 3 entries as a sanity check
        for entry in entries[:3]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            published = entry.get("published", entry.get("updated", ""))
            summary = entry.get("summary", entry.get("description", ""))

            print(f"- {title}")
            print(f"  published: {published}")
            print(f"  link: {link}")
            if summary:
                print(f"  summary: {summary[:140].strip()}...")
        print()

if __name__ == "__main__":
    main()
