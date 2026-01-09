from __future__ import annotations

from collections import defaultdict, Counter

from src.io_raw import load_latest_raw
from src.texts import build_texts, clean_title
from src.vectorize import vectorize_tfidf
from src.cluster import cluster_articles
from src.lsa import lsa_transform
from src.kmeans_cluster import kmeans_labels, choose_k


def main() -> None:
    articles = load_latest_raw()
    filtered, texts, stats = build_texts(articles)

    # Keep rare title terms to avoid generic mixed clusters
    vectorizer, X = vectorize_tfidf(texts, min_df=1, ngram_range=(1, 2), max_features=20000)

    # labels = cluster_articles(X.toarray(), distance_threshold=0.80)
    # Preserve more dimensions to avoid over-smoothing unrelated items
    n_components = min(200, X.shape[1] - 1, X.shape[0] - 1)
    n_components = max(80, n_components)
    X_lsa, _ = lsa_transform(X, n_components=n_components)
    k = choose_k(X_lsa.shape[0])
    labels = kmeans_labels(X_lsa, k=k)
    print(f"Using LSA+KMeans with k={k}, n_components={n_components}")

    # group indices by label
    groups = defaultdict(list)
    for idx, lab in enumerate(labels):
        groups[lab].append(idx)

    n_clusters = len(groups)
    sizes = [len(v) for v in groups.values()]
    singletons = sum(1 for s in sizes if s == 1)

    print("=== 5.5 Clustering summary ===")
    print(f"Docs: {len(filtered)}")
    print(f"Clusters: {n_clusters}")
    print(f"Singleton clusters (size=1): {singletons}")
    print(f"Largest cluster size: {max(sizes) if sizes else 0}")

    # print top 8 biggest clusters
    print("\nTop clusters (by size):")
    for cluster_id, idxs in sorted(groups.items(), key=lambda kv: len(kv[1]), reverse=True)[:8]:
        sources = [filtered[i].get("source", "UNKNOWN") for i in idxs]
        unique_sources = len(set(sources))

        print(f"\n--- Cluster {cluster_id} | size={len(idxs)} | sources={unique_sources} ---")

        for i in idxs[:5]:
            a = filtered[i]
            print(f"- [{a.get('source','UNKNOWN')}] {clean_title(a.get("title",""))}")



if __name__ == "__main__":
    main()
