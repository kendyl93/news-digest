from typing import List, Tuple, Dict, Any


def build_texts(articles: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str], Dict[str, int]]:
    """
    Build ML-friendly text for each article: title + summary.
    Returns:
      - filtered_articles: only those with non-empty resulting text
      - texts: list[str] aligned with filtered_articles
      - stats: basic counters
    """
    filtered: List[Dict[str, Any]] = []
    texts: List[str] = []

    stats = {
        "input": len(articles),
        "kept": 0,
        "dropped_empty": 0,
        "missing_title": 0,
        "missing_summary": 0,
        "used_title_only": 0,
    }

    for a in articles:
        title = (a.get("title") or "").strip()
        summary = (a.get("summary") or "").strip()

        if not title:
            stats["missing_title"] += 1

        if not summary:
            stats["missing_summary"] += 1

        # Combine
        if title and summary:
            text = f"{title}. {summary}"
        elif title:
            text = title
            stats["used_title_only"] += 1
        elif summary:
            # Rare, but allow summary-only if title missing
            text = summary
        else:
            text = ""

        text = " ".join(text.split()).strip()  # collapse whitespace

        if not text:
            stats["dropped_empty"] += 1
            continue

        filtered.append(a)
        texts.append(text)
        stats["kept"] += 1

    return filtered, texts, stats
