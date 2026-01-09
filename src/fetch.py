import feedparser
from src.texts import clean_title

def fetch_feed(url: str):
    parsed = feedparser.parse(url)
    entries = parsed.entries or []

    articles = []
    for entry in entries:
        title = clean_title(entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        summary = (entry.get("summary") or entry.get("description") or "").strip()
        published = entry.get("published") or entry.get("updated") or ""
        if not title or not link:
            continue

        articles.append({
            "title": title,
            "link": link,
            "summary": summary,
            "published": published,
        })

    return articles
