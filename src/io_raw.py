import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

from src.texts import clean_title


OUTPUTS_DIR = Path("outputs")


def find_latest_raw_file() -> Path:
    """
    Prefer today's raw file (UTC date). If it doesn't exist, pick the newest raw_*.json.
    """
    today = datetime.now(timezone.utc).date().isoformat()
    preferred = OUTPUTS_DIR / f"raw_{today}.json"
    if preferred.exists():
        return preferred

    candidates = sorted(OUTPUTS_DIR.glob("raw_*.json"))
    if not candidates:
        raise FileNotFoundError(
            "No raw_*.json found in outputs/. Run `python -m src.ingest` first."
        )
    return candidates[-1]


def load_latest_raw() -> List[Dict[str, Any]]:
    raw_path = find_latest_raw_file()
    data = json.loads(raw_path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Expected a list in {raw_path}, got: {type(data)}")

    # Attach info about where it came from (optional but useful for debugging)
    for item in data:
        if isinstance(item, dict):
            item["_raw_file"] = raw_path.name

    return data


if __name__ == "__main__":
    articles = load_latest_raw()
    print(f"Loaded {len(articles)} articles from outputs/{articles[0].get('_raw_file') if articles else 'N/A'}")

    print("\nSample (up to 5):")
    for a in articles[:5]:
        source = a.get("source", "UNKNOWN")
        title = clean_title(a.get("title","").strip())
        link = (a.get("link") or "").strip()
        published = a.get("published") or ""
        print(f"- {source}: {title}")
        if published:
            print(f"  published: {published}")
        print(f"  link: {link}")
