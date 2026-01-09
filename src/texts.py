from typing import List, Tuple, Dict, Any
import html
import re

def clean_title(title: str) -> str:
    t = (title or "").strip()

    # "Prawo.pl: ..." style prefixes (often source labels)
    t = re.sub(
        r"^\s*[^:]{2,40}\.(pl|com|net|org|eu|gov|edu|info|tv|io)\s*:\s+",
        "",
        t,
        flags=re.IGNORECASE,
    )

    # Google News & many sites: "Some headline - SourceName"
    t = re.sub(r"\s+-\s+[^-]{2,60}$", "", t)

    # Remove common breadcrumb-like endings
    t = re.sub(r"\s*[\\|/]\s*Aktualności.*$", "", t, flags=re.IGNORECASE)

    # Collapse whitespace
    t = " ".join(t.split()).strip()
    return t

_IMG_ALT_RE = re.compile(r"<img[^>]*alt=(\"|')(.*?)(\"|')[^>]*>", flags=re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_URL_RE = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
_DOMAIN_RE = re.compile(r"\b[\w.-]+\.(pl|com|net|org|eu|gov|edu|info|tv|io)\b", flags=re.IGNORECASE)
_ANCHOR_TEXT_RE = re.compile(r"<a[^>]*>(.*?)</a>", flags=re.IGNORECASE | re.DOTALL)
_LIST_RE = re.compile(r"</li>|<ol|<ul", flags=re.IGNORECASE)
_BOILERPLATE_RE = re.compile(r"\b(czytaj więcej|czytaj także|zobacz)\b", flags=re.IGNORECASE)
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

def _strip_html(text: str) -> str:
    if "<" not in text:
        return text
    text = re.sub(r"<\s*(br|/p|p)\s*/?>", " ", text, flags=re.IGNORECASE)
    text = _IMG_ALT_RE.sub(lambda m: f" {m.group(2).strip()} ", text)
    return _TAG_RE.sub(" ", text)

def _first_sentence(text: str) -> str:
    parts = [p.strip() for p in _SENT_SPLIT_RE.split(text) if p.strip()]
    for part in parts:
        if len(part.split()) >= 5:
            return part
    return parts[0] if parts else text

def _limit_tokens(text: str, max_tokens: int = 60) -> str:
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return text
    return " ".join(tokens[:max_tokens])

def clean_summary(summary: str, source: str = "") -> str:
    s = (summary or "").strip()
    if not s:
        return ""

    # Google News-like lists: keep only the first anchor text.
    if _LIST_RE.search(s):
        m = _ANCHOR_TEXT_RE.search(s)
        if m:
            s = m.group(1)

    s = _strip_html(s)
    s = html.unescape(s).replace("\xa0", " ")
    s = _URL_RE.sub(" ", s)
    s = _DOMAIN_RE.sub(" ", s)
    s = _BOILERPLATE_RE.sub(" ", s)

    if source:
        s = re.sub(re.escape(source), " ", s, flags=re.IGNORECASE)

    s = " ".join(s.split()).strip()
    if not s:
        return ""

    s = _first_sentence(s)
    s = _limit_tokens(s, max_tokens=60)
    return s.strip()

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
        title = clean_title(a.get("title") or "")
        raw_summary = (a.get("summary") or "").strip()
        summary = clean_summary(raw_summary, source=(a.get("source") or ""))

        if not title:
            stats["missing_title"] += 1

        if not raw_summary:
            stats["missing_summary"] += 1

        # Combine
        if title and summary:
            # Double title to emphasize event terms over source/style.
            text = f"{title}. {title}. {summary}"
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
