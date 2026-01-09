import numpy as np

from src.io_raw import load_latest_raw
from src.texts import build_texts
from src.vectorize import vectorize_tfidf


def top_terms_for_doc(vectorizer, X, doc_idx: int, top_n: int = 10):
    feature_names = vectorizer.get_feature_names_out()
    row = X[doc_idx].toarray().ravel()
    if row.max() == 0:
        return []
    top_idx = np.argsort(row)[::-1][:top_n]
    return [(feature_names[i], float(row[i])) for i in top_idx if row[i] > 0]


def main() -> None:
    articles = load_latest_raw()
    filtered, texts, stats = build_texts(articles)

    print("=== 5.3 TF-IDF ===")
    print(f"- docs (kept): {len(texts)}")

    vectorizer, X = vectorize_tfidf(texts, min_df=1, ngram_range=(1, 2), max_features=20000)

    print(f"- matrix shape: {X.shape} (docs x features)")
    print(f"- vocabulary size: {len(vectorizer.get_feature_names_out())}")

    # Show top terms for first 2 docs as sanity check
    for i in range(min(2, len(texts))):
        a = filtered[i]
        print(f"\nDoc {i} | {a.get('source','UNKNOWN')}")
        print(f"Title: {a.get('title','')}")
        terms = top_terms_for_doc(vectorizer, X, i, top_n=12)
        print("Top terms:", ", ".join([f"{t}:{w:.3f}" for t, w in terms]))

if __name__ == "__main__":
    main()
