from __future__ import annotations

from typing import List
import numpy as np
from sklearn.cluster import KMeans


def choose_k(n_docs: int) -> int:
    # Stable heuristic for news-like streams.
    # For 300-600 docs this yields ~55-80.
    k = int((n_docs ** 0.5) * 4)
    return max(40, min(120, k))


def kmeans_labels(X_dense: np.ndarray, k: int | None = None, random_state: int = 42) -> List[int]:
    if k is None:
        k = choose_k(X_dense.shape[0])

    model = KMeans(
        n_clusters=k,
        random_state=random_state,
        n_init="auto",
    )
    return model.fit_predict(X_dense).tolist()
