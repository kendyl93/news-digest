from src.io_raw import load_latest_raw
from src.texts import build_texts, clean_title


def main() -> None:
    articles = load_latest_raw()
    filtered, texts, stats = build_texts(articles)

    print("=== 5.2 Build texts summary ===")
    for k, v in stats.items():
        print(f"- {k}: {v}")

    print("\nSample texts (up to 5):")
    for i, t in enumerate(texts[:5], start=1):
        a = filtered[i - 1]
        print(f"\n{i}) {a.get('source', 'UNKNOWN')}")
        print(f"   title: {clean_title(a.get('title',''))}")
        if a.get("summary"):
            print(f"   summary: {(a.get('summary') or '')[:140]}...")
        print(f"   text: {t[:220]}...")

if __name__ == "__main__":
    main()
