from __future__ import annotations

from typing import List

from sklearn.cluster import AgglomerativeClustering


def cluster_articles(X, distance_threshold: float = 0.80) -> List[int]:
    """
    Agglomerative clustering using cosine distance.

    distance_threshold:
      - lower -> more clusters (stricter similarity)
      - higher -> fewer clusters (looser similarity)
    """
    model = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=distance_threshold,
        linkage="average",
        metric="cosine",
    )
    labels = model.fit_predict(X)
    return labels.tolist()
